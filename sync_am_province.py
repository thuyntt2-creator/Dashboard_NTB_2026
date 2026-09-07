import pandas as pd
import openpyxl
import gspread
from google.oauth2.service_account import Credentials
import os
import sys
import unicodedata
import math

# Configure output encoding for Vietnamese characters
sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
load_dotenv()

JSON_FILE = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') or r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
if not os.path.exists(JSON_FILE):
    JSON_FILE = 'credentials.json'

SHEET_ID = os.environ.get('SHEET_ID') or '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'

# Paths for Input (raw download) and Output (report file with formulas)
INPUT_PATH = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
OUTPUT_PATH = r"c:\Users\lap4all\Desktop\NTB_Bao_Cao_Van_Hanh_Co_Bieu_Do.xlsx"
if not os.path.exists(OUTPUT_PATH):
    OUTPUT_PATH = r"c:\Users\lap4all\Desktop\NTB_Bao_Cao_Van_Hanh_Corrected.xlsx"

print(f"Reading Excel raw data from: {INPUT_PATH}")
df_gtc_full = pd.read_excel(INPUT_PATH, sheet_name='dataGTC gốc full hàng')
df_gtc_tts = pd.read_excel(INPUT_PATH, sheet_name='dataGTC gốc TTS')
df_ltc_full = pd.read_excel(INPUT_PATH, sheet_name='dataLTC full hàng')
df_ltc_tts = pd.read_excel(INPUT_PATH, sheet_name='dataLTC TTS')
df_odr_full = pd.read_excel(INPUT_PATH, sheet_name='dataODRfull hàng ')
df_cocau = pd.read_excel(INPUT_PATH, sheet_name='cocau')

def normalize_name(name):
    if pd.isna(name): return ""
    return unicodedata.normalize('NFC', str(name).strip()).upper()

# Normalize cocau mappings
df_cocau['BC_norm'] = df_cocau['BC'].apply(normalize_name)
bc_to_am = dict(zip(df_cocau['BC_norm'], df_cocau['Am']))
bc_to_tinh = dict(zip(df_cocau['BC_norm'], df_cocau['Tỉnh']))

def map_am(bc_name):
    return bc_to_am.get(normalize_name(bc_name), None)

def map_tinh(bc_name):
    return bc_to_tinh.get(normalize_name(bc_name), None)

def get_province_from_ql(ql):
    ql_str = str(ql)
    if 'Đắk Nông' in ql_str or 'Đăk Nông' in ql_str: return 'Đắk Nông'
    if 'Bình Thuận' in ql_str: return 'Bình Thuận'
    if 'Khánh Hòa' in ql_str: return 'Khánh Hòa'
    if 'Lâm Đồng' in ql_str: return 'Lâm Đồng'
    if 'Ninh Thuận' in ql_str: return 'Ninh Thuận'
    return None

# Map raw sheets
for df in [df_gtc_full, df_ltc_full, df_odr_full]:
    if 'Chi tiết' in df.columns:
        df['AM_mapped'] = df['Chi tiết'].apply(map_am)
        df['Tỉnh_mapped'] = df['Chi tiết'].apply(map_tinh)
    if 'Quản lý' in df.columns:
        df['Tỉnh_mapped_ql'] = df['Quản lý'].apply(get_province_from_ql)
        df['Tỉnh_mapped'] = df['Tỉnh_mapped'].fillna(df['Tỉnh_mapped_ql'])

