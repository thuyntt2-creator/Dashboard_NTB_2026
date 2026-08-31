import pickle
import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\raw_sheets_data.pkl", "rb") as f:
    data = pickle.load(f)

df_rpt_thang = data['RPT_Tháng']
df_raw = data['Theo ngày'].copy()

# Clean raw data
df_raw['DoanhThu'] = pd.to_numeric(df_raw['DoanhThu'], errors='coerce').fillna(0)
df_raw['Volume'] = pd.to_numeric(df_raw['Volume'], errors='coerce').fillna(0)
df_raw['AM_clean'] = df_raw['AM_format'].astype(str).str.strip()

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

# Let's parse the dates in "Theo ngày" to check years and months
# The format of date is e.g. "4 thg 10, 2025" or "16 thg 6, 2026"
# Let's write a parser for these Vietnamese date strings
month_map = {
    'thg 1': 1, 'thg 2': 2, 'thg 3': 3, 'thg 4': 4, 'thg 5': 5, 'thg 6': 6,
    'thg 7': 7, 'thg 8': 8, 'thg 9': 9, 'thg 10': 10, 'thg 11': 11, 'thg 12': 12
}

def parse_vn_date(d_str):
    if not d_str or str(d_str).strip() == '':
        return None
    d_str = str(d_str).strip()
    # e.g., "16 thg 6, 2026"
    parts = d_str.split('thg')
    if len(parts) == 2:
        day = int(parts[0].strip())
        sub_parts = parts[1].split(',')
        month = int(sub_parts[0].strip())
        year = int(sub_parts[1].strip())
        return pd.Timestamp(year=year, month=month, day=day)
    return None

df_raw['Timestamp'] = df_raw['Ngay'].apply(parse_vn_date)
print("Minimum date in Theo ngày:", df_raw['Timestamp'].min())
print("Maximum date in Theo ngày:", df_raw['Timestamp'].max())

# Let's check date ranges:
# MTD T5/2026 (1–16): 2026-05-01 to 2026-05-16
# MTD T6/2026 (1–16): 2026-06-01 to 2026-06-16
# MTD T6/2025 (1–16): 2025-06-01 to 2025-06-16

def get_mtd_sum(start_date, end_date):
    sub = df_raw[(df_raw['Timestamp'] >= start_date) & (df_raw['Timestamp'] <= end_date)]
    gp = sub.groupby('Tinh_mapped').agg(
        dt_tr=('DoanhThu', lambda x: x.sum() / 1000000.0),
        vol=('Volume', 'sum')
    ).reset_index()
    return gp

mtd_t5_2026 = get_mtd_sum('2026-05-01', '2026-05-16')
mtd_t6_2026 = get_mtd_sum('2026-06-01', '2026-06-16')
mtd_t6_2025 = get_mtd_sum('2025-06-01', '2025-06-16')

provinces = ['Khánh Hòa', 'Lâm Đồng', 'Đắk Nông', 'Ninh Thuận', 'Bình Thuận', 'Khác']

print("\n=== CHECKING RPT_Tháng: REVENUE MTD ===")
print(f"{'TỈNH':<15} | {'T5/2026 Calc':<12} | {'T5/2026 Rpt':<12} | {'T6/2026 Calc':<12} | {'T6/2026 Rpt':<12} | {'T6/2025 Calc':<12} | {'T6/2025 Rpt':<12}")
print("-" * 110)
for p in provinces:
    calc_t5 = mtd_t5_2026[mtd_t5_2026['Tinh_mapped'] == p]['dt_tr'].values
    calc_t6_26 = mtd_t6_2026[mtd_t6_2026['Tinh_mapped'] == p]['dt_tr'].values
    calc_t6_25 = mtd_t6_2025[mtd_t6_2025['Tinh_mapped'] == p]['dt_tr'].values
    
    t5_val = calc_t5[0] if len(calc_t5) > 0 else 0.0
    t6_26_val = calc_t6_26[0] if len(calc_t6_26) > 0 else 0.0
    t6_25_val = calc_t6_25[0] if len(calc_t6_25) > 0 else 0.0
    
    # Rpt values
    rpt_row = df_rpt_thang[df_rpt_thang.iloc[:, 0].astype(str).str.strip() == p]
    if not rpt_row.empty:
        rpt_t5 = rpt_row.iloc[0, 1]
        rpt_t6_26 = rpt_row.iloc[0, 2]
        rpt_t6_25 = rpt_row.iloc[0, 4]
    else:
        rpt_t5, rpt_t6_26, rpt_t6_25 = "N/A", "N/A", "N/A"
        
    print(f"{p:<15} | {t5_val:<12.2f} | {rpt_t5:<12} | {t6_26_val:<12.2f} | {rpt_t6_26:<12} | {t6_25_val:<12.2f} | {rpt_t6_25:<12}")

print("\n=== CHECKING RPT_Tháng: VOLUME MTD ===")
print(f"{'TỈNH':<15} | {'T5/2026 Calc':<12} | {'T5/2026 Rpt':<12} | {'T6/2026 Calc':<12} | {'T6/2026 Rpt':<12} | {'T6/2025 Calc':<12} | {'T6/2025 Rpt':<12}")
print("-" * 110)
for p in provinces:
    calc_t5 = mtd_t5_2026[mtd_t5_2026['Tinh_mapped'] == p]['vol'].values
    calc_t6_26 = mtd_t6_2026[mtd_t6_2026['Tinh_mapped'] == p]['vol'].values
    calc_t6_25 = mtd_t6_2025[mtd_t6_2025['Tinh_mapped'] == p]['vol'].values
    
    t5_val = calc_t5[0] if len(calc_t5) > 0 else 0
    t6_26_val = calc_t6_26[0] if len(calc_t6_26) > 0 else 0
    t6_25_val = calc_t6_25[0] if len(calc_t6_25) > 0 else 0
    
    # Rpt values (second table starting at row 12)
    rpt_sub = df_rpt_thang.iloc[12:19]
    rpt_row = rpt_sub[rpt_sub.iloc[:, 0].astype(str).str.strip() == p]
    if not rpt_row.empty:
        rpt_t5 = rpt_row.iloc[0, 1]
        rpt_t6_26 = rpt_row.iloc[0, 2]
        rpt_t6_25 = rpt_row.iloc[0, 4]
    else:
        rpt_t5, rpt_t6_26, rpt_t6_25 = "N/A", "N/A", "N/A"
        
    print(f"{p:<15} | {t5_val:<12.0f} | {rpt_t5:<12} | {t6_26_val:<12.0f} | {rpt_t6_26:<12} | {t6_25_val:<12.0f} | {rpt_t6_25:<12}")
