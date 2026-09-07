import gspread
from google.oauth2.service_account import Credentials
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

JSON_FILE = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SHEET_ID = '1sTJEt8meKwVicbJAa8d7ml48yVoa_yD2_LAEbZ1ebGs'

creds = Credentials.from_service_account_file(
    JSON_FILE, 
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)

# Fetch token
from google.auth.transport.requests import Request
import requests
creds.refresh(Request())

print("Fetching full spreadsheet details from Google API via requests...")
headers = {"Authorization": f"Bearer {creds.token}"}
# Fetch only the pivot sheets grid data to save bandwidth and speed up the response
url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}?ranges=Bảng tổng hợp 1!A1:Z50&ranges=Bảng tổng hợp 3!A1:Z50&ranges=Bảng tổng hợp 5!A1:Z50&ranges=Bảng tổng hợp 6!A1:Z50&includeGridData=true"
res = requests.get(url, headers=headers)
metadata = res.json()

# Save to local file
out_file = r'C:\Users\lap4all\.gemini\antigravity-ide\scratch\spreadsheet_full_metadata.json'
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print("Saved metadata to:", out_file)

# Let's inspect the sheets and find any pivot tables in them
for sheet in metadata.get('sheets', []):
    title = sheet.get('properties', {}).get('title', '')
    print(f"\nSheet: '{title}'")
    # Pivot tables are in sheet['data'][...] if we request it, or sheet['pivots']
    # Actually, in Sheets API v4, pivot tables are defined inside the grid cells!
    # They are in rowData -> values -> pivotTable
    row_data = sheet.get('data', [{}])[0].get('rowData', [])
    found_pivot = False
    for r_idx, row in enumerate(row_data):
        for c_idx, cell in enumerate(row.get('values', [])):
            if 'pivotTable' in cell:
                found_pivot = True
                pt = cell['pivotTable']
                print(f"  -> Found Pivot Table at Row {r_idx+1}, Col {c_idx+1}!")
                print(f"     Source: Sheet ID {pt.get('source', {}).get('sheetId')}, "
                      f"Range: Row {pt.get('source', {}).get('startRowIndex')}-{pt.get('source', {}).get('endRowIndex')}, "
                      f"Col {pt.get('source', {}).get('startColumnIndex')}-{pt.get('source', {}).get('endColumnIndex')}")
                print(f"     Rows: {pt.get('rows', [])}")
                print(f"     Columns: {pt.get('columns', [])}")
                print(f"     Values: {pt.get('values', [])}")
                print(f"     Criteria/Filters: {pt.get('criteria', {})}")
    if not found_pivot:
        print("  No Pivot Tables found directly in this sheet's cell metadata.")
