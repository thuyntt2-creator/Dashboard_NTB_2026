import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

# 1. Check Snapshot in 15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM
res1 = service.spreadsheets().values().get(
    spreadsheetId='15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM',
    range="'Snapshot – FD N-1 (HUB)'!A4:G8"
).execute()
print("15Z (source) values:")
for r in res1.get('values', []):
    print(" ", r)

# 2. Check FD in 1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ
res2 = service.spreadsheets().values().get(
    spreadsheetId='1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ',
    range="'FD '!A4:G8"
).execute()
print("\n1JZ (consolidated) values:")
for r in res2.get('values', []):
    print(" ", r)
