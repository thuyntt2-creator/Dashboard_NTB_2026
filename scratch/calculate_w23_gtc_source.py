import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df = pd.read_excel(excel_path, sheet_name='dataGTC gốc full hàng')

df_cocau = pd.read_excel(excel_path, sheet_name='cocau')
df_cocau['BC_norm'] = df_cocau['BC'].str.strip().str.upper()
bc_to_am = dict(zip(df_cocau['BC_norm'], df_cocau['Am']))

df['BC_norm'] = df['Chi tiết'].str.strip().str.upper()
df['AM_mapped'] = df['BC_norm'].map(bc_to_am)

ndl_w23 = df[(df['AM_mapped'] == 'Nguyễn Duy Long') & (df['Time'] == '2026/23')]
print("Number of rows for NDL in W23:", len(ndl_w23))
print("Loại Hàng values in W23 for NDL:")
print(ndl_w23.groupby('Loại Hàng')['Volume'].sum())

# Scenario 1: all 3 types
vol_tot_3 = ndl_w23['Volume'].sum()
vol_gtc_3 = (ndl_w23['Volume'] * ndl_w23['% GTC']).sum()
pct_gtc_3 = vol_gtc_3 / vol_tot_3 if vol_tot_3 > 0 else 0
print(f"Scenario 1 (All 3 categories): {pct_gtc_3*100:.4f}%")

# Scenario 2: Ca 1 + Ca 2 (TTS)
ndl_w23_tts = ndl_w23[ndl_w23['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])]
vol_tot_2 = ndl_w23_tts['Volume'].sum()
vol_gtc_2 = (ndl_w23_tts['Volume'] * ndl_w23_tts['% GTC']).sum()
pct_gtc_2 = vol_gtc_2 / vol_tot_2 if vol_tot_2 > 0 else 0
print(f"Scenario 2 (Only Ca 1 + Ca 2): {pct_gtc_2*100:.4f}%")
