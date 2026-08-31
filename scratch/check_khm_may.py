import pickle
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"scratch\raw_sheets_data.pkl", "rb") as f:
    data = pickle.load(f)

df_khm = data['dataKHM']
print("df_khm head:")
print(df_khm.head())
print("\nUnique dates in Ngày LTC đầu tiên (first 50):")
print(df_khm['Ngày LTC đầu tiên'].unique()[:50])

# Let's count how many rows are parsed as May 2026
_MONTH_MAP = {f"thg {i}": i for i in range(1, 13)}
def parse_vn_date(s):
    if isinstance(s, (int, float)):
        return pd.to_datetime(s, unit='D', origin='1899-12-30').to_pydatetime()
    s = str(s).strip()
    if s.isdigit():
        return pd.to_datetime(int(s), unit='D', origin='1899-12-30').to_pydatetime()
    for m, num in _MONTH_MAP.items():
        if m in s:
            import re
            parts = re.findall(r"\d+", s)
            if len(parts) >= 2:
                from datetime import datetime
                return datetime(int(parts[-1]), num, int(parts[0]))
    return None

df_khm['ParsedDate'] = df_khm['Ngày LTC đầu tiên'].apply(parse_vn_date)
print("\nParsedDate non-null count:", df_khm['ParsedDate'].notna().sum())

# Filter for May 1 to May 16, 2026
from datetime import datetime
s_date = datetime(2026, 5, 1)
e_date = datetime(2026, 5, 16)
may_data = df_khm[(df_khm['ParsedDate'] >= s_date) & (df_khm['ParsedDate'] <= e_date)]
print(f"\nNumber of May 1-16 KHM records: {len(may_data)}")
print("May 1-16 records:")
print(may_data[['Mã KH', 'Tên KH', 'AM', 'Ngày LTC đầu tiên', 'DoanhThu_NoVAT', 'Volume']].head(20))

print("\nSum of DoanhThu_NoVAT for May 1-16:", may_data['DoanhThu_NoVAT'].astype(float).sum())
print("Sum of Volume for May 1-16:", may_data['Volume'].astype(float).sum())
print("Count of Mã KH for May 1-16:", may_data['Mã KH'].count())
