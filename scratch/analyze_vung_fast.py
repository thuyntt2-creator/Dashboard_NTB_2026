import pandas as pd
import os

path = "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx"
out_path = "scratch/analyze_vung_out.txt"

with open(out_path, "w", encoding="utf-8") as f:
    f.write("=== FAST ANALYSIS OF REGION DATA ===\n")
    if os.path.exists(path):
        f.write("File exists!\n")
        # Let's read with engine_kwargs to load fast
        # Note: pd.ExcelFile with engine_kwargs
        xls = pd.ExcelFile(path, engine='openpyxl', engine_kwargs={'read_only': True})
        f.write(f"Sheets: {xls.sheet_names}\n")
        
        # 1. Data sheet
        if 'Data' in xls.sheet_names:
            df_data = pd.read_excel(xls, sheet_name='Data')
            f.write(f"\n--- Data Sheet (shape: {df_data.shape}) ---\n")
            f.write(f"Unique Times: {df_data['Time'].unique().tolist()}\n")
            f.write(f"Unique Provinces: {df_data['Tỉnh'].unique().tolist()}\n")
            f.write(f"Unique Vùng: {df_data['Vùng'].unique().tolist()}\n")
            f.write(f"Unique AMs: {df_data['AM'].unique().tolist()}\n")
            f.write(f"Unique Cấp Quản Lý: {df_data['Cấp Quản Lý'].unique().tolist()[:10]}\n")
            f.write(f"Unique Loại Hàng: {df_data['Loại Hàng'].unique().tolist()}\n")
            
            # Let's summarize ODR or GTC if they are in here
            # Let's see last week's data (yesterday is usually in the latest week/day)
            # Let's print out some rows for W24 (since W24 is the latest week mentioned in automate_report_and_dashboard.py)
            df_w24 = df_data[df_data['Time'] == '2026/24']
            f.write(f"\n--- Data Sheet Summary for W24 (rows: {len(df_w24)}) ---\n")
            # Group by AM, Province, and Type of Goods
            summary_gtc = df_w24.groupby(['AM', 'Tỉnh', 'Loại Hàng']).agg(
                Vol=('Volume', 'sum'),
                GTC_rate=('% GTC', 'mean'),
                Gan_rate=('% Gán', 'mean')
            ).reset_index().head(20)
            f.write(summary_gtc.to_string() + "\n")
            
        # 2. DataLTC sheet
        if 'DataLTC' in xls.sheet_names:
            df_ltc = pd.read_excel(xls, sheet_name='DataLTC')
            f.write(f"\n--- DataLTC Sheet (shape: {df_ltc.shape}) ---\n")
            f.write(f"Columns: {df_ltc.columns.tolist()}\n")
            f.write(f"Unique Times: {df_ltc['Time'].unique().tolist()}\n")
            df_ltc_w24 = df_ltc[df_ltc['Time'] == '2026/24'] if 'Time' in df_ltc.columns else df_ltc
            f.write(f"LTC for W24 head:\n{df_ltc_w24.head(10).to_string()}\n")
            
        # 3. ODR TTS sheet
        if 'ODR TTS' in xls.sheet_names:
            df_odr = pd.read_excel(xls, sheet_name='ODR TTS')
            f.write(f"\n--- ODR TTS Sheet (shape: {df_odr.shape}) ---\n")
            f.write(f"Columns: {df_odr.columns.tolist()}\n")
            f.write(f"Head:\n{df_odr.head(10).to_string()}\n")
            
        # 4. Check 'Bưu cục' or 'Ca1 - Ca2 - Tồn' sheets to see what other details are there
        for name in ['Bưu cục', 'Ca1 - Ca2 - Tồn', 'raw', 'TTS']:
            if name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=name)
                f.write(f"\n--- Sheet {name} (shape: {df.shape}) ---\n")
                f.write(df.head(10).to_string() + "\n")
    else:
        f.write("File not found!\n")

print("Done fast inspecting!")
