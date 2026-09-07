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

# Filter criteria test:
# "Loại các đơn truy thu backlog giao - bắn kiểm - LC"
# Backlog categories:
# 1. Backlog Giao Hàng
# 2. Backlog Bắn Kiểm Lấy
# 3. Backlog Luân Chuyển Giao
# 4. Backlog Luân Chuyển Trả
# What about Backlog Trả Hàng? Let's check both including and excluding it.

exclude_list = ['Backlog Giao Hàng', 'Backlog Bắn Kiểm Lấy', 'Backlog Luân Chuyển Giao', 'Backlog Luân Chuyển Trả', 'Backlog Trả Hàng']
df_filtered = df_cu[~df_cu['Loại truy thu'].isin(exclude_list)]

bth1_test = df_filtered.groupby('Nơi vi phạm').agg(
    So_tien_ban_dau=('Số tiền ban đầu', 'sum'),
    Dieu_chinh=('Điều chỉnh (+|-)', 'sum'),
    Can_truy_thu_them=('Cần truy thu thêm', 'sum')
).reset_index().sort_values(by='Can_truy_thu_them', ascending=False)

print("--- Test with excluding all backlog categories ---")
print(bth1_test.head(10).to_string(index=False))

# Sum of total needs to match 26,766,437
print(f"Total sum of 'Cần truy thu thêm': {bth1_test['Can_truy_thu_them'].sum():,}")

# What if we include Backlog Trả Hàng?
exclude_list2 = ['Backlog Giao Hàng', 'Backlog Bắn Kiểm Lấy', 'Backlog Luân Chuyển Giao', 'Backlog Luân Chuyển Trả']
df_filtered2 = df_cu[~df_cu['Loại truy thu'].isin(exclude_list2)]
bth1_test2 = df_filtered2.groupby('Nơi vi phạm').agg(
    So_tien_ban_dau=('Số tiền ban đầu', 'sum'),
    Dieu_chinh=('Điều chỉnh (+|-)', 'sum'),
    Can_truy_thu_them=('Cần truy thu thêm', 'sum')
).reset_index().sort_values(by='Can_truy_thu_them', ascending=False)
print("\n--- Test excluding only 4 backlog categories ---")
print(bth1_test2.head(10).to_string(index=False))
print(f"Total sum: {bth1_test2['Can_truy_thu_them'].sum():,}")
