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
df_raw['AM'] = df_raw['AM'].astype(str).str.strip()

# Date parser
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

# Mappings
df_cocau = data['Cocauvung']
am_to_tinh = {}
for am, group in df_cocau.groupby('AM'):
    prov = group['Tỉnh'].iloc[0]
    am_to_tinh[am] = prov

# AM to Province mapping for NTB
ntb_provinces = ['Khánh Hòa', 'Lâm Đồng', 'Đắk Nông', 'Ninh Thuận', 'Bình Thuận']
df_raw['Tinh_mapped'] = df_raw['AM'].map(am_to_tinh)

# Group by Tinh_mapped and compute
def get_summary_for_period(df, start_date, end_date):
    sub = df[(df['Timestamp'] >= start_date) & (df['Timestamp'] <= end_date)]
    gp = sub.groupby('Tinh_mapped').agg(
        kh_count=('Mã KH', 'nunique'),
        vol=('Volume', 'sum'),
        dt_tr=('DoanhThu_NoVAT', lambda x: x.sum() / 1000000.0)
    ).reindex(ntb_provinces).fillna(0).reset_index()
    return gp

summary_16 = get_summary_for_period(df_raw, '2026-06-16', '2026-06-16')
summary_15 = get_summary_for_period(df_raw, '2026-06-15', '2026-06-15')
summary_mtd_t6 = get_summary_for_period(df_raw, '2026-06-01', '2026-06-16')
summary_mtd_t5 = get_summary_for_period(df_raw, '2026-05-01', '2026-05-16')

# Let's print out the comparison for each period
periods = [
    ('Ngày 16/06', summary_16),
    ('Ngày 15/06', summary_15),
    ('MTD T6 (1-16)', summary_mtd_t6),
    ('MTD T5 (1-16)', summary_mtd_t5)
]

for p_name, summary_df in periods:
    print(f"\n==================== PERIOD: {p_name} ====================")
    print(f"{'TỈNH':<15} | {'#KH Calc':<8} | {'Vol Calc':<8} | {'DT(M) Calc':<10}")
    print("-" * 55)
    tot_kh, tot_vol, tot_dt = 0, 0, 0.0
    for idx, r in summary_df.iterrows():
        print(f"{r['Tinh_mapped']:<15} | {r['kh_count']:<8.0f} | {r['vol']:<8.0f} | {r['dt_tr']:<10.2f}")
        tot_kh += r['kh_count']
        tot_vol += r['vol']
        tot_dt += r['dt_tr']
    print("-" * 55)
    print(f"{'TỔNG NTB':<15} | {tot_kh:<8.0f} | {tot_vol:<8.0f} | {tot_dt:<10.2f}")
