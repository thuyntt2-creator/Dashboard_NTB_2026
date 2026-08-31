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

_MONTH_MAP = {f"thg {i}": i for i in range(1, 13)}

def parse_vn_date(s):
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

    df_khm["Ngay"]           = df_khm["Ngày LTC đầu tiên"].apply(parse_vn_date)
    df_khm["DoanhThu_NoVAT"] = pd.to_numeric(df_khm["DoanhThu_NoVAT"], errors="coerce").fillna(0)
    df_khm["Volume"]         = pd.to_numeric(df_khm["Volume"],          errors="coerce").fillna(0)
    
    print(f"Total df_khm rows loaded: {len(df_khm)}")
    print(f"df_khm Null dates: {df_khm['Ngay'].isna().sum()}")
    
    df_ntb = df_khm[df_khm["AM"].isin(set(am_tinh.keys()))].copy()
    df_ntb["Tinh"] = df_ntb["AM"].apply(get_tinh)
    df_ntb = df_ntb[df_ntb["Tinh"].notna()]
    
    print(f"Total df_ntb rows: {len(df_ntb)}")
    
    # Calculate dates
    # Let's get the active dates from Theo ngày sheet
    df_day = pd.DataFrame(ss.worksheet("Theo ngày").get_all_values(value_render_option='UNFORMATTED_VALUE')[1:], columns=ss.worksheet("Theo ngày").get_all_values(value_render_option='UNFORMATTED_VALUE')[0])
    df_day["date"] = df_day["Ngay"].apply(parse_vn_date)
    df_day = df_day.dropna(subset=["date"])
    dates  = sorted(df_day["date"].unique())
    d_cur  = dates[-1]
    
    m_start      = d_cur.replace(day=1)
    prev_m_start = (m_start-timedelta(days=1)).replace(day=1)
    prev_m_end   = prev_m_start.replace(day=d_cur.day)
    
    print(f"d_cur: {d_cur}, m_start: {m_start}, prev_m_start: {prev_m_start}, prev_m_end: {prev_m_end}")
    
    def agg_khm(s, e=None):
        mask = (df_ntb["Ngay"]==s) if e is None else (df_ntb["Ngay"]>=s)&(df_ntb["Ngay"]<=e)
        res = df_ntb[mask]
        print(f"agg_khm mask size for s={s}, e={e}: {len(res)}")
        return (res.groupby("Tinh")
                .agg(SLKH=("Mã KH","count"),Vol=("Volume","sum"),DT=("DoanhThu_NoVAT","sum")))

    khm_mtd_prev = agg_khm(prev_m_start, prev_m_end)
    print("\nResulting khm_mtd_prev:")
    print(khm_mtd_prev)

if __name__ == "__main__":
    main()
