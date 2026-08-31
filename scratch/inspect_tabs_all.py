import json
import urllib.request
import urllib.parse
import requests
import re
import unicodedata
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# Read credentials
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

# Let's check candidate sheet IDs:
# 1. Consolidated company sheet
# 2. User sheet
# 3. Any other sheet in .env or recent scripts
sheets_to_check = [
    ('Company Consolidated', os.getenv('CONSOLIDATED_URL', '1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ')),
    ('User Sheet', os.getenv('USER_SHEET_ID', '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU')),
    ('User Sheet New', os.getenv('USER_SHEET_URL', '1V1JjSgU_M3xV0KkF3dC5t2Q2P8eN7vY5jA_8wX9zL0')),
]

pattern = r'\[\s*\d+\s*,\s*0\s*,\s*\\"?(\d+)\\"?\s*,\s*\[\s*\{\s*\\"?1\\"?\s*:\s*\[\s*\[\s*0\s*,\s*0\s*,\s*\\"?([^\\"\(\]]+)\\"?'

for title, s_id in sheets_to_check:
    match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', str(s_id))
    real_id = match.group(1) if match else str(s_id)
    url = f"https://docs.google.com/spreadsheets/d/{real_id}/edit"
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            matches = re.findall(pattern, r.text)
            print(f"=== {title} ({real_id}): {len(matches)} tabs ===")
            for gid, name in matches:
                print(f"  GID {gid}: '{name}'")
        else:
            print(f"=== {title} ({real_id}): HTTP {r.status_code} ===")
    except Exception as e:
        print(f"=== {title} ({real_id}): Error {e} ===")
