import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('BaoCao_Tuan_NTB_W37_2026.xlsx', data_only=True)

for sheetname in ['07_Gan', '05_ODR', '08_OPR TTS']:
    print(f"\n================ SHEET: {sheetname} ================")
    ws = wb[sheetname]
    for r in range(1, 35):
        row_vals = [ws.cell(r, c).value for c in range(1, 15)]
        if any(v is not None for v in row_vals):
            # clean display
            clean = [str(v) if v is not None else '' for v in row_vals]
            print(f"Row {r:2d}: " + " | ".join(clean[:10]))
