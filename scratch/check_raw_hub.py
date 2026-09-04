import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

source_id = "15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM"

# Let's get more rows from 'RAW FD N-1 (HUB)'
res = service.spreadsheets().values().get(
    spreadsheetId=source_id,
    range="'RAW FD N-1 (HUB)'!A1:G1000"
).execute()

rows = res.get('values', [])
print(f"Total rows retrieved: {len(rows)}")
if rows:
    header = rows[0]
    data = rows[1:]
    # filter rows that have at least 7 columns
    clean_data = [r[:7] for r in data if len(r) >= 6]
    df = pd.DataFrame(clean_data)
    print("Columns:", header)
    print(df.head(10))
    
    # Check Đức Lập
    duc_lap = df[df[3] == '(DNO) Đức Lập']
    print("\nĐức Lập rows:")
    print(duc_lap)
    
    # Check unique client types
    print("\nClient types:", df[4].unique())
