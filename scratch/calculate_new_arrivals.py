import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "new_arrivals_match.txt")

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="Data")
    df['date_str'] = df['Time'].apply(lambda x: str(x).split(' - ')[0])
    df['date'] = pd.to_datetime(df['date_str'], errors='coerce')
    
    # Calculate for WTD (2026-06-01 to 2026-06-07)
    df_wtd = df[(df['date'] >= '2026-06-01') & (df['date'] <= '2026-06-07')]
    prov_wtd = df_wtd.groupby('Tỉnh')['Hàng Mới Về Trong Ngày'].sum().reset_index()
    f.write("Sum of Hàng Mới Về Trong Ngày by Province for WTD (2026-06-01 to 2026-06-07):\n")
    f.write(prov_wtd.to_string() + "\n")
    f.write(f"Total: {df_wtd['Hàng Mới Về Trong Ngày'].sum()}\n")
    
    # Single days: D, D-1, D-2, D-7
    for label, d_str in [('D (2026-06-07)', '2026-06-07'), 
                         ('D-1 (2026-06-06)', '2026-06-06'), 
                         ('D-2 (2026-06-05)', '2026-06-05'), 
                         ('D-7 (2026-05-31)', '2026-05-31')]:
        df_d = df[df['date'] == d_str]
        f.write(f"\nSum of Hàng Mới Về Trong Ngày for {label}:\n")
        f.write(df_d.groupby('Tỉnh')['Hàng Mới Về Trong Ngày'].sum().reset_index().to_string() + "\n")
        f.write(f"Total: {df_d['Hàng Mới Về Trong Ngày'].sum()}\n")

print("New arrivals calculation completed.")
