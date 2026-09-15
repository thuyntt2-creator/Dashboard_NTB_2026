# -*- coding: utf-8 -*-
import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

try:
    wb = openpyxl.load_workbook(r'c:\Users\lap4all\Desktop\New folder\Bao_Cao_Hop_Van_Hanh_13h_NTB.xlsx', data_only=True)
    print("Sheets in 13h report:", wb.sheetnames)
except Exception as e:
    print("Error:", e)