# 1. GTC (Lọc chỉ lấy hàng mới, loại trừ Grand Total)
df_gtc = df_gtc_full[(df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2', 'Hàng Tồn'])) & (df_gtc_full['Chi tiết'] != 'Grand Total')].copy()
df_gtc['Vol_Gan'] = df_gtc['Volume'] * df_gtc['% Gán']
df_gtc['Vol_GTC'] = df_gtc['Volume'] * df_gtc['% GTC']
gtc_grouped = df_gtc.groupby(['AM_mapped', 'Tỉnh_mapped', 'Time']).agg(
    vol_gtc=('Volume', 'sum'),
    vol_gtc_ok=('Vol_GTC', 'sum')
).reset_index()
gtc_grouped['% GTC'] = gtc_grouped['vol_gtc_ok'] / gtc_grouped['vol_gtc']

# 2. Tính LTC (Lọc bỏ Grand Total theo Cấp quản lý)
df_ltc = df_ltc_full[df_ltc_full['Cấp quản lý'] != 'Grand Total'].copy()
df_ltc['Vol_Gan'] = df_ltc['Volume'] * df_ltc['%Gán']
df_ltc['Vol_LTC'] = df_ltc['Volume'] * df_ltc['%LTC']
ltc_grouped = df_ltc.groupby(['AM_mapped', 'Tỉnh_mapped', 'Time']).agg(
    vol_ltc_tot=('Volume', 'sum'),
    vol_gan_ltc=('Vol_Gan', 'sum'),
    vol_ltc_ok=('Vol_LTC', 'sum')
).reset_index()
ltc_grouped['% LTC'] = ltc_grouped['vol_ltc_ok'] / ltc_grouped['vol_ltc_tot']

# 3. Tính ODR
df_odr = df_odr_full.copy()
df_odr['Vol_Ontime'] = df_odr['GTC'] * df_odr['%Ontime']
odr_grouped = df_odr.groupby(['Tỉnh_mapped', 'Time']).agg(
    vol_odr_gtc=('GTC', 'sum'),
    vol_odr_ok=('Vol_Ontime', 'sum')
).reset_index()
odr_grouped['% ODR'] = odr_grouped['vol_odr_ok'] / odr_grouped['vol_odr_gtc']

# Tổ hợp AM-Tỉnh 4 tuần
df_pairs = df_cocau[['Am', 'Tỉnh']].dropna().drop_duplicates()
weeks = ['2026/21', '2026/22', '2026/23', '2026/24']
rows_list = []
for _, r_pair in df_pairs.iterrows():
    am = r_pair['Am']
    tinh = r_pair['Tỉnh']
    for wk in weeks:
        rows_list.append({'AM_mapped': am, 'Tỉnh_mapped': tinh, 'Time': wk})
df_base = pd.DataFrame(rows_list)

df_m = pd.merge(df_base, gtc_grouped[['AM_mapped', 'Tỉnh_mapped', 'Time', 'vol_gtc', '% GTC']], on=['AM_mapped', 'Tỉnh_mapped', 'Time'], how='left')
df_m = pd.merge(df_m, ltc_grouped[['AM_mapped', 'Tỉnh_mapped', 'Time', '% LTC']], on=['AM_mapped', 'Tỉnh_mapped', 'Time'], how='left')
df_m = pd.merge(df_m, odr_grouped[['Tỉnh_mapped', 'Time', '% ODR']], on=['Tỉnh_mapped', 'Time'], how='left')

# Đổi tên và chuẩn hoá dữ liệu
df_m = df_m.rename(columns={
    'AM_mapped': 'AM',
    'Tỉnh_mapped': 'Tỉnh',
    'Time': 'Tuần',
    'vol_gtc': 'Sản lượng giao',
    '% GTC': 'Tỉ lệ GTC',
    '% LTC': 'Tỉ lệ LTC',
    '% ODR': 'Tỉ lệ ODR'
}).sort_values(by=['AM', 'Tỉnh', 'Tuần']).reset_index(drop=True)

# 4. Tạo các bảng tóm tắt
df_am_w24 = df_m[df_m['Tuần'] == '2026/24'].groupby('AM').agg(
    sl=('Sản lượng giao', 'sum'),
    gtc=('Tỉ lệ GTC', 'mean')
).reset_index().sort_values(by='sl', ascending=False)
df_am_w24 = df_am_w24.rename(columns={'AM': 'AM W24', 'sl': 'Sản lượng W24', 'gtc': 'Tỉ lệ GTC W24'})

df_prov_w24_gtc = df_gtc[df_gtc['Time'] == '2026/24']
prov_gtc = df_prov_w24_gtc.groupby('Tỉnh_mapped').agg(v=('Volume', 'sum'), vok=('Vol_GTC', 'sum')).reset_index()
prov_gtc['GTC'] = prov_gtc['vok'] / prov_gtc['v']

df_prov_w24_ltc = df_ltc[df_ltc['Time'] == '2026/24']
prov_ltc = df_prov_w24_ltc.groupby('Tỉnh_mapped').agg(v=('Volume', 'sum'), vok=('Vol_LTC', 'sum')).reset_index()
prov_ltc['LTC'] = prov_ltc['vok'] / prov_ltc['v']


df_prov_w24_odr = df_odr[df_odr['Time'] == '2026/24']
prov_odr = df_prov_w24_odr.groupby('Tỉnh_mapped').agg(v=('GTC', 'sum'), vok=('Vol_Ontime', 'sum')).reset_index()
prov_odr['ODR'] = prov_odr['vok'] / prov_odr['v']

df_prov_w24 = pd.DataFrame({'Tỉnh W24': ['Khánh Hòa', 'Lâm Đồng', 'Bình Thuận', 'Ninh Thuận', 'Đắk Nông']})
df_prov_w24 = pd.merge(df_prov_w24, prov_gtc[['Tỉnh_mapped', 'v', 'GTC']], left_on='Tỉnh W24', right_on='Tỉnh_mapped', how='left').rename(columns={'v': 'Sản lượng W24', 'GTC': 'Tỉ lệ GTC W24'})
df_prov_w24 = pd.merge(df_prov_w24, prov_ltc[['Tỉnh_mapped', 'LTC']], left_on='Tỉnh W24', right_on='Tỉnh_mapped', how='left').rename(columns={'LTC': 'Tỉ lệ LTC W24'})
df_prov_w24 = pd.merge(df_prov_w24, prov_odr[['Tỉnh_mapped', 'ODR']], left_on='Tỉnh W24', right_on='Tỉnh_mapped', how='left').rename(columns={'ODR': 'Tỉ lệ ODR W24'})
df_prov_w24 = df_prov_w24.drop(columns=['Tỉnh_mapped_x', 'Tỉnh_mapped_y', 'Tỉnh_mapped']).fillna(0)

weekly_vols = []
for wk in weeks:
    sub_tot = df_gtc_full[df_gtc_full['Time'] == wk]
    ca1 = sub_tot[sub_tot['Loại Hàng'] == 'Hàng Mới Ca 1']['Volume'].sum()
    ca2 = sub_tot[sub_tot['Loại Hàng'] == 'Hàng Mới Ca 2']['Volume'].sum()
    ton = sub_tot[sub_tot['Loại Hàng'] == 'Hàng Tồn']['Volume'].sum()
    weekly_vols.append({'Tuần': 'W' + wk.split('/')[-1], 'Ca 1': ca1, 'Ca 2': ca2, 'Hàng Tồn': ton})
df_struct = pd.DataFrame(weekly_vols)

# Ghi vào Excel local
print("Đang ghi kết quả phân tích và bảng tóm tắt vào Excel local...")
wb_excel = openpyxl.load_workbook(OUTPUT_PATH)
if 'Phân tích AM-Tỉnh' in wb_excel.sheetnames:
    del wb_excel['Phân tích AM-Tỉnh']
ws = wb_excel.create_sheet('Phân tích AM-Tỉnh')
ws.views.sheetView[0].showGridLines = True

headers = ['AM', 'Tỉnh', 'Tuần', 'Sản lượng giao', 'Tỉ lệ GTC', 'Tỉ lệ LTC', 'Tỉ lệ ODR']
ws.append(headers)
for r_idx, row in df_m.iterrows():
    row_vals = [None if pd.isna(row[c]) else row[c] for c in df_m.columns]
    ws.append(row_vals)

# Summary 1 (I-K)
ws.cell(row=1, column=9, value="AM W24")
ws.cell(row=1, column=10, value="Sản lượng W24")
ws.cell(row=1, column=11, value="Tỉ lệ GTC W24")
for r_idx, row in df_am_w24.iterrows():
    ws.cell(row=r_idx + 2, column=9, value=row['AM W24'])
    ws.cell(row=r_idx + 2, column=10, value=float(row['Sản lượng W24']))
    ws.cell(row=r_idx + 2, column=11, value=float(row['Tỉ lệ GTC W24']))

# Summary 2 (M-Q)
ws.cell(row=1, column=13, value="Tỉnh W24")
ws.cell(row=1, column=14, value="Sản lượng W24")
ws.cell(row=1, column=15, value="Tỉ lệ GTC W24")
ws.cell(row=1, column=16, value="Tỉ lệ LTC W24")
ws.cell(row=1, column=17, value="Tỉ lệ ODR W24")
for r_idx, row in df_prov_w24.iterrows():
    ws.cell(row=r_idx + 2, column=13, value=row['Tỉnh W24'])
    ws.cell(row=r_idx + 2, column=14, value=float(row['Sản lượng W24']))
    ws.cell(row=r_idx + 2, column=15, value=float(row['Tỉ lệ GTC W24']))
    ws.cell(row=r_idx + 2, column=16, value=float(row['Tỉ lệ LTC W24']))
    ws.cell(row=r_idx + 2, column=17, value=float(row['Tỉ lệ ODR W24']))

# Summary 3 (S-V)
ws.cell(row=1, column=19, value="Tuần")
ws.cell(row=1, column=20, value="Ca 1")
ws.cell(row=1, column=21, value="Ca 2")
ws.cell(row=1, column=22, value="Hàng Tồn")
for r_idx, row in df_struct.iterrows():
    ws.cell(row=r_idx + 2, column=19, value=row['Tuần'])
    ws.cell(row=r_idx + 2, column=20, value=float(row['Ca 1']))
    ws.cell(row=r_idx + 2, column=21, value=float(row['Ca 2']))
    ws.cell(row=r_idx + 2, column=22, value=float(row['Hàng Tồn']))

# Format Excel local
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
header_fill = PatternFill(start_color='1E293B', end_color='1E293B', fill_type='solid')
header_font = Font(name='Segoe UI', size=11, bold=True, color='FFFFFF')
align_center = Alignment(horizontal='center', vertical='center')
align_left = Alignment(horizontal='left', vertical='center')
align_right = Alignment(horizontal='right', vertical='center')
thin_border = Border(left=Side(style='thin', color='CBD5E1'), right=Side(style='thin', color='CBD5E1'), top=Side(style='thin', color='CBD5E1'), bottom=Side(style='thin', color='CBD5E1'))

for col_idx in [1,2,3,4,5,6,7, 9,10,11, 13,14,15,16,17, 19,20,21,22]:
    cell = ws.cell(row=1, column=col_idx)
    cell.fill, cell.font, cell.alignment, cell.border = header_fill, header_font, align_center, thin_border

for r in range(2, ws.max_row + 1):
    for c in [1,2,3,4,5,6,7, 9,10,11, 13,14,15,16,17, 19,20,21,22]:
        cell = ws.cell(row=r, column=c)
        if cell.value is None: continue
        cell.font, cell.border = Font(name='Segoe UI', size=10), thin_border
        if c in [1, 2, 9, 13]: cell.alignment = align_left
        elif c in [3, 19]: cell.alignment = align_center
        elif c in [4, 10, 14, 20, 21, 22]: cell.alignment, cell.number_format = align_right, '#,##0'
        elif c in [5, 6, 7, 11, 15, 16, 17]: cell.alignment, cell.number_format = align_right, '0.00%'

for col in ws.columns:
    col_letter = openpyxl.utils.get_column_letter(col[0].column)
    ws.column_dimensions[col_letter].width = 14

try:
    wb_excel.save(OUTPUT_PATH)
    print(f"✔️ Đã cập nhật file Excel local tại: {OUTPUT_PATH}")
except PermissionError:
    ALT_PATH = r"c:\Users\lap4all\Desktop\NTB_Bao_Cao_Van_Hanh_Corrected.xlsx"
    wb_excel.save(ALT_PATH)

# Đồng bộ lên Google Sheet
print("Đang kết nối để cập nhật Google Sheet trực tuyến...")
creds = Credentials.from_service_account_file(JSON_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
gc = gspread.authorize(creds)
sh = gc.open_by_key(SHEET_ID)

try:
    ws_gsheet = sh.worksheet('Phân tích AM-Tỉnh')
    ws_id = ws_gsheet.id
except gspread.exceptions.WorksheetNotFound:
    ws_gsheet = sh.add_worksheet(title='Phân tích AM-Tỉnh', rows="200", cols="30")
    ws_id = ws_gsheet.id

ws_gsheet.clear()
ws_gsheet.resize(rows=200, cols=30)

print("Đang đồng bộ dữ liệu của tất cả bảng tóm tắt lên Google Sheet...")
max_cols = 22
values = []
for r in range(1, ws.max_row + 1):
    row_vals = []
    for c in range(1, max_cols + 1):
        val = ws.cell(row=r, column=c).value
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
            val = None
        row_vals.append(val)
    values.append(row_vals)

ws_gsheet.update(range_name='A1', values=values, value_input_option='USER_ENTERED')

# Format Google Sheets
try:
    for col_range in ["A1:G1", "I1:K1", "M1:Q1", "S1:V1"]:
        ws_gsheet.format(col_range, {
            "backgroundColor": {"red": 30/255, "green": 41/255, "blue": 59/255},
            "horizontalAlignment": "CENTER",
            "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontFamily": "Segoe UI", "fontSize": 11}
        })
    ws_gsheet.format(f"A2:V{ws.max_row}", {
        "textFormat": {"fontFamily": "Segoe UI", "fontSize": 10}
    })
except:
    pass

# Vẽ biểu đồ trực tuyến
print("Đang vẽ biểu đồ trực tiếp trên Google Sheet...")
chart1 = {
    "addChart": {
        "chart": {
            "spec": {
                "title": "BẢNG XẾP HẠNG SẢN LƯỢNG AM - TUẦN 24",
                "basicChart": {
                    "chartType": "BAR",
                    "legendPosition": "NO_LEGEND",
                    "axis": [
                        {"position": "BOTTOM_AXIS", "title": "Sản lượng giao"},
                        {"position": "LEFT_AXIS", "title": "AM"}
                    ],
                    "domains": [
                        {"domain": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 1, "endRowIndex": 21, "startColumnIndex": 8, "endColumnIndex": 9}]}}}
                    ],
                    "series": [
                        {"series": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 0, "endRowIndex": 21, "startColumnIndex": 9, "endColumnIndex": 10}]}}, "targetAxis": "BOTTOM_AXIS"}
                    ]
                }
            },
            "position": {
                "overlayPosition": {
                    "anchorCell": {"sheetId": ws_id, "rowIndex": 1, "columnIndex": 24},
                    "offsetXPixels": 0, "offsetYPixels": 0
                }
            }
        }
    }
}

