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
        if not s or str(s).strip() == "":
            return "EMPTY"
        s_str = str(s).strip()
        if s_str.isdigit():
            return pd.to_datetime(int(s_str), unit='D', origin='1899-12-30')
        for m, num in _MONTH_MAP.items():
            if m in s_str:
                parts = re.findall(r"\d+", s_str)
                if len(parts) >= 2:
                    return datetime(int(parts[-1]), num, int(parts[0]))
        res = pd.to_datetime(s_str, errors='ignore')
        if isinstance(res, pd.Timestamp):
            return res
        return "FAILED"

    df_khm["Parsed"] = df_khm["Ngày LTC đầu tiên"].apply(parse_vn_date)
    
    # Check parsing status
    print("Parsing status counts:")
    failed_mask = df_khm["Parsed"] == "FAILED"
    empty_mask = df_khm["Parsed"] == "EMPTY"
    parsed_mask = ~failed_mask & ~empty_mask
    
    print(f"  - Successfully parsed: {parsed_mask.sum()}")
    print(f"  - Failed to parse: {failed_mask.sum()}")
    print(f"  - Empty: {empty_mask.sum()}")
    
    if failed_mask.sum() > 0:
        print("\nSome raw values that failed to parse:")
        print(df_khm[failed_mask]["Ngày LTC đầu tiên"].unique()[:10])
        
    # Check if there are years other than 2026
    parsed_dfs = df_khm[parsed_mask].copy()
    parsed_dfs["Year"] = parsed_dfs["Parsed"].apply(lambda x: x.year)
    parsed_dfs["Month"] = parsed_dfs["Parsed"].apply(lambda x: x.month)
    print("\nParsed records by Year:")
    print(parsed_dfs["Year"].value_counts())
    
    print("\nParsed records by Month in 2026:")
    print(parsed_dfs[parsed_dfs["Year"] == 2026]["Month"].value_counts())

if __name__ == "__main__":
    main()
