import requests
from requests.auth import HTTPBasicAuth
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://ntb-mauve.vercel.app/api/files-status"
try:
    res = requests.get(url, auth=HTTPBasicAuth('admin', 'admin123'), timeout=15)
    print("Status Code:", res.status_code)
    if res.status_code == 200:
        print(json.dumps(res.json(), indent=2))
    else:
        print("Response Text:", res.text)
except Exception as e:
    print("Error:", e)
