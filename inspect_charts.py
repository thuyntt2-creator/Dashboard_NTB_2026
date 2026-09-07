import gspread
from google.oauth2.service_account import Credentials
import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

JSON_FILE = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SHEET_ID = '1sTJEt8meKwVicbJAa8d7ml48yVoa_yD2_LAEbZ1ebGs'

creds = Credentials.from_service_account_file(
    JSON_FILE, 
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)

from google.auth.transport.requests import Request
creds.refresh(Request())

headers = {"Authorization": f"Bearer {creds.token}"}
# Fetch spreadsheet metadata (without grid data is very small)
url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}"
res = requests.get(url, headers=headers)
metadata = res.json()

print("Embedded Charts in Spreadsheet:")
for sheet in metadata.get('sheets', []):
    title = sheet.get('properties', {}).get('title', '')
    charts = sheet.get('charts', [])
    if charts:
        print(f"\nSheet: '{title}' has {len(charts)} chart(s):")
        for idx, chart in enumerate(charts):
            spec = chart.get('spec', {})
            print(f"  Chart {idx+1} (ID: {chart.get('chartId')}):")
            print(f"    Title: {spec.get('title')}")
            print(f"    Type: {list(spec.keys())}")
    else:
        print(f"Sheet: '{title}' - No charts.")
