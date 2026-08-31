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
    df_khm["DoanhThu_NoVAT"] = pd.to_numeric(df_khm["DoanhThu_NoVAT"], errors="coerce").fillna(0)
    df_khm["Volume"] = pd.to_numeric(df_khm["Volume"], errors="coerce").fillna(0)
    
    # Filter May 1-16 vs June 1-16
    may_mask = (df_khm["Ngay"] >= pd.Timestamp("2026-05-01")) & (df_khm["Ngay"] <= pd.Timestamp("2026-05-16"))
    june_mask = (df_khm["Ngay"] >= pd.Timestamp("2026-06-01")) & (df_khm["Ngay"] <= pd.Timestamp("2026-06-16"))
    
    df_may = df_khm[may_mask]
    df_june = df_khm[june_mask]
    
    print("RAW KHM SUMS (No AM/Province filtering):")
    print(f"May MTD (1-16 May):")
    print(f"  - Count: {len(df_may)}")
    print(f"  - Vol:   {df_may['Volume'].sum():,}")
    print(f"  - DT:    {df_may['DoanhThu_NoVAT'].sum()/1e6:,.2f}M")
    
    print(f"June MTD (1-16 June):")
    print(f"  - Count: {len(df_june)}")
    print(f"  - Vol:   {df_june['Volume'].sum():,}")
    print(f"  - DT:    {df_june['DoanhThu_NoVAT'].sum()/1e6:,.2f}M")

if __name__ == "__main__":
    main()
