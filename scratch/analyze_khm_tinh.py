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
    
    # Parse dates in KHM
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
    
    # Filter May 1 - May 16 in KHM
    start_date = pd.Timestamp("2026-05-01")
    end_date = pd.Timestamp("2026-05-16")
    df_may = df_khm[(df_khm["Ngay"] >= start_date) & (df_khm["Ngay"] <= end_date)].copy()
    
    print(f"Total May KHM records: {len(df_may)}")
    
    # Let's count records by the 'Tinh' column in May
    print("\nMay KHM records by 'Tinh' column:")
    print(df_may["Tinh"].value_counts())
    
    # Let's print the 'AM' and 'Bưu Cục SO' for records where Tinh is in NTB provinces
    ntb_provinces = ["Khánh Hòa", "Lâm Đồng", "Đắk Nông", "Ninh Thuận", "Bình Thuận"]
    
    df_may_ntb_tinh = df_may[df_may["Tinh"].isin(ntb_provinces)].copy()
    print(f"\nMay KHM records where 'Tinh' is in NTB: {len(df_may_ntb_tinh)}")
    
    print("\nBreakdown of AMs for May NTB by Tinh:")
    for tinh in ntb_provinces:
        df_t = df_may_ntb_tinh[df_may_ntb_tinh["Tinh"] == tinh]
        print(f"\nTinh: {tinh} (Total: {len(df_t)})")
        print(df_t["AM"].value_counts())
        
    # Let's check June KHM records too! Let's see how June KHM records are mapped.
    # June MTD: 2026-06-01 to 2026-06-16
    start_june = pd.Timestamp("2026-06-01")
    end_june = pd.Timestamp("2026-06-16")
    df_june = df_khm[(df_khm["Ngay"] >= start_june) & (df_khm["Ngay"] <= end_june)].copy()
    
    print(f"\nTotal June KHM records: {len(df_june)}")
    df_june_ntb_tinh = df_june[df_june["Tinh"].isin(ntb_provinces)].copy()
    print(f"June KHM records where 'Tinh' is in NTB: {len(df_june_ntb_tinh)}")
    
    print("\nBreakdown of AMs for June NTB by Tinh:")
    for tinh in ntb_provinces:
        df_t = df_june_ntb_tinh[df_june_ntb_tinh["Tinh"] == tinh]
        print(f"  - {tinh}: {len(df_t)} rows")
        if not df_t.empty:
            print(df_t["AM"].value_counts())

if __name__ == "__main__":
    main()
