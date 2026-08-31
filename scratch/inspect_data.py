import pandas as pd
import os
import sys

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
output_file = os.path.join(workspace_dir, "scratch", "inspect_data_res.txt")

with open(output_file, "w", encoding="utf-8") as f:
    f.write("--- INSPECTING OPR TTS.xlsx ---\n")
    opr_file = os.path.join(workspace_dir, "OPR TTS.xlsx")
    if os.path.exists(opr_file):
        xls = pd.ExcelFile(opr_file)
        f.write(f"Sheets in OPR TTS.xlsx: {xls.sheet_names}\n")
        
        # Read OPR
        df_opr = pd.read_excel(xls, sheet_name="OPR")
        f.write(f"\nOPR columns: {df_opr.columns.tolist()}\n")
        f.write(f"OPR shape: {df_opr.shape}\n")
        f.write(f"OPR sample data:\n{df_opr.head(5).to_string()}\n")
        f.write(f"\nUnique values of AM in OPR: {df_opr['AM'].dropna().unique().tolist()}\n")
        f.write(f"\nUnique values of Khung giờ tạo in OPR: {df_opr['Khung giờ tạo'].dropna().unique().tolist()}\n")
        f.write(f"\nUnique values of khung_gio_tao_don in OPR: {df_opr['khung_gio_tao_don'].dropna().unique().tolist()}\n")
        f.write(f"\nUnique values of tuan in OPR: {df_opr['tuan'].dropna().unique().tolist()}\n")
        f.write(f"\nUnique values of Tuần in OPR: {df_opr['Tuần'].dropna().unique().tolist()}\n")
        
        if "REPORT_OPR" in xls.sheet_names:
            df_rep = pd.read_excel(xls, sheet_name="REPORT_OPR")
            f.write(f"\nREPORT_OPR columns: {df_rep.columns.tolist()}\n")
            f.write(f"REPORT_OPR shape: {df_rep.shape}\n")
            f.write(f"REPORT_OPR sample data:\n{df_rep.head(15).to_string()}\n")
    else:
        f.write("OPR TTS.xlsx NOT FOUND\n")

    f.write("\n--- INSPECTING downloaded_user_sheet.xlsx ---\n")
    user_sheet_file = os.path.join(workspace_dir, "downloaded_user_sheet.xlsx")
    if os.path.exists(user_sheet_file):
        xls_user = pd.ExcelFile(user_sheet_file)
        f.write(f"Sheets in downloaded_user_sheet.xlsx: {xls_user.sheet_names}\n")
        
        sheets_of_interest = ['data rớt LC', 'dataLTC full hàng', 'dataLTC TTS', 'sản lượng']
        for s in sheets_of_interest:
            if s in xls_user.sheet_names:
                df_s = pd.read_excel(xls_user, sheet_name=s)
                f.write(f"\nSheet '{s}' shape: {df_s.shape}\n")
                f.write(f"Sheet '{s}' columns: {df_s.columns.tolist()}\n")
                f.write(f"Sheet '{s}' sample data:\n{df_s.head(5).to_string()}\n")
                if s == 'data rớt LC':
                    f.write(f"\nUnique values of week/tuan/time in '{s}':\n")
                    # Let's inspect column types or preview more rows
                    f.write(f"Describe:\n{df_s.describe(include='all').to_string()}\n")
                    f.write(f"More rows:\n{df_s.head(20).to_string()}\n")
            else:
                f.write(f"\nSheet '{s}' NOT found in downloaded_user_sheet.xlsx\n")
    else:
        f.write("downloaded_user_sheet.xlsx NOT FOUND\n")

print("Inspection file written successfully.")
