import urllib.request
import pandas as pd
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ss_id = '1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ'
gid = '260711009'
url = f'https://docs.google.com/spreadsheets/d/{ss_id}/export?format=csv&gid={gid}'

df = pd.read_csv(url, header=1)

print("=== SAMPLE 15 ROWS FOR ALL 3 CATEGORIES ===")
for i in range(15):
    r = df.iloc[i]
    print(f"Row {i+2}: {r.iloc[1]} | Date1: {r.iloc[3]}")
    print(f"  CA 1 -> Vol: {r.iloc[4]}, %Gán: {r.iloc[5]}, %GTC: {r.iloc[6]}, Col7(GTC): {r.iloc[7]}, Col8(Tồn): {r.iloc[8]}")
    print(f"  CA 2 -> Vol: {r.iloc[18]}, %Gán: {r.iloc[19]}, %GTC: {r.iloc[20]}, Col21(GTC): {r.iloc[21]}, Col22(Tồn): {r.iloc[22]}")
    print(f"  TỒN  -> Vol: {r.iloc[32]}, %Gán: {r.iloc[33]}, %GTC: {r.iloc[34]}, Col35(GTC): {r.iloc[35]}, Col36(Tồn): {r.iloc[36]}\n")
