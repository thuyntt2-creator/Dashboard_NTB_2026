import os
import sys
import pandas as pd
import re
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

downloads = r'C:\Users\lap4all\Downloads'
f1 = os.path.join(downloads, '[OE-IA] BÁO CÁO TRUY THU_Danh sách truy thu_Bảng.csv')
f2 = os.path.join(downloads, '[OE-IA] BÁO CÁO TRUY THU_Danh sách truy thu_Bảng (1).csv')
f_sheet = 'sheet_truythu.csv'

def parse_ghn_date(val):
    if not val or not isinstance(val, str):
        return None
    val = val.strip()
    m = re.search(r'(\d{1,2})\s+thg\s+(\d{1,2}),?\s+(\d{4})', val)
    if m:
        return datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    m2 = re.search(r'(\d{4})-(\d{2})-(\d{2})', val)
    if m2:
        return datetime(int(m2.group(1)), int(m2.group(2)), int(m2.group(3)))
    m3 = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', val)
    if m3:
        return datetime(int(m3.group(3)), int(m3.group(2)), int(m3.group(1)))
    return None

dfs = []
for p in [f1, f_sheet, f2]:
    if os.path.exists(p):
        d = pd.read_csv(p, low_memory=False)
        print(f"Loaded {p}: {len(d)} rows")
        dfs.append(d)

combined = pd.concat(dfs, ignore_index=True).drop_duplicates(subset=['Mã ticket', 'Mã truy thu', 'Nhân viên', 'Ngày kết luận truy thu'])
print(f"Combined deduplicated: {len(combined)} rows")

combined['date'] = combined['Ngày kết luận truy thu'].apply(parse_ghn_date)
w39 = combined[(combined['date'] >= '2026-09-21') & (combined['date'] <= '2026-09-27')]
w40 = combined[(combined['date'] >= '2026-09-28') & (combined['date'] <= '2026-10-04')]

print(f"W39 records: {len(w39):,}")
print(f"W40 records: {len(w40):,}")
