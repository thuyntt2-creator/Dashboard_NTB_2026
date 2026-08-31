import pickle
import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\raw_sheets_data.pkl", "rb") as f:
    data = pickle.load(f)

df_rpt_ngay = data['RPT_Ngày']
df_raw = data['Theo ngày'].copy()

# Clean raw data
df_raw['DoanhThu'] = pd.to_numeric(df_raw['DoanhThu'], errors='coerce').fillna(0)
df_raw['Volume'] = pd.to_numeric(df_raw['Volume'], errors='coerce').fillna(0)
df_raw['AM_clean'] = df_raw['AM_format'].astype(str).str.strip()

# AM-to-province mapping extracted from report
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

# Apply mapping
df_raw['Tinh_mapped'] = df_raw['AM_clean'].map(am_mapping).fillna('Khác')

# Group by Tinh and date
grouped = df_raw.groupby(['Tinh_mapped', 'Ngay']).agg(
    dt_tr=('DoanhThu', lambda x: x.sum() / 1000000.0),
    vol=('Volume', 'sum')
).reset_index()

# Target dates
dates = {
    'D': '16 thg 6, 2026',
    'D-1': '15 thg 6, 2026',
    'D-7': '9 thg 6, 2026'
}

# Let's extract values for report comparison
provinces = ['Khánh Hòa', 'Lâm Đồng', 'Đắk Nông', 'Ninh Thuận', 'Bình Thuận', 'Khác']

print("=== CHECKING RPT_Ngày: REVENUE ===")
print(f"{'TỈNH':<15} | {'D (16/06) Calc':<15} | {'D (16/06) Rpt':<15} | {'D-1 Calc':<10} | {'D-1 Rpt':<10} | {'D-7 Calc':<10} | {'D-7 Rpt':<10}")
print("-" * 100)

tot_dt = {'D': 0, 'D-1': 0, 'D-7': 0}

for p in provinces:
    # get values from raw grouped
    val_d = grouped[(grouped['Tinh_mapped'] == p) & (grouped['Ngay'] == dates['D'])]['dt_tr'].values
    val_d1 = grouped[(grouped['Tinh_mapped'] == p) & (grouped['Ngay'] == dates['D-1'])]['dt_tr'].values
    val_d7 = grouped[(grouped['Tinh_mapped'] == p) & (grouped['Ngay'] == dates['D-7'])]['dt_tr'].values
    
    d_val = val_d[0] if len(val_d) > 0 else 0.0
    d1_val = val_d1[0] if len(val_d1) > 0 else 0.0
    d7_val = val_d7[0] if len(val_d7) > 0 else 0.0
    
    # get values from report sheet
    # row index for p:
    # Khánh Hòa: row index 3
    # Lâm Đồng: row index 4
    # Đắk Nông: row index 5
    # Ninh Thuận: row index 6
    # Bình Thuận: row index 7
    # Khác: row index 8
    # We can search in df_rpt_ngay
    rpt_row = df_rpt_ngay[df_rpt_ngay.iloc[:, 0].astype(str).str.strip() == p]
    if not rpt_row.empty:
        rpt_d = rpt_row.iloc[0, 1]
        rpt_d1 = rpt_row.iloc[0, 2]
        rpt_d7 = rpt_row.iloc[0, 4]
    else:
        rpt_d, rpt_d1, rpt_d7 = "N/A", "N/A", "N/A"
        
    print(f"{p:<15} | {d_val:<15.2f} | {rpt_d:<15} | {d1_val:<10.2f} | {rpt_d1:<10} | {d7_val:<10.2f} | {rpt_d7:<10}")
    
    tot_dt['D'] += d_val
    tot_dt['D-1'] += d1_val
    tot_dt['D-7'] += d7_val

