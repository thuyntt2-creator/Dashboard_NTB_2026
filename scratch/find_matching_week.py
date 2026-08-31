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
    
    df_ntb['Tuan'] = df_ntb['Ngay'].apply(lambda d: f"{d.year}/{d.isocalendar()[1]:02d}" if pd.notna(d) else None)
    
    # Let's search by week
    print("--- SEARCHING BY WEEK ---")
    for w in sorted(df_ntb['Tuan'].dropna().unique()):
        week_df = df_ntb[df_ntb['Tuan'] == w]
        total_rev = week_df['Revenue'].sum()
        if total_rev == 0: continue
        by_group = week_df.groupby('Nhom')['Revenue'].sum()
        print(f"Week {w} (Total: {total_rev/1e6:.1f}M):")
        for group in ['A', 'BCD', 'EF', 'G']:
            val = by_group.get(group, 0)
            pct = val / total_rev * 100 if total_rev > 0 else 0
            print(f"  {group}: {val/1e6:.1f}M ({pct:.1f}%)")
            
    # Let's also check by single day (in case the screenshot is for a single day, or MTD, or rolling 7 days)
    print("\n--- SEARCHING BY DAY ---")
    for dt in sorted(df_ntb['Ngay'].dropna().unique()):
        day_df = df_ntb[df_ntb['Ngay'] == dt]
        total_rev = day_df['Revenue'].sum()
        if total_rev > 500e6: # If a day has >500M revenue (maybe consolidated?)
            print(f"Day {dt.date()} (Total: {total_rev/1e6:.1f}M):")
            by_group = day_df.groupby('Nhom')['Revenue'].sum()
            for group in ['A', 'BCD', 'EF', 'G']:
                val = by_group.get(group, 0)
                print(f"  {group}: {val/1e6:.1f}M")

if __name__ == '__main__':
    main()
