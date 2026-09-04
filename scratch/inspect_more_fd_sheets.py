import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
source_id = "15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM"

for title in ['Raw FD_Tổng', 'RAW FD_TTS', 'Snapshot – FD Tổng', 'MVĐ']:
    try:
        res = service.spreadsheets().values().get(
            spreadsheetId=source_id,
            range=f"'{title}'!A1:N5"
        ).execute()
        print(f"\n=== Sheet '{title}' ===")
        for i, r in enumerate(res.get('values', [])):
            print(f"Row {i+1}: {r}")
    except Exception as e:
        print(f"Error reading {title}: {e}")
