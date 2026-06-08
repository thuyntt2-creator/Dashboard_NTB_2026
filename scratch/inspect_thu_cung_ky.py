import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "inspect_thu_cung_ky_detailed.txt")

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    try:
        xls = pd.ExcelFile(file_path)
        sheet_name = None
        for s in xls.sheet_names:
            if "cùng kỳ" in s.lower() or "cung ky" in s.lower():
                sheet_name = s
                break
        f.write(f"Matched sheet name: {sheet_name}\n")
        if sheet_name:
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            f.write(f"Shape of sheet: {df.shape}\n")
            # Write non-null rows
            for idx, r in df.iterrows():
                row_vals = [str(x) for x in r.values if pd.notna(x)]
                if len(row_vals) > 0:
                    f.write(f"Row {idx}: {row_vals[:15]}\n")
        else:
            f.write("No matching sheet found.\n")
    except Exception as e:
        f.write(f"Error: {e}\n")

print("Inspection completed.")
