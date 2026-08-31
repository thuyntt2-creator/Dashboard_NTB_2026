import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
user_file = os.path.join(workspace_dir, "downloaded_user_sheet.xlsx")
output_file = os.path.join(workspace_dir, "scratch", "inspect_cocau_res.txt")

with open(output_file, "w", encoding="utf-8") as f:
    xls = pd.ExcelFile(user_file)
    if "cocau" in xls.sheet_names:
        df_cocau = pd.read_excel(xls, sheet_name="cocau")
        f.write("--- cocau sheet ---\n")
        f.write(f"Columns: {df_cocau.columns.tolist()}\n")
        f.write(f"Shape: {df_cocau.shape}\n")
        f.write(f"First 30 rows:\n{df_cocau.head(30).to_string()}\n")
    else:
        f.write("cocau sheet not found in downloaded_user_sheet.xlsx\n")
