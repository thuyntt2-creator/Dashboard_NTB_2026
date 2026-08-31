import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df_ltc_full = pd.read_excel(excel_path, sheet_name='dataLTC full hàng')

df_w24 = df_ltc_full[(df_ltc_full['Time'] == '2026/24') & (df_ltc_full['Cấp quản lý'] != 'Grand Total')].copy()
df_w24['Volume'] = pd.to_numeric(df_w24['Volume'], errors='coerce')
df_w24['%Gán'] = pd.to_numeric(df_w24['%Gán'], errors='coerce')
df_w24['%LTC'] = pd.to_numeric(df_w24['%LTC'], errors='coerce')

df_w24['Vol_Gan'] = df_w24['Volume'] * df_w24['%Gán']
df_w24['Vol_LTC'] = df_w24['Volume'] * df_w24['%LTC']

vol_tot = df_w24['Volume'].sum()
vol_gan = df_w24['Vol_Gan'].sum()
vol_ltc = df_w24['Vol_LTC'].sum()

print("Overall W24 totals:")
print(f"Total Volume: {vol_tot}")
print(f"Total Assigned Volume: {vol_gan}")
print(f"Total LTC Volume: {vol_ltc}")
print(f"Formula A (vol_ltc / Volume): {vol_ltc / vol_tot * 100:.4f}%")
print(f"Formula B (vol_ltc / Vol_Gan): {vol_ltc / vol_gan * 100:.4f}%")
