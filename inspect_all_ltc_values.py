import pandas as pd

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df_ltc_full = pd.read_excel(file_path, sheet_name='dataLTC full hàng')
df_cocau = pd.read_excel(file_path, sheet_name='cocau')
df_ltc_sheet = pd.read_excel(file_path, sheet_name='LTC')

# Clean dataLTC: map Chi tiết to AM
mapping_df = df_cocau[['BC', 'Am']].dropna().drop_duplicates()
bc_to_am = dict(zip(mapping_df['BC'], mapping_df['Am']))

df_ltc_full_clean = df_ltc_full[df_ltc_full['Chi tiết'] != 'Grand Total'].copy()
df_ltc_full_clean['AM'] = df_ltc_full_clean['Chi tiết'].map(bc_to_am)

# Calculate weighted average for all AMs and Weeks
df_ltc_full_clean['Vol_Gan'] = df_ltc_full_clean['Volume'] * df_ltc_full_clean['%Gán']
df_ltc_full_clean['Vol_LTC'] = df_ltc_full_clean['Volume'] * df_ltc_full_clean['%LTC']

grouped = df_ltc_full_clean.groupby(['AM', 'Time']).agg(
    Total_Vol=('Volume', 'sum'),
    Total_Vol_Gan=('Vol_Gan', 'sum'),
    Total_Vol_LTC=('Vol_LTC', 'sum')
).reset_index()

grouped['Pct_Gan'] = grouped['Total_Vol_Gan'] / grouped['Total_Vol']
grouped['Pct_LTC'] = grouped['Total_Vol_LTC'] / grouped['Total_Vol']

# Pivot to match sheet layout
pivot_gan = grouped.pivot(index='AM', columns='Time', values='Pct_Gan')
pivot_ltc = grouped.pivot(index='AM', columns='Time', values='Pct_LTC')

# Let's align LTC sheet values
df_ltc_sheet_clean = df_ltc_sheet.iloc[1:].copy()
df_ltc_sheet_clean.columns = ['AM', 'Gan_W21', 'LTC_W21', 'Gan_W22', 'LTC_W22', 'Gan_W23', 'LTC_W23', 'Gan_W24', 'LTC_W24', 'Comp', 'None', 'AM_TTS', 'Gan_TTS_W21', 'LTC_TTS_W21', 'Gan_TTS_W22', 'LTC_TTS_W22', 'Gan_TTS_W23', 'LTC_TTS_W23', 'Gan_TTS_W24', 'LTC_TTS_W24', 'Comp_TTS']

df_ltc_sheet_clean['AM'] = df_ltc_sheet_clean['AM'].str.strip()
df_ltc_sheet_clean = df_ltc_sheet_clean[['AM', 'Gan_W21', 'LTC_W21', 'Gan_W22', 'LTC_W22', 'Gan_W23', 'LTC_W23', 'Gan_W24', 'LTC_W24']].dropna()

comparison = df_ltc_sheet_clean.merge(grouped, on='AM', how='left')

output_lines = []
output_lines.append("=== COMPARISON OF LTC FOR W21 ===")
# merge on W21
w21_calc = grouped[grouped['Time'] == '2026/21']
m_w21 = df_ltc_sheet_clean.merge(w21_calc, on='AM', how='left')
output_lines.append(m_w21[['AM', 'Gan_W21', 'Pct_Gan', 'LTC_W21', 'Pct_LTC']].to_string())

output_lines.append("\n=== COMPARISON OF LTC FOR W22 ===")
w22_calc = grouped[grouped['Time'] == '2026/22']
m_w22 = df_ltc_sheet_clean.merge(w22_calc, on='AM', how='left')
output_lines.append(m_w22[['AM', 'Gan_W22', 'Pct_Gan', 'LTC_W22', 'Pct_LTC']].to_string())

output_lines.append("\n=== COMPARISON OF LTC FOR W23 ===")
w23_calc = grouped[grouped['Time'] == '2026/23']
m_w23 = df_ltc_sheet_clean.merge(w23_calc, on='AM', how='left')
output_lines.append(m_w23[['AM', 'Gan_W23', 'Pct_Gan', 'LTC_W23', 'Pct_LTC']].to_string())

output_lines.append("\n=== COMPARISON OF LTC FOR W24 ===")
w24_calc = grouped[grouped['Time'] == '2026/24']
m_w24 = df_ltc_sheet_clean.merge(w24_calc, on='AM', how='left')
output_lines.append(m_w24[['AM', 'Gan_W24', 'Pct_Gan', 'LTC_W24', 'Pct_LTC']].to_string())

with open(r"c:\Users\lap4all\Desktop\New folder\ltc_comparison.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print("Results written to ltc_comparison.txt")
