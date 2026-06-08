import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "gtc_wtd_vols_match.txt")

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="Data")
    df['date_str'] = df['Time'].apply(lambda x: str(x).split(' - ')[0])
    df['date'] = pd.to_datetime(df['date_str'], errors='coerce')
    df['gtc_vol'] = df['Volume'] * df['% GTC']
    
    # Let's calculate for WTD (2026-06-01 to 2026-06-07)
    df_wtd = df[(df['date'] >= '2026-06-01') & (df['date'] <= '2026-06-07')]
    prov_wtd = df_wtd.groupby('Tỉnh')['gtc_vol'].sum().reset_index()
    f.write("Sum of GTC Delivered Volume by Province for WTD (2026-06-01 to 2026-06-07):\n")
    f.write(prov_wtd.to_string() + "\n")
    
    # WTD-1: 2026-05-25 to 2026-05-31
    df_wtd_1 = df[(df['date'] >= '2026-05-25') & (df['date'] <= '2026-05-31')]
    prov_wtd_1 = df_wtd_1.groupby('Tỉnh')['gtc_vol'].sum().reset_index()
    f.write("\nSum of GTC Delivered Volume by Province for WTD-1 (2026-05-25 to 2026-05-31):\n")
    f.write(prov_wtd_1.to_string() + "\n")
    
    # WTD-2: 2026-05-18 to 2026-05-24
    df_wtd_2 = df[(df['date'] >= '2026-05-18') & (df['date'] <= '2026-05-24')]
    prov_wtd_2 = df_wtd_2.groupby('Tỉnh')['gtc_vol'].sum().reset_index()
    f.write("\nSum of GTC Delivered Volume by Province for WTD-2 (2026-05-18 to 2026-05-24):\n")
    f.write(prov_wtd_2.to_string() + "\n")
    
    # Let's also check single days: D = 2026-06-07, D-1 = 2026-06-06, D-2 = 2026-06-05, D-7 = 2026-05-31
    for label, d_str in [('D (2026-06-07)', '2026-06-07'), 
                         ('D-1 (2026-06-06)', '2026-06-06'), 
                         ('D-2 (2026-06-05)', '2026-06-05'), 
                         ('D-7 (2026-05-31)', '2026-05-31')]:
        df_d = df[df['date'] == d_str]
        prov_d = df_d.groupby('Tỉnh')['gtc_vol'].sum().reset_index()
        f.write(f"\nSum of GTC Delivered Volume for {label}:\n")
        f.write(prov_d.to_string() + "\n")
        
print("Calculations completed.")
