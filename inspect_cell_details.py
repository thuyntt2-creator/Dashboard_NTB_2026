import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')
INPUT_EXCEL = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"

wb = openpyxl.load_workbook(INPUT_EXCEL, data_only=False)

for sheet_name in ['sản lượng', 'gtcnew', 'gtc + tồn', 'ca2', 'LTC', 'ODR']:
    ws = wb[sheet_name]
    print(f"\n=== Sheet: {sheet_name} ===")
    
    # Print row 23/24 cell details
    for r in range(23, 29):
        if r <= ws.max_row:
            row_vals = [f"Col{c}: {ws.cell(row=r, column=c).value}" for c in range(1, 15) if ws.cell(row=r, column=c).value is not None]
            if row_vals:
                print(f"Row {r}: {row_vals}")
