import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "new_assigned_vols_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="Data")
    df['clean_prov'] = df['Tỉnh'].apply(lambda x: str(x).strip().replace('Khánh Hoà', 'Khánh Hòa').replace('Đắc Nông', 'Đắk Nông'))
    df['date'] = pd.to_datetime(df['Time'].apply(lambda x: str(x).split(' - ')[0]), errors='coerce')
    
    # Parse percentage strings to float if needed
    for col in ['% Gán', '% GTC']:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.replace('%', '', regex=False).str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce') / 100.0
            
    df['assigned_vol'] = df['Volume'] * df['% Gán']
    
    # Filter for new orders (Loại Hàng == 'Hàng Mới Ca 1' or 'Hàng Mới Ca 2')
    df_new = df[df['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])].copy()
    
    # WTD (2026-06-01 to 2026-06-07)
    df_wtd = df_new[(df_new['date'] >= '2026-06-01') & (df_new['date'] <= '2026-06-07')]
    f.write("New Orders Assigned Volume by Province for WTD:\n")
    f.write(df_wtd.groupby('clean_prov')['assigned_vol'].sum().reset_index().to_string() + "\n")
    f.write(f"Total: {df_wtd['assigned_vol'].sum()}\n\n")
    
    # Daily: D, D-1, D-2, D-7
    for label, d_str in [('D (2026-06-07)', '2026-06-07'), 
                         ('D-1 (2026-06-06)', '2026-06-06'), 
                         ('D-2 (2026-06-05)', '2026-06-05'), 
                         ('D-7 (2026-05-31)', '2026-05-31')]:
        df_d = df_new[df_new['date'] == d_str]
        f.write(f"New Orders Assigned Volume for {label}:\n")
        f.write(df_d.groupby('clean_prov')['assigned_vol'].sum().reset_index().to_string() + "\n")
        f.write(f"Total: {df_d['assigned_vol'].sum()}\n\n")

print("Done calculate_new_assigned_vols.")
