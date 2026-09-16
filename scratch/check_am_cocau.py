import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')
creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

res = service.spreadsheets().values().get(
    spreadsheetId='1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg',
    range="'cơ cấu'!A1:Z1500"
).execute()

rows = res.get('values', [])
max_c = max(len(r) for r in rows)
padded = [r + [''] * (max_c - len(r)) for r in rows]
df = pd.DataFrame(padded[1:], columns=padded[0])

print("Columns in cơ cấu:", df.columns.tolist())
matches = df[df['Huyện/TP'].str.contains("Đức Trọng|Di Linh|Đơn Dương|Đắk R|Gia Nghĩa|Đăk Glong", na=False, case=False)]
print("\nUnique combinations in cơ cấu for these areas:")
print(matches[['c', 'Huyện/TP', 'Bưu Cục new', 'AM']].drop_duplicates().to_string())
