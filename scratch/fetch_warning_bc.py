import sys
sys.stdout.reconfigure(encoding='utf-8')
import gspread
from google.oauth2.credentials import Credentials as UserCredentials
import pandas as pd
import json

scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = UserCredentials.from_authorized_user_file(r'C:\Users\lap4all\Desktop\auto-report\authorized_user.json', scopes=scopes)
gc = gspread.authorize(creds)

sh2 = gc.open_by_key('1lmQv8KwHJzDFs_RMz64ydu4SOmG3M1YAzILNFGtzFec')
print("Worksheets:", [w.title for w in sh2.worksheets()])

# Check NTB or BC_canh_bao or similar
for w in sh2.worksheets():
    if any(k in w.title.lower() for k in ['ntb', 'canh_bao', 'cảnh báo', 'bất ổn', 'luu_tru', 'lưu trữ']):
        print(f"\n--- Worksheet: {w.title} ---")
        vals = w.get_all_values()
        if vals:
            print("Header:", vals[0])
            print("Row count:", len(vals))
            if len(vals) > 1:
                print("First row:", vals[1])
