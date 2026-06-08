import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "buu_cuc_bat_on.xlsx")

df = pd.read_excel(file_path, sheet_name="NTB", header=None)
print("Shape of NTB sheet:", df.shape)

output_path = os.path.join(workspace_dir, "inspect_bat_on_ntb_res.txt")
with open(output_path, "w", encoding="utf-8") as f:
    for idx, row in df.iterrows():
        vals = [f"C{c}:{repr(val)}" for c, val in enumerate(row) if pd.notna(val)]
        if vals:
            f.write(f"Row {idx}: {', '.join(vals)}\n")

print("Done writing inspect_bat_on_ntb_res.txt")
