import sys
sys.stdout.reconfigure(encoding='utf-8')
import urllib.request
import openpyxl

SHEET_VAN_HANH_ID = "1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_VAN_HANH_ID}/export?format=xlsx"
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0')
with urllib.request.urlopen(req) as response:
    with open("temp_debug.xlsx", 'wb') as f:
        f.write(response.read())

wb = openpyxl.load_workbook("temp_debug.xlsx", read_only=True)
print("Sheetnames of Báo cáo vận hành:", wb.sheetnames)

import os
wb.close()
if os.path.exists("temp_debug.xlsx"):
    os.remove("temp_debug.xlsx")
