import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
path_ops = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "inspect_sheets_detail_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    if os.path.exists(path_ops):
        xls = pd.ExcelFile(path_ops)
        f.write(f"Sheets: {xls.sheet_names}\n")
        for sheet in xls.sheet_names:
            try:
                df = pd.read_excel(xls, sheet_name=sheet, nrows=5)
                f.write(f"\n--- Sheet: {sheet}\n")
                f.write(f"Shape of head: {df.shape}\n")
                f.write(f"Columns: {list(df.columns)}\n")
                f.write("First 2 rows:\n")
                f.write(df.head(2).to_string() + "\n")
            except Exception as e:
                f.write(f"Error reading {sheet}: {e}\n")
    else:
        f.write("BÁO CÁO VẬN HÀNH not found.\n")

print("Done writing inspect_sheets_detail_res.txt")
