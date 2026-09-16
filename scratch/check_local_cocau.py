import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv('co_cau_ntb.csv', header=None)
print("co_cau_ntb.csv shape:", df.shape)
print("Sample rows:")
for i, r in df.head(30).iterrows():
    print(r.tolist())

# Look for Duc Trong or Di Linh or Vu
matches = df[df[1].str.contains('Đức Trọng|Di Linh|Đơn Dương|Gia Nghĩa|Quảng Tín', na=False)]
print("\nMatches in co_cau_ntb.csv:")
for i, r in matches.drop_duplicates(subset=[1]).iterrows():
    print(r.tolist())
