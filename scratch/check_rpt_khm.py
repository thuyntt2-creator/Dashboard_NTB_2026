import pickle
import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\raw_sheets_data.pkl", "rb") as f:
    data = pickle.load(f)

df_rpt_khm = data['RPT_KHM']
df_raw = data['khách hàng mơi'].copy()

# Clean raw data
df_raw['DoanhThu_NoVAT'] = pd.to_numeric(df_raw['DoanhThu_NoVAT'], errors='coerce').fillna(0)
df_raw['Volume'] = pd.to_numeric(df_raw['Volume'], errors='coerce').fillna(0)
df_raw['Ngày LTC đầu tiên'] = df_raw['Ngày LTC đầu tiên'].astype(str).str.strip()
df_raw['Tinh'] = df_raw['Tinh'].astype(str).str.strip()
df_raw['AM'] = df_raw['AM'].astype(str).str.strip()

# Let's map Vietnamese months in date strings to Timestamp
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

# Let's see unique values of Tinh in raw KHM data
print("Unique Tinh in KHM raw data:", df_raw['Tinh'].unique())

# AM to Province mapping (via Cocauvung)
# Let's see if AM is in Cocauvung to get its Tỉnh
df_cocau = data['Cocauvung']
am_to_tinh = {}
for am, group in df_cocau.groupby('AM'):
    prov = group['Tỉnh'].iloc[0]
    am_to_tinh[am] = prov

# Let's define the province mapping for AM in KHM raw data
# What about AMs like "Đã nghỉ"?
# Let's write a function that maps each row to its Tỉnh.
# Does the report group by the "Tinh" column in the raw data directly?
# Let's write a check.

def get_khm_summary(df, start_date, end_date):
    sub = df[(df['Timestamp'] >= start_date) & (df['Timestamp'] <= end_date)]
    # Group by raw "Tinh"
    gp_tinh = sub.groupby('Tinh').agg(
        kh_count=('Mã KH', 'nunique'),
        vol=('Volume', 'sum'),
        dt_tr=('DoanhThu_NoVAT', lambda x: x.sum() / 1000000.0)
    ).reset_index()
    
    # Group by mapped AM Tỉnh
    sub_mapped = sub.copy()
    sub_mapped['Tinh_mapped'] = sub_mapped['AM'].map(am_to_tinh).fillna('Khác')
    gp_mapped = sub_mapped.groupby('Tinh_mapped').agg(
        kh_count=('Mã KH', 'nunique'),
        vol=('Volume', 'sum'),
        dt_tr=('DoanhThu_NoVAT', lambda x: x.sum() / 1000000.0)
    ).reset_index()
    
    return gp_tinh, gp_mapped

# June 16, 2026 summary
tinh_16, mapped_16 = get_khm_summary(df_raw, '2026-06-16', '2026-06-16')
print("\n=== Group by Raw Tinh on 16/06 ===")
print(tinh_16)
print("\n=== Group by Mapped AM Tinh on 16/06 ===")
print(mapped_16)

# Let's compare with RPT_KHM
# In RPT_KHM for 16/06:
# Khánh Hòa: 4 KH, 5 Vol, 0.1 DT
# Lâm Đồng: 1 KH, 1 Vol, — DT
# Đắk Nông: — KH, — Vol, — DT
# Ninh Thuận: 2 KH, 3 Vol, 0.1 DT
# Bình Thuận: — KH, — Vol, — DT
# TỔNG NTB: 7 KH, 9 Vol, 0.2 DT
