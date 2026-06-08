import os
import openpyxl
import pandas as pd

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
output_path = os.path.join(workspace_dir, "scratch", "looker_numbers_found.txt")

os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Looker totals:
# WTD = 371218
# D = 39567
# D-1 = 65687
# D-2 = 51274
# D-7 = 35931
targets = [371218, 39567, 65687, 51274, 35931]

with open(output_path, "w", encoding="utf-8") as f:
    for filename in os.listdir(workspace_dir):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(workspace_dir, filename)
            f.write(f"\nScanning Excel: {filename}\n")
            try:
                xls = pd.ExcelFile(file_path)
                for sheet in xls.sheet_names:
                    try:
                        df = pd.read_excel(xls, sheet_name=sheet, header=None)
                        for r_idx, row in df.iterrows():
                            for col_idx, val in enumerate(row):
                                if pd.notna(val):
                                    try:
                                        val_num = float(val)
                                        # If val_num matches one of the targets (or divided by 1000 for VN formatting, e.g. 371.218)
                                        if any(abs(val_num - t) < 2 or abs(val_num * 1000 - t) < 2 for t in targets):
                                            f.write(f"  FOUND in sheet '{sheet}' at row {r_idx}, col {col_idx}: val={val}\n")
                                    except:
                                        # String check
                                        val_str = str(val)
                                        if any(str(t) in val_str or f"{t:,}" in val_str or f"{t/1000:.3f}" in val_str for t in targets):
                                            f.write(f"  FOUND string in sheet '{sheet}' at row {r_idx}, col {col_idx}: val={val}\n")
                    except Exception as ex:
                        f.write(f"  Error sheet '{sheet}': {ex}\n")
            except Exception as e:
                f.write(f"  Error loading file: {e}\n")
        elif filename.endswith(".csv"):
            file_path = os.path.join(workspace_dir, filename)
            f.write(f"\nScanning CSV: {filename}\n")
            try:
                df = pd.read_csv(file_path, header=None)
                for r_idx, row in df.iterrows():
                    for col_idx, val in enumerate(row):
                        if pd.notna(val):
                            try:
                                val_num = float(val)
                                if any(abs(val_num - t) < 2 or abs(val_num * 1000 - t) < 2 for t in targets):
                                    f.write(f"  FOUND at row {r_idx}, col {col_idx}: val={val}\n")
                            except:
                                val_str = str(val)
                                if any(str(t) in val_str or f"{t:,}" in val_str or f"{t/1000:.3f}" in val_str for t in targets):
                                    f.write(f"  FOUND string at row {r_idx}, col {col_idx}: val={val}\n")
            except Exception as e:
                f.write(f"  Error loading CSV: {e}\n")

print("Target numbers search completed.")
