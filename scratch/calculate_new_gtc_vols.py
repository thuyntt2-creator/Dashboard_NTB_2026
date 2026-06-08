import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "new_gtc_wtd_vols.txt")

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="Data")
    df['date_str'] = df['Time'].apply(lambda x: str(x).split(' - ')[0])
    df['date'] = pd.to_datetime(df['date_str'], errors='coerce')
    df['gtc_vol'] = df['Volume'] * df['% GTC']
    
    # Filter for new orders only
    df_new = df[df['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])]
    
    # WTD (2026-06-01 to 2026-06-07)
    df_wtd = df_new[(df_new['date'] >= '2026-06-01') & (df_new['date'] <= '2026-06-07')]
    f.write("New Orders GTC Delivered Volume by Province for WTD:\n")
    f.write(df_wtd.groupby('Tỉnh')['gtc_vol'].sum().reset_index().to_string() + "\n")
    f.write(f"Total: {df_wtd['gtc_vol'].sum()}\n")
    
    # Days
    for label, d_str in [('D (2026-06-07)', '2026-06-07'), 
                         ('D-1 (2026-06-06)', '2026-06-06'), 
                         ('D-2 (2026-06-05)', '2026-06-05'), 
                         ('D-7 (2026-05-31)', '2026-05-31')]:
        df_d = df_new[df_new['date'] == d_str]
        f.write(f"\nNew Orders GTC Delivered Volume for {label}:\n")
        f.write(df_d.groupby('Tỉnh')['gtc_vol'].sum().reset_index().to_string() + "\n")
        f.write(f"Total: {df_d['gtc_vol'].sum()}\n")

print("New orders calculation completed.")
