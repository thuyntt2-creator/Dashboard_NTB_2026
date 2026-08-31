import json
import urllib.request
import urllib.parse
import os
import requests
import re
from dotenv import load_dotenv

load_dotenv(override=True)

with open('authorized_user.json', 'r') as f:
    token_data = json.load(f)

refresh_token = token_data.get("refresh_token")
client_id = token_data.get("client_id")
client_secret = token_data.get("client_secret")
token_uri = token_data.get("token_uri") or "https://oauth2.googleapis.com/token"

data = urllib.parse.urlencode({
    'grant_type': 'refresh_token',
    'client_id': client_id,
    'client_secret': client_secret,
    'refresh_token': refresh_token
}).encode('utf-8')

req = urllib.request.Request(token_uri, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

access_token = None
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        access_token = res.get("access_token")
except Exception as e:
    print(f"Token refresh failed: {e}", flush=True)

headers = {'Authorization': f'Bearer {access_token}'} if access_token else {}
print(f"Using access_token: {access_token[:15] if access_token else 'None'}...", flush=True)

urls_to_test = {
    'OPS_URL': os.getenv('OPS_URL'),
    'OPR_URL': os.getenv('OPR_URL'),
    'AGING_URL': os.getenv('AGING_URL'),
    'TREO_URL': os.getenv('TREO_URL'),
    'BAT_ON_URL': os.getenv('BAT_ON_URL'),
    'OFF_SPE_URL': os.getenv('OFF_SPE_URL'),
    'TAO_DON_URL': os.getenv('TAO_DON_URL'),
    'CONSOLIDATED_URL': os.getenv('CONSOLIDATED_URL'),
}

for name, url in urls_to_test.items():
    if not url:
        print(f"{name}: Missing URL", flush=True)
        continue
    match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
    if not match:
        print(f"{name}: Invalid URL format ({url})", flush=True)
        continue
    ssid = match.group(1)
    export_url = f"https://docs.google.com/spreadsheets/d/{ssid}/export?format=xlsx"
    
    print(f"\n--- Testing {name} ({ssid}) ---", flush=True)
    try:
        res_auth = requests.get(export_url, headers=headers, timeout=10)
        print(f"  With Auth: HTTP {res_auth.status_code}, len={len(res_auth.content)}", flush=True)
    except Exception as e:
        print(f"  With Auth Error: {e}", flush=True)
        
    try:
        res_noauth = requests.get(export_url, timeout=10)
        print(f"  No Auth:   HTTP {res_noauth.status_code}, len={len(res_noauth.content)}", flush=True)
    except Exception as e:
        print(f"  No Auth Error: {e}", flush=True)
