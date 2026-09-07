import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import sys
import os
import unicodedata
import math
from dotenv import load_dotenv

# Configure output encoding for Vietnamese characters
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

JSON_FILE = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') or r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
if not os.path.exists(JSON_FILE):
    JSON_FILE = 'credentials.json'

SHEET_ID = os.environ.get('SHEET_ID') or '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'

print("="*60)
print("BẮT ĐẦU CHẠY PIPELINE PHÂN TÍCH SONG SONG (ALL vs TTS) TRÊN GOOGLE SHEETS")
print("="*60)

# 1. Kết nối Google Sheet
print("Đang kết nối tới Google Sheets...")
creds = Credentials.from_service_account_file(
    JSON_FILE, 
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)
gc = gspread.authorize(creds)
sh = gc.open_by_key(SHEET_ID)

# 2. Hàm đọc worksheet thành DataFrame
def get_df_from_sheet(sheet_name):
    print(f"-> Đang tải worksheet '{sheet_name}'...")
    ws = sh.worksheet(sheet_name)
    data = ws.get_all_values(value_render_option='UNFORMATTED_VALUE')
    if not data:
        return pd.DataFrame()
    headers = data[0]
    df = pd.DataFrame(data[1:], columns=headers)
    return df

# Đọc tất cả 7 sheet thô (bao gồm cả các sheet TTS)
df_gtc_full = get_df_from_sheet('dataGTC gốc full hàng')
df_gtc_tts = get_df_from_sheet('dataGTC gốc TTS')
df_ltc_full = get_df_from_sheet('dataLTC full hàng')
df_ltc_tts = get_df_from_sheet('dataLTC TTS')
df_odr_full = get_df_from_sheet('dataODRfull hàng ')
df_odr_tts = get_df_from_sheet('dataODR TTS')
df_cocau = get_df_from_sheet('cocau')

print("✔️ Đã đọc xong tất cả dữ liệu thô (All & TTS) từ Google Sheets.")

# 3. Chuẩn hóa tên AM/Bưu cục
def normalize_name(name):
    if pd.isna(name): return ""
    return unicodedata.normalize('NFC', str(name).strip()).upper()

# Ánh xạ từ bưu cục sang AM và Tỉnh
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

# Ánh xạ AM và Tỉnh vào tất cả các sheet thô
for df in [df_gtc_full, df_gtc_tts, df_ltc_full, df_ltc_tts, df_odr_full, df_odr_tts]:
    if 'Chi tiết' in df.columns:
        df['AM_mapped'] = df['Chi tiết'].apply(map_am)
        df['Tỉnh_mapped'] = df['Chi tiết'].apply(map_tinh)
    if 'Quản lý' in df.columns:
        df['Tỉnh_mapped_ql'] = df['Quản lý'].apply(get_province_from_ql)
        df['Tỉnh_mapped'] = df['Tỉnh_mapped'].fillna(df['Tỉnh_mapped_ql'])

# Ép kiểu dữ liệu số để tránh lỗi tính toán
for df in [df_gtc_full, df_gtc_tts]:
    for col in ['Volume', '% Gán', '% GTC']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

for df in [df_ltc_full, df_ltc_tts]:
    for col in ['Volume', '%Gán', '%LTC']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

for df in [df_odr_full, df_odr_tts]:
    for col in ['GTC', '%Ontime']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

