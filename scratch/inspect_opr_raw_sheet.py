import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "OPR TTS.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "inspect_opr_raw_sheet_res.txt")

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    try:
        xls = pd.ExcelFile(file_path)
        if "raw" in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name="raw")
            f.write(f"Sheet 'raw' shape: {df.shape}\n")
            f.write(f"Columns: {list(df.columns)}\n")
            f.write("Rows:\n")
            f.write(df.to_string() + "\n")
        else:
            f.write("Sheet 'raw' not found.\n")
    except Exception as e:
        f.write(f"Error: {e}\n")

print("Inspection completed.")
