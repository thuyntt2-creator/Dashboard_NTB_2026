import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "OPR TTS.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "calculate_sheet33_vols_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="Sheet33")
    f.write(f"Sheet33 Columns: {list(df.columns)}\n")
    f.write(f"Sheet33 Shape: {df.shape}\n")
    
    # Extract Province from Cấp Quản Lý
    def get_prov(row):
        cql = str(row['Cấp Quản Lý'])
        if " - " in cql:
            return cql.split(" - ")[1].strip()
        return cql.strip()
        
    df['Tỉnh'] = df.apply(get_prov, axis=1)
    
    # Parse date
    df['date_str'] = df['Time'].apply(lambda x: str(x).split(' - ')[0])
    df['date'] = pd.to_datetime(df['date_str'], errors='coerce')
    
    # Convert percentages
    for col in ['% Gán', '% GTC', '% Chuyển trả']:
        df[col] = df[col].astype(str).str.replace('%', '', regex=False).str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce') / 100.0
        
    df['gtc_vol'] = df['Volume'] * df['% GTC']
    
    # WTD (2026-06-01 to 2026-06-07)
    df_wtd = df[(df['date'] >= '2026-06-01') & (df['date'] <= '2026-06-07')]
    f.write("WTD Volume (2026-06-01 to 2026-06-07) by Tỉnh:\n")
    f.write(df_wtd.groupby('Tỉnh')['Volume'].sum().reset_index().to_string() + "\n")
    f.write(f"Total WTD: {df_wtd['Volume'].sum()}\n\n")
    f.write("WTD GTC Delivered Volume by Tỉnh:\n")
    f.write(df_wtd.groupby('Tỉnh')['gtc_vol'].sum().reset_index().to_string() + "\n")
    f.write(f"Total WTD GTC: {df_wtd['gtc_vol'].sum()}\n\n")
    
    # Single days: D, D-1, D-2, D-7
    for label, d_str in [('D (2026-06-07)', '2026-06-07'), 
                         ('D-1 (2026-06-06)', '2026-06-06'), 
                         ('D-2 (2026-06-05)', '2026-06-05'), 
                         ('D-7 (2026-05-31)', '2026-05-31')]:
        df_d = df[df['date'] == d_str]
        f.write(f"{label} Volume by Tỉnh:\n")
        f.write(df_d.groupby('Tỉnh')['Volume'].sum().reset_index().to_string() + "\n")
        f.write(f"Total {label}: {df_d['Volume'].sum()}\n")
        f.write(f"{label} GTC Delivered Volume by Tỉnh:\n")
        f.write(df_d.groupby('Tỉnh')['gtc_vol'].sum().reset_index().to_string() + "\n")
        f.write(f"Total {label} GTC: {df_d['gtc_vol'].sum()}\n\n")
        
    # Let's also output WTD-1 (2026-05-25 to 2026-05-31) and WTD-2 (2026-05-18 to 2026-05-24)
    df_wtd1 = df[(df['date'] >= '2026-05-25') & (df['date'] <= '2026-05-31')]
    f.write("WTD-1 Volume by Tỉnh:\n")
    f.write(df_wtd1.groupby('Tỉnh')['Volume'].sum().reset_index().to_string() + "\n")
    f.write("WTD-1 GTC Delivered Volume by Tỉnh:\n")
    f.write(df_wtd1.groupby('Tỉnh')['gtc_vol'].sum().reset_index().to_string() + "\n")
    f.write(f"Total WTD-1 Volume: {df_wtd1['Volume'].sum()}\n")
    f.write(f"Total WTD-1 GTC: {df_wtd1['gtc_vol'].sum()}\n\n")
    
    df_wtd2 = df[(df['date'] >= '2026-05-18') & (df['date'] <= '2026-05-24')]
    f.write("WTD-2 Volume by Tỉnh:\n")
    f.write(df_wtd2.groupby('Tỉnh')['Volume'].sum().reset_index().to_string() + "\n")
    f.write("WTD-2 GTC Delivered Volume by Tỉnh:\n")
    f.write(df_wtd2.groupby('Tỉnh')['gtc_vol'].sum().reset_index().to_string() + "\n")
    f.write(f"Total WTD-2 Volume: {df_wtd2['Volume'].sum()}\n")
    f.write(f"Total WTD-2 GTC: {df_wtd2['gtc_vol'].sum()}\n\n")

print("Finished calculate_sheet33_vols.")
