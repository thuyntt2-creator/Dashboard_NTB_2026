import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('BaoCao_Tuan_NTB_W40_2026.xlsx', data_only=True)

def dump_sheet_clean(sheet_name, start_r, end_r, max_c=8):
    ws = wb[sheet_name]
    print(f"\n--- {sheet_name} (Rows {start_r} to {end_r}) ---")
    for r in range(start_r, end_r + 1):
        vals = [ws.cell(r, c).value for c in range(1, max_c + 1)]
        if any(vals):
            vals_str = [f"{v:.4f}" if isinstance(v, float) else f"{v}" for v in vals if v is not None]
            print(f"R{r:02d}: " + " | ".join(vals_str))

# Sheet 07_Gan:
dump_sheet_clean('07_Gan', 4, 32, 8)
# Sheet 05_ODR:
dump_sheet_clean('05_ODR', 4, 32, 8)
