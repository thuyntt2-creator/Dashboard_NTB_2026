import pickle
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\raw_sheets_data.pkl", "rb") as f:
    data = pickle.load(f)

df_raw = data['data theo tuần']
sub = df_raw[(df_raw['AM'].astype(str).str.contains('Phan Đình Duy')) & (df_raw['Ngay'] == '16 thg 6, 2026')]

print("=== Raw rows for Phan Đình Duy on 16/06 ===")
for idx, r in sub.iterrows():
    print(r.to_dict())
