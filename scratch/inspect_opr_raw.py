import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
file_path = os.path.join(workspace_dir, "OPR TTS.xlsx")
output_path = os.path.join(workspace_dir, "scratch", "inspect_opr_raw_res.txt")

with open(output_path, "w", encoding="utf-8") as f:
    # Let's inspect OPR TTS.xlsx sheets first
    xls = pd.ExcelFile(file_path)
    f.write(f"Sheets in OPR TTS.xlsx: {xls.sheet_names}\n")
    
    # Read RAW n-1
    if 'RAW n-1' in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name="RAW n-1")
        f.write(f"RAW n-1 shape: {df.shape}\n")
        f.write(f"RAW n-1 Columns: {list(df.columns)}\n")
        f.write("RAW n-1 head:\n")
        f.write(df.head(10).to_string() + "\n")
        f.write("RAW n-1 tail:\n")
        f.write(df.tail(10).to_string() + "\n")
    else:
        f.write("No RAW n-1 sheet found\n")

print("Done inspecting OPR raw sheet.")
