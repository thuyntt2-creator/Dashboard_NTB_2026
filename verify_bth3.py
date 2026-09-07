import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

JSON_FILE = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SHEET_ID = '1sTJEt8meKwVicbJAa8d7ml48yVoa_yD2_LAEbZ1ebGs'

creds = Credentials.from_service_account_file(
    JSON_FILE, 
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)
gc = gspread.authorize(creds)
sh = gc.open_by_key(SHEET_ID)

def get_df(name):
    ws = sh.worksheet(name)
    data = ws.get_all_values()
    headers = data[0]
    max_cols = max(len(row) for row in data)
    if len(headers) < max_cols:
        headers += [f"Unnamed_{i}" for i in range(len(headers)+1, max_cols+1)]
    return pd.DataFrame(data[1:], columns=headers)

df_cu = get_df('data cũ')
for col in ['Số tiền ban đầu', 'Điều chỉnh (+|-)', 'Đã truy thu', 'Cần truy thu thêm']:
    df_cu[col] = pd.to_numeric(df_cu[col], errors='coerce').fillna(0)

# Filter for Bưu Cục 56... and AM = Võ Tấn Lợi (column 'AM')
sub_am = df_cu[(df_cu['Nơi vi phạm'] == 'Bưu Cục 56 Phan Đình Phùng-Cam Linh-Khánh Hòa') & (df_cu['AM'] == 'Võ Tấn Lợi')]
print(f"Rows with AM = Võ Tấn Lợi: {len(sub_am)}")
print(f"Sum of 'Số tiền ban đầu': {sub_am['Số tiền ban đầu'].sum():,}")
print(f"Sum of 'Cần truy thu thêm': {sub_am['Cần truy thu thêm'].sum():,}")

# Filter for Bưu Cục 56... and rr = Võ Tấn Lợi (column 'rr')
sub_rr = df_cu[(df_cu['Nơi vi phạm'] == 'Bưu Cục 56 Phan Đình Phùng-Cam Linh-Khánh Hòa') & (df_cu['rr'] == 'Võ Tấn Lợi')]
print(f"\nRows with rr = Võ Tấn Lợi: {len(sub_rr)}")
print(f"Sum of 'Số tiền ban đầu': {sub_rr['Số tiền ban đầu'].sum():,}")
print(f"Sum of 'Cần truy thu thêm': {sub_rr['Cần truy thu thêm'].sum():,}")
