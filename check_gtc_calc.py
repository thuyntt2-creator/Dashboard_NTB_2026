import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df_gtc_full = pd.read_excel(file_path, sheet_name='dataGTC gốc full hàng')
df_cocau = pd.read_excel(file_path, sheet_name='cocau')
df_gtcnew = pd.read_excel(file_path, sheet_name='gtcnew')

mapping_df = df_cocau[['BC', 'Am']].dropna().drop_duplicates()
bc_to_am = dict(zip(mapping_df['BC'], mapping_df['Am']))
df_gtc_full['AM'] = df_gtc_full['Chi tiết'].map(bc_to_am)

# Filter for new cargo (Ca1 + Ca2)
df_new = df_gtc_full[df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])].copy()

# Calculate helper columns
df_new['Vol_Gan'] = df_new['Volume'] * df_new['% Gán']
df_new['Vol_GTC'] = df_new['Volume'] * df_new['% GTC']

# Group by AM and Time
grouped = df_new.groupby(['AM', 'Time']).agg(
    Total_Vol=('Volume', 'sum'),
    Total_Vol_Gan=('Vol_Gan', 'sum'),
    Total_Vol_GTC=('Vol_GTC', 'sum')
).reset_index()

grouped['Pct_Gan'] = grouped['Total_Vol_Gan'] / grouped['Total_Vol']
grouped['Pct_GTC'] = grouped['Total_Vol_GTC'] / grouped['Total_Vol']

# Pivot to match gtcnew layout
pivot_gan = grouped.pivot(index='AM', columns='Time', values='Pct_Gan')
pivot_gtc = grouped.pivot(index='AM', columns='Time', values='Pct_GTC')

output = []
output.append("=== CALCULATED %GÁN ===")
output.append(pivot_gan.to_string())
output.append("\n=== CALCULATED %GTC ===")
output.append(pivot_gtc.to_string())

# Show first few rows of gtcnew sheet
output.append("\n=== gtcnew sheet data (first 5 rows) ===")
output.append(df_gtcnew.head(10).to_string())

with open(r"c:\Users\lap4all\Desktop\New folder\check_gtc_calc_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("Verification written to check_gtc_calc_res.txt")