# 4. Tính toán GTC (Tất cả hàng & Tuyến TTS)
print("Đang tổng hợp dữ liệu GTC (All & TTS)...")
# GTC Tất cả hàng
df_gtc = df_gtc_full[(df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2', 'Hàng Tồn'])) & (df_gtc_full['Chi tiết'] != 'Grand Total')].copy()
df_gtc['Vol_Gan'] = df_gtc['Volume'] * df_gtc['% Gán']
df_gtc['Vol_GTC'] = df_gtc['Volume'] * df_gtc['% GTC']
gtc_grouped = df_gtc.groupby(['AM_mapped', 'Tỉnh_mapped', 'Time']).agg(
    vol_gtc=('Volume', 'sum'),
    vol_gtc_ok=('Vol_GTC', 'sum')
).reset_index()
gtc_grouped['% GTC'] = gtc_grouped['vol_gtc_ok'] / gtc_grouped['vol_gtc']

# GTC TTS
df_gtc_tts_clean = df_gtc_tts[(df_gtc_tts['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_tts['Chi tiết'] != 'Grand Total')].copy()
df_gtc_tts_clean['Vol_Gan'] = df_gtc_tts_clean['Volume'] * df_gtc_tts_clean['% Gán']
df_gtc_tts_clean['Vol_GTC'] = df_gtc_tts_clean['Volume'] * df_gtc_tts_clean['% GTC']
gtc_tts_grouped = df_gtc_tts_clean.groupby(['AM_mapped', 'Tỉnh_mapped', 'Time']).agg(
    vol_gtc_tts=('Volume', 'sum'),
    vol_gtc_tts_ok=('Vol_GTC', 'sum')
).reset_index()
gtc_tts_grouped['% GTC TTS'] = gtc_tts_grouped['vol_gtc_tts_ok'] / gtc_tts_grouped['vol_gtc_tts']

# 5. Tính toán LTC (Tất cả hàng & Tuyến TTS)
print("Đang tổng hợp dữ liệu LTC (All & TTS)...")
# LTC Tất cả hàng
df_ltc = df_ltc_full[df_ltc_full['Cấp quản lý'] != 'Grand Total'].copy()
df_ltc['Vol_Gan'] = df_ltc['Volume'] * df_ltc['%Gán']
df_ltc['Vol_LTC'] = df_ltc['Volume'] * df_ltc['%LTC']
ltc_grouped = df_ltc.groupby(['AM_mapped', 'Tỉnh_mapped', 'Time']).agg(
    vol_ltc_tot=('Volume', 'sum'),
    vol_gan_ltc=('Vol_Gan', 'sum'),
    vol_ltc_ok=('Vol_LTC', 'sum')
).reset_index()
ltc_grouped['% LTC'] = ltc_grouped['vol_ltc_ok'] / ltc_grouped['vol_ltc_tot']

# LTC TTS
df_ltc_tts_clean = df_ltc_tts[df_ltc_tts['Cấp quản lý'] != 'Grand Total'].copy()
df_ltc_tts_clean['Vol_Gan'] = df_ltc_tts_clean['Volume'] * df_ltc_tts_clean['%Gán']
df_ltc_tts_clean['Vol_LTC'] = df_ltc_tts_clean['Volume'] * df_ltc_tts_clean['%LTC']
ltc_tts_grouped = df_ltc_tts_clean.groupby(['AM_mapped', 'Tỉnh_mapped', 'Time']).agg(
    vol_ltc_tts_tot=('Volume', 'sum'),
    vol_gan_ltc_tts=('Vol_Gan', 'sum'),
    vol_ltc_tts_ok=('Vol_LTC', 'sum')
).reset_index()
ltc_tts_grouped['% LTC TTS'] = ltc_tts_grouped['vol_ltc_tts_ok'] / ltc_tts_grouped['vol_ltc_tts_tot']

# 6. Tính toán ODR (Tất cả hàng & Tuyến TTS)
print("Đang tổng hợp dữ liệu ODR (All & TTS)...")
# ODR Tất cả hàng
df_odr = df_odr_full[~df_odr_full['Quản lý'].astype(str).str.contains('Grand Total|Tổng cộng', case=False, na=False)].copy()
df_odr['Vol_Ontime'] = df_odr['GTC'] * df_odr['%Ontime']
odr_grouped = df_odr.groupby(['Tỉnh_mapped', 'Time']).agg(
    vol_odr_gtc=('GTC', 'sum'),
    vol_odr_ok=('Vol_Ontime', 'sum')
).reset_index()
odr_grouped['% ODR'] = odr_grouped['vol_odr_ok'] / odr_grouped['vol_odr_gtc']

# ODR TTS
df_odr_tts_clean = df_odr_tts[~df_odr_tts['Quản lý'].astype(str).str.contains('Grand Total|Tổng cộng', case=False, na=False)].copy()
df_odr_tts_clean['Vol_Ontime'] = df_odr_tts_clean['GTC'] * df_odr_tts_clean['%Ontime']
odr_tts_grouped = df_odr_tts_clean.groupby(['Tỉnh_mapped', 'Time']).agg(
    vol_odr_gtc_tts=('GTC', 'sum'),
    vol_odr_ok_tts=('Vol_Ontime', 'sum')
).reset_index()
odr_tts_grouped['% ODR TTS'] = odr_tts_grouped['vol_odr_ok_tts'] / odr_tts_grouped['vol_odr_gtc_tts']

# 7. Tổ hợp AM-Tỉnh chéo trong 4 tuần (W21-W24)
print("Đang ghép dữ liệu thành bảng phân tích song song...")
df_pairs = df_cocau[['Am', 'Tỉnh']].dropna().drop_duplicates()
weeks = ['2026/21', '2026/22', '2026/23', '2026/24']
rows_list = []
for _, r_pair in df_pairs.iterrows():
    am = r_pair['Am']
    tinh = r_pair['Tỉnh']
    for wk in weeks:
        rows_list.append({'AM_mapped': am, 'Tỉnh_mapped': tinh, 'Time': wk})
df_base = pd.DataFrame(rows_list)

# Ghép chi tiết All
df_m = pd.merge(df_base, gtc_grouped[['AM_mapped', 'Tỉnh_mapped', 'Time', 'vol_gtc', '% GTC']], on=['AM_mapped', 'Tỉnh_mapped', 'Time'], how='left')
# Ghép chi tiết TTS
df_m = pd.merge(df_m, gtc_tts_grouped[['AM_mapped', 'Tỉnh_mapped', 'Time', 'vol_gtc_tts', '% GTC TTS']], on=['AM_mapped', 'Tỉnh_mapped', 'Time'], how='left')
# Ghép LTC All & TTS
df_m = pd.merge(df_m, ltc_grouped[['AM_mapped', 'Tỉnh_mapped', 'Time', '% LTC']], on=['AM_mapped', 'Tỉnh_mapped', 'Time'], how='left')
df_m = pd.merge(df_m, ltc_tts_grouped[['AM_mapped', 'Tỉnh_mapped', 'Time', '% LTC TTS']], on=['AM_mapped', 'Tỉnh_mapped', 'Time'], how='left')
# Ghép ODR All & TTS
df_m = pd.merge(df_m, odr_grouped[['Tỉnh_mapped', 'Time', '% ODR']], on=['Tỉnh_mapped', 'Time'], how='left')
df_m = pd.merge(df_m, odr_tts_grouped[['Tỉnh_mapped', 'Time', '% ODR TTS']], on=['Tỉnh_mapped', 'Time'], how='left')

df_m = df_m.rename(columns={
    'AM_mapped': 'AM',
    'Tỉnh_mapped': 'Tỉnh',
    'Time': 'Tuần',
    'vol_gtc': 'Sản lượng giao',
    'vol_gtc_tts': 'Sản lượng giao TTS',
    '% GTC': 'Tỉ lệ GTC',
    '% GTC TTS': 'Tỉ lệ GTC TTS',
    '% LTC': 'Tỉ lệ LTC',
    '% LTC TTS': 'Tỉ lệ LTC TTS',
    '% ODR': 'Tỉ lệ ODR',
    '% ODR TTS': 'Tỉ lệ ODR TTS'
}).sort_values(by=['AM', 'Tỉnh', 'Tuần']).reset_index(drop=True)

# 8. Tạo các bảng tóm tắt song song để vẽ biểu đồ
print("Đang chuẩn bị các bảng tóm tắt song song...")

# Bảng 1: AM Tuần 24 (All vs TTS)
df_am_w24 = df_m[df_m['Tuần'] == '2026/24'].groupby('AM').agg(
    sl=('Sản lượng giao', 'sum'),
    sl_tts=('Sản lượng giao TTS', 'sum'),
    gtc=('Tỉ lệ GTC', 'mean'),
    gtc_tts=('Tỉ lệ GTC TTS', 'mean')
).reset_index().sort_values(by='sl', ascending=False)
df_am_w24 = df_am_w24.rename(columns={
    'AM': 'AM W24', 
    'sl': 'Sản lượng W24', 
    'sl_tts': 'Sản lượng TTS W24', 
    'gtc': 'Tỉ lệ GTC W24', 
    'gtc_tts': 'Tỉ lệ GTC TTS W24'
})

# Bảng 2: Tỉnh Tuần 24 (All vs TTS)
df_prov_w24_gtc = df_gtc[df_gtc['Time'] == '2026/24']
prov_gtc = df_prov_w24_gtc.groupby('Tỉnh_mapped').agg(v=('Volume', 'sum'), vok=('Vol_GTC', 'sum')).reset_index()
prov_gtc['GTC'] = prov_gtc['vok'] / prov_gtc['v']

df_prov_w24_gtc_tts = df_gtc_tts_clean[df_gtc_tts_clean['Time'] == '2026/24']
prov_gtc_tts = df_prov_w24_gtc_tts.groupby('Tỉnh_mapped').agg(v=('Volume', 'sum'), vok=('Vol_GTC', 'sum')).reset_index()
prov_gtc_tts['GTC_TTS'] = prov_gtc_tts['vok'] / prov_gtc_tts['v']

df_prov_w24_ltc = df_ltc[df_ltc['Time'] == '2026/24']
prov_ltc = df_prov_w24_ltc.groupby('Tỉnh_mapped').agg(v=('Volume', 'sum'), vok=('Vol_LTC', 'sum')).reset_index()
prov_ltc['LTC'] = prov_ltc['vok'] / prov_ltc['v']

df_prov_w24_ltc_tts = df_ltc_tts_clean[df_ltc_tts_clean['Time'] == '2026/24']
prov_ltc_tts = df_prov_w24_ltc_tts.groupby('Tỉnh_mapped').agg(v=('Volume', 'sum'), vok=('Vol_LTC', 'sum')).reset_index()
prov_ltc_tts['LTC_TTS'] = prov_ltc_tts['vok'] / prov_ltc_tts['v']


df_prov_w24_odr = df_odr[df_odr['Time'] == '2026/24']
prov_odr = df_prov_w24_odr.groupby('Tỉnh_mapped').agg(v=('GTC', 'sum'), vok=('Vol_Ontime', 'sum')).reset_index()
prov_odr['ODR'] = prov_odr['vok'] / prov_odr['v']

df_prov_w24_odr_tts = df_odr_tts_clean[df_odr_tts_clean['Time'] == '2026/24']
prov_odr_tts = df_prov_w24_odr_tts.groupby('Tỉnh_mapped').agg(v=('GTC', 'sum'), vok=('Vol_Ontime', 'sum')).reset_index()
prov_odr_tts['ODR_TTS'] = prov_odr_tts['vok'] / prov_odr_tts['v']

df_prov_w24 = pd.DataFrame({'Tỉnh W24': ['Khánh Hòa', 'Lâm Đồng', 'Bình Thuận', 'Ninh Thuận', 'Đắk Nông']})

# 1. Merge GTC
df_prov_w24 = pd.merge(df_prov_w24, prov_gtc[['Tỉnh_mapped', 'v', 'GTC']], left_on='Tỉnh W24', right_on='Tỉnh_mapped', how='left')
df_prov_w24 = df_prov_w24.rename(columns={'v': 'Sản lượng W24', 'GTC': 'Tỉ lệ GTC W24'}).drop(columns=['Tỉnh_mapped'])

# 2. Merge GTC TTS
df_prov_w24 = pd.merge(df_prov_w24, prov_gtc_tts[['Tỉnh_mapped', 'v', 'GTC_TTS']], left_on='Tỉnh W24', right_on='Tỉnh_mapped', how='left')
df_prov_w24 = df_prov_w24.rename(columns={'v': 'Sản lượng TTS W24', 'GTC_TTS': 'Tỉ lệ GTC TTS W24'}).drop(columns=['Tỉnh_mapped'])

# 3. Merge LTC
df_prov_w24 = pd.merge(df_prov_w24, prov_ltc[['Tỉnh_mapped', 'LTC']], left_on='Tỉnh W24', right_on='Tỉnh_mapped', how='left')
df_prov_w24 = df_prov_w24.rename(columns={'LTC': 'Tỉ lệ LTC W24'}).drop(columns=['Tỉnh_mapped'])

# 4. Merge LTC TTS
df_prov_w24 = pd.merge(df_prov_w24, prov_ltc_tts[['Tỉnh_mapped', 'LTC_TTS']], left_on='Tỉnh W24', right_on='Tỉnh_mapped', how='left')
df_prov_w24 = df_prov_w24.rename(columns={'LTC_TTS': 'Tỉ lệ LTC TTS W24'}).drop(columns=['Tỉnh_mapped'])

# 5. Merge ODR
df_prov_w24 = pd.merge(df_prov_w24, prov_odr[['Tỉnh_mapped', 'ODR']], left_on='Tỉnh W24', right_on='Tỉnh_mapped', how='left')
df_prov_w24 = df_prov_w24.rename(columns={'ODR': 'Tỉ lệ ODR W24'}).drop(columns=['Tỉnh_mapped'])

# 6. Merge ODR TTS
df_prov_w24 = pd.merge(df_prov_w24, prov_odr_tts[['Tỉnh_mapped', 'ODR_TTS']], left_on='Tỉnh W24', right_on='Tỉnh_mapped', how='left')
df_prov_w24 = df_prov_w24.rename(columns={'ODR_TTS': 'Tỉ lệ ODR TTS W24'}).drop(columns=['Tỉnh_mapped'])

df_prov_w24 = df_prov_w24.fillna(0)

# Bảng 3: Cơ cấu sản lượng & Tỉ lệ GTC Ca 1 + Tồn (All vs TTS) hàng tuần
weekly_vols = []
for wk in weeks:
    # All cargo
    sub_tot = df_gtc_full[df_gtc_full['Time'] == wk]
    ca1 = sub_tot[sub_tot['Loại Hàng'] == 'Hàng Mới Ca 1']['Volume'].sum()
    ca2 = sub_tot[sub_tot['Loại Hàng'] == 'Hàng Mới Ca 2']['Volume'].sum()
    ton = sub_tot[sub_tot['Loại Hàng'] == 'Hàng Tồn']['Volume'].sum()
    
    # GTC Ca 1 + Tồn cho All
    sub_gtc_ton_all = sub_tot[sub_tot['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Tồn']) & (sub_tot['Chi tiết'] != 'Grand Total')]
    gtc_ton_all_rate = (sub_gtc_ton_all['Volume'] * sub_gtc_ton_all['% GTC']).sum() / sub_gtc_ton_all['Volume'].sum() if not sub_gtc_ton_all.empty else 0
    
    # TTS cargo
    sub_tts = df_gtc_tts[df_gtc_tts['Time'] == wk]
    ca1_tts = sub_tts[sub_tts['Loại Hàng'] == 'Hàng Mới Ca 1']['Volume'].sum()
    ca2_tts = sub_tts[sub_tts['Loại Hàng'] == 'Hàng Mới Ca 2']['Volume'].sum()
    ton_tts = sub_tts[sub_tts['Loại Hàng'] == 'Hàng Tồn']['Volume'].sum()
    
    # GTC Ca 1 + Tồn cho TTS
    sub_gtc_ton_tts = sub_tts[sub_tts['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Tồn']) & (sub_tts['Chi tiết'] != 'Grand Total')]
    gtc_ton_tts_rate = (sub_gtc_ton_tts['Volume'] * sub_gtc_ton_tts['% GTC']).sum() / sub_gtc_ton_tts['Volume'].sum() if not sub_gtc_ton_tts.empty else 0
    
    weekly_vols.append({
        'Tuần': 'W' + wk.split('/')[-1],
        'Ca 1': ca1,
        'Ca 1 TTS': ca1_tts,
        'Ca 2': ca2,
        'Ca 2 TTS': ca2_tts,
        'Hàng Tồn': ton,
        'Hàng Tồn TTS': ton_tts,
        'GTC Ca 1+Tồn': gtc_ton_all_rate,
        'GTC Ca 1+Tồn TTS': gtc_ton_tts_rate
    })
df_struct = pd.DataFrame(weekly_vols)

# 9. Ghi dữ liệu trực tiếp lên worksheet 'Phân tích AM-Tỉnh'
print("Đang ghi dữ liệu và định dạng worksheet 'Phân tích AM-Tỉnh'...")
try:
    ws_gsheet = sh.worksheet('Phân tích AM-Tỉnh')
    ws_id = ws_gsheet.id
except gspread.exceptions.WorksheetNotFound:
    ws_gsheet = sh.add_worksheet(title='Phân tích AM-Tỉnh', rows="200", cols="45")
    ws_id = ws_gsheet.id

ws_gsheet.clear()
ws_gsheet.resize(rows=200, cols=45)

# Xây dựng ma trận dữ liệu
num_rows = max(len(df_m) + 5, len(df_am_w24) + 5, len(df_prov_w24) + 5, len(df_struct) + 5, 200)
num_cols = 38  # Cột A đến AL

matrix = [["" for _ in range(num_cols)] for _ in range(num_rows)]

# 1. Detailed Table (A-K, cột index 0-10)
matrix[0][0:11] = ['AM', 'Tỉnh', 'Tuần', 'Sản lượng giao', 'Sản lượng giao TTS', 'Tỉ lệ GTC', 'Tỉ lệ GTC TTS', 'Tỉ lệ LTC', 'Tỉ lệ LTC TTS', 'Tỉ lệ ODR', 'Tỉ lệ ODR TTS']
for idx, r in df_m.iterrows():
    matrix[idx + 1][0:11] = [
        r['AM'], r['Tỉnh'], r['Tuần'],
        None if pd.isna(r['Sản lượng giao']) else int(r['Sản lượng giao']),
        None if pd.isna(r['Sản lượng giao TTS']) else int(r['Sản lượng giao TTS']),
        None if pd.isna(r['Tỉ lệ GTC']) else float(r['Tỉ lệ GTC']),
        None if pd.isna(r['Tỉ lệ GTC TTS']) else float(r['Tỉ lệ GTC TTS']),
        None if pd.isna(r['Tỉ lệ LTC']) else float(r['Tỉ lệ LTC']),
        None if pd.isna(r['Tỉ lệ LTC TTS']) else float(r['Tỉ lệ LTC TTS']),
        None if pd.isna(r['Tỉ lệ ODR']) else float(r['Tỉ lệ ODR']),
        None if pd.isna(r['Tỉ lệ ODR TTS']) else float(r['Tỉ lệ ODR TTS'])
    ]

# 2. Summary 1 (M-Q, cột index 12-16)
matrix[0][12:17] = ["AM W24", "Sản lượng W24", "Sản lượng TTS W24", "Tỉ lệ GTC W24", "Tỉ lệ GTC TTS W24"]
for idx, r in df_am_w24.iterrows():
    matrix[idx + 1][12:17] = [
        r['AM W24'],
        None if pd.isna(r['Sản lượng W24']) else int(r['Sản lượng W24']),
        None if pd.isna(r['Sản lượng TTS W24']) else int(r['Sản lượng TTS W24']),
        None if pd.isna(r['Tỉ lệ GTC W24']) else float(r['Tỉ lệ GTC W24']),
        None if pd.isna(r['Tỉ lệ GTC TTS W24']) else float(r['Tỉ lệ GTC TTS W24'])
    ]

# 3. Summary 2 (S-AA, cột index 18-26)
matrix[0][18:27] = ["Tỉnh W24", "Sản lượng W24", "Sản lượng TTS W24", "Tỉ lệ GTC W24", "Tỉ lệ GTC TTS W24", "Tỉ lệ LTC W24", "Tỉ lệ LTC TTS W24", "Tỉ lệ ODR W24", "Tỉ lệ ODR TTS W24"]
for idx, r in df_prov_w24.iterrows():
    matrix[idx + 1][18:27] = [
        r['Tỉnh W24'],
        None if pd.isna(r['Sản lượng W24']) else int(r['Sản lượng W24']),
        None if pd.isna(r['Sản lượng TTS W24']) else int(r['Sản lượng TTS W24']),
        None if pd.isna(r['Tỉ lệ GTC W24']) else float(r['Tỉ lệ GTC W24']),
        None if pd.isna(r['Tỉ lệ GTC TTS W24']) else float(r['Tỉ lệ GTC TTS W24']),
        None if pd.isna(r['Tỉ lệ LTC W24']) else float(r['Tỉ lệ LTC W24']),
        None if pd.isna(r['Tỉ lệ LTC TTS W24']) else float(r['Tỉ lệ LTC TTS W24']),
        None if pd.isna(r['Tỉ lệ ODR W24']) else float(r['Tỉ lệ ODR W24']),
        None if pd.isna(r['Tỉ lệ ODR TTS W24']) else float(r['Tỉ lệ ODR TTS W24'])
    ]

# 4. Summary 3 (AC-AK, cột index 28-36)
matrix[0][28:37] = ["Tuần", "Ca 1", "Ca 1 TTS", "Ca 2", "Ca 2 TTS", "Hàng Tồn", "Hàng Tồn TTS", "GTC Ca 1+Tồn", "GTC Ca 1+Tồn TTS"]
for idx, r in df_struct.iterrows():
    matrix[idx + 1][28:37] = [
        r['Tuần'],
        None if pd.isna(r['Ca 1']) else int(r['Ca 1']),
        None if pd.isna(r['Ca 1 TTS']) else int(r['Ca 1 TTS']),
        None if pd.isna(r['Ca 2']) else int(r['Ca 2']),
        None if pd.isna(r['Ca 2 TTS']) else int(r['Ca 2 TTS']),
        None if pd.isna(r['Hàng Tồn']) else int(r['Hàng Tồn']),
        None if pd.isna(r['Hàng Tồn TTS']) else int(r['Hàng Tồn TTS']),
        None if pd.isna(r['GTC Ca 1+Tồn']) else float(r['GTC Ca 1+Tồn']),
        None if pd.isna(r['GTC Ca 1+Tồn TTS']) else float(r['GTC Ca 1+Tồn TTS'])
    ]

# Upload ma trận dữ liệu lên Google Sheets
ws_gsheet.update(range_name='A1', values=matrix, value_input_option='USER_ENTERED')
print("✔️ Đã đồng bộ dữ liệu song song (All & TTS) lên Google Sheets.")

# 10. Định dạng giao diện (Premium Style)
print("Đang áp dụng định dạng giao diện cao cấp...")
try:
    # Định dạng tiêu đề cho từng bảng
    for col_range in ["A1:K1", "M1:Q1", "S1:AA1", "AC1:AK1"]:
        ws_gsheet.format(col_range, {
            "backgroundColor": {"red": 30/255, "green": 41/255, "blue": 59/255},
            "horizontalAlignment": "CENTER",
            "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontFamily": "Segoe UI", "fontSize": 11}
        })
        
    # Font chữ chung
    ws_gsheet.format(f"A2:AK{num_rows}", {
        "textFormat": {"fontFamily": "Segoe UI", "fontSize": 10}
    })
    
    # Căn lề trái
    for rng in [f"A2:B{num_rows}", f"M2:M{num_rows}", f"S2:S{num_rows}"]:
        ws_gsheet.format(rng, {"horizontalAlignment": "LEFT"})
    # Căn lề giữa
    for rng in [f"C2:C{num_rows}", f"AC2:AC{num_rows}"]:
        ws_gsheet.format(rng, {"horizontalAlignment": "CENTER"})
    # Căn lề phải
    for rng in [f"D2:K{num_rows}", f"N2:Q{num_rows}", f"T2:AA{num_rows}", f"AD2:AK{num_rows}"]:
        ws_gsheet.format(rng, {"horizontalAlignment": "RIGHT"})

    # Định dạng hiển thị hiển thị Số nguyên và tỷ lệ phần trăm %
    # Detailed Table
    ws_gsheet.format(f"D2:E{num_rows}", {"numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
    ws_gsheet.format(f"F2:K{num_rows}", {"numberFormat": {"type": "PERCENT", "pattern": "0.00%"}})
    # Summary 1
    ws_gsheet.format(f"N2:O{num_rows}", {"numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
    ws_gsheet.format(f"P2:Q{num_rows}", {"numberFormat": {"type": "PERCENT", "pattern": "0.00%"}})
    # Summary 2
    ws_gsheet.format(f"T2:U{num_rows}", {"numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
    ws_gsheet.format(f"V2:AA{num_rows}", {"numberFormat": {"type": "PERCENT", "pattern": "0.00%"}})
    # Summary 3
    ws_gsheet.format(f"AD2:AI{num_rows}", {"numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
    ws_gsheet.format(f"AJ2:AK{num_rows}", {"numberFormat": {"type": "PERCENT", "pattern": "0.00%"}})

    # Hiện đường lưới mặc định của Google Sheet
    sh.batch_update({
        "requests": [
            {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": ws_id,
                        "gridProperties": {
                            "hideGridlines": False
                        }
                    },
                    "fields": "gridProperties.hideGridlines"
                }
            }
        ]
    })
    print("✔️ Đã định dạng và bật lưới thành công.")
except Exception as fe:
    print(f"⚠️ Cảnh báo định dạng giao diện: {fe}")

# 11. Xoá các biểu đồ cũ (nếu có) tránh bị chồng lấp
print("Đang kiểm tra và xoá biểu đồ cũ trên sheet...")
try:
    sheet_metadata = sh.fetch_sheet_metadata()
    charts_to_delete = []
    for sheet in sheet_metadata.get('sheets', []):
        if sheet.get('properties', {}).get('sheetId') == ws_id:
            for chart in sheet.get('charts', []):
                charts_to_delete.append({
                    "deleteEmbeddedObject": {
                        "objectId": chart.get('chartId')
                    }
                })
    if charts_to_delete:
        sh.batch_update({"requests": charts_to_delete})
        print(f"✔️ Đã dọn dẹp {len(charts_to_delete)} biểu đồ cũ.")
except Exception as e:
    print(f"⚠️ Cảnh báo dọn dẹp biểu đồ: {e}")

# 12. Thêm 3 biểu đồ trực tuyến tương tác cao (Mô hình song song All vs TTS)
print("Đang chèn 3 biểu đồ động song song trực tiếp lên Google Sheets...")

# Biểu đồ 1: BAR chart so sánh sản lượng giao All vs TTS của các AM ở Tuần 24
chart1 = {
    "addChart": {
        "chart": {
            "spec": {
                "title": "SẢN LƯỢNG GIAO TỔNG vs TTS CỦA AM - TUẦN 24",
                "basicChart": {
                    "chartType": "BAR",
                    "legendPosition": "BOTTOM_LEGEND",
                    "headerCount": 1,
                    "axis": [
                        {"position": "BOTTOM_AXIS", "title": "Sản lượng giao (Đơn)"},
                        {"position": "LEFT_AXIS", "title": "AM"}
                    ],
                    "domains": [
                        {"domain": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 0, "endRowIndex": 21, "startColumnIndex": 12, "endColumnIndex": 13}]}}}
                    ],
                    "series": [
                        {"series": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 0, "endRowIndex": 21, "startColumnIndex": 13, "endColumnIndex": 14}]}}, "targetAxis": "BOTTOM_AXIS"},
                        {"series": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 0, "endRowIndex": 21, "startColumnIndex": 14, "endColumnIndex": 15}]}}, "targetAxis": "BOTTOM_AXIS"}
                    ]
                }
            },
            "position": {
                "overlayPosition": {
                    "anchorCell": {"sheetId": ws_id, "rowIndex": 1, "columnIndex": 39}, # Cột AM (chỉ số 39)
                    "offsetXPixels": 0, "offsetYPixels": 0
                }
            }
        }
    }
}

