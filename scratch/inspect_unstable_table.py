import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import pandas as pd
import os

file_path = "buu_cuc_bat_on.csv"
df_raw = pd.read_csv(file_path, header=None)

header_row_idx = None
for r_idx in range(len(df_raw)):
    row_vals = [str(x).lower().strip() for x in df_raw.iloc[r_idx].values]
    print(f"Row {r_idx}: {row_vals[:8]}")
    if any("tổng số lượng" in x or "thời gian cập nhật" in x for x in row_vals):
        continue
    if any(x == "bưu cục" or x == "chi tiết" or x == "tên bc" or "tên bưu cục" in x or "kho_giao_id" in x or "kho_giao_name" in x or "tinh_giao" in x for x in row_vals):
        header_row_idx = r_idx
        break

print(f"\nDetected header_row_idx: {header_row_idx}")

if header_row_idx is not None:
    df_table = pd.read_csv(file_path, skiprows=header_row_idx)
    print("df_table columns:", list(df_table.columns))
    print("df_table shape:", df_table.shape)
    print("df_table head(5):")
    print(df_table.head(5).to_string())
    
    # check columns for id_col and name_col
    id_col = next((c for c in df_table.columns if "id" in c.lower() or "kho_giao_id" in c.lower()), df_table.columns[0])
    name_col = next((c for c in df_table.columns if "name" in c.lower() or "bưu cục" in c.lower() or "kho_giao_name" in c.lower()), df_table.columns[1] if len(df_table.columns) > 1 else df_table.columns[0])
    print(f"\nid_col: {id_col}, name_col: {name_col}")
    
    # Filter empty rows
    df_table_filtered = df_table.dropna(subset=[id_col, name_col], how='all')
    df_table_filtered = df_table_filtered[df_table_filtered[id_col].astype(str).str.strip() != ""]
    print("df_table_filtered shape:", df_table_filtered.shape)
    print("df_table_filtered head(2):")
    print(df_table_filtered.head(2).to_string())
