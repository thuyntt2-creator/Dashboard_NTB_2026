import re
import sys
from datetime import datetime, timedelta
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

sys.stdout.reconfigure(encoding='utf-8')

CREDENTIALS_PATH = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SPREADSHEET_ID   = '1XaziS_8UB2lCwL01bxam106EdIUHtlMISDGJX1PU5A8'
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

TINH_ORDER = ["Khánh Hòa", "Lâm Đồng", "Đắk Nông", "Ninh Thuận", "Bình Thuận"]
AM_EXTRA_MAP = {
    "Trần Công Hậu":          "Khánh Hòa",
    "Phạm Đức Thắng":         "Lâm Đồng",
    "Nguyễn Vĩnh Tường":      "Khánh Hòa",
    "Nguyễn Tống Hùng Phong": "Khánh Hòa",
}

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

def ws_to_df(ss, name):
    print(f"  📥 {name} ...", end=" ", flush=True)
    data = ss.worksheet(name).get_all_values(value_render_option='UNFORMATTED_VALUE')
    if not data: print("trống"); return pd.DataFrame()
    df = pd.DataFrame(data[1:], columns=data[0])
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except Exception: pass
    print(f"{len(df)} dòng ✅"); return df

def main():
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    ss = gspread.authorize(creds).open_by_key(SPREADSHEET_ID)
    
    print("📂 Loading data...")
    df_tq  = ws_to_df(ss, "tong_quan")
    df_khm = ws_to_df(ss, "f30")
    df_coc = ws_to_df(ss, "CoCauVung")
    
    am_tinh = (df_coc[["AM","Tỉnh"]].dropna()
               .drop_duplicates("AM").set_index("AM")["Tỉnh"].to_dict())
    am_tinh.update(AM_EXTRA_MAP)

    def get_tinh(am):
        am = str(am).strip()
        if am in am_tinh: return am_tinh[am]
        for k, v in am_tinh.items():
            if am in k or k in am: return v
        return None

    # Parse tong_quan
    df_tq["date"] = df_tq["Ngay"].apply(parse_vn_date)
    df_tq["DoanhThu"] = pd.to_numeric(df_tq["DoanhThu"], errors="coerce").fillna(0)
    df_tq["Volume"]   = pd.to_numeric(df_tq["Volume"],   errors="coerce").fillna(0)
    df_tq = df_tq.dropna(subset=["date"])
    df_tq = df_tq[~df_tq["AM_format"].astype(str).str.contains(",", na=False)]
    df_tq["Tinh"] = df_tq["AM_format"].apply(get_tinh)
    df_tq = df_tq[df_tq["Tinh"].notna()]
    
    dates = sorted(df_tq["date"].unique())
    d_cur = dates[-1]
    d_prev = dates[-2]
    d7 = min(dates, key=lambda d: abs((d-(d_cur-timedelta(days=7))).days))
    
    print(f"\nd_cur = {d_cur.date()} | d_prev = {d_prev.date()} | d7 = {d7.date()}")
    
    # Check daily
    t_cur = df_tq[df_tq["date"] == d_cur].groupby("Tinh")[["DoanhThu","Volume"]].sum()
    print("\nDaily Sums for d_cur:")
    print(t_cur)
    print("Total daily DT:", t_cur["DoanhThu"].sum() / 1e6, "M")
    
    # Check weekly
    df_tq["Tuan"] = df_tq["date"].apply(lambda d: f"{d.year}/{d.isocalendar()[1]:02d}")
    weeks = sorted([w for w in df_tq["Tuan"].unique() if w])
    w_cur, w_prev = weeks[-1], weeks[-2]
    print(f"\nw_cur = {w_cur} | w_prev = {w_prev}")
    wt_cur = df_tq[df_tq["Tuan"] == w_cur].groupby("Tinh")[["DoanhThu","Volume"]].sum()
    print("\nWeekly Sum for w_cur:")
    print(wt_cur)
    
    # Check monthly MTD
    m_start = d_cur.replace(day=1)
    prev_m_start = (m_start - timedelta(days=1)).replace(day=1)
    prev_m_end = prev_m_start.replace(day=d_cur.day)
    
    # MTD is cumulative from day 1 to day of d_cur
    mtd_cur = df_tq[(df_tq["date"] >= m_start) & (df_tq["date"] <= d_cur)].groupby("Tinh")[["DoanhThu","Volume"]].sum()
    mtd_prev = df_tq[(df_tq["date"] >= prev_m_start) & (df_tq["date"] <= prev_m_end)].groupby("Tinh")[["DoanhThu","Volume"]].sum()
    
    print("\nMTD Current Month:")
    print(mtd_cur)
    print("Total MTD Current:", mtd_cur["DoanhThu"].sum() / 1e6, "M")
    print("\nMTD Previous Month (1 to day of cur):")
    print(mtd_prev)
    print("Total MTD Previous:", mtd_prev["DoanhThu"].sum() / 1e6, "M")

if __name__ == "__main__":
    main()
