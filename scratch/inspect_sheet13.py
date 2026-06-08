import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "inspect_sheet13_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="Sheet13")
    f.write(f"Sheet13 Columns: {list(df.columns)}\n")
    f.write(f"Sheet13 Shape: {df.shape}\n")
    f.write("Sheet13 Head:\n")
    f.write(df.head(10).to_string() + "\n")
    f.write("Sheet13 types:\n")
    f.write(df.dtypes.to_string() + "\n")

print("Done inspecting sheet13.")
