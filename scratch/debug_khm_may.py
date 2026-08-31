import re
import sys
from datetime import datetime, timedelta
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
    
    # Load sheets
    print("Reading sheets...")
    
    def ws_to_df(name):
        data = ss.worksheet(name).get_all_values(value_render_option='UNFORMATTED_VALUE')
        if not data: return pd.DataFrame()
        return pd.DataFrame(data[1:], columns=data[0])
        
    df_khm = ws_to_df("khách hàng mơi")
    df_coc = ws_to_df("Cocauvung")
    
    print(f"Total KHM rows: {len(df_khm)}")
    print(f"Total Cocauvung rows: {len(df_coc)}")
    
    # Parse dates in KHM
    _MONTH_MAP = {f"thg {i}": i for i in range(1, 13)}
    
    def parse_vn_date(s):
        s = str(s).strip()
        if not s:
            return None
        # Handle Excel serial dates
        if s.isdigit():
            return pd.to_datetime(int(s), unit='D', origin='1899-12-30')
        for m, num in _MONTH_MAP.items():
            if m in s:
                parts = re.findall(r"\d+", s)
                if len(parts) >= 2:
                    return datetime(int(parts[-1]), num, int(parts[0]))
        return pd.to_datetime(s, errors='coerce')

    df_khm["Ngay"] = df_khm["Ngày LTC đầu tiên"].apply(parse_vn_date)
    
    # Print date range in KHM
    print("KHM Date Range:")
    print(df_khm["Ngay"].min(), "to", df_khm["Ngay"].max())
    
    # Get active AM list from Cocauvung
    df_coc["AM"] = df_coc["AM"].astype(str).str.strip()
    am_tinh = df_coc[df_coc["AM"] != ""][["AM", "Tỉnh"]].drop_duplicates("AM").set_index("AM")["Tỉnh"].to_dict()
    
    # Manual additions in ntb_baocao_kinhdoanh_4.py
    AM_EXTRA_MAP = {
        "Trần Công Hậu":          "Khánh Hòa",
        "Phạm Đức Thắng":         "Lâm Đồng",
        "Nguyễn Vĩnh Tường":      "Khánh Hòa",
        "Nguyễn Tống Hùng Phong": "Khánh Hòa",
    }
    am_tinh.update(AM_EXTRA_MAP)
    
    print("\nAM in Cocauvung + Extra Map:")
    for k, v in sorted(am_tinh.items()):
        print(f"  - '{k}': '{v}'")
        
    # Filter May 1 - May 16 in KHM
    # Current date is 2026-06-16, so same period in May is 2026-05-01 to 2026-05-16
    start_date = pd.Timestamp("2026-05-01")
    end_date = pd.Timestamp("2026-05-16")
    
    df_may = df_khm[(df_khm["Ngay"] >= start_date) & (df_khm["Ngay"] <= end_date)].copy()
    print(f"\nTotal May KHM records (1-16 May 2026): {len(df_may)}")
    
    # Check AM mappings for May
    df_may["AM_clean"] = df_may["AM"].astype(str).str.strip()
    
    print("\nBreakdown of AMs in May KHM:")
    am_counts = df_may["AM_clean"].value_counts()
    for am, count in am_counts.items():
        is_mapped = am in am_tinh
        mapped_to = am_tinh.get(am, None)
        print(f"  - AM: '{am}' | Count: {count} | In am_tinh: {is_mapped} | Mapped to: {mapped_to}")
        
    # Let's check which ones didn't map and see if we can fuzzy match
    print("\nUnmapped AMs in May KHM:")
    unmapped = df_may[~df_may["AM_clean"].isin(am_tinh.keys())]
    print(f"Total unmapped: {len(unmapped)}")
    for am in unmapped["AM_clean"].unique():
        print(f"  - '{am}'")

if __name__ == "__main__":
    main()
