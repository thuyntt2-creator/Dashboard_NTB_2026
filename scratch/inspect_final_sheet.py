import sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

res = service.spreadsheets().values().get(
    spreadsheetId='15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM',
    range="'Snapshot – FD N-1 (HUB)'!A1:I25"
).execute()

for i, r in enumerate(res.get('values', [])):
    print(f'R{i+1}: {r}')
