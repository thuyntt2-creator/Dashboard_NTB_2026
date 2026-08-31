import sys
import requests
from requests.auth import HTTPBasicAuth
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

url_sync = "https://ntb-ops-dashboard-five.vercel.app/api/sync"
url_status = "https://ntb-ops-dashboard-five.vercel.app/api/sync/status"
auth = HTTPBasicAuth('admin', 'admin123')

print("Triggering sync on the new Vercel project...")
try:
    res = requests.post(url_sync, auth=auth, timeout=30)
    print("Post Response Code:", res.status_code)
    print("Post Response JSON:", res.json())
except Exception as e:
    print("Error POST sync:", e)

# Poll status
start_time = time.time()
print("Polling sync status...")
for i in range(15):
    try:
        res = requests.get(url_status, auth=auth, timeout=10)
        data = res.json()
        status = data.get("status")
        progress = data.get("progress")
        error = data.get("error")
        ts = data.get("timestamp")
        
        elapsed = time.time() - start_time
        print(f"[{elapsed:.1f}s] status: {status}, progress: {progress}, error: {error}, timestamp: {ts}")
        
        if status in ["success", "error"]:
            break
    except Exception as e:
        print("Polling error:", e)
    time.sleep(2)
