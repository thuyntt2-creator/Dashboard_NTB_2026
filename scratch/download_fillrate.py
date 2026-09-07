import sys
sys.stdout.reconfigure(encoding='utf-8')
import gspread
from google.oauth2.credentials import Credentials
import json, os

# Load credentials
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

# Fill rate sheet
SHEET_ID = '1rfoi8QaZSZNiYf8IyKNN4QLrjAVxCCGrX9Yli0D8T84'
GID = '1126040883'

try:
    sh = gc.open_by_key(SHEET_ID)
    print("Workbook sheets:")
    for ws in sh.worksheets():
        print(f"  - {ws.title} (gid={ws.id})")
    
    # Try to get the specific sheet
    target = None
    for ws in sh.worksheets():
        if str(ws.id) == GID:
            target = ws
            break
    
    if target:
        print(f"\nSheet: {target.title}")
        data = target.get_all_values()
        print(f"Rows: {len(data)}")
        for i, row in enumerate(data[:30]):
            print(f"Row {i+1}: {row}")
    else:
        print(f"Sheet with gid={GID} not found")
        # Try first sheet
        ws = sh.sheet1
        data = ws.get_all_values()
        print(f"Sheet1: {ws.title}, rows: {len(data)}")
        for i, row in enumerate(data[:20]):
            print(f"Row {i+1}: {row}")
            
except Exception as e:
    print(f"Error: {e}")
