import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"

output_path = os.path.join(workspace_dir, "inspect_files_res.txt")
with open(output_path, "w", encoding="utf-8") as f:
    # 1. BÁO CÁO VẬN HÀNH
    f.write("=== Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx ===\n")
    path_ops = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
    if os.path.exists(path_ops):
        xls = pd.ExcelFile(path_ops)
        f.write(f"Sheets: {xls.sheet_names}\n")
        for sheet in xls.sheet_names[:5]: # print columns of first 5 sheets
            df = pd.read_excel(xls, sheet_name=sheet, nrows=5)
            f.write(f"Sheet '{sheet}' columns: {list(df.columns)}\n")
    else:
        f.write("Not found.\n")
        
    # 2. OPR TTS
    f.write("\n=== OPR TTS.xlsx ===\n")
    path_opr = os.path.join(workspace_dir, "OPR TTS.xlsx")
    if os.path.exists(path_opr):
        xls = pd.ExcelFile(path_opr)
        f.write(f"Sheets: {xls.sheet_names}\n")
        for sheet in xls.sheet_names[:5]:
            df = pd.read_excel(xls, sheet_name=sheet, nrows=5)
            f.write(f"Sheet '{sheet}' columns: {list(df.columns)}\n")
    else:
        f.write("Not found.\n")
        
    # 3. ODR TTS.csv
    f.write("\n=== ODR TTS.csv ===\n")
    path_odr = os.path.join(workspace_dir, "ODR TTS.csv")
    if os.path.exists(path_odr):
        df = pd.read_csv(path_odr, nrows=5)
        f.write(f"Columns: {list(df.columns)}\n")
    else:
        f.write("Not found.\n")

print("Done writing inspect_files_res.txt")
