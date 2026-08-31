import pandas as pd
import json

df_sl = pd.read_csv("scratch/sheet_sl_10kg_raw.csv")
df_tren = pd.read_csv("scratch/sheet_tren10kg_raw.csv")

print("=== SL > 10kg ===")
print("Columns:", list(df_sl.columns))
print("Shape:", df_sl.shape)
print("Time unique (top 5):", df_sl['Time'].dropna().unique()[:5])
print("Loại Hàng unique:", df_sl['Loại Hàng'].dropna().unique() if 'Loại Hàng' in df_sl else "N/A")
print("Loại Khối Lượng unique:", df_sl['Loại Khối Lượng'].dropna().unique() if 'Loại Khối Lượng' in df_sl else "N/A")
print("Chi tiết (Bưu cục) count:", df_sl['Chi tiết'].nunique() if 'Chi tiết' in df_sl else "N/A")

print("\n=== treen10kg ===")
print("Columns:", list(df_tren.columns))
print("Shape:", df_tren.shape)
for col in df_tren.columns:
    print(f"Col: {col} | Non-null: {df_tren[col].count()} | Sample: {df_tren[col].dropna().iloc[:3].tolist()}")
