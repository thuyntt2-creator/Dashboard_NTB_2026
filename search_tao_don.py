import os
import openpyxl
import pandas as pd

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
output_path = os.path.join(workspace_dir, "search_tao_don_res.txt")

keywords = ["tạo", "tao", "đơn", "don", "create", "created"]

with open(output_path, "w", encoding="utf-8") as f:
    for filename in os.listdir(workspace_dir):
        if filename.endswith(".xlsx"):
            f.write(f"\nFile: {filename}\n")
            try:
                xls = pd.ExcelFile(os.path.join(workspace_dir, filename))
                for sheet in xls.sheet_names:
                    f.write(f"  Sheet: {sheet}\n")
                    df = pd.read_excel(xls, sheet_name=sheet, nrows=5)
                    cols = list(df.columns)
                    f.write(f"    Columns: {cols}\n")
                    for c in cols:
                        if any(k in str(c).lower() for k in keywords):
                            f.write(f"      Matched Column: {c}\n")
            except Exception as e:
                f.write(f"  Error: {e}\n")
        elif filename.endswith(".csv"):
            f.write(f"\nFile: {filename}\n")
            try:
                df = pd.read_csv(os.path.join(workspace_dir, filename), nrows=5)
                cols = list(df.columns)
                f.write(f"    Columns: {cols}\n")
                for c in cols:
                    if any(k in str(c).lower() for k in keywords):
                        f.write(f"      Matched Column: {c}\n")
            except Exception as e:
                f.write(f"  Error: {e}\n")

print("Done searching for order creation keywords.")
