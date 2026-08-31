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
TINH_ORDER = ["Khánh Hòa", "Lâm Đồng", "Đắk Nông", "Ninh Thuận", "Bình Thuận"]

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
    
    # New Mapping logic
    def determine_khm_tinh(row):
        t = str(row.get("Tinh", "")).strip()
        if t in TINH_ORDER:
            return t
        am = str(row.get("AM", "")).strip()
        if am:
            return get_tinh(am)
        return None

    df_khm["Tinh_mapped"] = df_khm.apply(determine_khm_tinh, axis=1)
    df_ntb = df_khm[df_khm["Tinh_mapped"].notna()].copy()
    df_ntb["Tinh"] = df_ntb["Tinh_mapped"]
    
    d_cur = pd.Timestamp("2026-06-16")
    m_start = pd.Timestamp("2026-06-01")
    prev_m_start = pd.Timestamp("2026-05-01")
    prev_m_end = pd.Timestamp("2026-05-16")
    
    def sums(df2):
        if df2 is None or df2.empty: return 0, 0, 0.0
        return int(df2["SLKH"].sum()), int(df2["Vol"].sum()), df2["DT"].sum()/1e6
        
    def agg_khm(s, e=None):
        mask = (df_ntb["Ngay"]==s) if e is None else (df_ntb["Ngay"]>=s)&(df_ntb["Ngay"]<=e)
        return (df_ntb[mask].groupby("Tinh")
                .agg(SLKH=("Mã KH","count"),Vol=("Volume","sum"),DT=("DoanhThu_NoVAT","sum")))
                
    khm_mtd_cur = agg_khm(m_start, d_cur)
    khm_mtd_prev = agg_khm(prev_m_start, prev_m_end)
    
    sc, vc, dc = sums(khm_mtd_cur)
    sp, vp, dp = sums(khm_mtd_prev)
    
    print("New Mapping logic results:")
    print(f"June MTD: {sc} shop – {dc:.1f}M")
    print(f"May MTD:  {sp} shop – {dp:.1f}M")
    
    def pct_str(cur, prev):
        if not prev: return "—"
        p = (cur-prev)/prev*100
        return f"{'▲' if p>=0 else '▼'} {abs(p):.1f}%"
        
    print(f"Growth:   {pct_str(dc*1e6, dp*1e6)}")

if __name__ == "__main__":
    main()
