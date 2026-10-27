import openpyxl, os, sys
sys.stdout.reconfigure(encoding='utf-8')

for fname in ['BaoCao_Tuan_NTB_W43_2026.xlsx', 'BaoCao_AM_W43_2026.xlsx']:
    if os.path.exists(fname):
        wb = openpyxl.load_workbook(fname, read_only=True)
        print(f"{fname} sheets:", wb.sheetnames)
