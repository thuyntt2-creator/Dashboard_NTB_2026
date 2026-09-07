import pandas as pd
import unicodedata
import sys

sys.stdout.reconfigure(encoding='utf-8')
INPUT_EXCEL = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"

df_gtc_full = pd.read_excel(INPUT_EXCEL, sheet_name='dataGTC gốc full hàng')
df_gtc_tts = pd.read_excel(INPUT_EXCEL, sheet_name='dataGTC gốc TTS')
df_ltc_full = pd.read_excel(INPUT_EXCEL, sheet_name='dataLTC full hàng')
df_ltc_tts = pd.read_excel(INPUT_EXCEL, sheet_name='dataLTC TTS')
df_odr_full = pd.read_excel(INPUT_EXCEL, sheet_name='dataODRfull hàng ')
df_cocau = pd.read_excel(INPUT_EXCEL, sheet_name='cocau')

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

# 1. GTC
df_gtc = df_gtc_full[(df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2', 'Hàng Tồn'])) & (df_gtc_full['Chi tiết'] != 'Grand Total')].copy()
df_gtc['Vol_Gan'] = df_gtc['Volume'] * df_gtc['% Gán']
df_gtc['Vol_GTC'] = df_gtc['Volume'] * df_gtc['% GTC']
gtc_grouped = df_gtc.groupby(['AM_mapped', 'Tỉnh_mapped', 'Time']).agg(
    vol_gtc=('Volume', 'sum'),
    vol_gan_gtc=('Vol_Gan', 'sum'),
    vol_gtc_ok=('Vol_GTC', 'sum')
).reset_index()
gtc_grouped['% GTC'] = gtc_grouped['vol_gtc_ok'] / gtc_grouped['vol_gtc']

# 2. LTC
df_ltc = df_ltc_full[df_ltc_full['Cấp quản lý'] != 'Grand Total'].copy()
df_ltc['Vol_Gan'] = df_ltc['Volume'] * df_ltc['%Gán']
df_ltc['Vol_LTC'] = df_ltc['Volume'] * df_ltc['%LTC']
ltc_grouped = df_ltc.groupby(['AM_mapped', 'Tỉnh_mapped', 'Time']).agg(
    vol_ltc_raw=('Volume', 'sum'),
    vol_gan_ltc=('Vol_Gan', 'sum'),
    vol_ltc_ok=('Vol_LTC', 'sum')
).reset_index()
ltc_grouped['% LTC'] = ltc_grouped['vol_ltc_ok'] / ltc_grouped['vol_ltc_raw']

# 3. ODR
df_odr = df_odr_full.copy()
df_odr['Vol_Ontime'] = df_odr['GTC'] * df_odr['%Ontime']
odr_grouped = df_odr.groupby(['Tỉnh_mapped', 'Time']).agg(
    vol_odr_gtc=('GTC', 'sum'),
    vol_odr_ok=('Vol_Ontime', 'sum')
).reset_index()
odr_grouped['% ODR'] = odr_grouped['vol_odr_ok'] / odr_grouped['vol_odr_gtc']

# Merge base
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

df_m = df_m.rename(columns={
    'AM_mapped': 'AM',
    'Tỉnh_mapped': 'Tỉnh',
    'Time': 'Tuần',
    'vol_gtc': 'Sản lượng giao',
    '% GTC': 'Tỉ lệ GTC',
    '% LTC': 'Tỉ lệ LTC',
    '% ODR': 'Tỉ lệ ODR'
})

df_m = df_m.sort_values(by=['AM', 'Tỉnh', 'Tuần']).reset_index(drop=True)
print(df_m.head(20))
print("\nTotal rows in analysis:", len(df_m))
