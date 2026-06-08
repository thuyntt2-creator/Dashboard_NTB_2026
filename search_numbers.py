import openpyxl
import os
import pandas as pd

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
log_path = os.path.join(workspace_dir, "search_numbers_res.txt")

# Target numbers from Looker screenshot (Đắk Nông row)
targets = [45277, 42176, 44558, 4738, 6269]

with open(log_path, "w", encoding="utf-8") as f:
    for filename in os.listdir(workspace_dir):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(workspace_dir, filename)
            f.write(f"\nScanning: {filename}\n")
            try:
                xls = pd.ExcelFile(file_path)
                for sheet in xls.sheet_names:
                    try:
                        df = pd.read_excel(xls, sheet_name=sheet, header=None)
                        for r_idx, row in df.iterrows():
                            for col_idx, val in enumerate(row):
                                if pd.notna(val):
                                    try:
                                        # Try converting cell val to float/int
                                        val_num = float(val)
                                        # Match check: if cell matches within integer bounds
                                        if any(abs(val_num - t) < 5 or abs(val_num * 1000 - t) < 5 for t in targets):
                                            f.write(f"  FOUND in sheet '{sheet}' at row {r_idx}, col {col_idx}: val={val}\n")
                                    except:
                                        # If it's a string, check if it contains the target as a substring
                                        val_str = str(val)
                                        if any(str(t) in val_str or f"{t:,}" in val_str or f"{t/1000:.3f}" in val_str for t in targets):
                                            f.write(f"  FOUND string in sheet '{sheet}' at row {r_idx}, col {col_idx}: val={val}\n")
                    except Exception as sheet_e:
                        f.write(f"  Error reading sheet '{sheet}': {sheet_e}\n")
            except Exception as e:
                f.write(f"  Error loading file: {e}\n")

print("Done searching numbers.")
