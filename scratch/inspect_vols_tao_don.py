import json
import urllib.request
import urllib.parse
import requests
import io
import os
import sys
import pandas as pd
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv(override=True)

# 1. Inspect local vols_tao_don.csv
if os.path.exists('vols_tao_don.csv'):
    df_local = pd.read_csv('vols_tao_don.csv', low_memory=False)
    print("Local vols_tao_don.csv shape:", df_local.shape)
    print("Local vols_tao_don.csv columns:", df_local.columns.tolist()[:10])
    for col in df_local.columns:
        if any(k in str(col).lower() for k in ['date', 'ngày', 'ngay', 'time', 'thời gian', 'hen_lay']):
            u = sorted(df_local[col].dropna().astype(str).unique())
            print(f"Local {col} dates ({len(u)}): {u[-10:]}")

# 2. Check online Google Sheet GID 849609343 ('shopee_tiktok')
with open('authorized_user.json', 'r', encoding='utf-8') as f:
    token_data = json.load(f)

data = urllib.parse.urlencode({
    'grant_type': 'refresh_token',
    'client_id': token_data['client_id'],
    'client_secret': token_data['client_secret'],
    'refresh_token': token_data['refresh_token']
}).encode('utf-8')
req = urllib.request.Request(token_data['token_uri'], data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
with urllib.request.urlopen(req, timeout=10) as resp:
    res = json.loads(resp.read().decode('utf-8'))
    access_token = res.get('access_token')

headers = {'Authorization': f'Bearer {access_token}'}
spreadsheet_id = '1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ'

# Let's inspect GID 849609343
csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid=849609343"
r = requests.get(csv_url, headers=headers, timeout=60)
print(f"\nOnline 'shopee_tiktok' (GID 849609343): status={r.status_code}, length={len(r.content)} bytes")
if r.status_code == 200:
    df_online = pd.read_csv(io.BytesIO(r.content), low_memory=False)
    print("Online shape:", df_online.shape)
    print("Online columns:", df_online.columns.tolist()[:10])
    for col in df_online.columns:
        if any(k in str(col).lower() for k in ['date', 'ngày', 'ngay', 'time', 'thời gian', 'hen_lay']):
            u = sorted(df_online[col].dropna().astype(str).unique())
            print(f"Online {col} dates ({len(u)}): {u[-10:]}")
