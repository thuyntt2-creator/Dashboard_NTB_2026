import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')
INPUT_EXCEL = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"

df_cocau = pd.read_excel(INPUT_EXCEL, sheet_name='cocau')
print("=== AM - Province Mapping in cocau Sheet ===")
# Group by Am and Tỉnh to see the relationship
am_prov = df_cocau.groupby(['Am', 'Tỉnh']).size().reset_index(name='BC_count')
print(am_prov)

print("\n=== Unique Provinces per AM ===")
for am, group in am_prov.groupby('Am'):
    prov_list = group['Tỉnh'].tolist()
    print(f"AM '{am}' manages post offices in: {prov_list}")
