import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")

df = pd.read_excel(file_path, sheet_name="Data")
# Filter for D (2026-06-07)
df_d = df[df['Time'].str.startswith('2026-06-07', na=False)].copy()

print("Columns in Data:")
print(list(df.columns))

print("\nRows matching 2026-06-07:", len(df_d))

# Group by Province and sum different candidate fields
summary = df_d.groupby('Tỉnh').agg({
    'Volume': 'sum',
    'Sản Lượng Giao Thành Công': 'sum',
    'Sản Lượng Gán': 'sum',
    'Hàng Mới Về Trong Ngày': 'sum'
}).reset_index()

# Also try computing Volume * % GTC manually or standard delivered_vol
df_d['delivered_vol_calc'] = df_d['Volume'] * df_d['% GTC']
df_d['delivered_vol_calc_percent'] = df_d['Volume'] * (df_d['% GTC'] / 100 if df_d['% GTC'].max() > 1 else df_d['% GTC'])

summary_calc = df_d.groupby('Tỉnh').agg({
    'delivered_vol_calc': 'sum',
    'delivered_vol_calc_percent': 'sum'
}).reset_index()

merged = pd.merge(summary, summary_calc, on='Tỉnh')
print("\nSums by Province:")
print(merged.to_string())

# Let's print out the Looker Targets for comparison:
# Đắk Nông: 4460
# Ninh Thuận: 3727
# Lâm Đồng: 9496
# Khánh Hòa: 11515
# Bình Thuận: 10369
print("\nLooker Targets:")
print("Đắk Nông: 4460, Ninh Thuận: 3727, Lâm Đồng: 9496, Khánh Hòa: 11515, Bình Thuận: 10369")
