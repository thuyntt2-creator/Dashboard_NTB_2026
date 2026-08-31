import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
user_file = os.path.join(workspace_dir, "downloaded_user_sheet.xlsx")
output_file = os.path.join(workspace_dir, "scratch", "check_unmatched_res.txt")

with open(output_file, "w", encoding="utf-8") as f:
    df_cocau = pd.read_excel(user_file, sheet_name="cocau")
    
    match_585 = df_cocau[df_cocau['Bưu cục'].astype(str).str.contains("585") | df_cocau['BC'].astype(str).str.contains("585")]
    f.write("Matching 585 in cocau:\n")
    f.write(match_585.to_string() + "\n\n")

    match_luong_son = df_cocau[df_cocau['Bưu cục'].astype(str).str.contains("Lương Sơn") | df_cocau['BC'].astype(str).str.contains("Lương Sơn")]
    f.write("Matching Lương Sơn in cocau:\n")
    f.write(match_luong_son.to_string() + "\n")
