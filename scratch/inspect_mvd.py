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
    range="'MVĐ'!A1:O5",
    valueRenderOption='FORMULA'
).execute()
print("Formulas in MVĐ row 1-5:")
for i, r in enumerate(res_f.get('values', [])):
    print(f"Row {i+1}: {r}")

res_v = service.spreadsheets().values().get(
    spreadsheetId=source_id,
    range="'MVĐ'!A1:O10"
).execute()
print("\nValues in MVĐ row 1-10:")
for i, r in enumerate(res_v.get('values', [])):
    print(f"Row {i+1}: {r}")
