import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
source_id = "15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM"

meta = service.spreadsheets().get(spreadsheetId=source_id).execute()
for s in meta['sheets']:
    p = s['properties']
    title = p['title']
    res = service.spreadsheets().values().get(
        spreadsheetId=source_id,
        range=f"'{title}'!A1:D3"
    ).execute()
    vals = res.get('values', [])
    print(f"[{title}] rows: {p.get('gridProperties', {}).get('rowCount')}, cols: {p.get('gridProperties', {}).get('columnCount')}")
    if vals:
        print("   sample:", vals[0] if len(vals) > 0 else "")
