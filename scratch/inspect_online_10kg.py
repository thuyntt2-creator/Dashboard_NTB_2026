import json
import urllib.request
import urllib.parse
import requests
import io
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

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

# Check GID 1203902008 ('trên10kg')
gid_10kg = '1203902008'
csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid_10kg}"
r = requests.get(csv_url, headers=headers, timeout=30)
print(f"Status for 'trên10kg' (gid={gid_10kg}): {r.status_code}, length={len(r.content)} bytes")

if r.status_code == 200:
    df = pd.read_csv(io.BytesIO(r.content), low_memory=False)
    print("DataFrame shape:", df.shape)
    print("Columns:", df.columns.tolist()[:15])
    for col in df.columns:
        if any(k in str(col).lower() for k in ['date', 'ngày', 'ngay', 'time']):
            u = sorted(df[col].dropna().astype(str).unique())
            print(f"  Col '{col}' ({len(u)} unique dates): min={u[0] if u else None}, max={u[-1] if u else None}")
            print(f"  Top 10 latest dates in {col}: {u[-10:]}")

# Check GID 1204060280 ('SL ')
gid_sl = '1204060280'
csv_url2 = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid_sl}"
r2 = requests.get(csv_url2, headers=headers, timeout=30)
print(f"\nStatus for 'SL ' (gid={gid_sl}): {r2.status_code}, length={len(r2.content)} bytes")
if r2.status_code == 200:
    df2 = pd.read_csv(io.BytesIO(r2.content), low_memory=False)
    print("DataFrame shape:", df2.shape)
    print("Columns:", df2.columns.tolist()[:15])
    for col in df2.columns:
        if any(k in str(col).lower() for k in ['date', 'ngày', 'ngay', 'time']):
            u = sorted(df2[col].dropna().astype(str).unique())
            print(f"  Col '{col}' ({len(u)} unique dates): min={u[0] if u else None}, max={u[-1] if u else None}")
            print(f"  Top 10 latest dates in {col}: {u[-10:]}")