# Biểu đồ 2: COMBO chart so sánh sản lượng & tỉ lệ GTC (All vs TTS) theo tỉnh ở Tuần 24
chart2 = {
    "addChart": {
        "chart": {
            "spec": {
                "title": "HIỆU SUẤT VẬN HÀNH THEO TỈNH (ALL vs TTS) - TUẦN 24",
                "basicChart": {
                    "chartType": "COMBO",
                    "legendPosition": "BOTTOM_LEGEND",
                    "headerCount": 1,
                    "axis": [
                        {"position": "BOTTOM_AXIS", "title": "Tỉnh thành"},
                        {"position": "LEFT_AXIS", "title": "Sản lượng"},
                        {"position": "RIGHT_AXIS", "title": "Tỉ lệ GTC (%)"}
                    ],
                    "domains": [
                        {"domain": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 0, "endRowIndex": 6, "startColumnIndex": 18, "endColumnIndex": 19}]}}}
                    ],
                    "series": [
                        {"series": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 0, "endRowIndex": 6, "startColumnIndex": 19, "endColumnIndex": 20}]}}, "targetAxis": "LEFT_AXIS", "type": "COLUMN"},
                        {"series": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 0, "endRowIndex": 6, "startColumnIndex": 20, "endColumnIndex": 21}]}}, "targetAxis": "LEFT_AXIS", "type": "COLUMN"},
                        {"series": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 0, "endRowIndex": 6, "startColumnIndex": 21, "endColumnIndex": 22}]}}, "targetAxis": "RIGHT_AXIS", "type": "LINE"},
                        {"series": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 0, "endRowIndex": 6, "startColumnIndex": 22, "endColumnIndex": 23}]}}, "targetAxis": "RIGHT_AXIS", "type": "LINE"}
                    ]
                }
            },
            "position": {
                "overlayPosition": {
                    "anchorCell": {"sheetId": ws_id, "rowIndex": 22, "columnIndex": 39},
                    "offsetXPixels": 0, "offsetYPixels": 0
                }
            }
        }
    }
}

