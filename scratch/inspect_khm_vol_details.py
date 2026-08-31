import pickle
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\raw_sheets_data.pkl", "rb") as f:
    data = pickle.load(f)

df_raw = data['khách hàng mơi'].copy()
df_raw['DoanhThu_NoVAT'] = pd.to_numeric(df_raw['DoanhThu_NoVAT'], errors='coerce').fillna(0)
df_raw['Volume'] = pd.to_numeric(df_raw['Volume'], errors='coerce').fillna(0)
df_raw['Ngày LTC đầu tiên'] = df_raw['Ngày LTC đầu tiên'].astype(str).str.strip()
df_raw['AM'] = df_raw['AM'].astype(str).str.strip()

# AM to Province mapping
df_cocau = data['Cocauvung']
am_to_tinh = {}
for am, group in df_cocau.groupby('AM'):
    prov = group['Tỉnh'].iloc[0]
    am_to_tinh[am] = prov

df_raw['Tinh_mapped'] = df_raw['AM'].map(am_to_tinh)
ntb_provinces = ['Khánh Hòa', 'Lâm Đồng', 'Đắk Nông', 'Ninh Thuận', 'Bình Thuận']

# Filter only NTB rows for 16/06 and 15/06
sub_16 = df_raw[(df_raw['Ngày LTC đầu tiên'] == '16 thg 6, 2026') & (df_raw['Tinh_mapped'].isin(ntb_provinces))]
sub_15 = df_raw[(df_raw['Ngày LTC đầu tiên'] == '15 thg 6, 2026') & (df_raw['Tinh_mapped'].isin(ntb_provinces))]

print("=== Raw KHM rows for NTB on 16/06 ===")
for idx, r in sub_16.iterrows():
    print(f"Index {idx}: Mã KH: {r['Mã KH']} | Tên KH: {r['Tên KH']} | Tinh: {r['Tinh']} | Bưu cục: {r['Bưu Cục SO']} | AM: {r['AM']} (Mapped: {r['Tinh_mapped']}) | Vol: {r['Volume']} | DT: {r['DoanhThu_NoVAT']}")

print("\n=== Raw KHM rows for NTB on 15/06 ===")
for idx, r in sub_15.iterrows():
    print(f"Index {idx}: Mã KH: {r['Mã KH']} | Tên KH: {r['Tên KH']} | Tinh: {r['Tinh']} | Bưu cục: {r['Bưu Cục SO']} | AM: {r['AM']} (Mapped: {r['Tinh_mapped']}) | Vol: {r['Volume']} | DT: {r['DoanhThu_NoVAT']}")
