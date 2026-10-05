import os
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

xl_path = r'C:\Users\lap4all\Downloads\_NTB - BÁO CÁO TUẦN KINH DOANH (Looker).xlsx'
df_kha = pd.read_excel(xl_path, sheet_name='KH A')
print("=== KH A ===")
print("Columns:", df_kha.columns.tolist())
print("Head:")
print(df_kha.head(3))

df_tq = pd.read_excel(xl_path, sheet_name='tong_quan')
print("\n=== TONG QUAN ===")
print("Columns:", df_tq.columns.tolist())
print("Head:")
print(df_tq.head(3))
