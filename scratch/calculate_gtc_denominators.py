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

subset = df[(df['AM_mapped'] == 'Nguyễn Duy Long') & (df['Time'] == '2026/24')]

vol_tot = subset['Volume'].sum()
vol_gan = (subset['Volume'] * subset['% Gán']).sum()
vol_gtc = (subset['Volume'] * subset['% GTC']).sum()

print(f"Nguyễn Duy Long W24 raw sums:")
print(f"  Total Volume: {vol_tot}")
print(f"  Assigned Volume: {vol_gan}")
print(f"  GTC Volume: {vol_gtc}")
print(f"  Formula A (vol_gtc / Volume): {vol_gtc / vol_tot * 100:.4f}%")
print(f"  Formula B (vol_gtc / Vol_Gan): {vol_gtc / vol_gan * 100:.4f}%")
