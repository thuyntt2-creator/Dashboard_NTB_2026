import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

source_sheet_id = "1odUPX5mWpUYUUQOrhX_k8kXWV7drMUdQ58DRwgSQNS8"
try:
    meta = service.spreadsheets().get(spreadsheetId=source_sheet_id).execute()
    print("Master FD title:", meta.get('properties', {}).get('title'))
    for s in meta.get('sheets', []):
        print(f"  Sheet: {s.get('properties', {}).get('title')} (id: {s.get('properties', {}).get('sheetId')})")
    
    res = service.spreadsheets().values().get(
        spreadsheetId=source_sheet_id,
        range="'FD'!A1:K10"
    ).execute()
    rows = res.get('values', [])
    print(f"\nRows in 'FD' sheet of Master FD ({len(rows)} rows):")
    for i, r in enumerate(rows):
        print(f"Row {i+1}: {r}")

except Exception as e:
    print(f"Error accessing Master FD: {e}")
