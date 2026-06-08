import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "thu_cung_ky.csv")

with open(os.path.join(workspace_dir, "scratch", "inspect_csv_res.txt"), "w", encoding="utf-8") as f:
    df = pd.read_csv(file_path)
    f.write(f"Columns: {list(df.columns)}\n")
    f.write(f"First col unique: {list(df.iloc[:, 0].dropna().unique())}\n")
    df_prov = df[df.iloc[:, 0].notna() & (df.iloc[:, 0] != "")]
    f.write("\nRows with first column populated:\n")
    f.write(df_prov.to_string() + "\n")

