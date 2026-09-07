import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')
INPUT_EXCEL = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"

wb = openpyxl.load_workbook(INPUT_EXCEL, data_only=False)

for sheet_name in ['gtc + tồn', 'ca2', 'LTC']:
    ws = wb[sheet_name]
    print(f"\n=== Sheet: {sheet_name} ===")
    for r in range(40, 48):
        row_vals = []
        for c in range(1, 10):
            cell = ws.cell(row=r, column=c)
            row_vals.append(f"Col{c}: {cell.value}")
        print(f"Row {r}: {row_vals}")
