import requests
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

url = "http://127.0.0.1:5000/api/operational"
try:
    res = requests.get(url, auth=('admin', 'admin123'))
    print("Status:", res.status_code)
    if res.status_code == 200:
        data = res.json()
        print("\n--- Operational API response ---")
        # Print top-level keys and values except the trends and top/worst lists which could be long
        for k in data.keys():
            if not isinstance(data[k], list):
                print(f"{k}: {data[k]}")
                
        print("\ntrend_ltc (last 3):")
        print(json.dumps(data.get('trend_ltc', [])[-3:], indent=2))
        
        print("\ntop_10_ltc (first 2):")
        print(json.dumps(data.get('top_10_ltc', [])[:2], indent=2))
    else:
        print("Error response:", res.text)
except Exception as e:
    print("Request failed:", e)
