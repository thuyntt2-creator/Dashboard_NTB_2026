import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "OPR TTS.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "inspect_opr_data.txt")

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    try:
        xls = pd.ExcelFile(file_path)
        for s in ["data", "RAW n-1", "OPR"]:
            if s in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=s, nrows=200000)
                f.write(f"Sheet: {s}, Shape: {df.shape}\n")
                f.write(f"  Columns: {list(df.columns)}\n")
                # Show first few non-null rows
                f.write("  First 3 rows:\n")
                f.write(df.head(3).to_string() + "\n")
                # Check date ranges
                date_cols = [c for c in df.columns if "ngay" in c.lower() or "time" in c.lower() or "tạo" in c.lower() or "tao" in c.lower() or "ltc" in c.lower()]
                for dc in date_cols:
                    try:
                        vals = df[dc].dropna().unique()
                        f.write(f"    Col '{dc}': unique count = {len(vals)}, min = {min(vals)}, max = {max(vals)}\n")
                    except Exception as ex:
                        f.write(f"    Col '{dc}': error getting range: {ex}\n")
    except Exception as e:
        f.write(f"Error: {e}\n")

print("Inspection completed.")
