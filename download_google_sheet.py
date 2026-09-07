import urllib.request
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://docs.google.com/spreadsheets/d/1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU/export?format=xlsx"
output_file = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"

req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

print("Starting download...")
try:
    with urllib.request.urlopen(req) as response:
        with open(output_file, 'wb') as out_file:
            out_file.write(response.read())
    print(f"Successfully downloaded to {output_file}")
    
    # Let's inspect the sheets in the downloaded file
    import pandas as pd
    xls = pd.ExcelFile(output_file)
    print("Sheets present:")
    for name in xls.sheet_names:
        print(f" - {name}")
except Exception as e:
    print(f"Error occurred: {e}")
