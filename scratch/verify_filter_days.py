import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "vols_tao_don.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "verify_filter_days_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="shopee_tiktok")
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Apply filter: exclude 'BC Cũ/Không thuộc ĐCL'
    df_filtered = df[df['bat_on'] != 'BC Cũ/Không thuộc ĐCL'].copy()
    
    # 1. Check Daily Sums for D (2026-06-07) and D-1 (2026-06-06)
    f.write("--- Daily Sums with Filter (exclude 'BC Cũ/Không thuộc ĐCL') ---\n")
    for d_str in ['2026-06-07', '2026-06-06', '2026-06-05', '2026-06-04', '2026-06-03', '2026-06-02', '2026-06-01', '2026-05-31']:
        df_date = df_filtered[df_filtered['Date'] == d_str]
        f.write(f"\nDate: {d_str}\n")
        f.write(df_date.groupby('Tỉnh')['Volume'].sum().to_string() + "\n")
        f.write(f"Total: {df_date['Volume'].sum()}\n")

    # 2. Check WTD (2026-06-01 to 2026-06-07)
    f.write("\n\n--- WTD Sums with Filter ---\n")
    df_wtd = df_filtered[(df_filtered['Date'] >= '2026-06-01') & (df_filtered['Date'] <= '2026-06-07')]
    f.write(df_wtd.groupby('Tỉnh')['Volume'].sum().to_string() + "\n")
    f.write(f"Total WTD: {df_wtd['Volume'].sum()}\n")
    
    # 3. Check WTD-1 (2026-05-25 to 2026-05-31)
    f.write("\n\n--- WTD-1 Sums with Filter ---\n")
    df_wtd1 = df_filtered[(df_filtered['Date'] >= '2026-05-25') & (df_filtered['Date'] <= '2026-05-31')]
    f.write(df_wtd1.groupby('Tỉnh')['Volume'].sum().to_string() + "\n")
    f.write(f"Total WTD-1: {df_wtd1['Volume'].sum()}\n")

    # 4. Check WTD-2 (2026-05-18 to 2026-05-24)
    f.write("\n\n--- WTD-2 Sums with Filter ---\n")
    df_wtd2 = df_filtered[(df_filtered['Date'] >= '2026-05-18') & (df_filtered['Date'] <= '2026-05-24')]
    f.write(df_wtd2.groupby('Tỉnh')['Volume'].sum().to_string() + "\n")
    f.write(f"Total WTD-2: {df_wtd2['Volume'].sum()}\n")
    
print("Done writing verify_filter_days_res.txt")
