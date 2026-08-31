import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import sys

sys.stdout.reconfigure(encoding='utf-8')

CREDENTIALS_PATH = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SPREADSHEET_ID   = '1XaziS_8UB2lCwL01bxam106EdIUHtlMISDGJX1PU5A8'
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

def main():
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    ss = gspread.authorize(creds).open_by_key(SPREADSHEET_ID)
    ws = ss.worksheet("phan_nhom")
    data = ws.get_all_values(value_render_option='UNFORMATTED_VALUE')
    df = pd.DataFrame(data[1:], columns=data[0])
    
    df_ntb = df[df['Vung'].astype(str).str.startswith('NTB')].copy()
    def parse_nhom_date(val):
        if isinstance(val, (int, float)):
            return pd.to_datetime(val, unit='D', origin='1899-12-30')
        s = str(val).strip()
        if s.isdigit():
            return pd.to_datetime(int(s), unit='D', origin='1899-12-30')
        return pd.to_datetime(s, errors='coerce')
    df_ntb['Ngay'] = df_ntb['Ngay'].apply(parse_nhom_date)
    
    df_ntb['DT_vol'] = pd.to_numeric(df_ntb['DT'], errors='coerce').fillna(0)
    df_ntb['AOV'] = pd.to_numeric(df_ntb['AOV'], errors='coerce').fillna(0)
    df_ntb['Revenue'] = df_ntb['DT_vol'] * df_ntb['AOV']
    
    # Let's filter to:
    # WTD current (Mon 15/06 to Wed 17/06)
    # WTD previous (Mon 08/06 to Wed 10/06)
    
    wtd_cur_dates = [pd.Timestamp('2026-06-15'), pd.Timestamp('2026-06-16'), pd.Timestamp('2026-06-17')]
    wtd_prev_dates = [pd.Timestamp('2026-06-08'), pd.Timestamp('2026-06-09'), pd.Timestamp('2026-06-10')]
    
    print("--- WTD CURRENT (15/06 - 17/06) ---")
    df_wtd_c = df_ntb[df_ntb['Ngay'].isin(wtd_cur_dates)]
    total_rev_c = df_wtd_c['Revenue'].sum()
    print(f"Total Revenue: {total_rev_c/1e6:.1f} million")
    by_group_c = df_wtd_c.groupby('Nhom')['Revenue'].sum()
    for group in ['A', 'BCD', 'EF', 'G']:
        val = by_group_c.get(group, 0)
        pct = val / total_rev_c * 100 if total_rev_c > 0 else 0
        print(f"  {group}: {val/1e6:.1f} million ({pct:.1f}%)")
        
    print("\n--- WTD PREVIOUS (08/06 - 10/06) ---")
    df_wtd_p = df_ntb[df_ntb['Ngay'].isin(wtd_prev_dates)]
    total_rev_p = df_wtd_p['Revenue'].sum()
    print(f"Total Revenue: {total_rev_p/1e6:.1f} million")
    by_group_p = df_wtd_p.groupby('Nhom')['Revenue'].sum()
    for group in ['A', 'BCD', 'EF', 'G']:
        val = by_group_p.get(group, 0)
        pct = val / total_rev_p * 100 if total_rev_p > 0 else 0
        print(f"  {group}: {val/1e6:.1f} million ({pct:.1f}%)")

if __name__ == '__main__':
    main()
