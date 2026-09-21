import sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
work_id = '15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM'

res = service.spreadsheets().values().get(spreadsheetId=work_id, range="'RAW FD N-1 (HUB)'!A1:H").execute()
rows = res.get('values', [])
df = pd.DataFrame(rows[1:], columns=rows[0])
df['dt'] = pd.to_datetime(df['delivery_date'], errors='coerce')
df['Total'] = pd.to_numeric(df['Total đơn'].str.replace(',', ''), errors='coerce').fillna(0)
df['Return'] = pd.to_numeric(df['Đơn return'].str.replace(',', ''), errors='coerce').fillna(0)
df['BC'] = df['Tên bưu cục'].astype(str).str.strip()

for name in ['(DNO) Kiến Đức', '(KHO) Tây Nha Trang']:
    sub = df[df['BC'] == name]
    sub_grp = sub.groupby('dt').agg({'Total': 'sum', 'Return': 'sum'}).reset_index()
    sub_grp['%FD'] = (sub_grp['Return'] / sub_grp['Total'] * 100).round(2)
    print(f"\n{name} by date:")
    for _, r in sub_grp.iterrows():
        print(f"  {r['dt'].strftime('%Y-%m-%d (%a)')}: Total={r['Total']}, Return={r['Return']}, %FD={r['%FD']}%")
