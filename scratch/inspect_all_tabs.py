import openpyxl
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = "scratch/downloaded_sheets.xlsx"
wb = openpyxl.load_workbook(file_path, read_only=True)

with open("scratch/all_tabs_details.txt", "w", encoding="utf-8") as f:
    f.write(f"Workbook tabs inspection: {file_path}\n")
    f.write("=" * 60 + "\n\n")
    
    for name in wb.sheetnames:
        f.write(f"Tab Name: {name}\n")
        f.write("-" * 40 + "\n")
        try:
            # Load sheet with pandas (first 5 rows only to be fast and safe)
            df_head = pd.read_excel(file_path, sheet_name=name, nrows=5)
            # Load full shape by reading only index/columns if possible, or just shape
            df_full = pd.read_excel(file_path, sheet_name=name)
            
            f.write(f"Shape: {df_full.shape}\n")
            f.write(f"Columns: {list(df_full.columns)}\n")
            f.write("\nFirst 5 rows:\n")
            f.write(df_head.to_string())
            f.write("\n\n" + "=" * 60 + "\n\n")
            print(f"Tab '{name}' processed. Shape: {df_full.shape}")
        except Exception as e:
            f.write(f"Error reading tab {name}: {e}\n\n")
            print(f"Error reading tab '{name}': {e}")
            
print("Done writing scratch/all_tabs_details.txt")
