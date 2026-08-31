import pandas as pd
import os

path = "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx"
out_path = "scratch/inspect_excel_out.txt"

with open(out_path, "w", encoding="utf-8") as f:
    f.write("Starting inspection...\n")
    if os.path.exists(path):
        f.write("File exists!\n")
        xls = pd.ExcelFile(path)
        f.write(f"Sheets: {xls.sheet_names}\n")
        
        for name in ['Bưu cục', 'Ca1 - Ca2 - Tồn', 'Thứ cùng kỳ', 'Cơ cấu', 'Data']:
            if name in xls.sheet_names:
                f.write(f"\n--- Sheet {name} columns ---\n")
                df = pd.read_excel(xls, sheet_name=name, nrows=10)
                f.write(str(df.columns.tolist()) + "\n")
                f.write(str(df.head(5)) + "\n")
    else:
        f.write("File not found!\n")

print("Done inspecting!")
