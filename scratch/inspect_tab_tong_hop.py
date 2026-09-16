import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')
creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

res = service.spreadsheets().values().get(
    spreadsheetId='1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg',
    range="'Tổng Hợp KA OFF'!A1:Z50"
).execute()

rows = res.get('values', [])
df = pd.DataFrame(rows[1:], columns=rows[0])
print(df[['Tỉnh', 'Quận/ huyện', 'Phường/xã cần tắt', 'ID phường/xã', 'Bưu Cục', 'AM', 'Thời gian tắt (KA)', 'Thời gian mở (KA)', 'Phân loại đề xuất']].to_string())
print('\nDistinct AMs in Tổng Hợp KA OFF:', df['AM'].unique().tolist())
