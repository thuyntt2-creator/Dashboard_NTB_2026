import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('BaoCao_Tuan_NTB_W40_2026.xlsx', data_only=True)
ws = wb['03b_GTC Ca1 thuan']

print("=== CHECK SHEET 03b_GTC Ca1 thuan ROWS 33 TO 56 ===")
for r in range(33, 56):
    row_vals = [str(ws.cell(r, c).value or '')[:20] for c in range(1, 10)]
    print(f"Row {r:2d}: {row_vals}")
