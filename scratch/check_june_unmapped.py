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
    df_coc = pd.DataFrame(ss.worksheet("Cocauvung").get_all_values(value_render_option='UNFORMATTED_VALUE')[1:], columns=ss.worksheet("Cocauvung").get_all_values(value_render_option='UNFORMATTED_VALUE')[0])
    
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
    
    # Active AMs
    df_coc["AM"] = df_coc["AM"].astype(str).str.strip()
    am_tinh = df_coc[df_coc["AM"] != ""][["AM", "Tỉnh"]].drop_duplicates("AM").set_index("AM")["Tỉnh"].to_dict()
    
    AM_EXTRA_MAP = {
        "Trần Công Hậu":          "Khánh Hòa",
        "Phạm Đức Thắng":         "Lâm Đồng",
        "Nguyễn Vĩnh Tường":      "Khánh Hòa",
        "Nguyễn Tống Hùng Phong": "Khánh Hòa",
    }
    am_tinh.update(AM_EXTRA_MAP)
    
    # Check June
    start_june = pd.Timestamp("2026-06-01")
    end_june = pd.Timestamp("2026-06-16")
    df_june = df_khm[(df_khm["Ngay"] >= start_june) & (df_khm["Ngay"] <= end_june)].copy()
    
    df_june["AM_clean"] = df_june["AM"].astype(str).str.strip()
    unmapped_june = df_june[~df_june["AM_clean"].isin(am_tinh.keys())]
    
    print(f"Total June unmapped records: {len(unmapped_june)}")
    print("\nUnmapped AMs in June:")
    print(unmapped_june["AM_clean"].value_counts())
    
    # Let's see how many of these unmapped have Tinh in NTB
    ntb_provinces = ["Khánh Hòa", "Lâm Đồng", "Đắk Nông", "Ninh Thuận", "Bình Thuận"]
    unmapped_june_ntb = unmapped_june[unmapped_june["Tinh"].isin(ntb_provinces)]
    print(f"\nUnmapped June records that belong to NTB: {len(unmapped_june_ntb)}")
    print(unmapped_june_ntb[["AM_clean", "Tinh", "Bưu Cục SO"]].value_counts())

if __name__ == "__main__":
    main()
