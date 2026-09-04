import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
target_sheet_id = "15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM"

res = service.spreadsheets().values().get(
    spreadsheetId=target_sheet_id,
    range="'RAW FD N-1 (HUB)'!A1:H10"
).execute()

rows = res.get('values', [])
print(f"Read {len(rows)} rows from RAW FD N-1 (HUB):")
for i, r in enumerate(rows):
    print(f"Row {i+1}: {r}")
