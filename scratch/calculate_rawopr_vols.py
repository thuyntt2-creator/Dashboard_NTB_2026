import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "OPR TTS.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "calculate_rawopr_vols_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="rawopr")
    f.write(f"rawopr Columns: {list(df.columns)}\n")
    f.write(f"rawopr Shape: {df.shape}\n")
    
    df['date'] = pd.to_datetime(df['NgayLTC'], errors='coerce')
    df['vol'] = pd.to_numeric(df['vol_ltc'], errors='coerce').fillna(0)
    
    # Filter for NTB vung
    # Let's check if the 'vung' column exists
    if 'vung' in df.columns:
        df_ntb = df[df['vung'] == 'NTB'].copy()
    else:
        df_ntb = df.copy()
        
    f.write(f"NTB rows: {len(df_ntb)}\n")
    
    # Let's calculate for WTD (2026-06-01 to 2026-06-07)
    df_wtd = df_ntb[(df_ntb['date'] >= '2026-06-01') & (df_ntb['date'] <= '2026-06-07')]
    f.write("\nNTB WTD (2026-06-01 to 2026-06-07) Volume by tutinh:\n")
    f.write(df_wtd.groupby('tutinh')['vol'].sum().reset_index().to_string() + "\n")
    f.write(f"Total NTB WTD: {df_wtd['vol'].sum()}\n\n")
    
    # NTB WTD-1 (2026-05-25 to 2026-05-31)
    df_wtd1 = df_ntb[(df_ntb['date'] >= '2026-05-25') & (df_ntb['date'] <= '2026-05-31')]
    f.write("NTB WTD-1 (2026-05-25 to 2026-05-31) Volume by tutinh:\n")
    f.write(df_wtd1.groupby('tutinh')['vol'].sum().reset_index().to_string() + "\n")
    f.write(f"Total NTB WTD-1: {df_wtd1['vol'].sum()}\n\n")
    
    # NTB WTD-2 (2026-05-18 to 2026-05-24)
    df_wtd2 = df_ntb[(df_ntb['date'] >= '2026-05-18') & (df_ntb['date'] <= '2026-05-24')]
    f.write("NTB WTD-2 (2026-05-18 to 2026-05-24) Volume by tutinh:\n")
    f.write(df_wtd2.groupby('tutinh')['vol'].sum().reset_index().to_string() + "\n")
    f.write(f"Total NTB WTD-2: {df_wtd2['vol'].sum()}\n\n")
    
    # Daily: D, D-1, D-2, D-7
    for label, d_str in [('D (2026-06-07)', '2026-06-07'), 
                         ('D-1 (2026-06-06)', '2026-06-06'), 
                         ('D-2 (2026-06-05)', '2026-06-05'), 
                         ('D-7 (2026-05-31)', '2026-05-31')]:
        df_d = df_ntb[df_ntb['date'] == d_str]
        f.write(f"NTB {label} Volume by tutinh:\n")
        f.write(df_d.groupby('tutinh')['vol'].sum().reset_index().to_string() + "\n")
        f.write(f"Total NTB {label}: {df_d['vol'].sum()}\n\n")

print("Done calculate_rawopr_vols.")
