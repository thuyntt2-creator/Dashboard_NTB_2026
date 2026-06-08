import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "buu_cuc_bat_on.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "inspect_bat_on_res.txt")

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    try:
        xls = pd.ExcelFile(file_path)
        f.write(f"Sheets: {xls.sheet_names}\n")
        for s in ["Datatoday", "Data", "NTB"]:
            if s in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=s)
                f.write(f"\nSheet '{s}' shape: {df.shape}\n")
                f.write(f"Columns: {list(df.columns)}\n")
                f.write("First 5 rows:\n")
                f.write(df.head(5).to_string() + "\n")
                
                # Check date column if present
                date_cols = [c for c in df.columns if "ngay" in c.lower() or "date" in c.lower() or "time" in c.lower()]
                for dc in date_cols:
                    vals = df[dc].dropna().unique()
                    f.write(f"  Col '{dc}': count={len(vals)}, min={min(vals)}, max={max(vals)}\n")
    except Exception as e:
        f.write(f"Error: {e}\n")

print("Inspection completed.")