# Biểu đồ 3: LINE chart xu hướng tỉ lệ GTC Ca 1 + Tồn (All vs TTS) hàng tuần
chart3 = {
    "addChart": {
        "chart": {
            "spec": {
                "title": "XU HƯỚNG TỈ LỆ GTC CA 1 + TỒN (ALL vs TTS)",
                "basicChart": {
                    "chartType": "LINE",
                    "legendPosition": "BOTTOM_LEGEND",
                    "headerCount": 1,
                    "axis": [
                        {"position": "BOTTOM_AXIS", "title": "Tuần"},
                        {"position": "LEFT_AXIS", "title": "Tỉ lệ GTC (%)"}
                    ],
                    "domains": [
                        {"domain": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 0, "endRowIndex": 5, "startColumnIndex": 28, "endColumnIndex": 29}]}}}
                    ],
                    "series": [
                        {"series": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 0, "endRowIndex": 5, "startColumnIndex": 35, "endColumnIndex": 36}]}}, "targetAxis": "LEFT_AXIS"},
                        {"series": {"sourceRange": {"sources": [{"sheetId": ws_id, "startRowIndex": 0, "endRowIndex": 5, "startColumnIndex": 36, "endColumnIndex": 37}]}}, "targetAxis": "LEFT_AXIS"}
                    ]
                }
            },
            "position": {
                "overlayPosition": {
                    "anchorCell": {"sheetId": ws_id, "rowIndex": 43, "columnIndex": 39},
                    "offsetXPixels": 0, "offsetYPixels": 0
                }
            }
        }
    }
}

