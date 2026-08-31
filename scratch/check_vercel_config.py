import sys
import requests
from requests.auth import HTTPBasicAuth

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://ntb-ops-dashboard-five.vercel.app/api/config"
auth = HTTPBasicAuth('admin', 'admin123')

print("Fetching Vercel app configuration...")
try:
    res = requests.get(url, auth=auth, timeout=15)
    print("Response Code:", res.status_code)
    if res.status_code == 200:
        print("Config details (masked):", res.json())
    else:
        print("Response Text:", res.text)
except Exception as e:
    print("Error:", e)
