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
    'Authorization': f'Bearer {access_token}'
}

ssid = "1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ"

# Method 2: Drive API export with Auth header
url2 = f"https://www.googleapis.com/drive/v3/files/{ssid}/export?mimeType=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
print("--- Drive API v3 export WITH Auth ---", flush=True)
r2 = requests.get(url2, headers=headers_auth, timeout=15)
print(f"Status: {r2.status_code}, len={len(r2.content)}", flush=True)
if r2.status_code != 200:
    print(r2.text[:300], flush=True)
