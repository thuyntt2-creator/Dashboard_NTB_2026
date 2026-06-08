import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "vols_tao_don.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "aggregate_user_vols_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="shopee_tiktok")
    
    # Ensure Date column is datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    f.write("DATES IN DATASET:\n")
    f.write(f"Min date: {df['Date'].min()}\n")
    f.write(f"Max date: {df['Date'].max()}\n\n")
    
    # Let's aggregate for 2026-06-07
    d_date = pd.to_datetime('2026-06-07')
    df_d = df[df['Date'] == d_date]
    f.write(f"Total rows on 2026-06-07: {len(df_d)}\n")
    
    grouped_d = df_d.groupby('Tỉnh')['Volume'].sum().reset_index()
    f.write("\nVOLUME SUM BY PROVINCE ON 2026-06-07 (D):\n")
    f.write(grouped_d.to_string() + "\n")
    f.write(f"Total D volume: {grouped_d['Volume'].sum()}\n\n")
    
    # Let's aggregate for 2026-06-06 (D-1)
    d1_date = pd.to_datetime('2026-06-06')
    df_d1 = df[df['Date'] == d1_date]
    grouped_d1 = df_d1.groupby('Tỉnh')['Volume'].sum().reset_index()
    f.write("VOLUME SUM BY PROVINCE ON 2026-06-06 (D-1):\n")
    f.write(grouped_d1.to_string() + "\n")
    f.write(f"Total D-1 volume: {grouped_d1['Volume'].sum()}\n\n")

    # Let's check weekly sums (WTD: 2026-06-01 to 2026-06-07)
    df_wtd = df[(df['Date'] >= '2026-06-01') & (df['Date'] <= '2026-06-07')]
    grouped_wtd = df_wtd.groupby('Tỉnh')['Volume'].sum().reset_index()
    f.write("WTD VOLUME SUM BY PROVINCE (2026-06-01 to 2026-06-07):\n")
    f.write(grouped_wtd.to_string() + "\n")
    f.write(f"Total WTD volume: {grouped_wtd['Volume'].sum()}\n\n")
    
    # Let's check weekly sums (WTD-1: 2026-05-25 to 2026-05-31)
    df_wtd1 = df[(df['Date'] >= '2026-05-25') & (df['Date'] <= '2026-05-31')]
    grouped_wtd1 = df_wtd1.groupby('Tỉnh')['Volume'].sum().reset_index()
    f.write("WTD-1 VOLUME SUM BY PROVINCE (2026-05-25 to 2026-05-31):\n")
    f.write(grouped_wtd1.to_string() + "\n")
    f.write(f"Total WTD-1 volume: {grouped_wtd1['Volume'].sum()}\n\n")
    
print("Done writing aggregate_user_vols_res.txt")
