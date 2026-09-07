import urllib.request
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

sheet_id = "1x8MxOZV0wMFi7NmXlMaxjBbWjr6zyylUE2rjI4votmw"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
output_file = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet_2.xlsx"

req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

print("Starting download for new sheet ID:", sheet_id)
try:
    with urllib.request.urlopen(req) as response:
        with open(output_file, 'wb') as out_file:
            out_file.write(response.read())
    print(f"Successfully downloaded to {output_file}")
    
    # Check sheets inside it
    import openpyxl
    wb = openpyxl.load_workbook(output_file, read_only=True, data_only=True)
    print("Sheets inside the workbook:", wb.sheetnames)
    wb.close()
except Exception as e:
    print(f"Error occurred: {e}")
