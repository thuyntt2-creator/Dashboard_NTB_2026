import requests
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

url = "http://127.0.0.1:5000/api/summary-dashboard"
try:
    # Use Basic Auth (admin / admin123)
    res = requests.get(url, auth=('admin', 'admin123'))
    print("Status:", res.status_code)
    if res.status_code == 200:
        data = res.json()
        print("\n--- API response overview ---")
        print("latest_date:", data.get('latest_date'))
        print("\nkpis -> overall:")
        print(json.dumps(data.get('kpis', {}).get('overall', {}), indent=2))
        
        print("\nkpis -> lambda_dong (or similar):")
        # Print some keys in kpis
        kpis = data.get('kpis', {})
        for k in list(kpis.keys())[:3]:
            if k != 'overall':
                print(f"Key: {k}, name: {kpis[k].get('name')}")
                print(f"  ltc: {kpis[k].get('ltc')}%")
                print(f"  gtc: {kpis[k].get('gtc')}%")
                print(f"  ttc: {kpis[k].get('ttc')}%")
                
        # Also print completed_vols first 2 records
        print("\ncompleted_vols (first 2):")
        print(json.dumps(data.get('completed_vols', [])[:2], indent=2))
    else:
        print("Error response:", res.text)
except Exception as e:
    print("Request failed:", e)
