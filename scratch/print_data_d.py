import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")

df = pd.read_excel(file_path, sheet_name="Data")
# Extracted date from Time column (e.g. '2026-06-07 - Chủ Nhật')
df['date_str'] = df['Time'].apply(lambda x: str(x).split(' - ')[0])

# Filter for 2026-06-07
df_d = df[df['date_str'] == '2026-06-07'].copy()

# List numeric columns
numeric_cols = [
    'Volume', 'Sản Lượng Giao Thành Công', 'Sản Lượng Chuyển Trả', 
    'Sản Lượng Gán', 'Sản Lượng Trả', 'Sản Lượng Tồn', 
    'Sản Lượng Chưa Gán', 'Hàng Mới Về Trong Ngày'
]

print("SUMS GROUPED BY TINH ON 2026-06-07:")
grouped = df_d.groupby('Tỉnh')[numeric_cols].sum()
print(grouped.to_string())

print("\nCALCULATING Volume * % GTC / 100:")
df_d['calc_delivered'] = df_d['Volume'] * (df_d['% GTC'] / 100 if df_d['% GTC'].max() > 1 else df_d['% GTC'])
print(df_d.groupby('Tỉnh')['calc_delivered'].sum().to_string())
