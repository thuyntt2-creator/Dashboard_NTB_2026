import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "vols_tao_don.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "tao_don_db_summary.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="shopee_tiktok")
    df['Date'] = pd.to_datetime(df['Date'])
    
    f.write("=== Column Names ===\n")
    f.write(str(df.columns.tolist()) + "\n\n")
    
    f.write("=== Value Counts for bat_on ===\n")
    f.write(df['bat_on'].value_counts(dropna=False).to_string() + "\n\n")
    
    f.write("=== Date range in sheet ===\n")
    f.write(f"Min Date: {df['Date'].min()}\n")
    f.write(f"Max Date: {df['Date'].max()}\n\n")
    
    latest_dt = df['Date'].max()
    f.write(f"Latest Date (Today / Day N): {latest_dt.strftime('%Y-%m-%d')}\n\n")
    
    # Let's filter out 'BC Cũ/Không thuộc ĐCL' if that is what the app does
    df_filtered = df[df['bat_on'].fillna('').str.strip() != 'BC Cũ/Không thuộc ĐCL'].copy()
    
    f.write("=== Total volume by date (last 7 days, unfiltered) ===\n")
    by_date_raw = df.groupby('Date')['Volume'].sum().sort_index(ascending=False).head(10)
    f.write(by_date_raw.to_string() + "\n\n")
    
    f.write("=== Total volume by date (last 7 days, filtered: excluding BC Cũ/Không thuộc ĐCL) ===\n")
    by_date_filtered = df_filtered.groupby('Date')['Volume'].sum().sort_index(ascending=False).head(10)
    f.write(by_date_filtered.to_string() + "\n\n")
    
    f.write("=== Detailed Volume by Province for latest date (filtered) ===\n")
    df_latest = df_filtered[df_filtered['Date'] == latest_dt]
    by_prov = df_latest.groupby('Tỉnh')['Volume'].sum().reset_index()
    f.write(by_prov.to_string(index=False) + "\n\n")
    
    f.write("=== Detailed Volume by Province for latest date (unfiltered) ===\n")
    df_latest_raw = df[df['Date'] == latest_dt]
    by_prov_raw = df_latest_raw.groupby('Tỉnh')['Volume'].sum().reset_index()
    f.write(by_prov_raw.to_string(index=False) + "\n\n")

print("Done writing scratch/tao_don_db_summary.txt")
