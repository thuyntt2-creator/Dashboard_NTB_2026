import sys
import requests
from requests.auth import HTTPBasicAuth

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

url_dash = "https://ntb-ops-dashboard-five.vercel.app/api/summary-dashboard"
auth = HTTPBasicAuth('admin', 'admin123')

try:
    res = requests.get(url_dash, auth=auth, timeout=15)
    print("Status Code:", res.status_code)
    if res.status_code == 200:
        data = res.json()
        print("Keys in response:", list(data.keys()))
        if 'latest_date' in data:
            print("Latest date in API response:", data['latest_date'])
        else:
            print("latest_date key not found in response.")
        
        # Check volume or gtc data
        if 'total_volume' in data:
            print("Total Volume:", data['total_volume'])
        if 'overall_gtc' in data:
            print("Overall GTC:", data['overall_gtc'])
    else:
        print("Response Text:", res.text)
except Exception as e:
    print("Error querying summary dashboard:", e)
