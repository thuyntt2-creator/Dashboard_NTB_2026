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
    
    # We do NOT filter by Vung
    def parse_nhom_date(val):
        if isinstance(val, (int, float)):
            return pd.to_datetime(val, unit='D', origin='1899-12-30')
        s = str(val).strip()
        if s.isdigit():
            return pd.to_datetime(int(s), unit='D', origin='1899-12-30')
        return pd.to_datetime(s, errors='coerce')
    df['Ngay'] = df['Ngay'].apply(parse_nhom_date)
    
    df['DT_vol'] = pd.to_numeric(df['DT'], errors='coerce').fillna(0)
    df['AOV'] = pd.to_numeric(df['AOV'], errors='coerce').fillna(0)
    df['Revenue'] = df['DT_vol'] * df['AOV']
    
    df['Tuan'] = df['Ngay'].apply(lambda d: f"{d.year}/{d.isocalendar()[1]:02d}" if pd.notna(d) else None)
    
    print("--- SEARCHING ALL REGIONS BY WEEK ---")
    for w in sorted(df['Tuan'].dropna().unique()):
        week_df = df[df['Tuan'] == w]
        total_rev = week_df['Revenue'].sum()
        if total_rev == 0: continue
        by_group = week_df.groupby('Nhom')['Revenue'].sum()
        print(f"Week {w} (Total: {total_rev/1e6:.1f}M):")
        for group in ['A', 'BCD', 'EF', 'G']:
            val = by_group.get(group, 0)
            pct = val / total_rev * 100 if total_rev > 0 else 0
            print(f"  {group}: {val/1e6:.1f}M ({pct:.1f}%)")

if __name__ == '__main__':
    main()
