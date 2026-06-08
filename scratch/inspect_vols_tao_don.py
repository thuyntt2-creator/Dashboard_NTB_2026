import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "vols_tao_don.xlsx")

if not os.path.exists(file_path):
    print("File vols_tao_don.xlsx does not exist.")
else:
    xls = pd.ExcelFile(file_path)
    print("Sheets in vols_tao_don.xlsx:", xls.sheet_names)
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, nrows=5)
        print(f"\nSheet '{sheet}' head:")
        print(df.columns.tolist())
        print(df.head(2))
