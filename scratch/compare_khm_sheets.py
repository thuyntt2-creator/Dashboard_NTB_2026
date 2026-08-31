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
    
    def ws_to_df(name):
        data = ss.worksheet(name).get_all_values(value_render_option='UNFORMATTED_VALUE')
        if not data: return pd.DataFrame()
        return pd.DataFrame(data[1:], columns=data[0])
        
    df_khm = ws_to_df("khách hàng mơi")
    df_data = ws_to_df("dataKHM")
    
    print(f"khách hàng mơi: {len(df_khm)} rows")
    print(f"dataKHM:        {len(df_data)} rows")
    
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
    df_data["Ngay"] = df_data["Ngày LTC đầu tiên"].apply(parse_vn_date)
    
    # Filter May 1-16 in both sheets
    start_date = pd.Timestamp("2026-05-01")
    end_date = pd.Timestamp("2026-05-16")
    
    df_khm_may = df_khm[(df_khm["Ngay"] >= start_date) & (df_khm["Ngay"] <= end_date)]
    df_data_may = df_data[(df_data["Ngay"] >= start_date) & (df_data["Ngay"] <= end_date)]
    
    print(f"\nMay MTD (1-16) records in khách hàng mơi: {len(df_khm_may)}")
    print(f"May MTD (1-16) records in dataKHM:        {len(df_data_may)}")
    
    # Filter June 1-16 in both sheets
    start_june = pd.Timestamp("2026-06-01")
    end_june = pd.Timestamp("2026-06-16")
    df_khm_june = df_khm[(df_khm["Ngay"] >= start_june) & (df_khm["Ngay"] <= end_june)]
    df_data_june = df_data[(df_data["Ngay"] >= start_june) & (df_data["Ngay"] <= end_june)]
    
    print(f"\nJune MTD (1-16) records in khách hàng mơi: {len(df_khm_june)}")
    print(f"June MTD (1-16) records in dataKHM:        {len(df_data_june)}")
    
    # Let's count NTB provinces in both sheets for May
    ntb_provinces = ["Khánh Hòa", "Lâm Đồng", "Đắk Nông", "Ninh Thuận", "Bình Thuận"]
    
    print("\nMay NTB records in khách hàng mơi:")
    print(df_khm_may[df_khm_may["Tinh"].isin(ntb_provinces)]["Tinh"].value_counts())
    
    print("\nMay NTB records in dataKHM:")
    print(df_data_may[df_data_may["Tinh"].isin(ntb_provinces)]["Tinh"].value_counts())

if __name__ == "__main__":
    main()
