import sys
import re
from datetime import datetime
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
sheet_id = '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

print('Fetching all rows from truythu!A1:Q5530...')
res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="'truythu'!A1:Q5530").execute()
rows = res.get('values', [])
print(f'Total rows fetched: {len(rows)}')

header = rows[0]
data = rows[1:]

df = pd.DataFrame(data, columns=header)
print("DF shape:", df.shape)
print("Columns:", df.columns.tolist())

# Parse dates in 'Ngày kết luận truy thu'
# Format: '00:00:00 20 thg 9, 2026' or similar
def parse_ghn_date(val):
    if not val or not isinstance(val, str):
        return None
    val = val.strip()
    # match patterns like: '00:00:00 20 thg 9, 2026' or '20 thg 9, 2026' or '2026-09-20'
    m = re.search(r'(\d{1,2})\s+thg\s+(\d{1,2}),?\s+(\d{4})', val)
    if m:
        d, mth, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return datetime(y, mth, d)
    m2 = re.search(r'(\d{4})-(\d{2})-(\d{2})', val)
    if m2:
        return datetime(int(m2.group(1)), int(m2.group(2)), int(m2.group(3)))
    m3 = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', val)
    if m3:
        return datetime(int(m3.group(3)), int(m3.group(2)), int(m3.group(1)))
    return None

df['parsed_date'] = df['Ngày kết luận truy thu'].apply(parse_ghn_date)
print("\nParsed dates summary:")
print(df['parsed_date'].value_counts().sort_index())

print("\nMin date:", df['parsed_date'].min())
print("Max date:", df['parsed_date'].max())

# Save df to pickle or csv for fast local analysis
df.to_csv('scratch/truythu_raw.csv', index=False, encoding='utf-8')
print("Saved to scratch/truythu_raw.csv")
