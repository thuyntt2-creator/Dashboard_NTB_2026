import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
source_id = "15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM"

# Read all of RAW FD N-1 (HUB)
res = service.spreadsheets().values().get(
    spreadsheetId=source_id,
    range="'RAW FD N-1 (HUB)'!A1:Z5000"
).execute()

rows = res.get('values', [])
print(f"Total rows in RAW FD N-1 (HUB): {len(rows)}")
if rows:
    print("Header:", rows[0])
    for r in rows[1:10]:
        print(r)

# Check if there are other columns in RAW FD N-1 (HUB)
# e.g. column H, I, J, K...
# Look at row 1 length
print("Row 1 length:", len(rows[0]))
for i, r in enumerate(rows[:5]):
    print(f"Row {i+1} len={len(r)}: {r}")
