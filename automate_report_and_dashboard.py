import pandas as pd
import openpyxl
from openpyxl.chart import BarChart, LineChart, Reference
import os
import sys
import unicodedata
import matplotlib.pyplot as plt
import numpy as np

# Đảm bảo in Tiếng Việt không lỗi font trên console Windows
sys.stdout.reconfigure(encoding='utf-8')

# --- CẤU HÌNH ĐƯỜNG DẪN (Chỉnh sửa ở đây khi sang tuần mới) ---
BASE_DIR = r"c:\Users\lap4all\Desktop"
INPUT_EXCEL = os.path.join(BASE_DIR, "New folder", "downloaded_user_sheet.xlsx")
OUTPUT_EXCEL = os.path.join(BASE_DIR, "NTB_Bao_Cao_Van_Hanh_Corrected.xlsx")
DESKTOP_DIR = BASE_DIR # Nơi lưu các tệp biểu đồ Dashboard (.png)

# Cấu hình danh sách tuần thô trong raw data và nhãn hiển thị trên biểu đồ
weeks_keys = ['2026/21', '2026/22', '2026/23', '2026/24']
weeks_label = ['W21', 'W22', 'W23', 'W24']


print("="*60)
print("BẮT ĐẦU CHẠY PIPELINE TỰ ĐỘNG HÓA BÁO CÁO VẬN HÀNH NTB")
print("="*60)

# -------------------------------------------------------------
# BƯỚC 1: LOAD DỮ LIỆU TỪ FILE EXCEL GỐC
# -------------------------------------------------------------
print("\n[BƯỚC 1] Đang đọc dữ liệu từ các sheet gốc...")
try:
    df_gtc_full = pd.read_excel(INPUT_EXCEL, sheet_name='dataGTC gốc full hàng')
    df_gtc_tts = pd.read_excel(INPUT_EXCEL, sheet_name='dataGTC gốc TTS')
    df_ltc_full = pd.read_excel(INPUT_EXCEL, sheet_name='dataLTC full hàng')
    df_ltc_tts = pd.read_excel(INPUT_EXCEL, sheet_name='dataLTC TTS')
    df_odr_full = pd.read_excel(INPUT_EXCEL, sheet_name='dataODRfull hàng ')
    df_odr_tts = pd.read_excel(INPUT_EXCEL, sheet_name='dataODR TTS')
    df_cocau = pd.read_excel(INPUT_EXCEL, sheet_name='cocau')
    
    # Load openpyxl workbook để ghi đè công thức
    wb = openpyxl.load_workbook(INPUT_EXCEL, data_only=False)
except Exception as e:
    print(f"❌ LỖI: Không thể mở file excel gốc hoặc thiếu sheet. Chi tiết: {e}")
    sys.exit(1)

# -------------------------------------------------------------
# BƯỚC 2: CHUẨN HÓA KHỚP NỐI DANH SÁCH AM & TỈNH (Unicode NFC)
# -------------------------------------------------------------
print("\n[BƯỚC 2] Chuẩn hóa Unicode và ánh xạ (mapping)...")
def normalize_name(name):
    if pd.isna(name):
        return ""
    # Loại bỏ khoảng trắng thừa, viết hoa, chuẩn hóa Unicode dựng sẵn NFC
    return unicodedata.normalize('NFC', str(name).strip()).upper()

df_cocau['BC_norm'] = df_cocau['BC'].apply(normalize_name)
df_cocau['Am_norm'] = df_cocau['Am'].apply(normalize_name)
df_cocau['Tỉnh_norm'] = df_cocau['Tỉnh'].apply(normalize_name)

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

# Ánh xạ AM và Tỉnh vào các sheet dữ liệu thô
for df in [df_gtc_full, df_gtc_tts, df_ltc_full, df_ltc_tts, df_odr_full, df_odr_tts]:
    if 'Chi tiết' in df.columns:
        df['AM_mapped'] = df['Chi tiết'].apply(map_am)
        df['Tỉnh_mapped'] = df['Chi tiết'].apply(map_tinh)
    if 'Quản lý' in df.columns:
        df['Tỉnh_mapped_ql'] = df['Quản lý'].apply(get_province_from_ql)
        if 'Tỉnh_mapped' in df.columns:
            df['Tỉnh_mapped'] = df['Tỉnh_mapped'].fillna(df['Tỉnh_mapped_ql'])
        else:
            df['Tỉnh_mapped'] = df['Tỉnh_mapped_ql']

# -------------------------------------------------------------
# BƯỚC 3: TÍNH TOÁN & GHI ĐÈ FILE EXCEL
# -------------------------------------------------------------
print("\n[BƯỚC 3] Đang tính toán dữ liệu chính xác và ghi đè vào file excel...")

