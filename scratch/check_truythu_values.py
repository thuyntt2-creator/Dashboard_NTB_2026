import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
sheet_id = '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

# Fetch unformatted values
res_unformatted = service.spreadsheets().values().get(
    spreadsheetId=sheet_id, 
    range="'truythu'!A1:Q15",
    valueRenderOption='UNFORMATTED_VALUE'
).execute()

# Fetch formatted values
res_formatted = service.spreadsheets().values().get(
    spreadsheetId=sheet_id, 
    range="'truythu'!A1:Q15",
    valueRenderOption='FORMATTED_VALUE'
).execute()

print("--- UNFORMATTED VALUES (first 5 rows) ---")
for r in res_unformatted.get('values', [])[:5]:
    print(r)

print("\n--- FORMATTED VALUES (first 5 rows) ---")
for r in res_formatted.get('values', [])[:5]:
    print(r)
