import os, sys, io, gspread
from google.oauth2.credentials import Credentials as UserCredentials

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = r'c:\Users\lap4all\Desktop\New folder'
SHEET_KEY = '1YlLYFhCioAelNLaLyHg95UmH6QuasvEP50fcp-A-Yg4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds = UserCredentials.from_authorized_user_file(os.path.join(BASE_DIR, 'authorized_user.json'), scopes=SCOPES)
gc = gspread.authorize(creds)
sh = gc.open_by_key(SHEET_KEY)
ws_data = sh.worksheet('data')

# Set V1 = 'aging' and V2 = formula
ws_data.update(range_name='V1:V2', values=[['aging'], ['=ARRAYFORMULA(IF(B2:B="", "", XLOOKUP(B2:B, LM!B:B, LM!G:G, "")))']], value_input_option='USER_ENTERED')
print('Updated V1 and V2 successfully!')

vals = ws_data.get('T1:V10')
for idx, r in enumerate(vals):
    print(f'Row {idx+1}: {r}')
