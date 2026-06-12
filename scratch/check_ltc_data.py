import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import pandas as pd
df = pd.read_csv('ops_ltc.csv')
df_day = df[df['Time'] == '2026-06-11 - Thứ 5']
print("Rows for 2026-06-11 - Thứ 5 in ops_ltc.csv:")
print(df_day[['Cấp quản lý', 'Chi tiết', 'Volume', '%LTC']].to_string())
