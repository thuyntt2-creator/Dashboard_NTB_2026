import pandas as pd

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df_ltc_full = pd.read_excel(file_path, sheet_name='dataLTC full hàng')
df_cocau = pd.read_excel(file_path, sheet_name='cocau')

# Check raw rows in dataLTC full where Time is 2026/21
df_w21 = df_ltc_full[df_ltc_full['Time'] == '2026/21'].copy()

# Map to AM using cocau
mapping_df = df_cocau[['BC', 'Am']].dropna().drop_duplicates()
bc_to_am = dict(zip(mapping_df['BC'], mapping_df['Am']))

df_w21['AM_mapped'] = df_w21['Chi tiết'].map(bc_to_am)

# Find all rows that mention 'Lâm Đồng' in Cấp quản lý or Chi tiết
df_ld = df_w21[df_w21['Cấp quản lý'].str.contains('Lâm Đồng', na=False) | df_w21['Chi tiết'].str.contains('Lâm Đồng', na=False)].copy()
df_ld['AM_mapped'] = df_ld['Chi tiết'].map(bc_to_am)

output = []
output.append("Unique Cấp quản lý in W21: " + str(df_w21['Cấp quản lý'].unique().tolist()))

output.append("\n=== LÂM ĐỒNG ROWS IN W21 ===")
output.append(df_ld[['Chi tiết', 'Volume', '%Gán', '%LTC', 'AM_mapped']].to_string())

output.append("\n=== MAPPED TO HỒNG BÍCH NGA ===")
df_nga_mapped = df_w21[df_w21['AM_mapped'] == 'Hồng Bích Nga']
output.append(df_nga_mapped[['Chi tiết', 'Volume', '%Gán', '%LTC']].to_string())

# Calculate weighted average for mapped rows
vol_sum = df_nga_mapped['Volume'].sum()
gan_sum = (df_nga_mapped['Volume'] * df_nga_mapped['%Gán']).sum()
ltc_sum = (df_nga_mapped['Volume'] * df_nga_mapped['%LTC']).sum()
output.append(f"\nCalculated from MAPPED rows:")
output.append(f"Volume: {vol_sum}")
output.append(f"Weighted average %Gán: {gan_sum / vol_sum if vol_sum > 0 else 0}")
output.append(f"Weighted average %LTC: {ltc_sum / vol_sum if vol_sum > 0 else 0}")

# Let's see if there is any row matching 'Hồng Bích Nga' (with different unicode normalization)
# The AM name in cocau might have different unicode normalization (e.g. 'Hồng Bích Nga' vs 'Hồng Bích Nga')
# Let's inspect unique AM values in cocau
unique_ams = df_cocau['Am'].dropna().unique().tolist()
output.append("\nUnique AMs in cocau: " + str(unique_ams))

with open(r"c:\Users\lap4all\Desktop\New folder\inspect_nga_ltc_rows_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("Verification written to inspect_nga_ltc_rows_res.txt")
