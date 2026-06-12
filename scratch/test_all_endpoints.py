import requests
from requests.auth import HTTPBasicAuth

endpoints = [
    '/api/operational',
    '/api/opr',
    '/api/backlog',
    '/api/unstable-po',
    '/api/off-spe',
    '/api/volume-creation'
]

url_base = "https://ntb-mauve.vercel.app"
auth = HTTPBasicAuth('admin', 'admin123')

print("Querying all endpoints on Vercel...")
for ep in endpoints:
    url = url_base + ep
    try:
        res = requests.get(url, auth=auth, timeout=15)
        print(f"\n--- {ep} ---")
        print("Status Code:", res.status_code)
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, dict) and 'error' in data and data['error']:
                print("Returned JSON Error:", data['error'])
            else:
                print("Response JSON Keys:", list(data.keys()) if isinstance(data, dict) else "Not a dict")
        else:
            print("Response Text:", res.text[:200])
    except Exception as e:
        print(f"Error querying {ep}: {e}")
