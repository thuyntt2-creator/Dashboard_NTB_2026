# -*- coding: utf-8 -*-
import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

excel_path = r'C:\Users\lap4all\Downloads\BaoCao_Tuan_NTB_W37_2026.xlsx'
wb = openpyxl.load_workbook(excel_path, data_only=True)
print("Sheets:", wb.sheetnames)

ws_tq = wb['00_Tong quan']
print("\n--- 00_Tong quan ---")
for r in range(1, 40):
    v = ws_tq.cell(r, 1).value
    if v:
        row_vals = [ws_tq.cell(r, c).value for c in range(1, 8)]
        print(f"Row {r}: {row_vals}")

odr_sheets = [s for s in wb.sheetnames if 'odr' in s.lower()]
print("\nODR sheets:", odr_sheets)
for s in odr_sheets:
    ws = wb[s]
    print(f"\n--- {s} (first 25 rows) ---")
    for r in range(1, 25):
        row_vals = [ws.cell(r, c).value for c in range(1, 10)]
        if any(row_vals):
            print(f"Row {r}: {row_vals}")
