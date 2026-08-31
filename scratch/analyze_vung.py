import pandas as pd
import os

path = "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx"
out_path = "scratch/analyze_vung_out.txt"

with open(out_path, "w", encoding="utf-8") as f:
    f.write("=== ANALYSIS OF REGION DATA ===\n")
    xls = pd.ExcelFile(path)
    
    # 1. Inspect Data sheet
    if 'Data' in xls.sheet_names:
        df_data = pd.read_excel(xls, sheet_name='Data')
        f.write(f"\n--- Data Sheet (shape: {df_data.shape}) ---\n")
        f.write(f"Unique Times: {df_data['Time'].unique().tolist()}\n")
        f.write(f"Unique Provinces (Tỉnh): {df_data['Tỉnh'].unique().tolist()}\n")
        f.write(f"Unique Vùng: {df_data['Vùng'].unique().tolist()}\n")
        f.write(f"Unique AMs: {df_data['AM'].unique().tolist()}\n")
        f.write(f"Unique Cấp Quản Lý: {df_data['Cấp Quản Lý'].unique().tolist()[:10]}\n")
        f.write(f"Unique Loại Hàng: {df_data['Loại Hàng'].unique().tolist()}\n")
    
    # 2. Inspect DataLTC sheet
    if 'DataLTC' in xls.sheet_names:
        df_ltc = pd.read_excel(xls, sheet_name='DataLTC')
        f.write(f"\n--- DataLTC Sheet (shape: {df_ltc.shape}) ---\n")
        f.write(f"Columns: {df_ltc.columns.tolist()}\n")
        f.write(f"Unique Times: {df_ltc['Time'].unique().tolist()}\n")
        f.write(f"Unique AMs: {df_ltc['AM'].unique().tolist()}\n")
        f.write(f"Unique Cấp quản lý: {df_ltc['Cấp quản lý'].unique().tolist()[:10]}\n")
        
    # 3. Inspect ODR TTS or ODR sheets if any
    for name in ['ODR TTS', 'raw', 'TTS']:
        if name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=name)
            f.write(f"\n--- Sheet {name} (shape: {df.shape}) ---\n")
            f.write(f"Columns: {df.columns.tolist()}\n")
            f.write(f"Head:\n{df.head(2).to_string()}\n")
            
print("Done writing analyze_vung.py!")
