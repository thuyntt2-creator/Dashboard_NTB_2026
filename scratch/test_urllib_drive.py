import os
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

ssid = "1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ"
drive_url = f"https://www.googleapis.com/drive/v3/files/{ssid}/export?mimeType=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

req_drive = urllib.request.Request(drive_url, headers={'Authorization': f'Bearer {access_token}'})
print("Sending Drive API request via urllib...", flush=True)

try:
    with urllib.request.urlopen(req_drive, timeout=15) as resp:
        data = resp.read()
        print(f"Success! Status={resp.status}, Received {len(data)} bytes", flush=True)
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code} - {e.reason}", flush=True)
    print(e.read().decode('utf-8')[:300], flush=True)
except Exception as e:
    print(f"Error: {e}", flush=True)
