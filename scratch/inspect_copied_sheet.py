import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "vols_tao_don.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "inspect_copied_sheet_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    f.write("Opening vols_tao_don.xlsx...\n")
    xls = pd.ExcelFile(file_path)
    f.write(f"Sheets: {xls.sheet_names}\n\n")
    
    for sheet_name in xls.sheet_names:
        f.write(f"=== Sheet: {sheet_name} ===\n")
        df = pd.read_excel(xls, sheet_name=sheet_name)
        f.write(f"Shape: {df.shape}\n")
        f.write(f"Columns: {list(df.columns)}\n\n")
        f.write("First 3 rows:\n")
        f.write(df.head(3).to_string() + "\n\n")
        
        # Let's inspect specific columns
        if 'Ngay' in df.columns or 'ngay' in df.columns or 'Ngày' in df.columns:
            date_col = [c for c in df.columns if str(c).lower() in ['ngay', 'ngày']][0]
            f.write(f"Unique dates in '{date_col}': {list(df[date_col].unique()[:15])}\n\n")
            
        if 'Tỉnh' in df.columns or 'tinh' in df.columns:
            tinh_col = [c for c in df.columns if str(c).lower() in ['tỉnh', 'tinh']][0]
            f.write(f"Unique provinces in '{tinh_col}': {list(df[tinh_col].unique())}\n\n")
            
print("Done writing inspect_copied_sheet_res.txt")
