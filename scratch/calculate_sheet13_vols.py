import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "sheet13_vols_match.txt")

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="Sheet13")
    f.write(f"Sheet13 columns: {list(df.columns)}, total rows: {len(df)}\n")
    
    # Check date column
    # If the sheet doesn't have Tỉnh column, let's map it from Cơ cấu or Chi tiết
    # Let's map Tỉnh from Chi tiết
    # We can extract the province name from 'Chi tiết' or map via Cơ cấu sheet.
    df_cc = pd.read_excel(file_path, sheet_name="Cơ cấu")
    bc_to_prov = {}
    for _, r in df_cc.iterrows():
        bc = str(r.get('BC', '')).strip().lower()
        buucuc = str(r.get('Bưu cục', '')).strip().lower()
        prov = str(r.get('Tỉnh', '')).strip()
        if prov == 'Bình Phước':
            prov = 'Lâm Đồng'
        if bc and bc != 'nan':
            bc_to_prov[bc] = prov
        if buucuc and buucuc != 'nan':
            bc_to_prov[buucuc] = prov
            
    df['clean_bc'] = df['Chi tiết'].astype(str).str.strip().str.lower()
    df['Tỉnh_mapped'] = df['clean_bc'].map(bc_to_prov)
    
    # Fallback using suffix in Chi tiết (e.g. "Lâm Đồng")
    provinces = ['Lâm Đồng', 'Khánh Hòa', 'Bình Thuận', 'Ninh Thuận', 'Đắk Nông']
    def get_prov(row):
        p = row['Tỉnh_mapped']
        if pd.notna(p) and p != "Không xác định":
            return p
        ct = str(row['Chi tiết']).strip()
        for prov in provinces:
            if prov.lower() in ct.lower():
                return prov
        if "đắc nông" in ct.lower():
            return "Đắk Nông"
        if "khánh hoà" in ct.lower():
            return "Khánh Hòa"
        return "Không xác định"
        
    df['Tỉnh'] = df.apply(get_prov, axis=1)
    
    df['date_str'] = df['Time'].apply(lambda x: str(x).split(' - ')[0])
    df['date'] = pd.to_datetime(df['date_str'], errors='coerce')
    df['gtc_vol'] = df['Volume'] * df['% GTC']
    
    # Calculate for WTD (2026-06-01 to 2026-06-07)
    df_wtd = df[(df['date'] >= '2026-06-01') & (df['date'] <= '2026-06-07')]
    f.write("\nSum of Volume by Province for WTD:\n")
    f.write(df_wtd.groupby('Tỉnh')['Volume'].sum().reset_index().to_string() + "\n")
    f.write("\nSum of GTC Delivered Volume by Province for WTD:\n")
    f.write(df_wtd.groupby('Tỉnh')['gtc_vol'].sum().reset_index().to_string() + "\n")
    
    # Single days: D, D-1, D-2, D-7
    for label, d_str in [('D (2026-06-07)', '2026-06-07'), 
                         ('D-1 (2026-06-06)', '2026-06-06'), 
                         ('D-2 (2026-06-05)', '2026-06-05'), 
                         ('D-7 (2026-05-31)', '2026-05-31')]:
        df_d = df[df['date'] == d_str]
        f.write(f"\nSum of Volume for {label}:\n")
        f.write(df_d.groupby('Tỉnh')['Volume'].sum().reset_index().to_string() + "\n")
        f.write(f"Sum of GTC Delivered Volume for {label}:\n")
        f.write(df_d.groupby('Tỉnh')['gtc_vol'].sum().reset_index().to_string() + "\n")

print("Sheet13 calculations completed.")
