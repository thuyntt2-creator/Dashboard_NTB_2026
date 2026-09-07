import pandas as pd

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df_gtc_full = pd.read_excel(file_path, sheet_name='dataGTC gốc full hàng')
df_cocau = pd.read_excel(file_path, sheet_name='cocau')
df_gtc_ton = pd.read_excel(file_path, sheet_name='gtc + tồn')

mapping_df = df_cocau[['BC', 'Am']].dropna().drop_duplicates()
bc_to_am = dict(zip(mapping_df['BC'], mapping_df['Am']))
df_gtc_full['AM'] = df_gtc_full['Chi tiết'].map(bc_to_am)

# Filter for Trầm Hữu Tiến in W21
df_tien_w21 = df_gtc_full[(df_gtc_full['AM'] == 'Trầm Hữu Tiến') & (df_gtc_full['Time'] == '2026/21')]

# What is GTC for Ca1 + Tồn?
df_tien_w21_ca1_ton = df_tien_w21[df_tien_w21['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Tồn'])]
vol_sum = df_tien_w21_ca1_ton['Volume'].sum()
gan_sum = (df_tien_w21_ca1_ton['Volume'] * df_tien_w21_ca1_ton['% Gán']).sum()
gtc_sum = (df_tien_w21_ca1_ton['Volume'] * df_tien_w21_ca1_ton['% GTC']).sum()

output_lines = []
output_lines.append("Calculated Ca1 + Tồn for Trầm Hữu Tiến W21:")
output_lines.append(f"Volume: {vol_sum}")
output_lines.append(f"Weighted average % Gán: {gan_sum / vol_sum}")
output_lines.append(f"Weighted average % GTC: {gtc_sum / vol_sum}")

output_lines.append("\nValue in 'gtc + tồn' sheet for Trầm Hữu Tiến W21:")
df_gtc_ton_clean = df_gtc_ton.iloc[1:].copy()
df_gtc_ton_clean.columns = ['AM', 'Gan_W21', 'GTC_W21', 'Gan_W22', 'GTC_W22', 'Gan_W23', 'GTC_W23', 'Gan_W24', 'GTC_W24', 'Comp', 'AM_TTS', 'Gan_TTS_W21', 'GTC_TTS_W21', 'Gan_TTS_W22', 'GTC_TTS_W22', 'Gan_TTS_W23', 'GTC_TTS_W23', 'Gan_TTS_W24', 'GTC_TTS_W24', 'Comp_TTS']
row_tien = df_gtc_ton_clean[df_gtc_ton_clean['AM'].str.strip() == 'Trầm Hữu Tiến']
output_lines.append(row_tien[['AM', 'Gan_W21', 'GTC_W21']].to_string())

with open(r"c:\Users\lap4all\Desktop\New folder\inspect_gtc_ton_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print("Results written to inspect_gtc_ton_res.txt")