try:
    sh.batch_update({"requests": [chart1, chart2, chart3]})
    print("✔️ Đã vẽ thành công 3 biểu đồ song song trực quan động lên Google Sheet.")
except Exception as e:
    print(f"❌ Lỗi vẽ biểu đồ trên Google Sheets: {e}")

# =========================================================================
# PHẦN 2: BỔ SUNG TAB MỚI: PHÂN TÍCH SO SÁNH W24 VS W23 & TỈ TRỌNG AM
# =========================================================================
print("\n" + "="*60)
print("BẮT ĐẦU PHÂN TÍCH SO SÁNH TUẦN 24 VS TUẦN 23 & TỈ TRỌNG CỦA AM")
print("="*60)

# Nhóm dữ liệu thô GTC theo AM và Tuần (All & TTS)
am_gtc_all = df_gtc.groupby(['AM_mapped', 'Time']).agg(v=('Volume', 'sum'), vok=('Vol_GTC', 'sum')).reset_index()
am_gtc_all['GTC'] = am_gtc_all['vok'] / am_gtc_all['v']

am_gtc_tts = df_gtc_tts_clean.groupby(['AM_mapped', 'Time']).agg(v=('Volume', 'sum'), vok=('Vol_GTC', 'sum')).reset_index()
am_gtc_tts['GTC_TTS'] = am_gtc_tts['vok'] / am_gtc_tts['v']

# Nhóm dữ liệu thô LTC theo AM và Tuần (All & TTS)
am_ltc_all = df_ltc.groupby(['AM_mapped', 'Time']).agg(v=('Volume', 'sum'), vok=('Vol_LTC', 'sum')).reset_index()
am_ltc_all['LTC'] = am_ltc_all['vok'] / am_ltc_all['v']

am_ltc_tts = df_ltc_tts_clean.groupby(['AM_mapped', 'Time']).agg(v=('Volume', 'sum'), vok=('Vol_LTC', 'sum')).reset_index()
am_ltc_tts['LTC_TTS'] = am_ltc_tts['vok'] / am_ltc_tts['v']

# Nhóm dữ liệu thô ODR theo AM và Tuần (All & TTS)
df_odr_clean = df_odr.copy()
df_odr_clean['AM_mapped'] = df_odr_clean['Chi tiết'].apply(map_am)
am_odr_all = df_odr_clean.groupby(['AM_mapped', 'Time']).agg(v=('GTC', 'sum'), vok=('Vol_Ontime', 'sum')).reset_index()
am_odr_all['ODR'] = am_odr_all['vok'] / am_odr_all['v']

df_odr_tts_clean_am = df_odr_tts_clean.copy()
df_odr_tts_clean_am['AM_mapped'] = df_odr_tts_clean_am['Chi tiết'].apply(map_am)
am_odr_tts = df_odr_tts_clean_am.groupby(['AM_mapped', 'Time']).agg(v=('GTC', 'sum'), vok=('Vol_Ontime', 'sum')).reset_index()
am_odr_tts['ODR_TTS'] = am_odr_tts['vok'] / am_odr_tts['v']

# Tạo DataFrame so sánh
am_names = df_pairs['Am'].dropna().unique()
df_am_comp = pd.DataFrame({'AM': am_names})

# Ghép dữ liệu thô tuần 23 và 24 cho GTC
w23_all = am_gtc_all[am_gtc_all['Time'] == '2026/23']
df_am_comp = pd.merge(df_am_comp, w23_all[['AM_mapped', 'v', 'GTC']], left_on='AM', right_on='AM_mapped', how='left').rename(columns={'v': 'Sản lượng W23', 'GTC': 'Tỉ lệ GTC W23'}).drop(columns=['AM_mapped'])

w24_all = am_gtc_all[am_gtc_all['Time'] == '2026/24']
df_am_comp = pd.merge(df_am_comp, w24_all[['AM_mapped', 'v', 'GTC']], left_on='AM', right_on='AM_mapped', how='left').rename(columns={'v': 'Sản lượng W24', 'GTC': 'Tỉ lệ GTC W24'}).drop(columns=['AM_mapped'])

