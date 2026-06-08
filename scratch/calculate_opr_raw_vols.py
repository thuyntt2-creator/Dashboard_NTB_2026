import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "OPR TTS.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "calculate_opr_raw_vols_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    # Load CoCauVung mapping
    df_cc = pd.read_excel(file_path, sheet_name="CoCauVung")
    bc_to_prov = {}
    for _, r in df_cc.iterrows():
        bc = str(r.get('Bưu cục', '')).strip().lower()
        prov = str(r.get('Tỉnh', '')).strip()
        if bc:
            bc_to_prov[bc] = prov
            
    # Load RAW n-1 sheet
    df = pd.read_excel(file_path, sheet_name="RAW n-1")
    f.write(f"RAW n-1 Columns: {list(df.columns)}\n")
    f.write(f"RAW n-1 Shape: {df.shape}\n")
    
    # Map province
    df['clean_bc'] = df['BC lấy'].astype(str).str.strip().str.lower()
    df['Tỉnh'] = df['clean_bc'].map(bc_to_prov)
    
    # Fallback to suffix search
    provinces = ['Lâm Đồng', 'Khánh Hòa', 'Bình Thuận', 'Ninh Thuận', 'Đắk Nông']
    def get_prov_fallback(row):
        p = row['Tỉnh']
        if pd.notna(p):
            return p
        bc = str(row['BC lấy']).strip()
        for prov in provinces:
            if prov.lower() in bc.lower():
                return prov
        if "đắc nông" in bc.lower():
            return "Đắk Nông"
        if "khánh hoà" in bc.lower():
            return "Khánh Hòa"
        return "Không xác định"
        
    df['Tỉnh_clean'] = df.apply(get_prov_fallback, axis=1)
    
    # Parse creation date
    df['date'] = pd.to_datetime(df['Thời gian tạo'], errors='coerce').dt.date
    
    # Calculate for WTD (2026-06-01 to 2026-06-07)
    df_wtd = df[(df['date'] >= pd.to_datetime('2026-06-01').date()) & (df['date'] <= pd.to_datetime('2026-06-07').date())]
    f.write("\nOrder Count by Province for WTD (2026-06-01 to 2026-06-07):\n")
    f.write(df_wtd.groupby('Tỉnh_clean').size().reset_index(name='count').to_string() + "\n")
    f.write(f"Total WTD: {len(df_wtd)}\n\n")
    
    # Daily: D, D-1, D-2, D-7
    for label, d_str in [('D (2026-06-07)', '2026-06-07'), 
                         ('D-1 (2026-06-06)', '2026-06-06'), 
                         ('D-2 (2026-06-05)', '2026-06-05'), 
                         ('D-7 (2026-05-31)', '2026-05-31')]:
        df_d = df[df['date'] == pd.to_datetime(d_str).date()]
        f.write(f"Order Count for {label}:\n")
        f.write(df_d.groupby('Tỉnh_clean').size().reset_index(name='count').to_string() + "\n")
        f.write(f"Total {label}: {len(df_d)}\n\n")
        
    # Check WTD-1 and WTD-2
    df_wtd1 = df[(df['date'] >= pd.to_datetime('2026-05-25').date()) & (df['date'] <= pd.to_datetime('2026-05-31').date())]
    f.write("Order Count by Province for WTD-1 (2026-05-25 to 2026-05-31):\n")
    f.write(df_wtd1.groupby('Tỉnh_clean').size().reset_index(name='count').to_string() + "\n")
    f.write(f"Total WTD-1: {len(df_wtd1)}\n\n")
    
    df_wtd2 = df[(df['date'] >= pd.to_datetime('2026-05-18').date()) & (df['date'] <= pd.to_datetime('2026-05-24').date())]
    f.write("Order Count by Province for WTD-2 (2026-05-18 to 2026-05-24):\n")
    f.write(df_wtd2.groupby('Tỉnh_clean').size().reset_index(name='count').to_string() + "\n")
    f.write(f"Total WTD-2: {len(df_wtd2)}\n\n")

print("Done calculate_opr_raw_vols.")
