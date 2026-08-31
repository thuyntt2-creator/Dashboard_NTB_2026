import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import sys

sys.stdout.reconfigure(encoding='utf-8')

CREDENTIALS_PATH = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
OLD_SPREADSHEET_ID = '12VsqpIx1vLOqk6-JKHwgRmdrgu6fxSNPQcpyO0wpvdQ'
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

def main():
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    ss = gspread.authorize(creds).open_by_key(OLD_SPREADSHEET_ID)
    
    for title in ["Theo ngày", "Theo Tuần", "Theo Tháng"]:
        try:
            ws = ss.worksheet(title)
            data = ws.get_all_values()
            df = pd.DataFrame(data[1:], columns=data[0])
            print(f"\nWorksheet: '{title}' | columns: {list(df.columns)}")
            print(df.head(2))
            
            # Let's count unique values of the date column
            date_col = "Ngay" if "Ngay" in df.columns else ("Tuan" if "Tuan" in df.columns else "Thang")
            print(f"Unique values count in {date_col}: {df[date_col].nunique()}")
            print("Sample unique values:")
            print(list(df[date_col].unique())[:15])
        except Exception as e:
            print(f"Error on {title}: {e}")

if __name__ == "__main__":
    main()
