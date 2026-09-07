import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df_gtc_full = pd.read_excel(file_path, sheet_name='dataGTC gốc full hàng')
df_cocau = pd.read_excel(file_path, sheet_name='cocau')

mapping_df = df_cocau[['BC', 'Am']].dropna().drop_duplicates()
bc_to_am = dict(zip(mapping_df['BC'], mapping_df['Am']))

df_gtc_full['AM'] = df_gtc_full['Chi tiết'].map(bc_to_am)

# Filter for Hồng Bích Nga and W23 (Time == '2026/23')
df_nga_w23 = df_gtc_full[(df_gtc_full['AM'] == 'Hồng Bích Nga') & (df_gtc_full['Time'] == '2026/23')]

print("Hồng Bích Nga W23 details:")
print(df_nga_w23[['Chi tiết', 'Loại Hàng', 'Volume']])
print("\nSum by Loại Hàng:")
print(df_nga_w23.groupby('Loại Hàng')['Volume'].sum())

print("\nSum of Ca1 + Ca2:")
print(df_nga_w23[df_nga_w23['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])]['Volume'].sum())

print("\nSum of All (including Hàng Tồn):")
print(df_nga_w23['Volume'].sum())