chart2 = {
    "addChart": {
        "chart": {
            "spec": {
                "title": "HIỆU SUẤT VẬN HÀNH THEO TỈNH - TUẦN 24",
                "basicChart": {
                    "chartType": "COMBO",
                    "legendPosition": "BOTTOM_LEGEND",
                    "axis": [
                        {"position": "BOTTOM_AXIS", "title": "Tỉnh thành"},
                        {"position": "LEFT_AXIS", "title": "Sản lượng"},
                        {"position": "RIGHT_AXIS", "title": "Tỉ lệ (%)"}
                    ],
                    "domains": [
                        {"domain": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 1, "endRowIndex": 6, "startColumnIndex": 12, "endColumnIndex": 13}]}}}
                    ],
                    "series": [
                        {"series": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 0, "endRowIndex": 6, "startColumnIndex": 13, "endColumnIndex": 14}]}}, "targetAxis": "LEFT_AXIS", "type": "COLUMN"},
                        {"series": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 0, "endRowIndex": 6, "startColumnIndex": 14, "endColumnIndex": 15}]}}, "targetAxis": "RIGHT_AXIS", "type": "LINE"},
                        {"series": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 0, "endRowIndex": 6, "startColumnIndex": 15, "endColumnIndex": 16}]}}, "targetAxis": "RIGHT_AXIS", "type": "LINE"},
                        {"series": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 0, "endRowIndex": 6, "startColumnIndex": 16, "endColumnIndex": 17}]}}, "targetAxis": "RIGHT_AXIS", "type": "LINE"}
                    ]
                }
            },
            "position": {
                "overlayPosition": {
                    "anchorCell": {"sheetId": ws_id, "rowIndex": 22, "columnIndex": 24},
                    "offsetXPixels": 0, "offsetYPixels": 0
                }
            }
        }
    }
}

