import requests
import re
import os
import pandas as pd

url = "https://docs.google.com/spreadsheets/d/1OygEPTn6Qu8okwAqpbx_RBiYQr1cfpO5hiaxqu4AMNE/edit?gid=872540531#gid=872540531"
output_path = r"c:\Users\lap4all\Desktop\New folder\vols_tao_don.xlsx"

match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
if match:
    spreadsheet_id = match.group(1)
    export_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx"
    print(f"Export URL: {export_url}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        }
        response = requests.get(export_url, headers=headers, timeout=60)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print("Downloaded successfully to vols_tao_don.xlsx")
            
            # Inspect the sheet names
            xls = pd.ExcelFile(output_path)
            print(f"Sheet names: {xls.sheet_names}")
            for sheet in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet, nrows=5)
                print(f"Sheet '{sheet}' shape: {df.shape}, Columns: {list(df.columns)}")
        else:
            print(f"Failed to download. HTTP status: {response.status_code}")
    except Exception as e:
        print(f"Error downloading: {e}")
else:
    print("Invalid URL format")
