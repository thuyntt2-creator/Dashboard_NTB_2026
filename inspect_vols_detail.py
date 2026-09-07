import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df_gtc_full = pd.read_excel(file_path, sheet_name='dataGTC gốc full hàng')
df_cocau = pd.read_excel(file_path, sheet_name='cocau')
df_san_luong = pd.read_excel(file_path, sheet_name='sản lượng')

mapping_df = df_cocau[['BC', 'Am']].dropna().drop_duplicates()
bc_to_am = dict(zip(mapping_df['BC'], mapping_df['Am']))
df_gtc_full['AM'] = df_gtc_full['Chi tiết'].map(bc_to_am)

# Sum volumes by AM and Time and Loại Hàng
summary = df_gtc_full.groupby(['AM', 'Time', 'Loại Hàng'])['Volume'].sum().unstack(fill_value=0)
summary['Ca1_Ca2'] = summary['Hàng Mới Ca 1'] + summary['Hàng Mới Ca 2']
summary['Ca1_Tồn'] = summary['Hàng Mới Ca 1'] + summary['Hàng Tồn']
summary['Total'] = summary['Hàng Mới Ca 1'] + summary['Hàng Mới Ca 2'] + summary['Hàng Tồn']

# Match with sản lượng sheet
# We need to clean df_san_luong to get the AM name and W23 values
# Row 0 is headers: AM, 2026/21, 2026/22, 2026/23, 2026/24
df_sl_clean = df_san_luong.iloc[1:].copy()
df_sl_clean.columns = ['AM', 'W21_SL', 'W22_SL', 'W23_SL', 'W24_SL', 'So_W23', 'Pct_W23', 'None', 'AM_TTS', 'W21_TTS', 'W22_TTS', 'W23_TTS', 'W24_TTS', 'So_W23_TTS', 'None2']

df_sl_clean = df_sl_clean[['AM', 'W21_SL', 'W22_SL', 'W23_SL', 'W24_SL']].dropna()
df_sl_clean['AM'] = df_sl_clean['AM'].str.strip()

# Join with our group
w23_calc = summary.xs('2026/23', level='Time')

comparison = df_sl_clean.merge(w23_calc, on='AM', how='left')

output_lines = []
output_lines.append("=== COMPARISON FOR W23 ===")
output_lines.append(comparison[['AM', 'W23_SL', 'Hàng Mới Ca 1', 'Hàng Mới Ca 2', 'Hàng Tồn', 'Ca1_Ca2', 'Ca1_Tồn', 'Total']].to_string())

# Let's check other weeks too
w21_calc = summary.xs('2026/21', level='Time')
comparison_w21 = df_sl_clean.merge(w21_calc, on='AM', how='left')
output_lines.append("\n=== COMPARISON FOR W21 ===")
output_lines.append(comparison_w21[['AM', 'W21_SL', 'Hàng Mới Ca 1', 'Hàng Mới Ca 2', 'Hàng Tồn', 'Ca1_Ca2', 'Ca1_Tồn', 'Total']].to_string())

w22_calc = summary.xs('2026/22', level='Time')
comparison_w22 = df_sl_clean.merge(w22_calc, on='AM', how='left')
output_lines.append("\n=== COMPARISON FOR W22 ===")
output_lines.append(comparison_w22[['AM', 'W22_SL', 'Hàng Mới Ca 1', 'Hàng Mới Ca 2', 'Hàng Tồn', 'Ca1_Ca2', 'Ca1_Tồn', 'Total']].to_string())

w24_calc = summary.xs('2026/24', level='Time')
comparison_w24 = df_sl_clean.merge(w24_calc, on='AM', how='left')
output_lines.append("\n=== COMPARISON FOR W24 ===")
output_lines.append(comparison_w24[['AM', 'W24_SL', 'Hàng Mới Ca 1', 'Hàng Mới Ca 2', 'Hàng Tồn', 'Ca1_Ca2', 'Ca1_Tồn', 'Total']].to_string())

with open(r"c:\Users\lap4all\Desktop\New folder\vols_comparison.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print("Written to vols_comparison.txt")
