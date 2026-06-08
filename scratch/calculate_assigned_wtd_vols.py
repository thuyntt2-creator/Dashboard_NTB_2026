import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "assigned_wtd_vols.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="Data")
    df['date_str'] = df['Time'].apply(lambda x: str(x).split(' - ')[0])
    df['date'] = pd.to_datetime(df['date_str'], errors='coerce')
    
    # Parse percentage strings to float if needed
    for col in ['% Gán', '% GTC']:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.replace('%', '', regex=False).str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce') / 100.0
            
    df['assigned_vol'] = df['Volume'] * df['% Gán']
    df['gtc_vol'] = df['Volume'] * df['% GTC']
    
    # WTD (2026-06-01 to 2026-06-07)
    df_wtd = df[(df['date'] >= '2026-06-01') & (df['date'] <= '2026-06-07')]
    f.write("Assigned Volume by Province for WTD (2026-06-01 to 2026-06-07):\n")
    f.write(df_wtd.groupby('Tỉnh')['assigned_vol'].sum().reset_index().to_string() + "\n")
    f.write(f"Total Assigned WTD: {df_wtd['assigned_vol'].sum()}\n\n")
    
    # Check WTD-1 (2026-05-25 to 2026-05-31) and WTD-2 (2026-05-18 to 2026-05-24)
    df_wtd1 = df[(df['date'] >= '2026-05-25') & (df['date'] <= '2026-05-31')]
    f.write("Assigned Volume by Province for WTD-1:\n")
    f.write(df_wtd1.groupby('Tỉnh')['assigned_vol'].sum().reset_index().to_string() + "\n")
    f.write(f"Total Assigned WTD-1: {df_wtd1['assigned_vol'].sum()}\n\n")
    
    df_wtd2 = df[(df['date'] >= '2026-05-18') & (df['date'] <= '2026-05-24')]
    f.write("Assigned Volume by Province for WTD-2:\n")
    f.write(df_wtd2.groupby('Tỉnh')['assigned_vol'].sum().reset_index().to_string() + "\n")
    f.write(f"Total Assigned WTD-2: {df_wtd2['assigned_vol'].sum()}\n\n")
    
    # Daily: D, D-1, D-2, D-7
    for label, d_str in [('D (2026-06-07)', '2026-06-07'), 
                         ('D-1 (2026-06-06)', '2026-06-06'), 
                         ('D-2 (2026-06-05)', '2026-06-05'), 
                         ('D-7 (2026-05-31)', '2026-05-31')]:
        df_d = df[df['date'] == d_str]
        f.write(f"Assigned Volume for {label}:\n")
        f.write(df_d.groupby('Tỉnh')['assigned_vol'].sum().reset_index().to_string() + "\n")
        f.write(f"Total Assigned for {label}: {df_d['assigned_vol'].sum()}\n\n")

print("Done calculate_assigned_wtd_vols.")
