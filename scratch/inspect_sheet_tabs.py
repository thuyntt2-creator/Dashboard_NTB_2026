import json
import urllib.request
import urllib.parse
import re
import unicodedata
import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import requests
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

url = os.getenv('CONSOLIDATED_URL', 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit')
match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
spreadsheet_id = match.group(1)

headers = {'Authorization': f'Bearer {access_token}'}
r = requests.get(f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit', headers=headers, timeout=20)

pattern = r'\[\s*\d+\s*,\s*0\s*,\s*\\"?(\d+)\\"?\s*,\s*\[\s*\{\s*\\"?1\\"?\s*:\s*\[\s*\[\s*0\s*,\s*0\s*,\s*\\"?([^\\"\(\]]+)\\"?'
matches = re.findall(pattern, r.text)

print(f"Total tabs: {len(matches)}")
for gid, name in matches:
    print(f"GID: {gid} | Name: {name} | Normalized: {unicodedata.normalize('NFC', name.strip().lower())}")
