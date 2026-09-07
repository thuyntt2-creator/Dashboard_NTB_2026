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
df_ns = pd.read_csv(r'c:\Users\lap4all\Desktop\New folder\ops_nhan_su.csv', dtype=str)

# Clean and index df_ns
df_ns['ID_clean'] = df_ns['ID'].str.strip()
ns_id_to_am = dict(zip(df_ns['ID_clean'], df_ns['AM']))

# Map employee ID in df_cu
def get_employee_id(name):
    if not name: return ""
    parts = str(name).split('-')
    if parts:
        return parts[0].strip()
    return ""

df_cu['Emp_ID'] = df_cu['Nhân viên'].apply(get_employee_id)
df_cu['AM_from_ns'] = df_cu['Emp_ID'].apply(lambda x: ns_id_to_am.get(x, ""))

print("Checking first 15 rows of df_cu mapping vs actual column Q ('AM'):")
print(df_cu[['Nhân viên', 'AM', 'AM_from_ns']].head(15))

# Agreement rate
df_cu_nonempty = df_cu[df_cu['AM'].str.strip() != ''].copy()
agreement = (df_cu_nonempty['AM'].str.strip() == df_cu_nonempty['AM_from_ns'].str.strip()).mean()
print(f"\nAgreement rate (where AM is not empty): {agreement:.2%}")

# Let's print rows where it doesn't match
print("\nMismatches:")
mismatches = df_cu_nonempty[df_cu_nonempty['AM'].str.strip() != df_cu_nonempty['AM_from_ns'].str.strip()]
print(mismatches[['Nhân viên', 'AM', 'AM_from_ns']].head(15))
