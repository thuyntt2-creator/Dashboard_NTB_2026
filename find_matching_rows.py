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

targets = [8980808, 4100000, 2477998, 1982732]

print("Searching for exact matches in individual rows:")
for val in targets:
    print(f"\n--- Target: {val:,} ---")
    match_init = df_cu[df_cu['Số tiền ban đầu'] == val]
    if not match_init.empty:
        print(f"Match in 'Số tiền ban đầu' ({len(match_init)} rows):")
        print(match_init[['Nơi vi phạm', 'Loại truy thu', 'AM', 'Số tiền ban đầu', 'Cần truy thu thêm']])
        
    match_add = df_cu[df_cu['Cần truy thu thêm'] == val]
    if not match_add.empty:
        print(f"Match in 'Cần truy thu thêm' ({len(match_add)} rows):")
        print(match_add[['Nơi vi phạm', 'Loại truy thu', 'AM', 'Số tiền ban đầu', 'Cần truy thu thêm']])

# What if they match combinations? E.g. grouped by Mã ticket or Nhân viên?
print("\nSearching for grouped matches by 'Mã ticket' or other columns:")
for val in targets:
    print(f"\n--- Target: {val:,} ---")
    for group_col in ['Mã ticket', 'Mã truy thu', 'Nhân viên']:
        grouped = df_cu.groupby(group_col)['Cần truy thu thêm'].sum().reset_index()
        match = grouped[grouped['Cần truy thu thêm'] == val]
        if not match.empty:
            print(f"Match by grouping on '{group_col}':")
            print(match)
            # Show the original rows
            print(df_cu[df_cu[group_col].isin(match[group_col])][['Nơi vi phạm', 'Nhân viên', 'Loại truy thu', 'AM', 'Số tiền ban đầu', 'Cần truy thu thêm']])
