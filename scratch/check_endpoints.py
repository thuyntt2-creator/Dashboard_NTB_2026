import sys
import requests
from requests.auth import HTTPBasicAuth

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

endpoints = [
    "/api/summary-dashboard",
    "/api/operational",
    "/api/trends-dashboard",
    "/api/ntb-structure",
    "/api/opr",
    "/api/backlog",
    "/api/unstable-po",
    "/api/off-spe",
    "/api/volume-creation",
    "/api/fd"
]

base_url = "https://ntb-ops-dashboard-five.vercel.app"
auth = HTTPBasicAuth('admin', 'admin123')

print("Checking endpoints on Vercel...")
for path in endpoints:
    url = base_url + path
    try:
        res = requests.get(url, auth=auth, timeout=15)
        print(f"Endpoint: {path}")
        print(f"  Status Code: {res.status_code}")
        if res.status_code == 200:
            try:
                data = res.json()
                if isinstance(data, dict):
                    print(f"  Keys in response: {list(data.keys())}")
                    if "error" in data:
                        print(f"  Error key present: {data['error']}")
                elif isinstance(data, list):
                    print(f"  Response is a list of length {len(data)}")
            except Exception as je:
                print(f"  Success, but response is not JSON: {je}")
        else:
            print(f"  Response text snippet: {res.text[:200]}")
    except Exception as e:
        print(f"  Error calling {path}: {e}")
    print("-" * 50)
