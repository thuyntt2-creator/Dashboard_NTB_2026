import pandas as pd
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
output_file = os.path.join(workspace_dir, "scratch", "inspect_opr_and_lc_details.txt")

with open(output_file, "w", encoding="utf-8") as f:
    # 1. Inspect OPR TTS in downloaded_user_sheet.xlsx
    user_file = os.path.join(workspace_dir, "downloaded_user_sheet.xlsx")
    if os.path.exists(user_file):
        xls = pd.ExcelFile(user_file)
        if "OPR TTS" in xls.sheet_names:
            df_opr_tts = pd.read_excel(xls, sheet_name="OPR TTS")
            f.write("--- OPR TTS sheet in downloaded_user_sheet.xlsx ---\n")
            f.write(f"Shape: {df_opr_tts.shape}\n")
            f.write(f"Columns: {df_opr_tts.columns.tolist()}\n")
            f.write(f"Describe:\n{df_opr_tts.describe(include='all').to_string()}\n")
            f.write(f"Sample data:\n{df_opr_tts.head(10).to_string()}\n")
        else:
            f.write("OPR TTS sheet NOT found in downloaded_user_sheet.xlsx\n")
            
        # 2. Inspect data rớt LC
        if "data rớt LC" in xls.sheet_names:
            df_lc = pd.read_excel(xls, sheet_name="data rớt LC")
            f.write("\n--- data rớt LC details ---\n")
            f.write(f"Unique values of Tuần: {df_lc['Tuần'].dropna().unique().tolist()}\n")
            f.write(f"Unique values of AM: {df_lc['AM'].dropna().unique().tolist()}\n")
            
            # Check non-zero values of Vol rớt LC
            non_zero_vol = df_lc[df_lc['Vol rớt LC'] > 0]
            f.write(f"Number of rows where Vol rớt LC > 0: {len(non_zero_vol)}\n")
            if len(non_zero_vol) > 0:
                f.write(f"Sample where Vol rớt LC > 0:\n{non_zero_vol.head(10).to_string()}\n")
                
            # Check `%_rot_lc` values
            f.write(f"Unique values of %_rot_lc (sample of 20): {df_lc['%_rot_lc'].dropna().unique()[:20].tolist()}\n")
            
            # Check how Vol rớt LC is related to Vol cần LC and %_rot_lc
            # Let's convert %_rot_lc to float
            def parse_pct(val):
                if pd.isna(val):
                    return 0.0
                if isinstance(val, (int, float)):
                    return float(val)
                val_str = str(val).strip().replace('%', '')
                try:
                    return float(val_str) / 100.0
                except:
                    return 0.0
            
            df_lc['pct_float'] = df_lc['%_rot_lc'].apply(parse_pct)
            df_lc['calculated_vol_rot'] = df_lc['Vol cần LC'] * df_lc['pct_float']
            f.write(f"Sum of Vol cần LC: {df_lc['Vol cần LC'].sum()}\n")
            f.write(f"Sum of Vol rớt LC (original): {df_lc['Vol rớt LC'].sum()}\n")
            f.write(f"Sum of calculated_vol_rot: {df_lc['calculated_vol_rot'].sum()}\n")
            f.write(f"Sample calculated differences:\n{df_lc[df_lc['calculated_vol_rot'] > 0][['Chi tiết', 'Vol cần LC', '%_rot_lc', 'Vol rớt LC', 'calculated_vol_rot']].head(10).to_string()}\n")
            
    else:
        f.write("downloaded_user_sheet.xlsx NOT FOUND\n")

print("Details written successfully.")
