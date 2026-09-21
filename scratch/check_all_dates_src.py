import sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

source_id = '1odUPX5mWpUYUUQOrhX_k8kXWV7drMUdQ58DRwgSQNS8'
res = service.spreadsheets().values().get(spreadsheetId=source_id, range="FD!A1:B100000").execute()
rows = res.get('values', [])
df = pd.DataFrame(rows[1:], columns=rows[0])
print("All delivery_date in Master FD:", df['delivery_date'].dropna().unique())
print("NTB delivery_date in Master FD:", df[df['region_shortname'] == 'NTB']['delivery_date'].dropna().unique())
