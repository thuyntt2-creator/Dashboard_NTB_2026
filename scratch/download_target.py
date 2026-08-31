import urllib.request
import os
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

sheet_id = "12VsqpIx1vLOqk6-JKHwgRmdrgu6fxSNPQcpyO0wpvdQ"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
output_file = r"c:\Users\lap4all\Desktop\New folder\scratch\downloaded_check_sheet.xlsx"

req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

print("Starting download for sheet ID:", sheet_id)
try:
    with urllib.request.urlopen(req) as response:
        with open(output_file, 'wb') as out_file:
            out_file.write(response.read())
    print(f"Successfully downloaded to {output_file}")
    
    xls = pd.ExcelFile(output_file)
    print("Sheets present in downloaded file:")
    for name in xls.sheet_names:
        print(f" - {name}")
except Exception as e:
    print(f"Error occurred: {e}")
