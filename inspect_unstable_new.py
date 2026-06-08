import pandas as pd
import requests
import re

url = "https://docs.google.com/spreadsheets/d/1lmQv8KwHJzDFs_RMz64ydu4SOmG3M1YAzILNFGtzFec/edit?gid=250113221#gid=250113221"
match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
spreadsheet_id = match.group(1)
export_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx"

print("Downloading spreadsheet...")
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(export_url, headers=headers, timeout=60)
if response.status_code == 200:
    filename = "inspect_bat_on_new.xlsx"
    with open(filename, 'wb') as f:
        f.write(response.content)
    print("Downloaded successfully.")
    
    xls = pd.ExcelFile(filename)
    print("Sheet names:", xls.sheet_names)
    
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        print(f"\n--- Sheet: {sheet} ---")
        print("Columns:", list(df.columns))
        print("Shape:", df.shape)
        print("First 5 rows:")
        print(df.head(5))
else:
    print(f"Failed to download: {response.status_code}")
