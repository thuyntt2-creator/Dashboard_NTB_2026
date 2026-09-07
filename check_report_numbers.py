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

# Let's inspect unique dates in data cũ and their sums
print("Sums grouped by 'Ngày kết luận truy thu' in data cũ:")
summary_by_date = df_cu.groupby('Ngày kết luận truy thu').agg(
    rows=('Mã ticket', 'count'),
    So_tien_ban_dau=('Số tiền ban đầu', 'sum'),
    Can_truy_thu_them=('Cần truy thu thêm', 'sum')
).reset_index().sort_values(by='Ngày kết luận truy thu')
print(summary_by_date.to_string(index=False))

# Let's see the total sum in df_cu when Ngày kết luận truy thu contains '7 thg 6'
df_w23 = df_cu[df_cu['Ngày kết luận truy thu'].str.contains('7 thg 6', na=False)]
print(f"\nSum for '7 thg 6':")
print(f"Rows: {len(df_w23)}")
print(f"Số tiền ban đầu: {df_w23['Số tiền ban đầu'].sum():,}")
print(f"Cần truy thu thêm: {df_w23['Cần truy thu thêm'].sum():,}")

# Let's see the total sum in df_cu when Ngày kết luận truy thu contains '31 thg 5' or '1 thg 6'
df_prev = df_cu[df_cu['Ngày kết luận truy thu'].str.contains('31 thg 5|1 thg 6|2 thg 6|3 thg 6|4 thg 6|5 thg 6|6 thg 6', na=False)]
print(f"\nSum for other dates:")
print(f"Rows: {len(df_prev)}")
print(f"Số tiền ban đầu: {df_prev['Số tiền ban đầu'].sum():,}")
print(f"Cần truy thu thêm: {df_prev['Cần truy thu thêm'].sum():,}")
