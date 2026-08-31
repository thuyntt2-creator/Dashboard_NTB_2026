import os
import requests
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv

load_dotenv(override=True)

# 1. Test get token
token_data = {
    "refresh_token": "1//0gJt8eR012LtlCgYIARAAGBASNwF-L9IrpYOsOcfOgp5eCzJAypgBRv1e5V_iDaWGw6IH4d_pOTmypYuR31WoKcpeLWi7r5SGZxY",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "914783987908-0gknc947mqscj9krsud67ocgmftb2q62.apps.googleusercontent.com",
    "client_secret": "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"
}

data = urllib.parse.urlencode({
    'grant_type': 'refresh_token',
    'client_id': token_data['client_id'],
    'client_secret': token_data['client_secret'],
    'refresh_token': token_data['refresh_token']
}).encode('utf-8')

req = urllib.request.Request(token_data['token_uri'], data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

access_token = None
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        access_token = res.get("access_token")
        print("Access Token acquired:", access_token[:20])
except Exception as e:
    print(f"Token refresh failed: {e}")

# 2. Test downloading export URL with Authorization header
url = os.getenv('OPS_URL', 'https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/edit')
ssid = "1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk"
export_url = f"https://docs.google.com/spreadsheets/d/{ssid}/export?format=xlsx"

print("\n--- Test 1: export?format=xlsx WITH Auth header ---")
headers_auth = {'Authorization': f'Bearer {access_token}'} if access_token else {}
res = requests.get(export_url, headers=headers_auth, timeout=15)
print(f"Status: {res.status_code}")
print(f"Content Length: {len(res.content)}")
print(f"Content Preview: {res.content[:100]}")

print("\n--- Test 2: export?format=xlsx WITHOUT Auth header ---")
res2 = requests.get(export_url, timeout=15)
print(f"Status: {res2.status_code}")
print(f"Content Length: {len(res2.content)}")

print("\n--- Test 3: Google Drive API v3 Files Export WITH Auth header ---")
drive_export_url = f"https://www.googleapis.com/drive/v3/files/{ssid}/export?mimeType=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
res3 = requests.get(drive_export_url, headers=headers_auth, timeout=15)
print(f"Status: {res3.status_code}")
print(f"Content Length: {len(res3.content)}")
if res3.status_code != 200:
    print(f"Response: {res3.text[:200]}")
