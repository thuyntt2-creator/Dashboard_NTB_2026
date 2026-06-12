import requests
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

url = "http://127.0.0.1:5000/api/off-spe"
try:
    res = requests.get(url, auth=('admin', 'admin123'))
    print("Status:", res.status_code)
    if res.status_code == 200:
        data = res.json()
        print("\n--- OFF SPE API response ---")
        for k in data.keys():
            if not isinstance(data[k], list):
                print(f"{k}: {data[k]}")
        
        records = data.get('records', [])
        print("\nNumber of records:", len(records))
        if len(records) > 0:
            print("\nFirst 3 records:")
            print(json.dumps(records[:3], indent=2))
    else:
        print("Error response:", res.text)
except Exception as e:
    print("Request failed:", e)
