import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "vols_tao_don.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "po_growth_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="shopee_tiktok")
    df['Date'] = pd.to_datetime(df['Date'])
    latest_date = df['Date'].max()
    d7_date = latest_date - pd.Timedelta(days=7)
    
    f.write(f"Latest Date D: {latest_date}\n")
    f.write(f"Date D-7: {d7_date}\n\n")
    
    # Exclude 'BC Cũ/Không thuộc ĐCL' if needed
    df_filtered = df[df['bat_on'].fillna('').str.strip() != 'BC Cũ/Không thuộc ĐCL'].copy()
    
    # Calculate volume for D and D-7
    vol_d = df_filtered[df_filtered['Date'] == latest_date].groupby('Bưu cục')['Volume'].sum().reset_index(name='vol_d')
    vol_d7 = df_filtered[df_filtered['Date'] == d7_date].groupby('Bưu cục')['Volume'].sum().reset_index(name='vol_d7')
    
    merged = pd.merge(vol_d, vol_d7, on='Bưu cục', how='outer').fillna(0)
    merged['growth_abs'] = merged['vol_d'] - merged['vol_d7']
    merged['growth_pct'] = (merged['vol_d'] - merged['vol_d7']) / merged['vol_d7'] * 100
    merged.loc[merged['vol_d7'] == 0, 'growth_pct'] = 0.0
    
    f.write("=== Top 10 by Absolute Growth (vol_d - vol_d7) ===\n")
    f.write(merged.sort_values(by='growth_abs', ascending=False).head(15).to_string(index=False) + "\n\n")
    
    f.write("=== Top 10 by Percent Growth (vol_d - vol_d7) / vol_d7 ===\n")
    f.write(merged[merged['vol_d7'] >= 10].sort_values(by='growth_pct', ascending=False).head(15).to_string(index=False) + "\n\n")
    
    f.write("=== Specific check for the post offices shown in screenshot ===\n")
    pos_to_check = [
        "Bưu Cục 111 Lê Duẫn-Khánh Sơn-Khánh Hoà",
        "Bưu Cục Tổ Dân Phố 2-Ninh Hoà-Khánh Hoà",
        "Bưu cục DT707-Hàm Thuận Nam-Bình Thuận",
        "Bưu Cục Số 6 Trường Chinh-Phan Rang-Ninh Thuận",
        "Bưu Cục Thôn Long Điền-Chợ Lầu-Bình Thuận",
        "Bưu Cục 21 Trần Hưng Đạo-Cam Ranh-Khánh Hòa"
    ]
    for po in pos_to_check:
        row = merged[merged['Bưu cục'] == po]
        if not row.empty:
            f.write(row.to_string(index=False) + "\n")
        else:
            f.write(f"Not found: {po}\n")

print("Done writing scratch/po_growth_res.txt")
