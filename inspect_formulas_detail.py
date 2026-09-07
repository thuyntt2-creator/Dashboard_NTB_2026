import pandas as pd

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df_gtc_full = pd.read_excel(file_path, sheet_name='dataGTC gốc full hàng')
df_cocau = pd.read_excel(file_path, sheet_name='cocau')

mapping_df = df_cocau[['BC', 'Am']].dropna().drop_duplicates()
bc_to_am = dict(zip(mapping_df['BC'], mapping_df['Am']))
df_gtc_full['AM'] = df_gtc_full['Chi tiết'].map(bc_to_am)

# Filter for Trầm Hữu Tiến in W21
df_tien_w21 = df_gtc_full[(df_gtc_full['AM'] == 'Trầm Hữu Tiến') & (df_gtc_full['Time'] == '2026/21')]

# Filter for Hàng Mới Ca 1 and Hàng Mới Ca 2
df_tien_w21_new = df_tien_w21[df_tien_w21['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])]

output = []
output.append("=== TRẦM HỮU TIẾN W21 RAW ROWS ===")
output.append(df_tien_w21_new[['Chi tiết', 'Loại Hàng', 'Volume', '% Gán', '% GTC']].to_string())

output.append("\nCalculations on new cargo (Ca1 + Ca2):")
output.append(f"Simple average of % Gán: {df_tien_w21_new['% Gán'].mean()}")
output.append(f"Simple average of % GTC: {df_tien_w21_new['% GTC'].mean()}")

# Weighted average
vol_sum = df_tien_w21_new['Volume'].sum()
gan_sum = (df_tien_w21_new['Volume'] * df_tien_w21_new['% Gán']).sum()
gtc_sum = (df_tien_w21_new['Volume'] * df_tien_w21_new['% GTC']).sum()
output.append(f"Weighted average of % Gán: {gan_sum / vol_sum}")
output.append(f"Weighted average of % GTC: {gtc_sum / vol_sum}")

# What if including Hàng Tồn?
df_tien_w21_all = df_tien_w21.copy()
vol_sum_all = df_tien_w21_all['Volume'].sum()
gan_sum_all = (df_tien_w21_all['Volume'] * df_tien_w21_all['% Gán']).sum()
gtc_sum_all = (df_tien_w21_all['Volume'] * df_tien_w21_all['% GTC']).sum()
output.append("\nCalculations on ALL cargo (including Hàng Tồn):")
output.append(f"Simple average of % Gán (all): {df_tien_w21_all['% Gán'].mean()}")
output.append(f"Simple average of % GTC (all): {df_tien_w21_all['% GTC'].mean()}")
output.append(f"Weighted average of % Gán (all): {gan_sum_all / vol_sum_all}")
output.append(f"Weighted average of % GTC (all): {gtc_sum_all / vol_sum_all}")

# What if it's the average of the bưu cục averages?
# (first aggregate by bưu cục, then take average?)
bc_agg = df_tien_w21_new.groupby('Chi tiết').agg(
    vol=('Volume', 'sum'),
    vol_gan=('Volume', lambda x: (x * df_tien_w21_new.loc[x.index, '% Gán']).sum()),
    vol_gtc=('Volume', lambda x: (x * df_tien_w21_new.loc[x.index, '% GTC']).sum())
)
bc_agg['pct_gan'] = bc_agg['vol_gan'] / bc_agg['vol']
bc_agg['pct_gtc'] = bc_agg['vol_gtc'] / bc_agg['vol']
output.append("\nCalculations grouped by BC first, then simple average:")
output.append(f"Simple average of BC % Gán: {bc_agg['pct_gan'].mean()}")
output.append(f"Simple average of BC % GTC: {bc_agg['pct_gtc'].mean()}")

with open(r"c:\Users\lap4all\Desktop\New folder\formulas_check_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("Verification written to formulas_check_res.txt")
