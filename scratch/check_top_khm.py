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
    
    # NTB provinces
    ntb_provinces = ["Khánh Hòa", "Lâm Đồng", "Đắk Nông", "Ninh Thuận", "Bình Thuận"]
    
    df_may = df_khm[may_mask & df_khm["Tinh"].isin(ntb_provinces)].copy()
    df_june = df_khm[june_mask & df_khm["Tinh"].isin(ntb_provinces)].copy()
    
    print("TOP 10 MAY KHM CUSTOMERS (NTB):")
    df_may_sorted = df_may.sort_values(by="DoanhThu_NoVAT", ascending=False)
    print(df_may_sorted[["Mã KH", "Tên KH", "Tinh", "AM", "Volume", "DoanhThu_NoVAT"]].head(10).to_string(index=False))
    
    print("\nTOP 10 JUNE KHM CUSTOMERS (NTB):")
    df_june_sorted = df_june.sort_values(by="DoanhThu_NoVAT", ascending=False)
    print(df_june_sorted[["Mã KH", "Tên KH", "Tinh", "AM", "Volume", "DoanhThu_NoVAT"]].head(10).to_string(index=False))

if __name__ == "__main__":
    main()
