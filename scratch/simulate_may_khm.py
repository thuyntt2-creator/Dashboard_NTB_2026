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
    
    df_khm = pd.DataFrame(ss.worksheet("khách hàng mơi").get_all_values(value_render_option='UNFORMATTED_VALUE')[1:], columns=ss.worksheet("khách hàng mơi").get_all_values(value_render_option='UNFORMATTED_VALUE')[0])
    df_coc = pd.DataFrame(ss.worksheet("Cocauvung").get_all_values(value_render_option='UNFORMATTED_VALUE')[1:], columns=ss.worksheet("Cocauvung").get_all_values(value_render_option='UNFORMATTED_VALUE')[0])
    
    AM_EXTRA_MAP = {
        "Trần Công Hậu":          "Khánh Hòa",
        "Phạm Đức Thắng":         "Lâm Đồng",
        "Nguyễn Vĩnh Tường":      "Khánh Hòa",
        "Nguyễn Tống Hùng Phong": "Khánh Hòa",
    }
    
    am_tinh = (df_coc[["AM","Tỉnh"]].dropna()
               .drop_duplicates("AM").set_index("AM")["Tỉnh"].to_dict())
    am_tinh.update(AM_EXTRA_MAP)
    
    def get_tinh(am):
        am = str(am).strip()
        if am in am_tinh: return am_tinh[am]
        for k, v in am_tinh.items():
            if am in k or k in am: return v
        return None

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

    df_khm["Ngay"]           = df_khm["Ngày LTC đầu tiên"].apply(parse_vn_date)
    df_khm["DoanhThu_NoVAT"] = pd.to_numeric(df_khm["DoanhThu_NoVAT"], errors="coerce").fillna(0)
    df_khm["Volume"]         = pd.to_numeric(df_khm["Volume"],          errors="coerce").fillna(0)
    
    df_ntb = df_khm[df_khm["AM"].isin(set(am_tinh.keys()))].copy()
    df_ntb["Tinh"] = df_ntb["AM"].apply(get_tinh)
    df_ntb = df_ntb[df_ntb["Tinh"].notna()]
    
    # Calculate dates
    # Since d_cur is 2026-06-16:
    d_cur = pd.Timestamp("2026-06-16")
    m_start = pd.Timestamp("2026-06-01")
    prev_m_start = pd.Timestamp("2026-05-01")
    prev_m_end = pd.Timestamp("2026-05-16")
    
    # Filter May MTD
    mask_may = (df_ntb["Ngay"] >= prev_m_start) & (df_ntb["Ngay"] <= prev_m_end)
    df_may_ntb = df_ntb[mask_may].copy()
    
    print(f"Total rows in df_may_ntb: {len(df_may_ntb)}")
    print(f"Sum of DoanhThu_NoVAT: {df_may_ntb['DoanhThu_NoVAT'].sum():,}")
    print(f"Sum of Volume: {df_may_ntb['Volume'].sum():,}")
    
    print("\nAll rows in df_may_ntb:")
    pd.set_option('display.max_rows', None)
    print(df_may_ntb[["Mã KH", "Tên KH", "Ngay", "Tinh", "AM", "Volume", "DoanhThu_NoVAT"]])

if __name__ == "__main__":
    main()
