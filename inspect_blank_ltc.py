import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')
INPUT_EXCEL = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"

print("Reading 'dataLTC full hàng'...")
df_ltc_full = pd.read_excel(INPUT_EXCEL, sheet_name='dataLTC full hàng')

# Check nulls or empty spaces
blank_rows = df_ltc_full[df_ltc_full['Chi tiết'].isna() | (df_ltc_full['Chi tiết'].astype(str).str.strip() == '')]
print(f"Total blank/null post office rows: {len(blank_rows)}")
print("\nPreview of blank rows (first 10):")
print(blank_rows.head(10))

print("\nValue counts of non-blank 'Chi tiết' values:")
print(df_ltc_full['Chi tiết'].value_counts().head(20))
