import pandas as pd
import os

path = "ops_gtc.csv"
out_path = "scratch/analyze_large_pos_out.txt"

with open(out_path, "w", encoding="utf-8") as f:
    f.write("=== LARGE POS IN NTB ===\n")
    if os.path.exists(path):
        df = pd.read_csv(path)
        # Latest date
        latest_date = '2026-06-13 - Thứ 7'
        df_latest = df[df['Time'] == latest_date].copy()
        
        # Convert columns to numeric
        for col in ['Volume', 'Sản Lượng Giao Thành Công', 'Sản Lượng Tồn', 'Sản Lượng Chưa Gán']:
            df_latest[col] = pd.to_numeric(df_latest[col], errors='coerce').fillna(0)
            
        # Group by Chi tiết and AM
        pos = df_latest.groupby(['Chi tiết', 'AM', 'Tỉnh']).agg(
            Vol=('Volume', 'sum'),
            GTC=('Sản Lượng Giao Thành Công', 'sum'),
            Ton=('Sản Lượng Tồn', 'sum'),
            ChuaGan=('Sản Lượng Chưa Gán', 'sum')
        ).reset_index()
        pos['% GTC'] = (pos['GTC'] / pos['Vol'] * 100).round(2)
        pos['% Tồn'] = (pos['Ton'] / pos['Vol'] * 100).round(2)
        
        # Sort by Vol descending
        pos_sorted = pos.sort_values(by='Vol', ascending=False)
        f.write("\n--- Largest 10 Post Offices by Volume on 13/06 ---\n")
        f.write(pos_sorted.head(15).to_string() + "\n")
    else:
        f.write("ops_gtc.csv not found\n")

print("Done writing large POs!")
