import pickle
import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\raw_sheets_data.pkl", "rb") as f:
    data = pickle.load(f)

df_rpt_ngay = data['RPT_Ngày']
df_raw = data['Theo ngày'].copy()

print("Columns in 'Theo ngày':", list(df_raw.columns))
print("Data types:", df_raw.dtypes)

# Check unique dates in 'Theo ngày' for June 2026
june_dates = df_raw[df_raw['Ngay'].astype(str).str.contains('thg 6, 2026')]['Ngay'].unique()
print("June 2026 dates in 'Theo ngày':", june_dates)

# Let's clean the numeric columns
df_raw['DoanhThu'] = pd.to_numeric(df_raw['DoanhThu'], errors='coerce').fillna(0)
df_raw['Volume'] = pd.to_numeric(df_raw['Volume'], errors='coerce').fillna(0)

# Let's map each raw AM to the province based on RPT_Ngày's detail table
# Detail table AMs mapping
am_mapping = {
    'Phan Đình Duy': 'Khánh Hòa',
    'Thái Thị Thanh Thư': 'Khánh Hòa',
    'Nguyễn Duy Long': 'Ninh Thuận',
    'Trần Thị Nhung': 'Đắk Nông',
    'Nguyễn Lê Nguyên Vũ': 'Lâm Đồng',
    'Trần Công Hậu': 'Khác',
    'Trần Văn Phước': 'Đắk Nông',
    'Lê Văn Trường': 'Lâm Đồng',
    '': 'Khánh Hòa',
    'Huỳnh Tấn Hiền': 'Bình Thuận',
    'Hồng Bích Nga': 'Lâm Đồng',
    'Phạm Bá Thành Công': 'Khánh Hòa',
    'Huỳnh Thị Kim Chi': 'Lâm Đồng',
    'Trầm Hữu Tiến': 'Lâm Đồng',
    'Nguyễn Ngọc Khánh': 'Bình Thuận',
    'Lê Thanh Nhựt': 'Bình Thuận',
    'Nguyễn Hoàng Phi': 'Khánh Hòa',
    'Lê Minh Đại': 'Lâm Đồng',
    'Phan Đình Duy,Phạm Bá Thành Công': 'Khánh Hòa',
    'Nguyễn Thanh Long': 'Khánh Hòa',
    'Nguyễn Tống Hùng Phong,Thái Thị Thanh Thư,Trần Ngọc Trung': 'Khánh Hòa',
    'Võ Tấn Lợi': 'Lâm Đồng'
}

def clean_am_format(am_fmt):
    if not am_fmt:
        return ""
    return str(am_fmt).strip()

df_raw['AM_clean'] = df_raw['AM_format'].apply(clean_am_format)

# Group raw data by clean AM and date
df_raw_grouped = df_raw.groupby(['AM_clean', 'Ngay']).agg(
    dt_vnd=('DoanhThu', 'sum'),
    vol=('Volume', 'sum')
).reset_index()

df_raw_grouped['dt_tr'] = df_raw_grouped['dt_vnd'] / 1000000.0

# Verify on 16 thg 6, 2026
print("\n=== Calculations from 'Theo ngày' for 16/06 ===")
sub_16 = df_raw_grouped[df_raw_grouped['Ngay'] == '16 thg 6, 2026']
for idx, r in sub_16.iterrows():
    mapped_prov = am_mapping.get(r['AM_clean'], 'UNKNOWN')
    print(f"AM: '{r['AM_clean']}' ({mapped_prov}) | DT: {r['dt_tr']:.2f}M | Vol: {r['vol']:.0f}")

print("\nTotal calculated revenue for 16/06:", sub_16['dt_tr'].sum())
print("Total calculated volume for 16/06:", sub_16['vol'].sum())
