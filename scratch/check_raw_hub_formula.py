import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
source_id = "15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM"

res_f = service.spreadsheets().values().get(
    spreadsheetId=source_id,
    range="'RAW FD N-1 (HUB)'!A1:G5",
    valueRenderOption='FORMULA'
).execute()

print("Formulas in RAW FD N-1 (HUB):")
for i, r in enumerate(res_f.get('values', [])):
    print(f"Row {i+1}: {r}")
