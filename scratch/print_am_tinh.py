import pandas as pd
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
    
    df_coc = pd.DataFrame(ss.worksheet("CoCauVung").get_all_values(value_render_option='UNFORMATTED_VALUE'))
    df_coc.columns = df_coc.iloc[0]
    df_coc = df_coc.iloc[1:]
    
    print("CoCauVung active rows:")
    print(df_coc[["AM", "Tỉnh"]].dropna().drop_duplicates("AM"))
    
    am_tinh = (df_coc[["AM","Tỉnh"]].dropna()
               .drop_duplicates("AM").set_index("AM")["Tỉnh"].to_dict())
    
    print("\nam_tinh dict keys & values:")
    for k, v in list(am_tinh.items())[:10]:
        print(f"  {repr(k)}: {repr(v)}")

if __name__ == "__main__":
    main()
