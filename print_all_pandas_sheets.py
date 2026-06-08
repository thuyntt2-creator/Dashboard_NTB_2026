import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "print_all_pandas_sheets_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    if not os.path.exists(file_path):
        f.write("File not found\n")
    else:
        xls = pd.ExcelFile(file_path)
        f.write(f"Sheets: {xls.sheet_names}\n\n")
        for sheet_name in xls.sheet_names:
            try:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                f.write(f"Sheet '{sheet_name}': shape={df.shape}\n")
                f.write(f"  Columns: {list(df.columns)}\n")
                # check if there are non-empty values
                non_null = df.dropna(how='all')
                f.write(f"  Rows after dropna(how='all'): {len(non_null)}\n")
                if len(non_null) > 0:
                    f.write("  First 3 rows:\n")
                    f.write(non_null.head(3).to_string() + "\n")
                f.write("-" * 50 + "\n")
            except Exception as e:
                f.write(f"Error reading {sheet_name}: {e}\n")

print("Done writing print_all_pandas_sheets_res.txt")
