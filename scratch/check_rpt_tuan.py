import pickle
import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\raw_sheets_data.pkl", "rb") as f:
    data = pickle.load(f)

df_rpt_tuan = data['RPT_Tuần']
df_raw = data['Theo Tuần'].copy()

# Clean raw data
df_raw['DoanhThu'] = pd.to_numeric(df_raw['DoanhThu'], errors='coerce').fillna(0)
df_raw['Volume'] = pd.to_numeric(df_raw['Volume'], errors='coerce').fillna(0)
df_raw['AM_clean'] = df_raw['AM_format'].astype(str).str.strip()

# AM-to-province mapping (same as RPT_Ngày detail table)
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

df_raw['Tinh_mapped'] = df_raw['AM_clean'].map(am_mapping).fillna('Khác')

# Let's print unique values of Tuan in raw data for 2026/23 and 2026/24
print("Unique weeks in Theo Tuần:", df_raw['Tuan'].unique())

# Group by Tinh and Tuan
grouped = df_raw.groupby(['Tinh_mapped', 'Tuan']).agg(
    dt_tr=('DoanhThu', lambda x: x.sum() / 1000000.0),
    vol=('Volume', 'sum')
).reset_index()

target_weeks = ['2026/23', '2026/24']
provinces = ['Khánh Hòa', 'Lâm Đồng', 'Đắk Nông', 'Ninh Thuận', 'Bình Thuận', 'Khác']

print("\n=== CHECKING RPT_Tuần: REVENUE ===")
print(f"{'TỈNH':<15} | {'W23 Calc':<10} | {'W23 Rpt':<10} | {'W24 Calc':<10} | {'W24 Rpt':<10}")
print("-" * 70)
for p in provinces:
    val_w23 = grouped[(grouped['Tinh_mapped'] == p) & (grouped['Tuan'] == '2026/23')]['dt_tr'].values
    val_w24 = grouped[(grouped['Tinh_mapped'] == p) & (grouped['Tuan'] == '2026/24')]['dt_tr'].values
    w23_calc = val_w23[0] if len(val_w23) > 0 else 0.0
    w24_calc = val_w24[0] if len(val_w24) > 0 else 0.0
    
    # Rpt values (row search)
    rpt_row = df_rpt_tuan[df_rpt_tuan.iloc[:, 0].astype(str).str.strip() == p]
    if not rpt_row.empty:
        rpt_w23 = rpt_row.iloc[0, 1]
        rpt_w24 = rpt_row.iloc[0, 2]
    else:
        rpt_w23, rpt_w24 = "N/A", "N/A"
    print(f"{p:<15} | {w23_calc:<10.2f} | {rpt_w23:<10} | {w24_calc:<10.2f} | {rpt_w24:<10}")

print("\n=== CHECKING RPT_Tuần: VOLUME ===")
print(f"{'TỈNH':<15} | {'W23 Calc':<10} | {'W23 Rpt':<10} | {'W24 Calc':<10} | {'W24 Rpt':<10}")
print("-" * 70)
for p in provinces:
    val_w23 = grouped[(grouped['Tinh_mapped'] == p) & (grouped['Tuan'] == '2026/23')]['vol'].values
    val_w24 = grouped[(grouped['Tinh_mapped'] == p) & (grouped['Tuan'] == '2026/24')]['vol'].values
    w23_calc = val_w23[0] if len(val_w23) > 0 else 0
    w24_calc = val_w24[0] if len(val_w24) > 0 else 0
    
    # Rpt values (second table in RPT_Tuần starting at index 12)
    rpt_sub = df_rpt_tuan.iloc[12:19]
    rpt_row = rpt_sub[rpt_sub.iloc[:, 0].astype(str).str.strip() == p]
    if not rpt_row.empty:
        rpt_w23 = rpt_row.iloc[0, 1]
        rpt_w24 = rpt_row.iloc[0, 2]
    else:
        rpt_w23, rpt_w24 = "N/A", "N/A"
    print(f"{p:<15} | {w23_calc:<10.0f} | {rpt_w23:<10} | {w24_calc:<10.0f} | {rpt_w24:<10}")
