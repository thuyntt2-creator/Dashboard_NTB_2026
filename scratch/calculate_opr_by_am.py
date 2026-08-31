import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
user_file = os.path.join(workspace_dir, "downloaded_user_sheet.xlsx")
output_file = os.path.join(workspace_dir, "scratch", "calculate_opr_by_am_res.txt")

with open(output_file, "w", encoding="utf-8") as f:
    xls = pd.ExcelFile(user_file)
    
    # 1. Load sheets
    df_opr = pd.read_excel(xls, sheet_name="OPR TTS")
    df_cocau = pd.read_excel(xls, sheet_name="cocau")
    
    f.write(f"OPR TTS shape: {df_opr.shape}\n")
    f.write(f"cocau shape: {df_cocau.shape}\n\n")
    
    # 2. Map AM using cocau
    # Create mapping dict from cocau: Bưu cục -> Am, and BC -> Am
    mapping_buucuc = dict(zip(df_cocau['Bưu cục'].str.strip(), df_cocau['Am'].str.strip()))
    mapping_bc = dict(zip(df_cocau['BC'].str.strip(), df_cocau['Am'].str.strip()))
    
    # Let's clean OPR TTS kholay
    df_opr['kholay_clean'] = df_opr['kholay'].astype(str).str.strip()
    
    # Match using Bưu cục first, then BC
    df_opr['mapped_AM'] = df_opr['kholay_clean'].map(mapping_buucuc)
    unmapped = df_opr[df_opr['mapped_AM'].isna()]
    f.write(f"Rows unmapped after first pass: {len(unmapped)}\n")
    
    if len(unmapped) > 0:
        # Try mapping using BC
        df_opr.loc[df_opr['mapped_AM'].isna(), 'mapped_AM'] = df_opr.loc[df_opr['mapped_AM'].isna(), 'kholay_clean'].map(mapping_bc)
        unmapped_2 = df_opr[df_opr['mapped_AM'].isna()]
        f.write(f"Rows unmapped after second pass: {len(unmapped_2)}\n")
        if len(unmapped_2) > 0:
            f.write(f"Sample unmapped kholay values: {unmapped_2['kholay_clean'].unique()[:10].tolist()}\n")
            
    # Clean numeric columns
    df_opr['vol_ltc'] = pd.to_numeric(df_opr['vol_ltc'], errors='coerce').fillna(0)
    df_opr['ot'] = pd.to_numeric(df_opr['ot'], errors='coerce').fillna(0)
    
    # 3. Calculate OPR by week, AM, and Khung giờ
    f.write("\nUnique weeks in OPR TTS: " + str(df_opr['Tuần'].unique().tolist()) + "\n")
    f.write("Unique Khung giờ in OPR TTS: " + str(df_opr['Khung giờ'].unique().tolist()) + "\n")
    f.write("Unique khung_gio_tao_don in OPR TTS: " + str(df_opr['khung_gio_tao_don'].unique().tolist()) + "\n\n")
    
    for week in sorted(df_opr['Tuần'].dropna().unique()):
        f.write(f"=========================================\nWEEK: {week}\n=========================================\n")
        df_w = df_opr[df_opr['Tuần'] == week]
        
        # Group by mapped_AM and Khung giờ
        grouped = df_w.groupby(['mapped_AM', 'Khung giờ']).agg(
            total_vol=('vol_ltc', 'sum'),
            ot_vol=('ot', 'sum')
        ).reset_index()
        
        grouped['%OPR'] = (grouped['ot_vol'] / grouped['total_vol']).fillna(0)
        f.write("\nGrouping by mapped_AM and Khung giờ:\n")
        f.write(grouped.to_string(index=False) + "\n\n")
        
        # Group by mapped_AM and khung_gio_tao_don
        grouped_detail = df_w.groupby(['mapped_AM', 'khung_gio_tao_don']).agg(
            total_vol=('vol_ltc', 'sum'),
            ot_vol=('ot', 'sum')
        ).reset_index()
        
        grouped_detail['%OPR'] = (grouped_detail['ot_vol'] / grouped_detail['total_vol']).fillna(0)
        f.write("\nGrouping by mapped_AM and khung_gio_tao_don:\n")
        f.write(grouped_detail.to_string(index=False) + "\n\n")
