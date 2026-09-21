import sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

work_id = '15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM'
res = service.spreadsheets().values().get(
    spreadsheetId=work_id,
    range="'Top 10 FD (T2-Gio)'!A1:Z50"
).execute()

rows = res.get('values', [])
print(f"Total rows read: {len(rows)}")
for i, r in enumerate(rows):
    print(f"R{i+1}: {r}")

# Check formula as well
res_f = service.spreadsheets().values().get(
    spreadsheetId=work_id,
    range="'Top 10 FD (T2-Gio)'!A1:Z10",
    valueRenderOption='FORMULA'
).execute()
print("\nFormulas:")
for i, r in enumerate(res_f.get('values', [])):
    print(f"F{i+1}: {r}")
