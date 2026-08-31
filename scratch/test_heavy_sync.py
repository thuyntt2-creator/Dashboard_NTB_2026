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

# 1. Download SL (ops_heavy_10kg.csv) - gid=1204060280
gid_sl = '1204060280'
r_sl = requests.get(f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid_sl}", headers=headers, timeout=30)
if r_sl.status_code == 200:
    with open('ops_heavy_10kg.csv', 'wb') as f:
        f.write(r_sl.content)
    print(f"Downloaded ops_heavy_10kg.csv ({len(r_sl.content)} bytes)")

# 2. Download trên10kg (ops_tao_don_10kg.csv and raw_tren10kg.csv) - gid=1203902008
gid_10kg = '1203902008'
r_10kg = requests.get(f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid_10kg}", headers=headers, timeout=30)
if r_10kg.status_code == 200:
    with open('ops_tao_don_10kg.csv', 'wb') as f:
        f.write(r_10kg.content)
    with open('raw_tren10kg.csv', 'wb') as f:
        f.write(r_10kg.content)
    print(f"Downloaded ops_tao_don_10kg.csv & raw_tren10kg.csv ({len(r_10kg.content)} bytes)")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import process_heavy_10kg_report

res = process_heavy_10kg_report()
print("\n--- PROCESS RESULT ---")
print("Total ops vol:", res.get('total_ops_vol'))
print("Total created vol:", res.get('total_created_vol'))
print("Selected date:", res.get('selected_date'))
print("Available dates:", res.get('available_dates'))
