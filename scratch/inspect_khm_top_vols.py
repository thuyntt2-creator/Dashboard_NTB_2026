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

# Mappings of Vietnamese months in date strings to Timestamp
month_map = {
    'thg 1': 1, 'thg 2': 2, 'thg 3': 3, 'thg 4': 4, 'thg 5': 5, 'thg 6': 6,
    'thg 7': 7, 'thg 8': 8, 'thg 9': 9, 'thg 10': 10, 'thg 11': 11, 'thg 12': 12
}

def parse_vn_date(d_str):
    if not d_str or str(d_str).strip() == '':
        return None
    d_str = str(d_str).strip()
    parts = d_str.split('thg')
    if len(parts) == 2:
        day = int(parts[0].strip())
        sub_parts = parts[1].split(',')
        month = int(sub_parts[0].strip())
        year = int(sub_parts[1].strip())
        return pd.Timestamp(year=year, month=month, day=day)
    return None

df_raw['Timestamp'] = df_raw['Ngày LTC đầu tiên'].apply(parse_vn_date)

# Filter June MTD (1-16) for Khánh Hòa
sub_kh = df_raw[
    (df_raw['Timestamp'] >= '2026-06-01') & 
    (df_raw['Timestamp'] <= '2026-06-16') & 
    (df_raw['Tinh_mapped'] == 'Khánh Hòa')
]

print("=== Top customers by Vol in Khánh Hòa June MTD (1-16) ===")
sub_kh_sorted = sub_kh.sort_values(by='Volume', ascending=False)
for idx, r in sub_kh_sorted.head(10).iterrows():
    print(f"Mã KH: {r['Mã KH']} | Tên KH: {r['Tên KH']} | LTC: {r['Ngày LTC đầu tiên']} | Vol: {r['Volume']} | DT: {r['DoanhThu_NoVAT']}")

print(f"\nTotal Vol of Khánh Hòa MTD T6 (1-16): {sub_kh['Volume'].sum()}")
print(f"Total #KH of Khánh Hòa MTD T6 (1-16): {sub_kh['Mã KH'].nunique()}")
print(f"Total DT of Khánh Hòa MTD T6 (1-16): {sub_kh['DoanhThu_NoVAT'].sum() / 1000000.0:.2f} M")
