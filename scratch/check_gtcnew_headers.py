import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

excel_path = "downloaded_user_sheet.xlsx"

df_gtcnew = pd.read_excel(excel_path, sheet_name='gtcnew')
print("gtcnew columns:")
print(list(df_gtcnew.columns))
print("Nguyễn Duy Long row in gtcnew:")
ndl_gtcnew = df_gtcnew[df_gtcnew.iloc[:, 0] == 'Nguyễn Duy Long']
for col in ndl_gtcnew.columns:
    print(f"  {col}: {ndl_gtcnew[col].values[0]}")

df_gtc_ton = pd.read_excel(excel_path, sheet_name='gtc + tồn')
print("\ngtc + tồn columns:")
print(list(df_gtc_ton.columns))
print("Nguyễn Duy Long row in gtc + tồn:")
ndl_gtc_ton = df_gtc_ton[df_gtc_ton.iloc[:, 0] == 'Nguyễn Duy Long']
for col in ndl_gtc_ton.columns:
    print(f"  {col}: {ndl_gtc_ton[col].values[0]}")
