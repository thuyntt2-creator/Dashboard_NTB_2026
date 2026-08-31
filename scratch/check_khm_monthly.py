import re
import sys
from datetime import datetime
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
    
    data = ss.worksheet("khách hàng mơi").get_all_values(value_render_option='UNFORMATTED_VALUE')
    df_khm = pd.DataFrame(data[1:], columns=data[0])
    
    _MONTH_MAP = {f"thg {i}": i for i in range(1, 13)}
    
    def parse_vn_date(s):
        s = str(s).strip()
        if not s:
            return None
        if s.isdigit():
            return pd.to_datetime(int(s), unit='D', origin='1899-12-30')
        for m, num in _MONTH_MAP.items():
            if m in s:
                parts = re.findall(r"\d+", s)
                if len(parts) >= 2:
                    return datetime(int(parts[-1]), num, int(parts[0]))
        return pd.to_datetime(s, errors='coerce')

    df_khm["Ngay"] = df_khm["Ngày LTC đầu tiên"].apply(parse_vn_date)
    df_khm = df_khm.dropna(subset=["Ngay"])
    
    df_khm["Month"] = df_khm["Ngay"].dt.month
    df_khm["Day"] = df_khm["Ngay"].dt.day
    
    print("Total KHM records by month:")
    print(df_khm["Month"].value_counts())
    
    print("\nDaily KHM counts for May 2026:")
    df_may = df_khm[df_khm["Month"] == 5]
    print(df_may.groupby("Ngay").size())
    
    print("\nDaily KHM counts for June 2026:")
    df_june = df_khm[df_khm["Month"] == 6]
    print(df_june.groupby("Ngay").size())

if __name__ == "__main__":
    main()
