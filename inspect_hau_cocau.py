import pandas as pd

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df_ltc_full = pd.read_excel(file_path, sheet_name='dataLTC full hàng')
df_cocau = pd.read_excel(file_path, sheet_name='cocau')

# Filter cocau for Trần Công Hậu
df_hau_cocau = df_cocau[df_cocau['Am'].str.contains('Hậu', na=False, case=False)]

# Map Chi tiết to AM in LTC full for W21
df_w21 = df_ltc_full[df_ltc_full['Time'] == '2026/21'].copy()
mapping_df = df_cocau[['BC', 'Am']].dropna().drop_duplicates()
bc_to_am = dict(zip(mapping_df['BC'], mapping_df['Am']))
df_w21['AM_mapped'] = df_w21['Chi tiết'].map(bc_to_am)

output = []
output.append("=== TRẦN CÔNG HẬU IN COCAU ===")
output.append(df_hau_cocau.to_string())

output.append("\n=== TRẦN CÔNG HẬU ROWS IN W21 (MAPPED BY COCAU) ===")
df_hau_w21 = df_w21[df_w21['AM_mapped'].str.contains('Hậu', na=False, case=False)]
output.append(df_hau_w21[['Chi tiết', 'Volume', '%Gán', '%LTC']].to_string())

# Sum and weighted avg for Trần Công Hậu
v = df_hau_w21['Volume'].sum()
g = (df_hau_w21['Volume'] * df_hau_w21['%Gán']).sum() / v if v > 0 else 0
l = (df_hau_w21['Volume'] * df_hau_w21['%LTC']).sum() / v if v > 0 else 0
output.append(f"Calculated: Vol={v}, Gan={g}, LTC={l}")

# Let's search if there's any row in W21 that has %Gán = 0.6406 or %LTC = 0.6318
match_rows = df_w21[(df_w21['%Gán'] == 0.6406) | (df_w21['%LTC'] == 0.6318) | (df_w21['Volume'] == 6406)]
output.append("\n=== SEARCHING FOR 0.6406 or 0.6318 or Volume 6406 in df_w21 ===")
output.append(match_rows.to_string())

with open(r"c:\Users\lap4all\Desktop\New folder\hau_ltc_check.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("Results written to hau_ltc_check.txt")
