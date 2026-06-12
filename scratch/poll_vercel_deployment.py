import requests
import time
from requests.auth import HTTPBasicAuth

url_dash = "https://ntb-mauve.vercel.app/api/summary-dashboard"
auth = HTTPBasicAuth('admin', 'admin123')

print("Starting to poll Vercel deployment...")
for i in range(15):
    print(f"Attempt {i+1}/15...")
    try:
        res = requests.get(url_dash, auth=auth, timeout=15)
        if res.status_code == 200:
            data = res.json()
            latest_date = data.get('latest_date')
            print(f"Latest date on Vercel: {latest_date}")
            if latest_date and "06-11" in latest_date:
                print("Deployment successful and Neon DB data loaded on Vercel!")
                break
        else:
            print("Status code:", res.status_code)
    except Exception as e:
        print("Error:", e)
    time.sleep(5)
else:
    print("Polling timed out or latest date is still old. Vercel may still be building.")
