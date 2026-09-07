import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
xls = pd.ExcelFile(file_path)

output_info = []

sheets_to_preview = [
    'dataGTC gốc full hàng', 
    'dataGTC gốc TTS', 
    'dataODRfull hàng ', 
    'dataODR TTS', 
    'dataLTC full hàng', 
    'dataLTC TTS', 
    'data rớt LC',
    'sản lượng', 
    'gtcnew',
    'ca2',
    'gtc + tồn',
    'cocau'
]

for sheet_name in sheets_to_preview:
    if sheet_name in xls.sheet_names:
        output_info.append(f"\n=========================================\nSHEET: {sheet_name}\n=========================================")
        # Read the first 10 rows without header mapping to see raw formatting
        df = pd.read_excel(xls, sheet_name=sheet_name, nrows=15)
        output_info.append(df.to_string())
    else:
        output_info.append(f"\nSheet '{sheet_name}' NOT FOUND in workbook.")

with open(r"c:\Users\lap4all\Desktop\New folder\user_sheets_preview.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_info))

print("Preview written to user_sheets_preview.txt")
