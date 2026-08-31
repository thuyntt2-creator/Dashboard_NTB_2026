import urllib.request
import pandas as pd
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid=260711009'
df = pd.read_csv(url, header=1)

bcs = ['(LDO) 1 Bảo Lộc', "(LDO) B'Lao", '(LDO) Bảo Lâm 1', '(LDO) Bảo Lâm 3']

print("=== CA 1 DATA FOR 2026-07-23 (AM Nga) ===")
ca1_sub = df[(df.iloc[:, 1].isin(bcs)) & (df.iloc[:, 3] == '2026-07-23 - Thứ 5')]
print(ca1_sub.iloc[:, [1, 2, 3, 4, 12]])

print("\n=== CA 2 DATA (Cols 15-26) FOR SAME ROWS IN GSHEET ===")
print(ca1_sub.iloc[:, [15, 16, 17, 18, 26]])
