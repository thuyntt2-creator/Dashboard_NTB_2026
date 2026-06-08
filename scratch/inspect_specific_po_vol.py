import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "vols_tao_don.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "specific_po_vol_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="shopee_tiktok")
    df['Date'] = pd.to_datetime(df['Date'])
    latest_date = df['Date'].max()
    df_latest = df[df['Date'] == latest_date]

    f.write(f"Latest Date: {latest_date}\n\n")
    pos = ["Bưu Cục 111 Lê Duẫn-Khánh Sơn-Khánh Hoà", "Bưu Cục Tổ Dân Phố 2-Ninh Hoà-Khánh Hoà", "Bưu Cục 21 Trần Hưng Đạo-Cam Ranh-Khánh Hòa"]
    for po in pos:
        vol = df_latest[df_latest['Bưu cục'] == po]['Volume'].sum()
        f.write(f"{po}: Volume = {vol}\n")

print("Done writing scratch/specific_po_vol_res.txt")
