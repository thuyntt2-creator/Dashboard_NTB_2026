import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "inspect_rawltc_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="rawltc")
    f.write(f"rawltc columns: {list(df.columns)}\n")
    f.write(f"rawltc shape: {df.shape}\n")
    f.write("rawltc Head:\n")
    f.write(df.head(10).to_string() + "\n")

print("Done inspecting rawltc.")
