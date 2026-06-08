import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "calculate_wtd_vols_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="Data")
    f.write(f"Total rows: {len(df)}\n")
    f.write(f"Unique times in Data: {list(df['Time'].unique()[:15])}\n")

    # Let's parse dates
    # Time column has values like '2026-06-07 - Chủ Nhật'
    # Let's extract the date part (yyyy-mm-dd)
    df['date_str'] = df['Time'].apply(lambda x: str(x).split(' - ')[0])
    df['date'] = pd.to_datetime(df['date_str'], errors='coerce')

    # Let's filter for WTD: Monday 2026-06-01 to Sunday 2026-06-07
    df_wtd = df[(df['date'] >= '2026-06-01') & (df['date'] <= '2026-06-07')]
    f.write(f"WTD rows: {len(df_wtd)}\n")

    # Sum volume by Province (Tỉnh)
    prov_wtd = df_wtd.groupby('Tỉnh')['Volume'].sum().reset_index()
    f.write("\nSum of Volume by Province for WTD (2026-06-01 to 2026-06-07):\n")
    f.write(prov_wtd.to_string() + "\n")

    # Let's check for WTD-1: Monday 2026-05-25 to Sunday 2026-05-31
    df_wtd_1 = df[(df['date'] >= '2026-05-25') & (df['date'] <= '2026-05-31')]
    prov_wtd_1 = df_wtd_1.groupby('Tỉnh')['Volume'].sum().reset_index()
    f.write("\nSum of Volume by Province for WTD-1 (2026-05-25 to 2026-05-31):\n")
    f.write(prov_wtd_1.to_string() + "\n")

    # Let's check for WTD-2: Monday 2026-05-18 to Sunday 2026-05-24
    df_wtd_2 = df[(df['date'] >= '2026-05-18') & (df['date'] <= '2026-05-24')]
    prov_wtd_2 = df_wtd_2.groupby('Tỉnh')['Volume'].sum().reset_index()
    f.write("\nSum of Volume by Province for WTD-2 (2026-05-18 to 2026-05-24):\n")
    f.write(prov_wtd_2.to_string() + "\n")

print("Done writing calculate_wtd_vols_res.txt")
