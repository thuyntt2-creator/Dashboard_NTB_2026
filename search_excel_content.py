import pandas as pd
import os
import openpyxl

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"

keywords = ["WTD", "D/D-1", "D/D-7", "So sánh Volume", "WTD-1", "WTD-2"]
log_path = os.path.join(workspace_dir, "search_excel_content_res.txt")

with open(log_path, "w", encoding="utf-8") as f:
    for filename in os.listdir(workspace_dir):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(workspace_dir, filename)
            f.write(f"\nSearching file: {filename}\n")
            try:
                wb = openpyxl.load_workbook(file_path, read_only=True)
                for sheet in wb.sheetnames:
                    f.write(f"  Checking sheet: {sheet}\n")
                    # Read a small sample of the sheet to inspect values
                    df = pd.read_excel(file_path, sheet_name=sheet, nrows=50)
                    # Check column names
                    cols = [str(c) for c in df.columns]
                    for c in cols:
                        if any(k.lower() in c.lower() for k in keywords):
                            f.write(f"    FOUND in columns of '{sheet}': {c}\n")
                    # Check row content (convert cells to string and search)
                    for r_idx, row in df.iterrows():
                        for col in df.columns:
                            val_str = str(row[col])
                            if any(k.lower() in val_str.lower() for k in keywords):
                                f.write(f"    FOUND in cell ({r_idx}, {col}) of '{sheet}': {val_str}\n")
            except Exception as e:
                f.write(f"  Error loading workbook: {e}\n")

print("Done searching excel content.")
