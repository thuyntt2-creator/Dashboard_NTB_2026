import sys
sys.stdout.reconfigure(encoding='utf-8')
import gspread
from google.oauth2.credentials import Credentials
import json, os

with open('authorized_user.json', 'r') as f:
    creds_data = json.load(f)

creds = Credentials(
    token=creds_data.get('token'),
    refresh_token=creds_data.get('refresh_token'),
    token_uri=creds_data.get('token_uri'),
    client_id=creds_data.get('client_id'),
    client_secret=creds_data.get('client_secret'),
    scopes=creds_data.get('scopes')
)

gc = gspread.authorize(creds)
SHEET_ID = '1rfoi8QaZSZNiYf8IyKNN4QLrjAVxCCGrX9Yli0D8T84'
sh = gc.open_by_key(SHEET_ID)

# Check "Tong quan L3D" and "Theo Kho" for current week data
sheets_to_check = ['Tong quan L3D', 'Theo Kho (8N & 8T)', 'Ngay & Nhom (8N)', 'Bao cao Tuan', 'Tuan 35']

for sname in sheets_to_check:
    try:
        ws = sh.worksheet(sname)
        data = ws.get_all_values()
        print(f'\n=== Sheet: {sname} ({len(data)} rows) ===')
        for i, row in enumerate(data[:25]):
            if any(c.strip() for c in row):
                print(f'  Row {i+1}: {row[:8]}')
    except Exception as e:
        print(f'Error with {sname}: {e}')