w23_tts = am_gtc_tts[am_gtc_tts['Time'] == '2026/23']
df_am_comp = pd.merge(df_am_comp, w23_tts[['AM_mapped', 'v', 'GTC_TTS']], left_on='AM', right_on='AM_mapped', how='left').rename(columns={'v': 'Sản lượng TTS W23', 'GTC_TTS': 'Tỉ lệ GTC TTS W23'}).drop(columns=['AM_mapped'])

w24_tts = am_gtc_tts[am_gtc_tts['Time'] == '2026/24']
df_am_comp = pd.merge(df_am_comp, w24_tts[['AM_mapped', 'v', 'GTC_TTS']], left_on='AM', right_on='AM_mapped', how='left').rename(columns={'v': 'Sản lượng TTS W24', 'GTC_TTS': 'Tỉ lệ GTC TTS W24'}).drop(columns=['AM_mapped'])

# Ghép dữ liệu thô tuần 23 và 24 cho LTC
w23_ltc_all = am_ltc_all[am_ltc_all['Time'] == '2026/23']
df_am_comp = pd.merge(df_am_comp, w23_ltc_all[['AM_mapped', 'LTC']], left_on='AM', right_on='AM_mapped', how='left').rename(columns={'LTC': 'Tỉ lệ LTC W23'}).drop(columns=['AM_mapped'])

w24_ltc_all = am_ltc_all[am_ltc_all['Time'] == '2026/24']
df_am_comp = pd.merge(df_am_comp, w24_ltc_all[['AM_mapped', 'LTC']], left_on='AM', right_on='AM_mapped', how='left').rename(columns={'LTC': 'Tỉ lệ LTC W24'}).drop(columns=['AM_mapped'])

w23_ltc_tts = am_ltc_tts[am_ltc_tts['Time'] == '2026/23']
df_am_comp = pd.merge(df_am_comp, w23_ltc_tts[['AM_mapped', 'LTC_TTS']], left_on='AM', right_on='AM_mapped', how='left').rename(columns={'LTC_TTS': 'Tỉ lệ LTC TTS W23'}).drop(columns=['AM_mapped'])

w24_ltc_tts = am_ltc_tts[am_ltc_tts['Time'] == '2026/24']
df_am_comp = pd.merge(df_am_comp, w24_ltc_tts[['AM_mapped', 'LTC_TTS']], left_on='AM', right_on='AM_mapped', how='left').rename(columns={'LTC_TTS': 'Tỉ lệ LTC TTS W24'}).drop(columns=['AM_mapped'])

# Ghép dữ liệu thô tuần 23 và 24 cho ODR
w23_odr_all = am_odr_all[am_odr_all['Time'] == '2026/23']
df_am_comp = pd.merge(df_am_comp, w23_odr_all[['AM_mapped', 'ODR']], left_on='AM', right_on='AM_mapped', how='left').rename(columns={'ODR': 'Tỉ lệ ODR W23'}).drop(columns=['AM_mapped'])

w24_odr_all = am_odr_all[am_odr_all['Time'] == '2026/24']
df_am_comp = pd.merge(df_am_comp, w24_odr_all[['AM_mapped', 'ODR']], left_on='AM', right_on='AM_mapped', how='left').rename(columns={'ODR': 'Tỉ lệ ODR W24'}).drop(columns=['AM_mapped'])

w23_odr_tts = am_odr_tts[am_odr_tts['Time'] == '2026/23']
df_am_comp = pd.merge(df_am_comp, w23_odr_tts[['AM_mapped', 'ODR_TTS']], left_on='AM', right_on='AM_mapped', how='left').rename(columns={'ODR_TTS': 'Tỉ lệ ODR TTS W23'}).drop(columns=['AM_mapped'])

w24_odr_tts = am_odr_tts[am_odr_tts['Time'] == '2026/24']
df_am_comp = pd.merge(df_am_comp, w24_odr_tts[['AM_mapped', 'ODR_TTS']], left_on='AM', right_on='AM_mapped', how='left').rename(columns={'ODR_TTS': 'Tỉ lệ ODR TTS W24'}).drop(columns=['AM_mapped'])

# Tính chênh lệch
df_am_comp['Thay đổi Sản lượng'] = df_am_comp['Sản lượng W24'] - df_am_comp['Sản lượng W23']
df_am_comp['% Thay đổi Sản lượng'] = df_am_comp['Thay đổi Sản lượng'] / df_am_comp['Sản lượng W23']
df_am_comp['Thay đổi GTC'] = df_am_comp['Tỉ lệ GTC W24'] - df_am_comp['Tỉ lệ GTC W23']
df_am_comp['Thay đổi GTC TTS'] = df_am_comp['Tỉ lệ GTC TTS W24'] - df_am_comp['Tỉ lệ GTC TTS W23']
df_am_comp['Thay đổi LTC'] = df_am_comp['Tỉ lệ LTC W24'] - df_am_comp['Tỉ lệ LTC W23']
df_am_comp['Thay đổi LTC TTS'] = df_am_comp['Tỉ lệ LTC TTS W24'] - df_am_comp['Tỉ lệ LTC TTS W23']
df_am_comp['Thay đổi ODR'] = df_am_comp['Tỉ lệ ODR W24'] - df_am_comp['Tỉ lệ ODR W23']
df_am_comp['Thay đổi ODR TTS'] = df_am_comp['Tỉ lệ ODR TTS W24'] - df_am_comp['Tỉ lệ ODR TTS W23']

df_am_comp = df_am_comp.fillna(0).sort_values(by='Sản lượng W24', ascending=False).reset_index(drop=True)

# Tạo DataFrame tỉ trọng của AM trong Tuần 24
df_am_share = pd.DataFrame({'AM': am_names})
df_am_share = pd.merge(df_am_share, w24_all[['AM_mapped', 'v']], left_on='AM', right_on='AM_mapped', how='left').rename(columns={'v': 'Sản lượng W24'}).drop(columns=['AM_mapped'])
df_am_share = pd.merge(df_am_share, w24_tts[['AM_mapped', 'v']], left_on='AM', right_on='AM_mapped', how='left').rename(columns={'v': 'Sản lượng TTS W24'}).drop(columns=['AM_mapped'])
df_am_share = df_am_share.fillna(0)

total_sl_w24 = df_am_share['Sản lượng W24'].sum()
total_sl_tts_w24 = df_am_share['Sản lượng TTS W24'].sum()

df_am_share['Tỉ trọng'] = df_am_share['Sản lượng W24'] / total_sl_w24 if total_sl_w24 > 0 else 0
df_am_share['Tỉ trọng TTS'] = df_am_share['Sản lượng TTS W24'] / total_sl_tts_w24 if total_sl_tts_w24 > 0 else 0
df_am_share = df_am_share.sort_values(by='Sản lượng W24', ascending=False).reset_index(drop=True)

# Cấu hình sheet mới
print("Đang cấu hình sheet 'Phân tích AM W24 vs W23'...")
try:
    ws_comp = sh.worksheet('Phân tích AM W24 vs W23')
    comp_ws_id = ws_comp.id
except gspread.exceptions.WorksheetNotFound:
    ws_comp = sh.add_worksheet(title='Phân tích AM W24 vs W23', rows="100", cols="45")
    comp_ws_id = ws_comp.id

ws_comp.clear()
ws_comp.resize(rows=100, cols=45)

comp_rows = 100
comp_cols = 45
comp_matrix = [["" for _ in range(comp_cols)] for _ in range(comp_rows)]

