import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "buu_cuc_bat_on.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "check_bat_on_dates_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    df = pd.read_excel(file_path, sheet_name="NTB", header=3) # NTB headers start at row 4 (0-indexed 3)
    f.write(f"Columns: {list(df.columns)}\n")
    f.write(f"Shape: {df.shape}\n")
    if 'ngay' in df.columns:
        df['date'] = pd.to_datetime(df['ngay'], errors='coerce')
        f.write(f"Unique dates in ngay column:\n{df['date'].value_counts().to_string()}\n")
    else:
        # print first column
        first_col = df.columns[0]
        df['date'] = pd.to_datetime(df[first_col], errors='coerce')
        f.write(f"Unique dates in first column:\n{df['date'].value_counts().to_string()}\n")

print("Done checking bat_on dates.")
