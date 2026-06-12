import requests
import json

endpoints = [
    '/api/operational',
    '/api/opr',
    '/api/backlog',
    '/api/unstable-po',
    '/api/off-spe',
    '/api/volume-creation'
]

# Set up basic auth header since requires_auth/requires_permission is used
auth = ('admin', 'admin123')

for ep in endpoints:
    url = f"http://127.0.0.1:5000{ep}"
    try:
        print(f"Querying {url}...")
        res = requests.get(url, auth=auth, timeout=10)
        print(f"  Status: {res.status_code}")
        if res.status_code != 200:
            print(f"  Error Response: {res.text[:500]}")
        else:
            data = res.json()
            print(f"  Success! Keys: {list(data.keys()) if isinstance(data, dict) else len(data)}")
    except Exception as e:
        print(f"  Exception querying {url}: {e}")
