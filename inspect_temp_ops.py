import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "temp_ops_check.xlsx")
output_path = os.path.join(workspace_dir, "inspect_temp_ops_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    if not os.path.exists(file_path):
        f.write("File not found\n")
    else:
        xls = pd.ExcelFile(file_path)
        f.write(f"Sheets: {xls.sheet_names}\n\n")
        for sheet_name in xls.sheet_names:
            try:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                non_null = df.dropna(how='all')
                f.write(f"Sheet '{sheet_name}': shape={df.shape}, non_empty={len(non_null)}\n")
                if len(non_null) > 0:
                    f.write(f"  Columns: {list(df.columns)}\n")
                    f.write("  First 2 rows:\n")
                    f.write(non_null.head(2).to_string() + "\n")
            except Exception as e:
                f.write(f"Error reading {sheet_name}: {e}\n")

print("Done writing inspect_temp_ops_res.txt")
