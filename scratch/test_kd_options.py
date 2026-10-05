import pandas as pd
import re
from datetime import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel(r'C:\Users\lap4all\Downloads\_NTB - BÁO CÁO TUẦN KINH DOANH (Looker).xlsx', sheet_name='tong_quan')

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

# Option A: Sunday to Saturday (as requested in user prompt 7: 13-19/9 -> 20-26/9 -> 27/9 - 3/10)
# Prev: 2026-09-20 to 2026-09-26
# Curr: 2026-09-27 to 2026-10-03
optA_prev = df[(df['d'] >= '2026-09-20') & (df['d'] <= '2026-09-26')]
optA_curr = df[(df['d'] >= '2026-09-27') & (df['d'] <= '2026-10-03')]

print("=== OPTION A: 20-26/9 vs 27/9-03/10 ===")
print(f"Prev DT: {optA_prev['dt'].sum():,.0f} đ, Vol: {optA_prev['vol'].sum():,.0f}")
print(f"Curr DT: {optA_curr['dt'].sum():,.0f} đ, Vol: {optA_curr['vol'].sum():,.0f}")

# Option B: Monday to Sunday (standard ISO week: W39: 21-27/9 vs W40: 28/9 - 04/10)
optB_prev = df[(df['d'] >= '2026-09-21') & (df['d'] <= '2026-09-27')]
optB_curr = df[(df['d'] >= '2026-09-28') & (df['d'] <= '2026-10-04')]

print("\n=== OPTION B: 21-27/9 (W39) vs 28/9-04/10 (W40) ===")
print(f"Prev DT: {optB_prev['dt'].sum():,.0f} đ, Vol: {optB_prev['vol'].sum():,.0f}")
print(f"Curr DT: {optB_curr['dt'].sum():,.0f} đ, Vol: {optB_curr['vol'].sum():,.0f}")
