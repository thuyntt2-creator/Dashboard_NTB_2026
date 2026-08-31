import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df_ltc_full = pd.read_excel(excel_path, sheet_name='dataLTC full hàng')

print("Columns in dataLTC full hàng:")
print(list(df_ltc_full.columns))

# Check cocau mapping
df_cocau = pd.read_excel(excel_path, sheet_name='cocau')
df_cocau['BC_norm'] = df_cocau['BC'].str.strip().str.upper()
bc_to_tinh = dict(zip(df_cocau['BC_norm'], df_cocau['Tỉnh']))

df_ltc_full['BC_norm'] = df_ltc_full['Chi tiết'].str.strip().str.upper()
df_ltc_full['Tỉnh_mapped'] = df_ltc_full['BC_norm'].map(bc_to_tinh)

# We also fill province from ql for missing ones
def get_province_from_ql(ql):
    ql_str = str(ql)
    if 'Đắk Nông' in ql_str or 'Đăk Nông' in ql_str: return 'Đắk Nông'
    if 'Bình Thuận' in ql_str: return 'Bình Thuận'
    if 'Khánh Hòa' in ql_str: return 'Khánh Hòa'
    if 'Lâm Đồng' in ql_str: return 'Lâm Đồng'
    if 'Ninh Thuận' in ql_str: return 'Ninh Thuận'
    return None

# Find column that contains 'Quản lý'
ql_col = [c for c in df_ltc_full.columns if 'quản lý' in str(c).lower() or 'quan ly' in str(c).lower()]
if ql_col:
    print(f"Using column '{ql_col[0]}' for 'Quản lý'")
    df_ltc_full['Tỉnh_mapped_ql'] = df_ltc_full[ql_col[0]].apply(get_province_from_ql)
    df_ltc_full['Tỉnh_mapped'] = df_ltc_full['Tỉnh_mapped'].fillna(df_ltc_full['Tỉnh_mapped_ql'])
else:
    print("No column found for 'Quản lý'")

# Filter out Grand Total
cap_col = [c for c in df_ltc_full.columns if 'cấp quản lý' in str(c).lower() or 'cap quan ly' in str(c).lower()]
if cap_col:
    df_w24 = df_ltc_full[(df_ltc_full['Time'] == '2026/24') & (df_ltc_full[cap_col[0]] != 'Grand Total')].copy()
else:
    df_w24 = df_ltc_full[(df_ltc_full['Time'] == '2026/24')].copy()

# Print columns to make sure they are read correctly
for col in ['Volume', '%Gán', '%LTC']:
    actual_col = [c for c in df_w24.columns if str(c).lower() == col.lower()]
    if actual_col:
        df_w24[col] = pd.to_numeric(df_w24[actual_col[0]], errors='coerce')

df_w24['Vol_Gan'] = df_w24['Volume'] * df_w24['%Gán']
df_w24['Vol_LTC'] = df_w24['Volume'] * df_w24['%LTC']

prov_grp = df_w24.groupby('Tỉnh_mapped').agg(
    v_tot=('Volume', 'sum'),
    v_gan=('Vol_Gan', 'sum'),
    v_ltc=('Vol_LTC', 'sum')
).reset_index()

prov_grp['LTC_tot'] = prov_grp['v_ltc'] / prov_grp['v_tot']
prov_grp['LTC_gan'] = prov_grp['v_ltc'] / prov_grp['v_gan']

print("\nProvince W24 LTC rates comparison:")
print(f"{'Province':<15} | {'Vol_LTC / Volume':<20} | {'Vol_LTC / Vol_Gan':<20}")
print("-" * 65)
for _, r in prov_grp.iterrows():
    print(f"{r['Tỉnh_mapped']:<15} | {r['LTC_tot']*100:18.2f}% | {r['LTC_gan']*100:18.2f}%")