# Table 1 (A-W): So sánh W24 vs W23 đầy đủ GTC, LTC, ODR (All & TTS)
comp_matrix[0][0:23] = [
    'AM', 'Sản lượng W23', 'Sản lượng W24', 'Thay đổi Sản lượng', '% Thay đổi Sản lượng',
    'Tỉ lệ GTC W23', 'Tỉ lệ GTC W24', 'Thay đổi GTC',
    'Tỉ lệ GTC TTS W23', 'Tỉ lệ GTC TTS W24', 'Thay đổi GTC TTS',
    'Tỉ lệ LTC W23', 'Tỉ lệ LTC W24', 'Thay đổi LTC',
    'Tỉ lệ LTC TTS W23', 'Tỉ lệ LTC TTS W24', 'Thay đổi LTC TTS',
    'Tỉ lệ ODR W23', 'Tỉ lệ ODR W24', 'Thay đổi ODR',
    'Tỉ lệ ODR TTS W23', 'Tỉ lệ ODR TTS W24', 'Thay đổi ODR TTS'
]
for idx, r in df_am_comp.iterrows():
    comp_matrix[idx + 1][0:23] = [
        r['AM'],
        None if pd.isna(r['Sản lượng W23']) else int(r['Sản lượng W23']),
        None if pd.isna(r['Sản lượng W24']) else int(r['Sản lượng W24']),
        None if pd.isna(r['Thay đổi Sản lượng']) else int(r['Thay đổi Sản lượng']),
        None if pd.isna(r['% Thay đổi Sản lượng']) else float(r['% Thay đổi Sản lượng']),
        None if pd.isna(r['Tỉ lệ GTC W23']) else float(r['Tỉ lệ GTC W23']),
        None if pd.isna(r['Tỉ lệ GTC W24']) else float(r['Tỉ lệ GTC W24']),
        None if pd.isna(r['Thay đổi GTC']) else float(r['Thay đổi GTC']),
        None if pd.isna(r['Tỉ lệ GTC TTS W23']) else float(r['Tỉ lệ GTC TTS W23']),
        None if pd.isna(r['Tỉ lệ GTC TTS W24']) else float(r['Tỉ lệ GTC TTS W24']),
        None if pd.isna(r['Thay đổi GTC TTS']) else float(r['Thay đổi GTC TTS']),
        None if pd.isna(r['Tỉ lệ LTC W23']) else float(r['Tỉ lệ LTC W23']),
        None if pd.isna(r['Tỉ lệ LTC W24']) else float(r['Tỉ lệ LTC W24']),
        None if pd.isna(r['Thay đổi LTC']) else float(r['Thay đổi LTC']),
        None if pd.isna(r['Tỉ lệ LTC TTS W23']) else float(r['Tỉ lệ LTC TTS W23']),
        None if pd.isna(r['Tỉ lệ LTC TTS W24']) else float(r['Tỉ lệ LTC TTS W24']),
        None if pd.isna(r['Thay đổi LTC TTS']) else float(r['Thay đổi LTC TTS']),
        None if pd.isna(r['Tỉ lệ ODR W23']) else float(r['Tỉ lệ ODR W23']),
        None if pd.isna(r['Tỉ lệ ODR W24']) else float(r['Tỉ lệ ODR W24']),
        None if pd.isna(r['Thay đổi ODR']) else float(r['Thay đổi ODR']),
        None if pd.isna(r['Tỉ lệ ODR TTS W23']) else float(r['Tỉ lệ ODR TTS W23']),
        None if pd.isna(r['Tỉ lệ ODR TTS W24']) else float(r['Tỉ lệ ODR TTS W24']),
        None if pd.isna(r['Thay đổi ODR TTS']) else float(r['Thay đổi ODR TTS'])
    ]

# Table 2 (Y-AC): Tỉ trọng AM
comp_matrix[0][24:29] = ['AM', 'Sản lượng W24', 'Tỉ trọng sản lượng', 'Sản lượng TTS W24', 'Tỉ trọng TTS']
for idx, r in df_am_share.iterrows():
    comp_matrix[idx + 1][24:29] = [
        r['AM'],
        None if pd.isna(r['Sản lượng W24']) else int(r['Sản lượng W24']),
        None if pd.isna(r['Tỉ trọng']) else float(r['Tỉ trọng']),
        None if pd.isna(r['Sản lượng TTS W24']) else int(r['Sản lượng TTS W24']),
        None if pd.isna(r['Tỉ trọng TTS']) else float(r['Tỉ trọng TTS'])
    ]

ws_comp.update(range_name='A1', values=comp_matrix, value_input_option='USER_ENTERED')
print("✔️ Đã ghi dữ liệu so sánh và tỉ trọng thành công.")

# Định dạng bảng so sánh
try:
    for col_range in ["A1:W1", "Y1:AC1"]:
        ws_comp.format(col_range, {
            "backgroundColor": {"red": 30/255, "green": 41/255, "blue": 59/255},
            "horizontalAlignment": "CENTER",
            "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontFamily": "Segoe UI", "fontSize": 11}
        })
        
    ws_comp.format(f"A2:AC{comp_rows}", {"textFormat": {"fontFamily": "Segoe UI", "fontSize": 10}})
    
    for rng in [f"A2:A{comp_rows}", f"Y2:Y{comp_rows}"]:
        ws_comp.format(rng, {"horizontalAlignment": "LEFT"})
    for rng in [f"B2:W{comp_rows}", f"Z2:AC{comp_rows}"]:
        ws_comp.format(rng, {"horizontalAlignment": "RIGHT"})

    # Định dạng số & %
    for rng in [f"B2:D{comp_rows}", f"Z2:Z{comp_rows}", f"AB2:AB{comp_rows}"]:
        ws_comp.format(rng, {"numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
    for rng in [f"E2:W{comp_rows}", f"AA2:AA{comp_rows}", f"AC2:AC{comp_rows}"]:
        ws_comp.format(rng, {"numberFormat": {"type": "PERCENT", "pattern": "0.00%"}})

    # Hiện đường lưới
    sh.batch_update({
        "requests": [
            {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": comp_ws_id,
                        "gridProperties": {
                            "hideGridlines": False
                        }
                    },
                    "fields": "gridProperties.hideGridlines"
                }
            }
        ]
    })
    print("✔️ Đã định dạng giao diện tab so sánh thành công.")
except Exception as fe:
    print(f"⚠️ Cảnh báo định dạng giao diện tab so sánh: {fe}")

# Xoá biểu đồ cũ của tab so sánh
print("Đang xoá biểu đồ cũ trên tab so sánh...")
try:
    sheet_metadata = sh.fetch_sheet_metadata()
    comp_charts_to_delete = []
    for sheet in sheet_metadata.get('sheets', []):
        if sheet.get('properties', {}).get('sheetId') == comp_ws_id:
            for chart in sheet.get('charts', []):
                comp_charts_to_delete.append({
                    "deleteEmbeddedObject": {
                        "objectId": chart.get('chartId')
                    }
                })
    if comp_charts_to_delete:
        sh.batch_update({"requests": comp_charts_to_delete})
        print(f"✔️ Đã dọn dẹp {len(comp_charts_to_delete)} biểu đồ cũ ở sheet so sánh.")
except Exception as e:
    print(f"⚠️ Cảnh báo dọn dẹp biểu đồ sheet so sánh: {e}")

# Vẽ 5 biểu đồ so sánh & tỉ trọng
print("Đang chèn 5 biểu đồ so sánh và tỉ trọng của AM lên Google Sheets...")

# 1. Biểu đồ tròn/donut tỉ trọng sản lượng AM W24 (Cột Y & Z)
donut_chart = {
    "addChart": {
        "chart": {
            "spec": {
                "title": "TỈ TRỌNG SẢN LƯỢNG AM - TUẦN 24",
                "pieChart": {
                    "legendPosition": "BOTTOM_LEGEND",
                    "domain": {"sourceRange": {"sources": [{"sheetId": comp_ws_id, "startRowIndex": 0, "endRowIndex": 21, "startColumnIndex": 24, "endColumnIndex": 25}]}},
                    "series": {"sourceRange": {"sources": [{"sheetId": comp_ws_id, "startRowIndex": 0, "endRowIndex": 21, "startColumnIndex": 25, "endColumnIndex": 26}]}},
                    "pieHole": 0.4
                }
            },
            "position": {
                "overlayPosition": {
                    "anchorCell": {"sheetId": comp_ws_id, "rowIndex": 1, "columnIndex": 30}, # Cột AE (30)
                    "offsetXPixels": 0, "offsetYPixels": 0
                }
            }
        }
    }
}

