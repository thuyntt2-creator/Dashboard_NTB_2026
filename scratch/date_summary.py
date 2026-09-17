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

summary = df.groupby('dt').agg({'Total': 'sum', 'Return': 'sum', 'ID bưu cục': 'nunique'}).reset_index()
summary['%FD'] = (summary['Return'] / summary['Total'] * 100).round(2)
for _, r in summary.iterrows():
    print(f"Date: {r['dt'].strftime('%Y-%m-%d')} | Total: {r['Total']:,.0f} | Return: {r['Return']:,.0f} | %FD: {r['%FD']:.2f}% | BCs: {r['ID bưu cục']}")
