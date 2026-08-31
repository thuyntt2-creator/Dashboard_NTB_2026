import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df = pd.read_excel(excel_path, sheet_name='dataLTC full hàng')

# Check cocau mapping
df_cocau = pd.read_excel(excel_path, sheet_name='cocau')
df_cocau['BC_norm'] = df_cocau['BC'].str.strip().str.upper()
bc_to_am = dict(zip(df_cocau['BC_norm'], df_cocau['Am']))

df['BC_norm'] = df['Chi tiết'].str.strip().str.upper()
df['AM_mapped'] = df['BC_norm'].map(bc_to_am)

subset = df[(df['AM_mapped'] == 'Nguyễn Duy Long') & (df['Time'] == '2026/23')]
print("Raw rows for Nguyễn Duy Long in W23 in dataLTC full hàng:")
print(subset[['Chi tiết', 'Volume', '%Gán', '%LTC']])

vol_tot = subset['Volume'].sum()
vol_gan = (subset['Volume'] * subset['%Gán']).sum()
vol_ltc = (subset['Volume'] * subset['%LTC']).sum()

pct_ltc_tot = vol_ltc / vol_tot if vol_tot > 0 else 0
pct_ltc_gan = vol_ltc / vol_gan if vol_gan > 0 else 0

print(f"Formula A (vol_ltc / Volume): {pct_ltc_tot*100:.4f}%")
print(f"Formula B (vol_ltc / Vol_Gan): {pct_ltc_gan*100:.4f}%")