# 2. Biểu đồ cột so sánh sản lượng AM W24 vs W23 (Cột A & B, C)
comp_vol_chart = {
    "addChart": {
        "chart": {
            "spec": {
                "title": "SO SÁNH SẢN LƯỢNG AM - TUẦN 24 VS TUẦN 23",
                "basicChart": {
                    "chartType": "COLUMN",
                    "legendPosition": "BOTTOM_LEGEND",
                    "headerCount": 1,
                    "axis": [
                        {"position": "BOTTOM_AXIS", "title": "AM"},
                        {"position": "LEFT_AXIS", "title": "Sản lượng (Đơn)"}
                    ],
                    "domains": [
                        {"domain": {"sourceRange": {"sources": [{"sheetId": comp_ws_id, "startRowIndex": 0, "endRowIndex": 21, "startColumnIndex": 0, "endColumnIndex": 1}]}}}
                    ],
                    "series": [
                        {"series": {"sourceRange": {"sources": [{"sheetId": comp_ws_id, "startRowIndex": 0, "endRowIndex": 21, "startColumnIndex": 1, "endColumnIndex": 2}]}}, "targetAxis": "LEFT_AXIS"},
                        {"series": {"sourceRange": {"sources": [{"sheetId": comp_ws_id, "startRowIndex": 0, "endRowIndex": 21, "startColumnIndex": 2, "endColumnIndex": 3}]}}, "targetAxis": "LEFT_AXIS"}
                    ]
                }
            },
            "position": {
                "overlayPosition": {
                    "anchorCell": {"sheetId": comp_ws_id, "rowIndex": 22, "columnIndex": 30},
                    "offsetXPixels": 0, "offsetYPixels": 0
                }
            }
        }
    }
}

# 3. Biểu đồ cột so sánh tỉ lệ GTC AM W24 vs W23 (Cột A & F, G)
comp_gtc_chart = {
    "addChart": {
        "chart": {
            "spec": {
                "title": "SO SÁNH TỈ LỆ GTC CỦA AM - TUẦN 24 VS TUẦN 23",
                "basicChart": {
                    "chartType": "COLUMN",
                    "legendPosition": "BOTTOM_LEGEND",
                    "headerCount": 1,
                    "axis": [
                        {"position": "BOTTOM_AXIS", "title": "AM"},
                        {"position": "LEFT_AXIS", "title": "Tỉ lệ GTC (%)"}
                    ],
                    "domains": [
                        {"domain": {"sourceRange": {"sources": [{"sheetId": comp_ws_id, "startRowIndex": 0, "endRowIndex": 21, "startColumnIndex": 0, "endColumnIndex": 1}]}}}
                    ],
                    "series": [
                        {"series": {"sourceRange": {"sources": [{"sheetId": comp_ws_id, "startRowIndex": 0, "endRowIndex": 21, "startColumnIndex": 5, "endColumnIndex": 6}]}}, "targetAxis": "LEFT_AXIS"},
                        {"series": {"sourceRange": {"sources": [{"sheetId": comp_ws_id, "startRowIndex": 0, "endRowIndex": 21, "startColumnIndex": 6, "endColumnIndex": 7}]}}, "targetAxis": "LEFT_AXIS"}
                    ]
                }
            },
            "position": {
                "overlayPosition": {
                    "anchorCell": {"sheetId": comp_ws_id, "rowIndex": 43, "columnIndex": 30},
                    "offsetXPixels": 0, "offsetYPixels": 0
                }
            }
        }
    }
}

# 4. Biểu đồ cột so sánh tỉ lệ LTC AM W24 vs W23 (Cột A & L, M)
comp_ltc_chart = {
    "addChart": {
        "chart": {
            "spec": {
                "title": "SO SÁNH TỈ LỆ LTC CỦA AM - TUẦN 24 VS TUẦN 23",
                "basicChart": {
                    "chartType": "COLUMN",
                    "legendPosition": "BOTTOM_LEGEND",
                    "headerCount": 1,
                    "axis": [
                        {"position": "BOTTOM_AXIS", "title": "AM"},
                        {"position": "LEFT_AXIS", "title": "Tỉ lệ LTC (%)"}
                    ],
                    "domains": [
                        {"domain": {"sourceRange": {"sources": [{"sheetId": comp_ws_id, "startRowIndex": 0, "endRowIndex": 21, "startColumnIndex": 0, "endColumnIndex": 1}]}}}
                    ],
                    "series": [
                        {"series": {"sourceRange": {"sources": [{"sheetId": comp_ws_id, "startRowIndex": 0, "endRowIndex": 21, "startColumnIndex": 11, "endColumnIndex": 12}]}}, "targetAxis": "LEFT_AXIS"},
                        {"series": {"sourceRange": {"sources": [{"sheetId": comp_ws_id, "startRowIndex": 0, "endRowIndex": 21, "startColumnIndex": 12, "endColumnIndex": 13}]}}, "targetAxis": "LEFT_AXIS"}
                    ]
                }
            },
            "position": {
                "overlayPosition": {
                    "anchorCell": {"sheetId": comp_ws_id, "rowIndex": 64, "columnIndex": 30},
                    "offsetXPixels": 0, "offsetYPixels": 0
                }
            }
        }
    }
}

# 5. Biểu đồ cột so sánh tỉ lệ ODR AM W24 vs W23 (Cột A & R, S)
comp_odr_chart = {
    "addChart": {
        "chart": {
            "spec": {
                "title": "SO SÁNH TỈ LỆ ODR CỦA AM - TUẦN 24 VS TUẦN 23",
                "basicChart": {
                    "chartType": "COLUMN",
                    "legendPosition": "BOTTOM_LEGEND",
                    "headerCount": 1,
                    "axis": [
                        {"position": "BOTTOM_AXIS", "title": "AM"},
                        {"position": "LEFT_AXIS", "title": "Tỉ lệ ODR (%)"}
                    ],
                    "domains": [
                        {"domain": {"sourceRange": {"sources": [{"sheetId": comp_ws_id, "startRowIndex": 0, "endRowIndex": 21, "startColumnIndex": 0, "endColumnIndex": 1}]}}}
                    ],
                    "series": [
                        {"series": {"sourceRange": {"sources": [{"sheetId": comp_ws_id, "startRowIndex": 0, "endRowIndex": 21, "startColumnIndex": 17, "endColumnIndex": 18}]}}, "targetAxis": "LEFT_AXIS"},
                        {"series": {"sourceRange": {"sources": [{"sheetId": comp_ws_id, "startRowIndex": 0, "endRowIndex": 21, "startColumnIndex": 18, "endColumnIndex": 19}]}}, "targetAxis": "LEFT_AXIS"}
                    ]
                }
            },
            "position": {
                "overlayPosition": {
                    "anchorCell": {"sheetId": comp_ws_id, "rowIndex": 85, "columnIndex": 30},
                    "offsetXPixels": 0, "offsetYPixels": 0
                }
            }
        }
    }
}

try:
    sh.batch_update({"requests": [donut_chart, comp_vol_chart, comp_gtc_chart, comp_ltc_chart, comp_odr_chart]})
    print("✔️ Đã vẽ thành công 5 biểu đồ so sánh & tỉ trọng lên Google Sheets.")
except Exception as e:
    print(f"❌ Lỗi vẽ biểu đồ so sánh: {e}")

print("="*60)
print("🎉 ĐỒNG BỘ HÓA TOÀN BỘ PHÂN TÍCH & BIỂU ĐỒ SONG SONG LÊN CLOUD THÀNH CÔNG!")
print("="*60)
print("🎉 ĐỒNG BỘ HÓA DỮ LIỆU & BIỂU ĐỒ SONG SONG TRÊN CLOUD HOÀN TẤT!")
print("="*60)
