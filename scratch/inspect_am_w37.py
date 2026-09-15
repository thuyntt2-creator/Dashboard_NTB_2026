# -*- coding: utf-8 -*-
import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook(r'C:\Users\lap4all\Downloads\BaoCao_AM_W37_2026.xlsx', data_only=True)
print("Sheets in BaoCao_AM_W37_2026.xlsx:", wb.sheetnames)
for s in wb.sheetnames:
    if 'odr' in s.lower() or 'tong quan' in s.lower() or 'sl' in s.lower() or 'kpi' in s.lower():
        ws = wb[s]
        print(f"\n--- {s} (rows 1-15) ---")
        for r in range(1, min(ws.max_row + 1, 15)):
            row_v = [ws.cell(r, c).value for c in range(1, min(ws.max_column + 1, 10))]
            if any(row_v):
                print(f"Row {r}: {row_v}")
