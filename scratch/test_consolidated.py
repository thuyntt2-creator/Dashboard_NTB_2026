import os
import requests
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv

load_dotenv(override=True)

# 1. Get token from authorized_user.json if available
headers_auth = {}
try:
    with open('authorized_user.json', 'r') as f:
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
        access_token = res.get("access_token")
        headers_auth = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
            'Authorization': f'Bearer {access_token}'
        }
        print("Token acquired successfully:", access_token[:15])
except Exception as e:
    print("Failed to get token:", e)

url = os.getenv('CONSOLIDATED_URL', 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit')
print(f"Testing CONSOLIDATED_URL: {url}")

headers_noauth = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
}

# Test WITH Auth
print("\n--- Request WITH Auth Header ---")
r1 = requests.get(url, headers=headers_auth, timeout=15)
print(f"HTTP Status: {r1.status_code}")
print(f"Content Length: {len(r1.content)}")

# Test WITHOUT Auth
print("\n--- Request WITHOUT Auth Header ---")
r2 = requests.get(url, headers=headers_noauth, timeout=15)
print(f"HTTP Status: {r2.status_code}")
print(f"Content Length: {len(r2.content)}")
