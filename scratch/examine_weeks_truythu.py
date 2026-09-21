import pandas as pd
import sys
import re
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
df = pd.read_csv('scratch/truythu_raw.csv')

def parse_ghn_date(val):
    if not val or not isinstance(val, str):
        return None
    val = val.strip()
    m = re.search(r'(\d{1,2})\s+thg\s+(\d{1,2}),?\s+(\d{4})', val)
    if m:
        d, mth, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return datetime(y, mth, d)
    m2 = re.search(r'(\d{4})-(\d{2})-(\d{2})', val)
    if m2:
        return datetime(int(m2.group(1)), int(m2.group(2)), int(m2.group(3)))
    m3 = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', val)
    if m3:
        return datetime(int(m3.group(3)), int(m3.group(2)), int(m3.group(1)))
    return None

df['date'] = df['Ngày kết luận truy thu'].apply(parse_ghn_date)

# Let's see unique dates
print("Dates count:")
print(df['date'].value_counts().sort_index())

# Let's define the 2 weeks:
# Tuần N: 2026-09-14 to 2026-09-20
# Tuần N-1: 2026-09-07 to 2026-09-13 (plus 2026-09-06? Let's check 06/09)
def assign_week(d):
    if pd.isnull(d):
        return 'Unknown'
    if datetime(2026, 9, 14) <= d <= datetime(2026, 9, 20):
        return 'Tuần N (14/09-20/09)'
    elif datetime(2026, 9, 7) <= d <= datetime(2026, 9, 13):
        return 'Tuần N-1 (07/09-13/09)'
    elif d == datetime(2026, 9, 6):
        return '2026-09-06'
    else:
        return 'Khác'

df['week_group'] = df['date'].apply(assign_week)
print("\nWeek group counts:")
print(df['week_group'].value_counts())

# What about 2026-09-06?
row_sep6 = df[df['date'] == datetime(2026, 9, 6)]
print(f"\n2026-09-06 sample tickets: {len(row_sep6)}")
print(row_sep6[['Ngày kết luận truy thu', 'Loại truy thu', 'Số tiền ban đầu', 'Cần truy thu thêm']].head())