chart3 = {
    "addChart": {
        "chart": {
            "spec": {
                "title": "CƠ CẤU SẢN LƯỢNG VÀ HÀNG TỒN (W21 - W24)",
                "basicChart": {
                    "chartType": "COLUMN",
                    "legendPosition": "BOTTOM_LEGEND",
                    "stackedType": "STACKED",
                    "axis": [
                        {"position": "BOTTOM_AXIS", "title": "Tuần"},
                        {"position": "LEFT_AXIS", "title": "Số lượng đơn"}
                    ],
                    "domains": [
                        {"domain": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 1, "endRowIndex": 5, "startColumnIndex": 18, "endColumnIndex": 19}]}}}
                    ],
                    "series": [
                        {"series": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 0, "endRowIndex": 5, "startColumnIndex": 19, "endColumnIndex": 20}]}}, "targetAxis": "LEFT_AXIS"},
                        {"series": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 0, "endRowIndex": 5, "startColumnIndex": 20, "endColumnIndex": 21}]}}, "targetAxis": "LEFT_AXIS"},
                        {"series": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 0, "endRowIndex": 5, "startColumnIndex": 21, "endColumnIndex": 22}]}}, "targetAxis": "LEFT_AXIS"}
                    ]
                }
            },
            "position": {
                "overlayPosition": {
                    "anchorCell": {"sheetId": ws_id, "rowIndex": 43, "columnIndex": 24},
                    "offsetXPixels": 0, "offsetYPixels": 0
                }
            }
        }
    }
}

try:
    sh.batch_update({"requests": [chart1, chart2, chart3]})
    print("✔️ Đã vẽ thành công 3 biểu đồ trực quan động lên Google Sheet.")
except Exception as e:
    print(f"❌ Lỗi vẽ biểu đồ trên Google Sheets: {e}")

print("="*60)
print("🎉 ĐỒNG BỘ HÓA DỮ LIỆU & BIỂU ĐỒ LÊN GOOGLE SHEET HOÀN TẤT!")
print("="*60)
