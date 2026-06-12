import requests
import time
from requests.auth import HTTPBasicAuth

url_sync = "https://ntb-mauve.vercel.app/api/sync"
url_status = "https://ntb-mauve.vercel.app/api/sync/status"
auth = HTTPBasicAuth('admin', 'admin123')

print("Waiting 10 seconds for Vercel deploy to finalize...")
time.sleep(10)

print("Triggering sync on Vercel...")
try:
    res = requests.post(url_sync, auth=auth, timeout=60)
    print("Post Response Code:", res.status_code)
    print("Post Response JSON:", res.json())
except Exception as e:
    print("Error POST sync:", e)

# Poll status
start_time = time.time()
print("Polling Vercel status...")
for i in range(20):
    try:
        res = requests.get(url_status, auth=auth, timeout=10)
        data = res.json()
        status = data.get("status")
        progress = data.get("progress")
        error = data.get("error")
        
        elapsed = time.time() - start_time
        print(f"[{elapsed:.1f}s] status: {status}, progress: {progress}, error: {error}")
        
        if status in ["success", "error"]:
            break
    except Exception as e:
        print("Polling error:", e)
    time.sleep(2)
