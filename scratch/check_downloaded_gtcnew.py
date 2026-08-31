import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

excel_path = "downloaded_user_sheet.xlsx"

try:
    print("Sheets in file:")
    xl = pd.ExcelFile(excel_path)
    print(xl.sheet_names)
    
    # Read gtcnew for Nguyễn Duy Long
    print("\n--- gtcnew sheet sample for Nguyễn Duy Long ---")
    df_gtcnew = pd.read_excel(excel_path, sheet_name='gtcnew')
    print(df_gtcnew[df_gtcnew.iloc[:, 0] == 'Nguyễn Duy Long'])
    
    # Read gtc + tồn for Nguyễn Duy Long
    print("\n--- gtc + tồn sheet sample for Nguyễn Duy Long ---")
    df_gtc_ton = pd.read_excel(excel_path, sheet_name='gtc + tồn')
    print(df_gtc_ton[df_gtc_ton.iloc[:, 0] == 'Nguyễn Duy Long'])
    
except Exception as e:
    print(f"Error: {e}")
