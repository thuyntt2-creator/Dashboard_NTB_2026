import requests
from requests.auth import HTTPBasicAuth

endpoints = [
    '/api/operational',
    '/api/opr',
    '/api/backlog',
    '/api/unstable-po',
    '/api/off-spe',
    '/api/volume-creation',
    '/api/summary-dashboard'
]

auth = HTTPBasicAuth('admin', 'admin123')

for ep in endpoints:
    url = f"https://ntb-mauve.vercel.app{ep}"
    print(f"Testing {ep}...")
    try:
        res = requests.get(url, auth=auth, timeout=15)
        print(f"  Status Code: {res.status_code}")
        if res.status_code != 200:
            print(f"  Error Response: {res.text[:300]}")
        else:
            try:
                data = res.json()
                if isinstance(data, dict) and 'error' in data:
                    print(f"  JSON contains error: {data['error']}")
                else:
                    print(f"  Success (JSON format valid)")
            except:
                print("  Response is not valid JSON")
    except Exception as e:
        print(f"  Request failed: {e}")
