import requests
import json
import sys
from requests.auth import HTTPBasicAuth

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://ntb-mauve.vercel.app/api/off-spe"
try:
    print("Querying Vercel API: /api/off-spe...")
    res = requests.get(url, auth=HTTPBasicAuth('admin', 'admin123'), timeout=15)
    print("Status Code:", res.status_code)
    if res.status_code == 200:
        data = res.json()
        print("\n--- Vercel OFF SPE API response ---")
        for k in data.keys():
            if not isinstance(data[k], list):
                print(f"{k}: {data[k]}")
        records = data.get('records', [])
        print("\nNumber of records:", len(records))
        if len(records) > 0:
            print("\nFirst 3 records:")
            print(json.dumps(records[:3], indent=2))
    else:
        print("Response Text:", res.text)
except Exception as e:
    print("Error querying off-spe on Vercel:", e)
