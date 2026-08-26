import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r"c:\Users\lap4all\Desktop\NTB_Bao_Cao_Van_Hanh_Co_Bieu_Do.xlsx"
print(f"Reading {path} ...")
df_gtcnew = pd.read_excel(path, sheet_name='gtcnew')
ndl_row = df_gtcnew[df_gtcnew.iloc[:, 0] == 'Nguyễn Duy Long']
print("Nguyễn Duy Long in gtcnew:")
for col in ndl_row.columns:
    print(f"  {col}: {ndl_row[col].values[0]}")
