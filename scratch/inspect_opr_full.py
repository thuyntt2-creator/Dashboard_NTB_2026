import openpyxl

wb = openpyxl.load_workbook('BaoCao_Tuan_NTB_W38_2026.xlsx', data_only=True)
ws = wb['08_OPR TTS']

print("=== SHEET 08_OPR TTS INSPECTION ===")
for r in range(1, 35):
    row_vals = [ws.cell(r, c).value for c in range(1, 16)]
    if any(row_vals):
        print(f"Row {r:2d}: {row_vals}")
