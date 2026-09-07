import pandas as pd

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df_odr_full = pd.read_excel(file_path, sheet_name='dataODRfull hàng ')
df_odr_tts = pd.read_excel(file_path, sheet_name='dataODR TTS')

# We need to map Chi tiết to Tỉnh
# Let's extract BC to Tỉnh mapping from cocau
df_cocau = pd.read_excel(file_path, sheet_name='cocau')
bc_to_tinh = dict(zip(df_cocau['BC'].str.strip(), df_cocau['Tỉnh'].str.strip()))

# Clean sheet names and match
df_odr_full['BC_clean'] = df_odr_full['Chi tiết'].str.strip()
df_odr_tts['BC_clean'] = df_odr_tts['Chi tiết'].str.strip()

df_odr_full['Tỉnh'] = df_odr_full['BC_clean'].map(bc_to_tinh)
df_odr_tts['Tỉnh'] = df_odr_tts['BC_clean'].map(bc_to_tinh)

# What about unmatched bưu cục?
# Let's check if there are unmatched ones
unmatched_full = df_odr_full[df_odr_full['Tỉnh'].isna()]['BC_clean'].unique()
unmatched_tts = df_odr_tts[df_odr_tts['Tỉnh'].isna()]['BC_clean'].unique()

print(f"Unmatched full: {len(unmatched_full)}")
print(f"Unmatched tts: {len(unmatched_tts)}")

# Let's check: can we extract province from 'Quản lý'?
# 'NTB - Đắk Nông' -> 'Đắk Nông'
# Let's define a function to get province from Quản lý if Tỉnh mapping is missing
def get_prov(row):
    if pd.notna(row['Tỉnh']):
        return row['Tỉnh']
    ql = str(row['Quản lý'])
    if 'Đắk Nông' in ql: return 'Đắk Nông'
    if 'Bình Thuận' in ql: return 'Bình Thuận'
    if 'Khánh Hòa' in ql: return 'Khánh Hòa'
    if 'Lâm Đồng' in ql: return 'Lâm Đồng'
    if 'Ninh Thuận' in ql: return 'Ninh Thuận'
    return None

df_odr_full['Tỉnh_final'] = df_odr_full.apply(get_prov, axis=1)
df_odr_tts['Tỉnh_final'] = df_odr_tts.apply(get_prov, axis=1)

# Calculate weighted average ODR by Tỉnh and Time
# Vol = GTC column
df_odr_full['Vol_Ontime'] = df_odr_full['GTC'] * df_odr_full['%Ontime']
df_odr_tts['Vol_Ontime'] = df_odr_tts['GTC'] * df_odr_tts['%Ontime']

grouped_full = df_odr_full.groupby(['Tỉnh_final', 'Time']).agg(
    Total_Vol=('GTC', 'sum'),
    Total_Ontime=('Vol_Ontime', 'sum')
).reset_index()
grouped_full['ODR'] = grouped_full['Total_Ontime'] / grouped_full['Total_Vol']

grouped_tts = df_odr_tts.groupby(['Tỉnh_final', 'Time']).agg(
    Total_Vol=('GTC', 'sum'),
    Total_Ontime=('Vol_Ontime', 'sum')
).reset_index()
grouped_tts['ODR'] = grouped_tts['Total_Ontime'] / grouped_tts['Total_Vol']

pivot_full = grouped_full.pivot(index='Tỉnh_final', columns='Time', values='ODR')
pivot_tts = grouped_tts.pivot(index='Tỉnh_final', columns='Time', values='ODR')

output = []
output.append("=== CALCULATED ODR FULL ===")
output.append(pivot_full.to_string())
output.append("\n=== CALCULATED ODR TTS ===")
output.append(pivot_tts.to_string())

with open(r"c:\Users\lap4all\Desktop\New folder\check_odr_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("ODR calculations written.")
