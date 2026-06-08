import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "gtc_plus_return_vols.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="Data")
    df['clean_prov'] = df['Tỉnh'].apply(lambda x: str(x).strip().replace('Khánh Hoà', 'Khánh Hòa').replace('Đắc Nông', 'Đắk Nông'))
    df['date'] = pd.to_datetime(df['Time'].apply(lambda x: str(x).split(' - ')[0]), errors='coerce')
    
    # Parse percentage strings to float if needed
    for col in ['% Gán', '% GTC', '% Chuyển trả']:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.replace('%', '', regex=False).str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce') / 100.0
            
    df['gtc_vol'] = df['Volume'] * df['% GTC']
    df['return_vol'] = df['Volume'] * df['% Chuyển trả']
    df['gtc_plus_return'] = df['gtc_vol'] + df['return_vol']
    df['assigned_vol'] = df['Volume'] * df['% Gán']
    
    # WTD (2026-06-01 to 2026-06-07)
    df_wtd = df[(df['date'] >= '2026-06-01') & (df['date'] <= '2026-06-07')]
    f.write("GTC + Return Volume by Province for WTD:\n")
    f.write(df_wtd.groupby('clean_prov')['gtc_plus_return'].sum().reset_index().to_string() + "\n")
    f.write(f"Total WTD: {df_wtd['gtc_plus_return'].sum()}\n\n")
    
    # Daily: D, D-1, D-2, D-7
    for label, d_str in [('D (2026-06-07)', '2026-06-07'), 
                         ('D-1 (2026-06-06)', '2026-06-06'), 
                         ('D-2 (2026-06-05)', '2026-06-05'), 
                         ('D-7 (2026-05-31)', '2026-05-31')]:
        df_d = df[df['date'] == d_str]
        f.write(f"GTC + Return Volume for {label}:\n")
        f.write(df_d.groupby('clean_prov')['gtc_plus_return'].sum().reset_index().to_string() + "\n")
        f.write(f"Total for {label}: {df_d['gtc_plus_return'].sum()}\n\n")

print("Done calculate_gtc_plus_return.")
