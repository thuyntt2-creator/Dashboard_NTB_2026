import urllib.request
import pandas as pd
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid=260711009'
df = pd.read_csv(url, header=1)

print("=== ALL ROWS FOR 1 BẢO LỘC IN SOURCE GSHEET ===")
bl = df[df.iloc[:, 1].astype(str).str.contains('1 Bảo Lộc', na=False)]

for idx, r in bl.iterrows():
    print(f"\nRow {idx}:")
    print(f"  Ca 1 -> Time: {r.iloc[3]} | Vol: {r.iloc[4]} | %Gán: {r.iloc[5]} | %GTC: {r.iloc[6]} | GTC_col: {r.iloc[7]}")
    print(f"  Ca 2 -> Time: {r.iloc[17]} | Vol: {r.iloc[18]} | %Gán: {r.iloc[19]} | %GTC: {r.iloc[20]} | GTC_col: {r.iloc[21]}")
    print(f"  Tồn  -> Time: {r.iloc[31]} | Vol: {r.iloc[32]} | %Gán: {r.iloc[33]} | %GTC: {r.iloc[34]} | GTC_col: {r.iloc[35]}")
