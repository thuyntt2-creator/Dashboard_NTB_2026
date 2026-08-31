import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import json
import urllib.request
import urllib.parse
import os
import requests
import io
import pandas as pd
from dotenv import load_dotenv

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
    access_token = json.loads(resp.read().decode('utf-8'))['access_token']

headers = {'Authorization': f'Bearer {access_token}'}
url = 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid=204876430'
r = requests.get(url, headers=headers, timeout=30)

print(f"Status: {r.status_code}, Length: {len(r.content)} bytes")
lines = r.text.split('\n')
print(f"Total lines in 'baocao' tab: {len(lines)}")
print("First 20 lines:")
for i, line in enumerate(lines[:20]):
    print(f"Line {i+1}: {line}")
