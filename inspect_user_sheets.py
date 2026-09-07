import pandas as pd
import sys

# Set standard output encoding to utf-8 if possible
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
xls = pd.ExcelFile(file_path)

output_info = []
output_info.append(f"Workbook: {file_path}")
output_info.append(f"Number of sheets: {len(xls.sheet_names)}")
output_info.append("Sheets and their columns:")

for sheet_name in xls.sheet_names:
    output_info.append(f"\n--- Sheet: {sheet_name} ---")
    try:
        # read first 2 rows
        df = pd.read_excel(xls, sheet_name=sheet_name, nrows=2)
        output_info.append(f"Columns: {list(df.columns)}")
        output_info.append(f"Shape: {df.shape}")
    except Exception as e:
        output_info.append(f"Error reading: {e}")

with open(r"c:\Users\lap4all\Desktop\New folder\user_sheets_info.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_info))

print("Inspection completed. Saved to user_sheets_info.txt")
