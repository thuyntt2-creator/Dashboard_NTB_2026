import os
import requests
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv

load_dotenv(override=True)

with open('authorized_user.json', 'r') as f:
    token_data = json.load(f)

data = urllib.parse.urlencode({
    'grant_type': 'refresh_token',
    'client_id': token_data['client_id'],
    'client_secret': token_data['client_secret'],
    'refresh_token': token_data['refresh_token']
}).encode('utf-8')

req = urllib.request.Request(token_data['token_uri'], data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

access_token = None
with urllib.request.urlopen(req, timeout=10) as resp:
    res = json.loads(resp.read().decode('utf-8'))
    access_token = res.get("access_token")

headers_auth = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Authorization': f'Bearer {access_token}'
}

ssid = "1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ" # CONSOLIDATED_URL

# Method 1: Web export URL with Auth header
url1 = f"https://docs.google.com/spreadsheets/d/{ssid}/export?format=xlsx"
print("\n--- Method 1: web export?format=xlsx with Auth ---", flush=True)
r1 = requests.get(url1, headers=headers_auth, timeout=15)
print(f"Status: {r1.status_code}, len={len(r1.content)}", flush=True)

# Method 2: Drive API export with Auth header
url2 = f"https://www.googleapis.com/drive/v3/files/{ssid}/export?mimeType=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
print("\n--- Method 2: Drive API v3 export with Auth ---", flush=True)
r2 = requests.get(url2, headers=headers_auth, timeout=15)
print(f"Status: {r2.status_code}, len={len(r2.content)}", flush=True)

# Method 3: CSV Export for a specific GID using Drive API or web export with Auth header
gid = "260711009"
url3 = f"https://docs.google.com/spreadsheets/d/{ssid}/export?format=csv&gid={gid}"
print("\n--- Method 3: web export?format=csv&gid=... with Auth ---", flush=True)
r3 = requests.get(url3, headers=headers_auth, timeout=15)
print(f"Status: {r3.status_code}, len={len(r3.content)}", flush=True)
