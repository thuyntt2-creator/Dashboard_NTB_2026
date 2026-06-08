import os
import openpyxl
import pandas as pd

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
output_path = os.path.join(workspace_dir, "scratch", "all_workbooks_detailed.txt")

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    for filename in os.listdir(workspace_dir):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(workspace_dir, filename)
            f.write(f"\n=========================================\n")
            f.write(f"Workbook: {filename}\n")
            f.write(f"=========================================\n")
            try:
                xls = pd.ExcelFile(file_path)
                f.write(f"Sheet names: {xls.sheet_names}\n")
                for s in xls.sheet_names:
                    try:
                        # Load first 2 rows to get columns and check if empty
                        df = pd.read_excel(xls, sheet_name=s, nrows=2)
                        f.write(f"  Sheet '{s}': columns={list(df.columns)}, shape={df.shape}\n")
                    except Exception as ex:
                        f.write(f"  Sheet '{s}': Error reading columns: {ex}\n")
            except Exception as e:
                f.write(f"Error loading workbook: {e}\n")

print("Inspection completed.")
