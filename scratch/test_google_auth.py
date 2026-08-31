import json
import urllib.request
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv(override=True)

with open('authorized_user.json', 'r') as f:
    token_data = json.load(f)

refresh_token = token_data.get("refresh_token")
client_id = token_data.get("client_id")
client_secret = token_data.get("client_secret")
token_uri = token_data.get("token_uri") or "https://oauth2.googleapis.com/token"

print(f"Client ID: {client_id}")
print(f"Token URI: {token_uri}")

data = urllib.parse.urlencode({
    'grant_type': 'refresh_token',
    'client_id': client_id,
    'client_secret': client_secret,
    'refresh_token': refresh_token
}).encode('utf-8')

req = urllib.request.Request(token_uri, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print("Refresh Success!")
        print("New Access Token:", res.get("access_token")[:20] + "...")
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code} - {e.reason}")
    print(e.read().decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")
