import pandas as pd
import re
from datetime import datetime
import sys

sys.stdout.reconfigure(encoding='utf-8')

xl_path = r'C:\Users\lap4all\Downloads\_NTB - BÁO CÁO TUẦN KINH DOANH (Looker).xlsx'
df = pd.read_excel(xl_path, sheet_name='tong_quan')

def parse_d(val):
    if not val or not isinstance(val, str):
        return None
    m = re.search(r'(\d{1,2})\s+thg\s+(\d{1,2}),?\s+(\d{4})', val.strip())
    if m:
        return datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    return None

df['d'] = df['Ngay'].apply(parse_d)
df['dt'] = pd.to_numeric(df['DoanhThu'], errors='coerce').fillna(0)
df['vol'] = pd.to_numeric(df['Volume'], errors='coerce').fillna(0)

daily = df[df['d'] >= '2026-09-13'].groupby('d').agg({'dt': 'sum', 'vol': 'sum'}).sort_index()
for d, r in daily.iterrows():
    day_name = d.strftime('%a')
    print(f"{d.strftime('%Y-%m-%d')} ({day_name}): DT = {r['dt']/1e6:,.1f} Tr, Vol = {r['vol']:,.0f}")
