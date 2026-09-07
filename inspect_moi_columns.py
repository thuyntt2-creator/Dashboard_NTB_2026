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

df_moi = get_df('data mới')
df_cocau = get_df('CoCauVung')

# Build CoCauVung mapping
df_cocau['BC_norm'] = df_cocau['Bưu cục'].str.strip().str.lower()
bc_to_am = dict(zip(df_cocau['BC_norm'], df_cocau['AM']))

def get_am(bc_name):
    if not bc_name: return ""
    return bc_to_am.get(bc_name.strip().lower(), "")

df_moi['AM_mapped'] = df_moi['Nơi vi phạm'].apply(get_am)

print("data mới row count:", len(df_moi))
print("data mới non-empty 'AM':", (df_moi['AM'].str.strip() != "").sum())
print("data mới empty 'AM':", (df_moi['AM'].str.strip() == "").sum())

# Let's print some sample rows from data mới where AM is populated and see if it matches AM_mapped
print("\nSample rows where AM is populated in data mới:")
print(df_moi[df_moi['AM'].str.strip() != ''][['Nơi vi phạm', 'Nhân viên', 'AM', 'AM_mapped']].head(15))

# Let's print some sample rows where AM is empty in data mới
print("\nSample rows where AM is empty in data mới:")
print(df_moi[df_moi['AM'].str.strip() == ''][['Nơi vi phạm', 'Nhân viên', 'AM', 'AM_mapped']].head(15))

# Let's check the agreement between AM and AM_mapped when AM is not empty
df_moi_nonempty = df_moi[df_moi['AM'].str.strip() != ''].copy()
agreement = (df_moi_nonempty['AM'].str.strip() == df_moi_nonempty['AM_mapped'].str.strip()).mean()
print(f"\nAgreement between AM and AM_mapped (for non-empty AM rows): {agreement:.2%}")

# Let's inspect what AM names are in CoCauVung
print("\nUnique AMs in CoCauVung:")
print(df_cocau['AM'].unique())