# 3.1 Ghi đè sheet Sản lượng (Ca 1 + Ca 2 mới)
def overwrite_vols():
    ws = wb['sản lượng']
    df_tot = df_gtc_full[df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])]
    tot_grouped = df_tot.groupby(['AM_mapped', 'Time'])['Volume'].sum().unstack(fill_value=0)
    
    df_tts = df_gtc_tts[df_gtc_tts['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])]
    tts_grouped = df_tts.groupby(['AM_mapped', 'Time'])['Volume'].sum().unstack(fill_value=0)
    
    for row in range(3, 23):
        # Cột A: Tên AM, cột B-E: Tuần W21-W24
        am_name = ws.cell(row=row, column=1).value
        if am_name:
            norm_am = normalize_name(am_name)
            for idx in tot_grouped.index:
                if normalize_name(idx) == norm_am:
                    for col_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24'], start=2):
                        ws.cell(row=row, column=col_idx, value=float(tot_grouped.loc[idx, week]))
                    break
            ws.cell(row=row, column=6, value=f"=E{row}-D{row}")
            ws.cell(row=row, column=7, value=f"=IF(D{row}=0, 0, (E{row}-D{row})/D{row})")
            
        # Bảng TTS bên tay phải (cột I: AM, cột J-M: W21-W24)
        am_name_tts = ws.cell(row=row, column=9).value
        if am_name_tts:
            norm_am_tts = normalize_name(am_name_tts)
            for idx in tts_grouped.index:
                if normalize_name(idx) == norm_am_tts:
                    for col_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24'], start=10):
                        ws.cell(row=row, column=col_idx, value=float(tts_grouped.loc[idx, week]))
                    break
            ws.cell(row=row, column=14, value=f"=M{row}-L{row}")

    # Công thức hàng tổng cộng (Dòng 23)
    for c in [2, 3, 4, 5]:
        col_letter = openpyxl.utils.get_column_letter(c)
        ws.cell(row=23, column=c, value=f"=SUM({col_letter}3:{col_letter}22)")
    ws.cell(row=23, column=6, value="=E23-D23")
    ws.cell(row=23, column=7, value="=IF(D23=0, 0, (E23-D23)/D23)")
    
    for c in [10, 11, 12, 13]:
        col_letter = openpyxl.utils.get_column_letter(c)
        ws.cell(row=23, column=c, value=f"=SUM({col_letter}3:{col_letter}22)")
    ws.cell(row=23, column=14, value="=M23-L23")

# 3.2 Ghi đè các sheet tỉ lệ GTC (bình quân gia quyền)
def overwrite_gtc_rates(sheet_name, kinds, kinds_tts=None):
    if kinds_tts is None:
        kinds_tts = kinds
    ws = wb[sheet_name]
    df_tot = df_gtc_full[df_gtc_full['Loại Hàng'].isin(kinds)].copy()
    df_tot['Vol_Gan'] = df_tot['Volume'] * df_tot['% Gán']
    df_tot['Vol_GTC'] = df_tot['Volume'] * df_tot['% GTC']
    tot_grouped = df_tot.groupby(['AM_mapped', 'Time']).agg(v=('Volume', 'sum'), vg=('Vol_Gan', 'sum'), vc=('Vol_GTC', 'sum')).reset_index()
    tot_grouped['Pct_Gan'] = tot_grouped['vg'] / tot_grouped['v']
    tot_grouped['Pct_GTC'] = tot_grouped['vc'] / tot_grouped['v']
    
    df_tts = df_gtc_tts[df_gtc_tts['Loại Hàng'].isin(kinds_tts)].copy()
    df_tts['Vol_Gan'] = df_tts['Volume'] * df_tts['% Gán']
    df_tts['Vol_GTC'] = df_tts['Volume'] * df_tts['% GTC']
    tts_grouped = df_tts.groupby(['AM_mapped', 'Time']).agg(v=('Volume', 'sum'), vg=('Vol_Gan', 'sum'), vc=('Vol_GTC', 'sum')).reset_index()
    tts_grouped['Pct_Gan'] = tts_grouped['vg'] / tts_grouped['v']
    tts_grouped['Pct_GTC'] = tts_grouped['vc'] / tts_grouped['v']
    
    # Dynamically find the column index for the right-table AM
    col_am_tts = None
    for c in range(2, ws.max_column + 1):
        if ws.cell(row=3, column=c).value == 'AM':
            col_am_tts = c
            break
            
    if col_am_tts is None:
        col_am_tts = 13
        
    # Find 'So với' column for the right table (after col_am_tts)
    col_so_voi_tts = None
    for c in range(col_am_tts + 1, ws.max_column + 1):
        header_val = ws.cell(row=3, column=c).value
        if header_val and 'So với' in str(header_val):
            col_so_voi_tts = c
            break
            
    # Find left table 'So với' column
    col_so_voi_tot = None
    for c in range(2, col_am_tts):
        header_val = ws.cell(row=3, column=c).value
        if header_val and 'So với' in str(header_val):
            col_so_voi_tot = c
            break
            
    for row in range(4, 24):
        # Bảng Tổng
        am_name = ws.cell(row=row, column=1).value
        if am_name:
            norm_am = normalize_name(am_name)
            for week_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24']):
                subset = tot_grouped[(tot_grouped['AM_mapped'].apply(normalize_name) == norm_am) & (tot_grouped['Time'] == week)]
                if not subset.empty:
                    ws.cell(row=row, column=2 + 2*week_idx, value=float(subset.iloc[0]['Pct_Gan']))
                    ws.cell(row=row, column=3 + 2*week_idx, value=float(subset.iloc[0]['Pct_GTC']))
            if col_so_voi_tot:
                col_tot_w23_letter = openpyxl.utils.get_column_letter(col_so_voi_tot - 3)
                col_tot_w24_letter = openpyxl.utils.get_column_letter(col_so_voi_tot - 1)
                ws.cell(row=row, column=col_so_voi_tot, value=f"={col_tot_w24_letter}{row}-{col_tot_w23_letter}{row}")
            
        # Bảng TTS
        am_name_tts = ws.cell(row=row, column=col_am_tts).value
        if am_name_tts:
            norm_am_tts = normalize_name(am_name_tts)
            for week_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24']):
                subset = tts_grouped[(tts_grouped['AM_mapped'].apply(normalize_name) == norm_am_tts) & (tts_grouped['Time'] == week)]
                if not subset.empty:
                    ws.cell(row=row, column=col_am_tts + 1 + 2*week_idx, value=float(subset.iloc[0]['Pct_Gan']))
                    ws.cell(row=row, column=col_am_tts + 2 + 2*week_idx, value=float(subset.iloc[0]['Pct_GTC']))
            if col_so_voi_tts:
                col_tts_w23_letter = openpyxl.utils.get_column_letter(col_so_voi_tts - 3)
                col_tts_w24_letter = openpyxl.utils.get_column_letter(col_so_voi_tts - 1)
                ws.cell(row=row, column=col_so_voi_tts, value=f"={col_tts_w24_letter}{row}-{col_tts_w23_letter}{row}")

    # Set row 24 labels to "Tổng cộng"
    ws.cell(row=24, column=1, value="Tổng cộng")
    ws.cell(row=24, column=col_am_tts, value="Tổng cộng")

    # Ghi đè dòng tổng cộng vùng (Bình quân gia quyền vùng)
    for week_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24']):
        sub_tot = df_tot[df_tot['Time'] == week]
        if not sub_tot.empty:
            ws.cell(row=24, column=2 + 2*week_idx, value=float(sub_tot['Vol_Gan'].sum() / sub_tot['Volume'].sum()))
            ws.cell(row=24, column=3 + 2*week_idx, value=float(sub_tot['Vol_GTC'].sum() / sub_tot['Volume'].sum()))
        sub_tts = df_tts[df_tts['Time'] == week]
        if not sub_tts.empty:
            ws.cell(row=24, column=col_am_tts + 1 + 2*week_idx, value=float(sub_tts['Vol_Gan'].sum() / sub_tts['Volume'].sum()))
            ws.cell(row=24, column=col_am_tts + 2 + 2*week_idx, value=float(sub_tts['Vol_GTC'].sum() / sub_tts['Volume'].sum()))
            
    if col_so_voi_tot:
        col_tot_w23_letter = openpyxl.utils.get_column_letter(col_so_voi_tot - 3)
        col_tot_w24_letter = openpyxl.utils.get_column_letter(col_so_voi_tot - 1)
        ws.cell(row=24, column=col_so_voi_tot, value=f"={col_tot_w24_letter}24-{col_tot_w23_letter}24")
    if col_so_voi_tts:
        col_tts_w23_letter = openpyxl.utils.get_column_letter(col_so_voi_tts - 3)
        col_tts_w24_letter = openpyxl.utils.get_column_letter(col_so_voi_tts - 1)
        ws.cell(row=24, column=col_so_voi_tts, value=f"={col_tts_w24_letter}24-{col_tts_w23_letter}24")

# 3.3 Ghi đè sheet LTC (bình quân gia quyền theo sản lượng)
def overwrite_ltc_rates():
    ws = wb['LTC']
    df_tot = df_ltc_full[df_ltc_full['Cấp quản lý'] != 'Grand Total'].copy()
    df_tot['Vol_Gan'] = df_tot['Volume'] * df_tot['%Gán']
    df_tot['Vol_LTC'] = df_tot['Volume'] * df_tot['%LTC']
    tot_grouped = df_tot.groupby(['AM_mapped', 'Time']).agg(v=('Volume', 'sum'), vg=('Vol_Gan', 'sum'), vl=('Vol_LTC', 'sum')).reset_index()
    tot_grouped['Pct_Gan'] = tot_grouped['vg'] / tot_grouped['v']
    tot_grouped['Pct_LTC'] = tot_grouped['vl'] / tot_grouped['v']
    
    df_tts_clean = df_ltc_tts[df_ltc_tts['Cấp quản lý'] != 'Grand Total'].copy()
    df_tts_clean['Vol_Gan'] = df_tts_clean['Volume'] * df_tts_clean['%Gán']
    df_tts_clean['Vol_LTC'] = df_tts_clean['Volume'] * df_tts_clean['%LTC']
    tts_grouped = df_tts_clean.groupby(['AM_mapped', 'Time']).agg(v=('Volume', 'sum'), vg=('Vol_Gan', 'sum'), vl=('Vol_LTC', 'sum')).reset_index()
    tts_grouped['Pct_Gan'] = tts_grouped['vg'] / tts_grouped['v']
    tts_grouped['Pct_LTC'] = tts_grouped['vl'] / tts_grouped['v']
    
    for row in range(4, 24):
        # Bảng Tổng
        am_name = ws.cell(row=row, column=1).value
        if am_name:
            norm_am = normalize_name(am_name)
            for week_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24']):
                subset = tot_grouped[(tot_grouped['AM_mapped'].apply(normalize_name) == norm_am) & (tot_grouped['Time'] == week)]
                if not subset.empty:
                    ws.cell(row=row, column=2 + 2*week_idx, value=float(subset.iloc[0]['Pct_Gan']))
                    ws.cell(row=row, column=3 + 2*week_idx, value=float(subset.iloc[0]['Pct_LTC']))
            ws.cell(row=row, column=10, value=f"=I{row}-G{row}")
            
        # Bảng TTS
        am_name_tts = ws.cell(row=row, column=12).value
        if am_name_tts:
            norm_am_tts = normalize_name(am_name_tts)
            for week_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24']):
                subset = tts_grouped[(tts_grouped['AM_mapped'].apply(normalize_name) == norm_am_tts) & (tts_grouped['Time'] == week)]
                if not subset.empty:
                    ws.cell(row=row, column=13 + 2*week_idx, value=float(subset.iloc[0]['Pct_Gan']))
                    ws.cell(row=row, column=14 + 2*week_idx, value=float(subset.iloc[0]['Pct_LTC']))
            ws.cell(row=row, column=21, value=f"=T{row}-R{row}")

    # Dòng tổng cộng vùng (Row 24)
    for week_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24']):
        sub_tot = df_tot[df_tot['Time'] == week]
        if not sub_tot.empty:
            ws.cell(row=24, column=2 + 2*week_idx, value=float(sub_tot['Vol_Gan'].sum() / sub_tot['Volume'].sum()))
            ws.cell(row=24, column=3 + 2*week_idx, value=float(sub_tot['Vol_LTC'].sum() / sub_tot['Volume'].sum()))
        sub_tts = df_tts_clean[df_tts_clean['Time'] == week]
        if not sub_tts.empty:
            ws.cell(row=24, column=13 + 2*week_idx, value=float(sub_tts['Vol_Gan'].sum() / sub_tts['Volume'].sum()))
            ws.cell(row=24, column=14 + 2*week_idx, value=float(sub_tts['Vol_LTC'].sum() / sub_tts['Volume'].sum()))
    ws.cell(row=24, column=10, value="=I24-G24")
    ws.cell(row=24, column=21, value="=T24-R24")
    ws.cell(row=24, column=1, value="Tổng cộng")
    ws.cell(row=24, column=12, value="Tổng cộng")

# 3.4 Ghi đè sheet ODR (bình quân gia quyền theo số lượng GTC của tỉnh)
def overwrite_odr_rates():
    ws = wb['ODR']
    df_tot = df_odr_full.copy()
    df_tot['Vol_Ontime'] = df_tot['GTC'] * df_tot['%Ontime']
    tot_grouped = df_tot.groupby(['Tỉnh_mapped', 'Time']).agg(v=('GTC', 'sum'), vo=('Vol_Ontime', 'sum')).reset_index()
    tot_grouped['Pct_ODR'] = tot_grouped['vo'] / tot_grouped['v']
    
    df_tts = df_odr_tts.copy()
    df_tts['Vol_Ontime'] = df_tts['GTC'] * df_tts['%Ontime']
    tts_grouped = df_tts.groupby(['Tỉnh_mapped', 'Time']).agg(v=('GTC', 'sum'), vo=('Vol_Ontime', 'sum')).reset_index()
    tts_grouped['Pct_ODR'] = tts_grouped['vo'] / tts_grouped['v']
    
    # Bảng 1 & 2
    for row in range(3, 8):
        prov_name = ws.cell(row=row, column=1).value
        if prov_name:
            norm_prov = normalize_name(prov_name)
            for week_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24']):
                subset = tot_grouped[(tot_grouped['Tỉnh_mapped'].apply(normalize_name) == norm_prov) & (tot_grouped['Time'] == week)]
                if not subset.empty:
                    ws.cell(row=row, column=2 + week_idx, value=float(subset.iloc[0]['Pct_ODR']))
            ws.cell(row=row, column=6, value=f"=E{row}-D{row}")
            
        prov_name_t2 = ws.cell(row=row, column=8).value
        if prov_name_t2:
            norm_prov_t2 = normalize_name(prov_name_t2)
            for week_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24']):
                subset = tot_grouped[(tot_grouped['Tỉnh_mapped'].apply(normalize_name) == norm_prov_t2) & (tot_grouped['Time'] == week)]
                if not subset.empty:
                    ws.cell(row=row, column=9 + week_idx, value=float(subset.iloc[0]['Pct_ODR']))
            ws.cell(row=row, column=13, value=f"=L{row}-K{row}")

    for col_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24'], start=2):
        sub = df_tot[df_tot['Time'] == week]
        ws.cell(row=8, column=col_idx, value=float(sub['Vol_Ontime'].sum() / sub['GTC'].sum()))
    ws.cell(row=8, column=6, value="=E8-D8")
    
    for col_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24'], start=9):
        sub = df_tot[df_tot['Time'] == week]
        ws.cell(row=8, column=col_idx, value=float(sub['Vol_Ontime'].sum() / sub['GTC'].sum()))
    ws.cell(row=8, column=13, value="=L8-K8")

    # Bảng ODR TTS (Dòng 17-21, cột H-M)
    for row in range(17, 22):
        prov_name = ws.cell(row=row, column=8).value
        if prov_name:
            norm_prov = normalize_name(prov_name)
            for week_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24']):
                subset = tts_grouped[(tts_grouped['Tỉnh_mapped'].apply(normalize_name) == norm_prov) & (tts_grouped['Time'] == week)]
                if not subset.empty:
                    ws.cell(row=row, column=9 + week_idx, value=float(subset.iloc[0]['Pct_ODR']))
            ws.cell(row=row, column=13, value=f"=L{row}-K{row}")
            
    for col_idx, week in enumerate(['2026/21', '2026/22', '2026/23', '2026/24'], start=9):
        sub = df_tts[df_tts['Time'] == week]
        ws.cell(row=22, column=col_idx, value=float(sub['Vol_Ontime'].sum() / sub['GTC'].sum()))
    ws.cell(row=22, column=13, value="=L22-K22")

# Chạy tất cả hàm ghi đè dữ liệu
overwrite_vols()
overwrite_gtc_rates('gtcnew', ['Hàng Mới Ca 1', 'Hàng Mới Ca 2', 'Hàng Tồn'], ['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])
overwrite_gtc_rates('gtc + tồn', ['Hàng Mới Ca 1', 'Hàng Tồn'])
overwrite_gtc_rates('ca2', ['Hàng Mới Ca 2'])
overwrite_ltc_rates()
overwrite_odr_rates()

def fix_chart_grids():
    print("\n[BƯỚC 3.5] Đang sửa lỗi công thức lưới biểu đồ (#VALUE! và #N/A)...")
    
    # 1. Tab gtc + tồn (B32:C35)
    ws_gtc_ton = wb['gtc + tồn']
    ws_gtc_ton['A31'] = "Tuần"
    ws_gtc_ton['B31'] = "%GTC Tổng"
    ws_gtc_ton['C31'] = "%GTC TTS"
    weeks_cols_gtc = [("W21", "C", "M"), ("W22", "E", "O"), ("W23", "G", "Q"), ("W24", "I", "S")]
    for idx, (wk, col_tot, col_tts) in enumerate(weeks_cols_gtc, start=32):
        ws_gtc_ton[f'A{idx}'] = wk
        ws_gtc_ton[f'B{idx}'] = f"={col_tot}24"
        ws_gtc_ton[f'C{idx}'] = f"={col_tts}24"
    # Xoá dòng thừa 36
    ws_gtc_ton['A36'] = None
    ws_gtc_ton['B36'] = None
    ws_gtc_ton['C36'] = None
    
    # 2. Tab ca2 (B32:C35)
    ws_ca2 = wb['ca2']
    ws_ca2['A31'] = "Tuần"
    ws_ca2['B31'] = "%GTC Tổng"
    ws_ca2['C31'] = "%GTC TTS"
    for idx, (wk, col_tot, col_tts) in enumerate(weeks_cols_gtc, start=32):
        ws_ca2[f'A{idx}'] = wk
        ws_ca2[f'B{idx}'] = f"={col_tot}24"
        ws_ca2[f'C{idx}'] = f"={col_tts}24"
    ws_ca2['A36'] = None
    ws_ca2['B36'] = None
    ws_ca2['C36'] = None
    
    # 3. Tab LTC (B31:C34)
    ws_ltc = wb['LTC']
    ws_ltc['A30'] = "Tuần"
    ws_ltc['B30'] = "LTC Tổng"
    ws_ltc['C30'] = "LTC TTS"
    weeks_cols_ltc = [("W21", "C", "N"), ("W22", "E", "P"), ("W23", "G", "R"), ("W24", "I", "T")]
    for idx, (wk, col_tot, col_tts) in enumerate(weeks_cols_ltc, start=31):
        ws_ltc[f'A{idx}'] = wk
        ws_ltc[f'B{idx}'] = f"={col_tot}24"
        ws_ltc[f'C{idx}'] = f"={col_tts}24"
    ws_ltc['A35'] = None
    ws_ltc['B35'] = None
    ws_ltc['C35'] = None
    
    # 4. Tab gtcnew (A35:C35)
    ws_gtc = wb['gtcnew']
    ws_gtc['A35'] = None
    ws_gtc['B35'] = None
    ws_gtc['C35'] = None

fix_chart_grids()

# -------------------------------------------------------------
# BƯỚC 4: CẬP NHẬT THẺ CHỮ TÓM TẮT (SUMMARY TEXT CARDS) TRONG FILE EXCEL
# -------------------------------------------------------------
print("\n[BƯỚC 4] Đang cập nhật thẻ chữ tóm tắt báo cáo...")
# Sản lượng
df_gtc_new = df_gtc_full[(df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_full['Chi tiết'] != 'Grand Total')]
df_tts_new = df_gtc_tts[(df_gtc_tts['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_tts['Chi tiết'] != 'Grand Total')]
v_w23, v_w24 = df_gtc_new[df_gtc_new['Time'] == '2026/23']['Volume'].sum(), df_gtc_new[df_gtc_new['Time'] == '2026/24']['Volume'].sum()
vt_w23, vt_w24 = df_tts_new[df_tts_new['Time'] == '2026/23']['Volume'].sum(), df_tts_new[df_tts_new['Time'] == '2026/24']['Volume'].sum()
diff_tot, pct_tot = v_w24 - v_w23, (v_w24 - v_w23) / v_w23 if v_w23 > 0 else 0
diff_tts, pct_tts = vt_w24 - vt_w23, (vt_w24 - vt_w23) / vt_w23 if vt_w23 > 0 else 0

card_sl = f"Sản lượng tổng: Sản lượng tăng {diff_tot:,.0f} đơn (tăng {pct_tot:.2%}) so với tuần 23 | TTS tăng {diff_tts:,.0f} đơn (tăng {pct_tts:.2%}) so với tuần 23"
wb['sản lượng']['A27'] = card_sl

# GTC
sub_w23 = df_gtc_full[(df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_full['Time'] == '2026/23') & (df_gtc_full['Chi tiết'] != 'Grand Total')]
sub_w24 = df_gtc_full[(df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_full['Time'] == '2026/24') & (df_gtc_full['Chi tiết'] != 'Grand Total')]
overall_gtc_w23 = (sub_w23['Volume'] * sub_w23['% GTC']).sum() / sub_w23['Volume'].sum()
overall_gtc_w24 = (sub_w24['Volume'] * sub_w24['% GTC']).sum() / sub_w24['Volume'].sum()

sub_tts_w23 = df_gtc_tts[(df_gtc_tts['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_tts['Time'] == '2026/23') & (df_gtc_tts['Chi tiết'] != 'Grand Total')]
sub_tts_w24 = df_gtc_tts[(df_gtc_tts['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_tts['Time'] == '2026/24') & (df_gtc_tts['Chi tiết'] != 'Grand Total')]
overall_gtc_tts_w23 = (sub_tts_w23['Volume'] * sub_tts_w23['% GTC']).sum() / sub_tts_w23['Volume'].sum()
overall_gtc_tts_w24 = (sub_tts_w24['Volume'] * sub_tts_w24['% GTC']).sum() / sub_tts_w24['Volume'].sum()

diff_gtc = overall_gtc_w24 - overall_gtc_w23
diff_gtc_tts = overall_gtc_tts_w24 - overall_gtc_tts_w23
card_gtc = f"Giao thành công tổng: Tỉ lệ GTC tổng {'tăng' if diff_gtc >= 0 else 'giảm'} {abs(diff_gtc):.2%} so với tuần 23 | TTS {'tăng' if diff_gtc_tts >= 0 else 'giảm'} {abs(diff_gtc_tts):.2%} so với tuần 23"
wb['gtcnew']['A27'] = card_gtc

# -------------------------------------------------------------
# BƯỚC 5: TẠO BIỂU ĐỒ NATIVE (BẢN ĐỒ EXCEL GỐC) ĐỂ IMPORT LÊN GOOGLE SHEETS
# -------------------------------------------------------------
print("\n[BƯỚC 5] Đang vẽ biểu đồ Excel gốc để import lên Google Sheets...")

# 5.1 Biểu đồ sản lượng
ws_sl = wb['sản lượng']
ws_sl['A29'] = "Bảng dữ liệu biểu đồ"
ws_sl['A30'] = "Tuần"
ws_sl['B30'] = "Tổng vùng NTB"
ws_sl['C30'] = "Tuyến TTS"
weeks_cols = [("W21", "B", "J"), ("W22", "C", "K"), ("W23", "D", "L"), ("W24", "E", "M")]
for idx, (wk, col_tot, col_tts) in enumerate(weeks_cols, start=31):
    ws_sl[f'A{idx}'] = wk
    ws_sl[f'B{idx}'] = f"={col_tot}23"
    ws_sl[f'C{idx}'] = f"={col_tts}23"
chart_sl = BarChart()
chart_sl.type = "col"
chart_sl.style = 10
chart_sl.title = "SẢN LƯỢNG GIAO TỔNG & TTS VÙNG NTB (W21 - W24)"
chart_sl.add_data(Reference(ws_sl, min_col=2, min_row=30, max_col=3, max_row=34), titles_from_data=True)
chart_sl.set_categories(Reference(ws_sl, min_col=1, min_row=31, max_row=34))
chart_sl.width, chart_sl.height = 16, 10
ws_sl.add_chart(chart_sl, "A36")

# 5.2 Biểu đồ GTC
ws_gtc = wb['gtcnew']
ws_gtc['A29'] = "Bảng dữ liệu biểu đồ"
ws_gtc['A30'] = "Tuần"
ws_gtc['B30'] = "GTC Tổng"
ws_gtc['C30'] = "GTC TTS"
gtc_cols = [("W21", "C", "O"), ("W22", "E", "Q"), ("W23", "G", "S"), ("W24", "I", "U")]
for idx, (wk, col_tot, col_tts) in enumerate(gtc_cols, start=31):
    ws_gtc[f'A{idx}'] = wk
    ws_gtc[f'B{idx}'] = f"={col_tot}24"
    ws_gtc[f'C{idx}'] = f"={col_tts}24"
chart_gtc = LineChart()
chart_gtc.title = "XU HƯỚNG TỈ LỆ GIAO THÀNH CÔNG MỚI (W21 - W24)"
chart_gtc.add_data(Reference(ws_gtc, min_col=2, min_row=30, max_col=3, max_row=34), titles_from_data=True)
chart_gtc.set_categories(Reference(ws_gtc, min_col=1, min_row=31, max_row=34))
chart_gtc.width, chart_gtc.height = 16, 10
ws_gtc.add_chart(chart_gtc, "A36")

# 5.3 Biểu đồ LTC
ws_ltc = wb['LTC']
ws_ltc['A29'] = "Bảng dữ liệu biểu đồ"
ws_ltc['A30'] = "Tuần"
ws_ltc['B30'] = "LTC Tổng"
ws_ltc['C30'] = "LTC TTS"
ltc_cols = [("W21", "C", "N"), ("W22", "E", "P"), ("W23", "G", "R"), ("W24", "I", "T")]
for idx, (wk, col_tot, col_tts) in enumerate(ltc_cols, start=31):
    ws_ltc[f'A{idx}'] = wk
    ws_ltc[f'B{idx}'] = f"={col_tot}24"
    ws_ltc[f'C{idx}'] = f"={col_tts}24"
chart_ltc = LineChart()
chart_ltc.title = "XU HƯỚNG TỈ LỆ LẤY THÀNH CÔNG (W21 - W24)"
chart_ltc.add_data(Reference(ws_ltc, min_col=2, min_row=30, max_col=3, max_row=34), titles_from_data=True)
chart_ltc.set_categories(Reference(ws_ltc, min_col=1, min_row=31, max_row=34))
chart_ltc.width, chart_ltc.height = 16, 10
ws_ltc.add_chart(chart_ltc, "A36")

# 5.4 Biểu đồ ODR
ws_odr = wb['ODR']
ws_odr['A25'] = "Bảng dữ liệu biểu đồ"
ws_odr['A26'] = "Tuần"
ws_odr['B26'] = "Bình Thuận"
ws_odr['C26'] = "Khánh Hòa"
ws_odr['D26'] = "Lâm Đồng"
ws_odr['E26'] = "Ninh Thuận"
ws_odr['F26'] = "Đắk Nông"
odr_cols = ["B", "C", "D", "E"]
for idx, wk in enumerate(["W21", "W22", "W23", "W24"]):
    row_idx = 27 + idx
    col_letter = odr_cols[idx]
    ws_odr[f'A{row_idx}'] = wk
    ws_odr[f'B{row_idx}'] = f"={col_letter}3"
    ws_odr[f'C{row_idx}'] = f"={col_letter}4"
    ws_odr[f'D{row_idx}'] = f"={col_letter}5"
    ws_odr[f'E{row_idx}'] = f"={col_letter}6"
    ws_odr[f'F{row_idx}'] = f"={col_letter}7"
chart_odr = LineChart()
chart_odr.title = "XU HƯỚNG ODR THEO TỈNH VÙNG NTB (W21 - W24)"
chart_odr.add_data(Reference(ws_odr, min_col=2, min_row=26, max_col=6, max_row=30), titles_from_data=True)
chart_odr.set_categories(Reference(ws_odr, min_col=1, min_row=27, max_row=30))
chart_odr.width, chart_odr.height = 16, 10
ws_odr.add_chart(chart_odr, "A32")

# Lưu Workbook đã sửa đổi
try:
    wb.save(OUTPUT_EXCEL)
    print(f"✔️ Đã lưu workbook hoàn chỉnh tại: {OUTPUT_EXCEL}")
except PermissionError:
    ALT_OUTPUT = os.path.join(BASE_DIR, "NTB_Bao_Cao_Van_Hanh_Co_Bieu_Do.xlsx")
    wb.save(ALT_OUTPUT)
    print(f"⚠️ Cảnh báo: File '{OUTPUT_EXCEL}' đang bị mở ở chương trình khác.")
    print(f"✔️ Đã lưu dự phòng sang file mới: {ALT_OUTPUT}")
except Exception as e:
    print(f"❌ LỖI: Không thể lưu file Excel đầu ra. Chi tiết: {e}")

# -------------------------------------------------------------
# BƯỚC 6: VẼ BIỂU ĐỒ SAAS DASHBOARD CARDS (DARK THEME) RA FILE ẢNH DESKTOP
# -------------------------------------------------------------
print("\n[BƯỚC 6] Đang vẽ các biểu đồ Dashboard dạng ảnh cao cấp (SaaS style) ra Desktop...")

# Cấu hình Theme của Dashboard
plt.rcParams['figure.facecolor'] = '#0B0F19'
plt.rcParams['axes.facecolor'] = '#0B0F19'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Roboto', 'Arial', 'sans-serif']
plt.rcParams['text.color'] = '#F8FAFC'
plt.rcParams['axes.labelcolor'] = '#94A3B8'
plt.rcParams['xtick.color'] = '#94A3B8'
plt.rcParams['ytick.color'] = '#94A3B8'

weeks_label = ['W21', 'W22', 'W23', 'W24']
x = np.arange(len(weeks_label))
vols_tot = [df_gtc_new[df_gtc_new['Time'] == wk]['Volume'].sum() for wk in weeks_keys]
vols_tts = [df_tts_new[df_tts_new['Time'] == wk]['Volume'].sum() for wk in weeks_keys]

# Tính toán các tỉ lệ cho GTC
gtc_tot_rates = []
gtc_tts_rates = []
for week in weeks_keys:
    sub_tot = df_gtc_full[(df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_full['Time'] == week) & (df_gtc_full['Chi tiết'] != 'Grand Total')]
    gtc_tot_rates.append((sub_tot['Volume'] * sub_tot['% GTC']).sum() / sub_tot['Volume'].sum() if not sub_tot.empty else 0)
    sub_tts = df_gtc_tts[(df_gtc_tts['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_tts['Time'] == week) & (df_gtc_tts['Chi tiết'] != 'Grand Total')]
    gtc_tts_rates.append((sub_tts['Volume'] * sub_tts['% GTC']).sum() / sub_tts['Volume'].sum() if not sub_tts.empty else 0)

# Tính toán các tỉ lệ cho LTC
ltc_tot_rates = []
ltc_tts_rates = []
for week in weeks_keys:
    sub_tot = df_ltc_full[(df_ltc_full['Cấp quản lý'] != 'Grand Total') & (df_ltc_full['Time'] == week)]
    ltc_tot_rates.append((sub_tot['Volume'] * sub_tot['%LTC']).sum() / sub_tot['Volume'].sum() if not sub_tot.empty else 0)
    sub_tts = df_ltc_tts[(df_ltc_tts['Cấp quản lý'] != 'Grand Total') & (df_ltc_tts['Time'] == week)]
    ltc_tts_rates.append((sub_tts['Volume'] * sub_tts['%LTC']).sum() / sub_tts['Volume'].sum() if not sub_tts.empty else 0)


# Tính toán ODR theo tỉnh
df_odr_tot = df_odr_full.copy()
df_odr_tot['Vol_Ontime'] = df_odr_tot['GTC'] * df_odr_tot['%Ontime']
odr_grouped = df_odr_tot.groupby(['Tỉnh_mapped', 'Time']).agg(v=('GTC', 'sum'), vo=('Vol_Ontime', 'sum')).reset_index()
odr_grouped['Pct_ODR'] = odr_grouped['vo'] / odr_grouped['v']
provinces = odr_grouped['Tỉnh_mapped'].dropna().unique()
colors = ['#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6']

# 6.1 Card Sản lượng
fig, ax = plt.subplots(figsize=(8, 5.2))
fig.subplots_adjust(top=0.70, left=0.08, right=0.92, bottom=0.12)
ax.plot(x, vols_tot, marker='o', linewidth=3.5, color='#4F46E5', mfc='white', mew=2.5, ms=8, label='Tổng Vùng NTB', zorder=4)
ax.fill_between(x, vols_tot, color='#4F46E5', alpha=0.15)
ax.plot(x, vols_tts, marker='o', linewidth=3.5, color='#06B6D4', mfc='white', mew=2.5, ms=8, label='Trong đó: Tuyến TTS', zorder=4)
ax.fill_between(x, vols_tts, color='#06B6D4', alpha=0.15)
fig.text(0.06, 0.89, "SẢN LƯỢNG GIAO TỔNG & TTS VÙNG NTB", fontsize=10, fontweight='bold', color='#94A3B8')
fig.text(0.06, 0.77, f"{vols_tot[-1]:,.0f} đơn", fontsize=24, fontweight='bold', color='#FFFFFF')
fig.text(0.34, 0.78, f"▲ +{pct_tot:.2%} vs W23", fontsize=9.5, fontweight='bold', color='#10B981', bbox=dict(facecolor='#064E3B', edgecolor='none', boxstyle='round,pad=0.3'))
ax.set_ylim(0, 430000)
ax.set_xticks(x)
ax.set_xticklabels(weeks_label, fontsize=10)
ax.grid(axis='y', linestyle=':', alpha=0.2, color='#E2E8F0', zorder=0)
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)
ax.legend(frameon=False, loc='upper left', fontsize=9, labelcolor='#94A3B8')
ax.annotate(f"{vols_tot[-1]:,.0f}", (x[-1], vols_tot[-1]), textcoords="offset points", xytext=(0,12), ha='center', fontweight='bold', color='#4F46E5')
ax.annotate(f"{vols_tts[-1]:,.0f}", (x[-1], vols_tts[-1]), textcoords="offset points", xytext=(0,12), ha='center', fontweight='bold', color='#06B6D4')
plt.savefig(os.path.join(DESKTOP_DIR, "db_card_volume.png"), dpi=200, facecolor='#0B0F19')
plt.close()

# 6.2 Card GTC
fig, ax = plt.subplots(figsize=(8, 5.2))
fig.subplots_adjust(top=0.70, left=0.08, right=0.92, bottom=0.12)
ax.plot(x, [r * 100 for r in gtc_tot_rates], marker='o', linewidth=3.5, color='#4F46E5', mfc='white', mew=2.5, ms=8, label='GTC Tổng', zorder=4)
ax.fill_between(x, [r * 100 for r in gtc_tot_rates], color='#4F46E5', alpha=0.1)
ax.plot(x, [r * 100 for r in gtc_tts_rates], marker='o', linewidth=3.5, color='#F43F5E', mfc='white', mew=2.5, ms=8, label='GTC TTS', zorder=4)
ax.fill_between(x, [r * 100 for r in gtc_tts_rates], color='#F43F5E', alpha=0.1)
fig.text(0.06, 0.89, "TỈ LỆ GIAO THÀNH CÔNG MỚI (GTC)", fontsize=10, fontweight='bold', color='#94A3B8')
fig.text(0.06, 0.77, f"{gtc_tot_rates[-1]:.2%}", fontsize=24, fontweight='bold', color='#FFFFFF')
fig.text(0.24, 0.78, f"{'▲' if diff_gtc >= 0 else '▼'} {diff_gtc:+.2%} vs W23", fontsize=9.5, fontweight='bold', color='#10B981' if diff_gtc >= 0 else '#EF4444', bbox=dict(facecolor='#064E3B' if diff_gtc >= 0 else '#7F1D1D', edgecolor='none', boxstyle='round,pad=0.3'))
ax.set_ylim(40, 85)
ax.set_xticks(x)
ax.set_xticklabels(weeks_label, fontsize=10)
ax.grid(axis='y', linestyle=':', alpha=0.2, color='#E2E8F0', zorder=0)
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)
ax.legend(frameon=False, loc='lower right', fontsize=9, labelcolor='#94A3B8')
for i, (t, s) in enumerate(zip(gtc_tot_rates, gtc_tts_rates)):
    ax.annotate(f'{t:.2%}', (x[i], t*100), textcoords="offset points", xytext=(0, 12), ha='center', fontweight='semibold', color='#4F46E5', fontsize=9)
    ax.annotate(f'{s:.2%}', (x[i], s*100), textcoords="offset points", xytext=(0, -20), ha='center', fontweight='semibold', color='#F43F5E', fontsize=9)
plt.savefig(os.path.join(DESKTOP_DIR, "db_card_gtc.png"), dpi=200, facecolor='#0B0F19')
plt.close()

# 6.3 Card LTC
fig, ax = plt.subplots(figsize=(8, 5.2))
fig.subplots_adjust(top=0.70, left=0.08, right=0.92, bottom=0.12)
ax.plot(x, [r * 100 for r in ltc_tot_rates], marker='o', linewidth=3.5, color='#10B981', mfc='white', mew=2.5, ms=8, label='LTC Tổng', zorder=4)
ax.fill_between(x, [r * 100 for r in ltc_tot_rates], color='#10B981', alpha=0.1)
ax.plot(x, [r * 100 for r in ltc_tts_rates], marker='o', linewidth=3.5, color='#F59E0B', mfc='white', mew=2.5, ms=8, label='LTC TTS', zorder=4)
ax.fill_between(x, [r * 100 for r in ltc_tts_rates], color='#F59E0B', alpha=0.1)
fig.text(0.06, 0.89, "TỈ LỆ LẤY THÀNH CÔNG (LTC)", fontsize=10, fontweight='bold', color='#94A3B8')
fig.text(0.06, 0.77, f"{ltc_tot_rates[-1]:.2%}", fontsize=24, fontweight='bold', color='#FFFFFF')
fig.text(0.24, 0.78, f"{'▲' if (ltc_tot_rates[-1]-ltc_tot_rates[-2]) >= 0 else '▼'} {(ltc_tot_rates[-1]-ltc_tot_rates[-2]):+.2%} vs W23", fontsize=9.5, fontweight='bold', color='#10B981' if (ltc_tot_rates[-1]-ltc_tot_rates[-2]) >= 0 else '#EF4444', bbox=dict(facecolor='#064E3B' if (ltc_tot_rates[-1]-ltc_tot_rates[-2]) >= 0 else '#7F1D1D', edgecolor='none', boxstyle='round,pad=0.3'))
ax.set_ylim(80, 100)
ax.set_xticks(x)
ax.set_xticklabels(weeks_label, fontsize=10)
ax.grid(axis='y', linestyle=':', alpha=0.2, color='#E2E8F0', zorder=0)
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)
ax.legend(frameon=False, loc='lower right', fontsize=9, labelcolor='#94A3B8')
for i, (t, s) in enumerate(zip(ltc_tot_rates, ltc_tts_rates)):
    ax.annotate(f'{t:.2%}', (x[i], t*100), textcoords="offset points", xytext=(0, 12), ha='center', fontweight='semibold', color='#10B981', fontsize=9)
    ax.annotate(f'{s:.2%}', (x[i], s*100), textcoords="offset points", xytext=(0, -20), ha='center', fontweight='semibold', color='#F59E0B', fontsize=9)
plt.savefig(os.path.join(DESKTOP_DIR, "db_card_ltc.png"), dpi=200, facecolor='#0B0F19')
plt.close()

# 6.4 Card ODR
fig, ax = plt.subplots(figsize=(8, 5.2))
fig.subplots_adjust(top=0.72, left=0.08, right=0.92, bottom=0.12)
for idx, prov in enumerate(provinces):
    sub = odr_grouped[odr_grouped['Tỉnh_mapped'] == prov]
    sub = sub.set_index('Time').reindex(weeks_keys).reset_index()
    rates = sub['Pct_ODR'].fillna(0) * 100
    ax.plot(x, rates, marker='o', linewidth=2.5, color=colors[idx % len(colors)], mfc='white', mew=2, ms=7, label=prov)
    if not rates.empty:
        val = rates.iloc[-1]
        ax.annotate(f'{val/100:.1%}', (x[-1], val), textcoords="offset points", xytext=(10, -3), ha='left', fontweight='semibold', color=colors[idx % len(colors)], fontsize=9)

# Calculate region average ODR for W24 and W23
df_odr_w24 = df_odr_full[df_odr_full['Time'] == '2026/24']
df_odr_w23 = df_odr_full[df_odr_full['Time'] == '2026/23']
odr_w24_avg = (df_odr_w24['GTC'] * df_odr_w24['%Ontime']).sum() / df_odr_w24['GTC'].sum()
odr_w23_avg = (df_odr_w23['GTC'] * df_odr_w23['%Ontime']).sum() / df_odr_w23['GTC'].sum()
diff_odr = odr_w24_avg - odr_w23_avg

fig.text(0.06, 0.89, "TỈ LỆ GIAO ĐÚNG HẠN ODR THEO TỈNH", fontsize=10, fontweight='bold', color='#94A3B8')
fig.text(0.06, 0.77, f"{odr_w24_avg:.2%}", fontsize=24, fontweight='bold', color='#FFFFFF')
fig.text(0.24, 0.78, f"{'▲' if diff_odr >= 0 else '▼'} {diff_odr:+.2%} vs W23", fontsize=9.5, fontweight='bold', color='#10B981' if diff_odr >= 0 else '#EF4444', bbox=dict(facecolor='#064E3B' if diff_odr >= 0 else '#7F1D1D', edgecolor='none', boxstyle='round,pad=0.3'))
ax.set_ylim(80, 100)
ax.set_xticks(x)
ax.set_xticklabels(weeks_label, fontsize=10)
ax.grid(axis='y', linestyle=':', alpha=0.2, color='#E2E8F0', zorder=0)
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)
ax.legend(frameon=False, loc='lower left', fontsize=9, labelcolor='#94A3B8')
plt.savefig(os.path.join(DESKTOP_DIR, "db_card_odr.png"), dpi=200, facecolor='#0B0F19')
plt.close()

print("\n" + "="*60)
print("✔️ HOÀN THÀNH PIPELINE! Toàn bộ file Excel và 4 biểu đồ đã được lưu.")
print("="*60)
