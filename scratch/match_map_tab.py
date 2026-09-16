import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

def clean_text(s):
    if not s:
        return ""
    s = unicodedata.normalize('NFC', str(s).strip().lower())
    for p in ['thị trấn ', 'thị xã ', 'thành phố ', 'quận ', 'huyện ', 'phường ', 'xã ']:
        if s.startswith(p):
            s = s[len(p):]
    s = s.replace("'", "").replace("’", "").replace("-", " ")
    return " ".join(s.split())

# 1. Fetch tab map
res_map = service.spreadsheets().values().get(
    spreadsheetId='1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg',
    range="'map'!A1:D200"
).execute()
rows_map = res_map.get('values', [])
df_map = pd.DataFrame(rows_map[1:], columns=rows_map[0])
print("Tab map total rows:", len(df_map))

# 2. Fetch tab cơ cấu
res_cc = service.spreadsheets().values().get(
    spreadsheetId='1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg',
    range="'cơ cấu'!A1:I1500"
).execute()
rows_cc = res_cc.get('values', [])
max_c = max(len(r) for r in rows_cc)
padded = [r + [''] * (max_c - len(r)) for r in rows_cc]
df_cc = pd.DataFrame(padded[1:], columns=padded[0])

# Check unique BC in KA OFF
res_ka = service.spreadsheets().values().get(
    spreadsheetId='1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg',
    range="'Tổng Hợp KA OFF'!A1:J30"
).execute()
rows_ka = res_ka.get('values', [])
df_ka = pd.DataFrame(rows_ka[1:], columns=rows_ka[0])

print("\nChecking BC matching with tab map:")
for bc in df_ka['Bưu Cục'].unique():
    # Look up in map
    m = df_map[df_map['Bưu cục'].str.contains(bc, na=False, case=False, regex=False)]
    if not m.empty:
        print(f"BC '{bc}' -> AM: '{m.iloc[0]['AM']}' (match: {m.iloc[0]['Bưu cục']})")
    else:
        # try reverse
        found = False
        for _, mr in df_map.iterrows():
            if mr['Bưu cục'] in bc or bc in mr['Bưu cục']:
                print(f"BC '{bc}' -> AM: '{mr['AM']}' (fuzzy: {mr['Bưu cục']})")
                found = True
                break
        if not found:
            print(f"BC '{bc}' -> NOT FOUND IN TAB MAP!")
