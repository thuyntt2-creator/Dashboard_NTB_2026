import re
import sys
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

sys.stdout.reconfigure(encoding='utf-8')

CREDENTIALS_PATH = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SPREADSHEET_ID   = '12VsqpIx1vLOqk6-JKHwgRmdrgu6fxSNPQcpyO0wpvdQ'
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

def main():
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    ss = gspread.authorize(creds).open_by_key(SPREADSHEET_ID)
    
    data = ss.worksheet("Theo ngày").get_all_values(value_render_option='UNFORMATTED_VALUE')
    df = pd.DataFrame(data[1:], columns=data[0])
    
    df["DoanhThu"] = pd.to_numeric(df["DoanhThu"], errors="coerce").fillna(0)
    
    print("Some raw DoanhThu values:")
    print(df["DoanhThu"].head(10))
    print(df["DoanhThu"].describe())
    
    # Check sum of DoanhThu
    print(f"\nSum of all DoanhThu: {df['DoanhThu'].sum():,}")

if __name__ == "__main__":
    main()
