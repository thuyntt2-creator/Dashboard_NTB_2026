import openpyxl
import sys
sys.stdout.reconfigure(encoding='utf-8')
excel_path = r"c:\Users\lap4all\Desktop\New folder\NTB_Bao_Cao_Van_Hanh_Corrected.xlsx"
wb = openpyxl.load_workbook(excel_path, read_only=True)
print("Sheet names in NTB_Bao_Cao_Van_Hanh_Corrected.xlsx:")
print(wb.sheetnames)
