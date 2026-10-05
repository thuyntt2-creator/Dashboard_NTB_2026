import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('BaoCao_Tuan_NTB_W40_2026.xlsx', data_only=True)
ws = wb['01_San luong']

print("=== CHECK 01_San luong ===")
for r in range(10, 56):
    c1 = str(ws.cell(r, 1).value or '').strip()
    if c1:
        print(f"Row {r:2d}: {c1}")
