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
df_moi = get_df('data mới')
df_cocau = get_df('CoCauVung')

# Convert numeric
for col in ['Số tiền ban đầu', 'Điều chỉnh (+|-)', 'Đã truy thu', 'Cần truy thu thêm']:
    df_cu[col] = pd.to_numeric(df_cu[col], errors='coerce').fillna(0)
    df_moi[col] = pd.to_numeric(df_moi[col], errors='coerce').fillna(0)

# Build CoCauVung mapping
df_cocau['BC_norm'] = df_cocau['Bưu cục'].str.strip().str.lower()
bc_to_am = dict(zip(df_cocau['BC_norm'], df_cocau['AM']))

def get_am(bc_name):
    if not bc_name: return ""
    return bc_to_am.get(bc_name.strip().lower(), "")

df_cu['AM_mapped'] = df_cu['Nơi vi phạm'].apply(get_am)
df_moi['AM_mapped'] = df_moi['Nơi vi phạm'].apply(get_am)

print("--- Comparison for 'data cũ' ---")
# Let's see if AM column matches AM_mapped or rr matches AM_mapped
print(df_cu[['AM', 'rr', 'AM_mapped']].head(15))

# Check agreement rate
matching_am = (df_cu['AM'] == df_cu['AM_mapped']).mean()
matching_rr = (df_cu['rr'] == df_cu['AM_mapped']).mean()
print(f"AM == AM_mapped agreement: {matching_am:.2%}")
print(f"rr == AM_mapped agreement: {matching_rr:.2%}")

# Let's print rows where rr != AM_mapped
print("\nRows where rr != AM_mapped (sample):")
mismatch_rr = df_cu[df_cu['rr'] != df_cu['AM_mapped']]
print(mismatch_rr[['Nơi vi phạm', 'AM', 'rr', 'AM_mapped']].head(15))

# Let's print rows where AM != AM_mapped
print("\nRows where AM != AM_mapped (sample):")
mismatch_am = df_cu[df_cu['AM'] != df_cu['AM_mapped']]
print(mismatch_am[['Nơi vi phạm', 'AM', 'rr', 'AM_mapped']].head(15))
