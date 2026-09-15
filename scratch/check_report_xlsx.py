# -*- coding: utf-8 -*-
import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r'C:\Users\lap4all\Downloads\report.xlsx'
wb = openpyxl.load_workbook(file_path, read_only=True)
print("Sheets in report.xlsx:")
for s in wb.sheetnames:
    print(f"  - {s}")