# Add Total row
rpt_total_row = df_rpt_ngay[df_rpt_ngay.iloc[:, 0].astype(str).str.contains('TỔNG VÙNG NTB', na=False)]
if not rpt_total_row.empty:
    rpt_tot_d = rpt_total_row.iloc[0, 1]
    rpt_tot_d1 = rpt_total_row.iloc[0, 2]
    rpt_tot_d7 = rpt_total_row.iloc[0, 4]
else:
    rpt_tot_d, rpt_tot_d1, rpt_tot_d7 = "N/A", "N/A", "N/A"
print("-" * 100)
print(f"{'TỔNG VÙNG NTB':<15} | {tot_dt['D']:<15.2f} | {rpt_tot_d:<15} | {tot_dt['D-1']:<10.2f} | {rpt_tot_d1:<10} | {tot_dt['D-7']:<10.2f} | {rpt_tot_d7:<10}")

print("\n=== CHECKING RPT_Ngày: VOLUME ===")
print(f"{'TỈNH':<15} | {'D (16/06) Calc':<15} | {'D (16/06) Rpt':<15} | {'D-1 Calc':<10} | {'D-1 Rpt':<10} | {'D-7 Calc':<10} | {'D-7 Rpt':<10}")
print("-" * 100)

tot_vol = {'D': 0, 'D-1': 0, 'D-7': 0}

for p in provinces:
    val_d = grouped[(grouped['Tinh_mapped'] == p) & (grouped['Ngay'] == dates['D'])]['vol'].values
    val_d1 = grouped[(grouped['Tinh_mapped'] == p) & (grouped['Ngay'] == dates['D-1'])]['vol'].values
    val_d7 = grouped[(grouped['Tinh_mapped'] == p) & (grouped['Ngay'] == dates['D-7'])]['vol'].values
    
    d_val = val_d[0] if len(val_d) > 0 else 0
    d1_val = val_d1[0] if len(val_d1) > 0 else 0
    d7_val = val_d7[0] if len(val_d7) > 0 else 0
    
    # get volume from report (second table, which starts around row 13 in the sheet)
    # let's search from row 12 onwards in RPT_Ngày
    rpt_sub = df_rpt_ngay.iloc[12:19]
    rpt_row = rpt_sub[rpt_sub.iloc[:, 0].astype(str).str.strip() == p]
    if not rpt_row.empty:
        rpt_d = rpt_row.iloc[0, 1]
        rpt_d1 = rpt_row.iloc[0, 2]
        rpt_d7 = rpt_row.iloc[0, 4]
    else:
        rpt_d, rpt_d1, rpt_d7 = "N/A", "N/A", "N/A"
        
    print(f"{p:<15} | {d_val:<15.0f} | {rpt_d:<15} | {d1_val:<10.0f} | {rpt_d1:<10} | {d7_val:<10.0f} | {rpt_d7:<10}")
    
    tot_vol['D'] += d_val
    tot_vol['D-1'] += d1_val
    tot_vol['D-7'] += d7_val

# Add Total volume row
rpt_tot_vol_row = df_rpt_ngay.iloc[12:20]
rpt_tot_vol_row = rpt_tot_vol_row[rpt_tot_vol_row.iloc[:, 0].astype(str).str.contains('TỔNG VÙNG NTB', na=False)]
if not rpt_tot_vol_row.empty:
    rpt_tot_d = rpt_tot_vol_row.iloc[0, 1]
    rpt_tot_d1 = rpt_tot_vol_row.iloc[0, 2]
    rpt_tot_d7 = rpt_tot_vol_row.iloc[0, 4]
else:
    rpt_tot_d, rpt_tot_d1, rpt_tot_d7 = "N/A", "N/A", "N/A"
print("-" * 100)
print(f"{'TỔNG VÙNG NTB':<15} | {tot_vol['D']:<15.0f} | {rpt_tot_d:<15} | {tot_vol['D-1']:<10.0f} | {rpt_tot_d1:<10} | {tot_vol['D-7']:<10.0f} | {rpt_tot_d7:<10}")
