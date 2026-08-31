import gspread
from google.oauth2.service_account import Credentials
import sys

sys.stdout.reconfigure(encoding='utf-8')

CREDENTIALS_PATH = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SPREADSHEET_ID   = '1XaziS_8UB2lCwL01bxam106EdIUHtlMISDGJX1PU5A8'
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

def main():
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    ss = gspread.authorize(creds).open_by_key(SPREADSHEET_ID)
    
    target_gid = 1467753509
    for ws in ss.worksheets():
        if ws.id == target_gid:
            print(f"FOUND worksheet name: '{ws.title}' for gid {target_gid}")
            # print first 50 rows
            values = ws.get_all_values()
            print("First 20 rows:")
            for r in values[:20]:
                print(r)
            break
    else:
        print(f"No worksheet found for gid {target_gid}")

if __name__ == '__main__':
    main()
