import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df_tts = pd.read_excel(excel_path, sheet_name='dataGTC gốc TTS')

# Check cocau mapping
df_cocau = pd.read_excel(excel_path, sheet_name='cocau')
df_cocau['BC_norm'] = df_cocau['BC'].str.strip().str.upper()
bc_to_am = dict(zip(df_cocau['BC_norm'], df_cocau['Am']))

df_tts['BC_norm'] = df_tts['Chi tiết'].str.strip().str.upper()
df_tts['AM_mapped'] = df_tts['BC_norm'].map(bc_to_am)

subset = df_tts[(df_tts['AM_mapped'] == 'Nguyễn Duy Long') & (df_tts['Time'] == '2026/23')]

print("Raw rows in dataGTC gốc TTS for Nguyễn Duy Long W23:")
print(subset[['Loại Hàng', 'Volume', '% GTC']])

# Test combination 1: Hàng Mới Ca 1
sub_c1 = subset[subset['Loại Hàng'] == 'Hàng Mới Ca 1']
vol_tot_c1 = sub_c1['Volume'].sum()
vol_gtc_c1 = (sub_c1['Volume'] * sub_c1['% GTC']).sum()
print(f"Only Ca 1: {vol_gtc_c1 / vol_tot_c1 * 100:.4f}%" if vol_tot_c1 > 0 else "No Ca 1 data")

# Test combination 2: Hàng Mới Ca 1 + Hàng Tồn
sub_c2 = subset[subset['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Tồn'])]
vol_tot_c2 = sub_c2['Volume'].sum()
vol_gtc_c2 = (sub_c2['Volume'] * sub_c2['% GTC']).sum()
print(f"Ca 1 + Tồn: {vol_gtc_c2 / vol_tot_c2 * 100:.4f}%" if vol_tot_c2 > 0 else "No Ca 1 + Tồn data")

# Test combination 3: All categories present in dataGTC gốc TTS
vol_tot_all = subset['Volume'].sum()
vol_gtc_all = (subset['Volume'] * subset['% GTC']).sum()
print(f"All categories in TTS sheet: {vol_gtc_all / vol_tot_all * 100:.4f}%")
