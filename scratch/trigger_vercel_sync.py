import requests
from requests.auth import HTTPBasicAuth

url_sync = "https://ntb-mauve.vercel.app/api/sync"
print("Triggering sync on Vercel...")
try:
    res = requests.post(url_sync, auth=HTTPBasicAuth('admin', 'admin123'), timeout=60)
    print("Status Code:", res.status_code)
    print("Response Text:", res.text)
except Exception as e:
    print("Error triggering sync:", e)
