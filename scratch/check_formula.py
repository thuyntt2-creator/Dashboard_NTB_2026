import sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

work_id = '15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM'
res = service.spreadsheets().values().get(
    spreadsheetId=work_id,
    range="'RAW FD N-1 (HUB)'!A1:A3",
    valueRenderOption='FORMULA'
).execute()
print("Formulas:", res.get('values', []))
