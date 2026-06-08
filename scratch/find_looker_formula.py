import pandas as pd
import os
import numpy as np

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"

targets_d = {
    'Bình Thuận': 10371,
    'Khánh Hòa': 11517,
    'Lâm Đồng': 9190,
    'Ninh Thuận': 3725,
    'Đắk Nông': 4764
}

targets_d1 = {
    'Bình Thuận': 18143,
    'Khánh Hòa': 19228,
    'Lâm Đồng': 14658,
    'Ninh Thuận': 6249,
    'Đắk Nông': 7409
}

def clean_province(p):
    p = str(p).strip()
    if p == 'Đắc Nông':
        return 'Đắk Nông'
    if p == 'Khánh Hoà':
        return 'Khánh Hòa'
    return p

# We will load Data, DataLTC, and Sheet13 from Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
xls = pd.ExcelFile(file_path)

with open(os.path.join(workspace_dir, "scratch", "find_looker_formula_res.txt"), "w", encoding="utf-8") as out:
    for sheet in ['Data', 'DataLTC', 'Sheet13']:
        if sheet in xls.sheet_names:
            out.write(f"\n================= SHEET: {sheet} =================\n")
            df = pd.read_excel(xls, sheet_name=sheet)
            
            # Find province column
            prov_col = None
            for c in df.columns:
                if 'tỉnh' in c.lower() or 'cấp quản lý' in c.lower():
                    prov_col = c
                    break
            if not prov_col:
                # try to map via a dictionary if Chi tiết is present
                continue
                
            # Find time column
            time_col = None
            for c in df.columns:
                if 'time' in c.lower() or 'ngay' in c.lower():
                    time_col = c
                    break
            if not time_col:
                continue
                
            # Add clean province and date
            if 'cấp quản lý' in prov_col.lower():
                df['clean_prov'] = df[prov_col].apply(lambda x: str(x).split(' - ')[1].strip() if ' - ' in str(x) else str(x).strip())
            else:
                df['clean_prov'] = df[prov_col].apply(clean_province)
                
            df['date'] = pd.to_datetime(df[time_col].apply(lambda x: str(x).split(' - ')[0]), errors='coerce')
            
            # Get numeric columns and percentage columns
            num_cols = []
            pct_cols = []
            for c in df.columns:
                if c in ['clean_prov', 'date', prov_col, time_col]:
                    continue
                # check if numeric
                dtype = df[c].dtype
                if np.issubdtype(dtype, np.number):
                    num_cols.append(c)
                else:
                    # check if it contains percentage strings
                    sample = df[c].dropna().head(10).astype(str)
                    if sample.str.contains('%').any():
                        pct_cols.append(c)
                        # convert to float
                        df[c+'_float'] = df[c].astype(str).str.replace('%', '', regex=False).str.replace(',', '.', regex=False)
                        df[c+'_float'] = pd.to_numeric(df[c+'_float'], errors='coerce') / 100.0
                        num_cols.append(c+'_float')
            
            out.write(f"Numeric columns: {num_cols}\n")
            
            # Let's test different calculations for D (2026-06-07) and D-1 (2026-06-06)
            df_d = df[df['date'] == '2026-06-07']
            df_d1 = df[df['date'] == '2026-06-06']
            
            # 1. Single column sum
            for c in num_cols:
                sum_d = df_d.groupby('clean_prov')[c].sum().to_dict()
                sum_d1 = df_d1.groupby('clean_prov')[c].sum().to_dict()
                
                # check match
                match_d = all(abs(sum_d.get(p, 0) - val) < 5 for p, val in targets_d.items())
                match_d1 = all(abs(sum_d1.get(p, 0) - val) < 5 for p, val in targets_d1.items())
                
                if match_d or match_d1:
                    out.write(f"MATCH found in single column '{c}':\n")
                    out.write(f"  D matches? {match_d} (Bình Thuận: {sum_d.get('Bình Thuận')}, Khánh Hòa: {sum_d.get('Khánh Hòa')})\n")
                    out.write(f"  D-1 matches? {match_d1} (Bình Thuận: {sum_d1.get('Bình Thuận')}, Khánh Hòa: {sum_d1.get('Khánh Hòa')})\n")
            
            # 2. Product of two columns (e.g. Volume * % GTC)
            for c1 in num_cols:
                for c2 in num_cols:
                    if c1 == c2:
                        continue
                    df_d['prod'] = df_d[c1] * df_d[c2]
                    df_d1['prod'] = df_d1[c1] * df_d1[c2]
                    
                    sum_d = df_d.groupby('clean_prov')['prod'].sum().to_dict()
                    sum_d1 = df_d1.groupby('clean_prov')['prod'].sum().to_dict()
                    
                    match_d = all(abs(sum_d.get(p, 0) - val) < 5 for p, val in targets_d.items())
                    match_d1 = all(abs(sum_d1.get(p, 0) - val) < 5 for p, val in targets_d1.items())
                    
                    if match_d or match_d1:
                        out.write(f"MATCH found in product '{c1} * {c2}':\n")
                        out.write(f"  D matches? {match_d} (Bình Thuận: {sum_d.get('Bình Thuận')}, Khánh Hòa: {sum_d.get('Khánh Hòa')})\n")
                        out.write(f"  D-1 matches? {match_d1} (Bình Thuận: {sum_d1.get('Bình Thuận')}, Khánh Hòa: {sum_d1.get('Khánh Hòa')})\n")

print("Done searching for looker formulas.")
