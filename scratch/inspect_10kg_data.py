import os, sys, json, requests
import pandas as pd
from io import StringIO

sys.stdout.reconfigure(encoding='utf-8')

possible_paths = [
    r'authorized_user.json',
    r'C:\Users\lap4all\Documents\Auto report\authorized_user.json',
    r'C:\Users\lap4all\Desktop\Backlog_Automation\authorized_user.json',
]

access_token = None
for token_path in possible_paths:
    if not os.path.exists(token_path):
        continue
    try:
        with open(token_path, 'r', encoding='utf-8') as f:
            token_data = json.load(f)
        resp = requests.post(token_data['token_uri'], data={
            'grant_type': 'refresh_token',
            'client_id': token_data['client_id'],
            'client_secret': token_data['client_secret'],
            'refresh_token': token_data['refresh_token']
        }, timeout=10)
        if resp.status_code == 200:
            access_token = resp.json().get("access_token")
            break
    except Exception as e:
        pass

if not access_token:
    print("Failed to get token")
    sys.exit(1)

sheet_id = "1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ"
headers = {
    'Authorization': f'Bearer {access_token}',
    'User-Agent': 'Mozilla/5.0'
}

# 1. Fetch SL > 10kg (gid: 1204060280)
url_sl = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1204060280"
res_sl = requests.get(url_sl, headers=headers, timeout=30)
if res_sl.status_code == 200:
    with open("scratch/sheet_sl_10kg_raw.csv", "wb") as f:
        f.write(res_sl.content)
    print("Successfully saved scratch/sheet_sl_10kg_raw.csv")
else:
    print(f"Error fetching SL > 10kg: {res_sl.status_code}")

# 2. Fetch tren10kg (gid: 1203902008)
url_tren = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1203902008"
res_tren = requests.get(url_tren, headers=headers, timeout=30)
if res_tren.status_code == 200:
    with open("scratch/sheet_tren10kg_raw.csv", "wb") as f:
        f.write(res_tren.content)
    print("Successfully saved scratch/sheet_tren10kg_raw.csv")
else:
    print(f"Error fetching tren10kg: {res_tren.status_code}")

df_sl = pd.read_csv("scratch/sheet_sl_10kg_raw.csv")
print("\n--- DF SL > 10kg ---")
print("Shape:", df_sl.shape)
print("Columns:", list(df_sl.columns))
print(df_sl.head(2))

df_tren = pd.read_csv("scratch/sheet_tren10kg_raw.csv")
print("\n--- DF tren10kg (Tạo đơn) ---")
print("Shape:", df_tren.shape)
print("Columns:", list(df_tren.columns))
print(df_tren.head(2))

