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

_MONTH_MAP = {f"thg {i}": i for i in range(1, 13)}

# Exact parse_vn_date from ntb_baocao_kinhdoanh_4.py
def parse_vn_date_main(s):
    if isinstance(s, (int, float)):
        return pd.to_datetime(s, unit='D', origin='1899-12-30').to_pydatetime()
    s = str(s).strip()
    if s.isdigit():
        return pd.to_datetime(int(s), unit='D', origin='1899-12-30').to_pydatetime()
    for m, num in _MONTH_MAP.items():
        if m in s:
            parts = re.findall(r"\d+", s)
            if len(parts) >= 2:
                return datetime(int(parts[-1]), num, int(parts[0]))
    return None

def main():
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    ss = gspread.authorize(creds).open_by_key(SPREADSHEET_ID)
    
    data = ss.worksheet("khách hàng mơi").get_all_values(value_render_option='UNFORMATTED_VALUE')
    df_khm = pd.DataFrame(data[1:], columns=data[0])
    
    df_khm["Parsed"] = df_khm["Ngày LTC đầu tiên"].apply(parse_vn_date_main)
    
    # Check how many are None
    print(f"Total rows in khách hàng mơi: {len(df_khm)}")
    print(f"Parsed as None: {df_khm['Parsed'].isna().sum()}")
    
    # Print some raw values that failed to parse
    failed = df_khm[df_khm["Parsed"].isna()]
    if not failed.empty:
        print("\nRaw values that failed to parse:")
        print(failed["Ngày LTC đầu tiên"].value_counts().head(20))

if __name__ == "__main__":
    main()
