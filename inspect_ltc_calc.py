import pandas as pd

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df_ltc_full = pd.read_excel(file_path, sheet_name='dataLTC full hàng')
df_cocau = pd.read_excel(file_path, sheet_name='cocau')
df_ltc_sheet = pd.read_excel(file_path, sheet_name='LTC')

mapping_df = df_cocau[['BC', 'Am']].dropna().drop_duplicates()
bc_to_am = dict(zip(mapping_df['BC'], mapping_df['Am']))

# Clean dataLTC: map Chi tiết to AM
df_ltc_full_clean = df_ltc_full[df_ltc_full['Chi tiết'] != 'Grand Total'].copy()
df_ltc_full_clean['AM'] = df_ltc_full_clean['Chi tiết'].map(bc_to_am)

# Filter for Hồng Bích Nga in W21
df_nga_w21 = df_ltc_full_clean[(df_ltc_full_clean['AM'] == 'Hồng Bích Nga') & (df_ltc_full_clean['Time'] == '2026/21')]

# Calculate weighted average
vol_sum = df_nga_w21['Volume'].sum()
gan_sum = (df_nga_w21['Volume'] * df_nga_w21['%Gán']).sum()
ltc_sum = (df_nga_w21['Volume'] * df_nga_w21['%LTC']).sum()

output = []
output.append("Calculated LTC for Hồng Bích Nga W21:")
output.append(f"Volume: {vol_sum}")
output.append(f"Weighted average %Gán: {gan_sum / vol_sum}")
output.append(f"Weighted average %LTC: {ltc_sum / vol_sum}")

output.append("\nValues in LTC sheet for Hồng Bích Nga W21:")
df_ltc_sheet_clean = df_ltc_sheet.iloc[1:].copy()
df_ltc_sheet_clean.columns = ['AM', 'Gan_W21', 'LTC_W21', 'Gan_W22', 'LTC_W22', 'Gan_W23', 'LTC_W23', 'Gan_W24', 'LTC_W24', 'Comp', 'None', 'AM_TTS', 'Gan_TTS_W21', 'LTC_TTS_W21', 'Gan_TTS_W22', 'LTC_TTS_W22', 'Gan_TTS_W23', 'LTC_TTS_W23', 'Gan_TTS_W24', 'LTC_TTS_W24', 'Comp_TTS']
row_nga = df_ltc_sheet_clean[df_ltc_sheet_clean['AM'].str.strip() == 'Hồng Bích Nga']
output.append(row_nga[['AM', 'Gan_W21', 'LTC_W21']].to_string())

with open(r"c:\Users\lap4all\Desktop\New folder\inspect_ltc_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("LTC verification written to inspect_ltc_res.txt")
