import requests
import json
from requests.auth import HTTPBasicAuth

url_status = "https://ntb-mauve.vercel.app/api/sync/status"
url_dash = "https://ntb-mauve.vercel.app/api/summary-dashboard"

output = []

output.append("Querying Vercel API sync status...")
try:
    res = requests.get(url_status, auth=HTTPBasicAuth('admin', 'admin123'), timeout=15)
    output.append(f"Status Code: {res.status_code}")
    output.append(f"Response JSON: {res.json()}")
except Exception as e:
    output.append(f"Error querying sync status: {e}")

output.append("\nQuerying Vercel API summary dashboard...")
try:
    res = requests.get(url_dash, auth=HTTPBasicAuth('admin', 'admin123'), timeout=15)
    output.append(f"Status Code: {res.status_code}")
    if res.status_code == 200:
        data = res.json()
        output.append(f"Keys in response: {list(data.keys())}")
        if 'latest_date' in data:
            output.append(f"Latest date: {data['latest_date']}")
        if 'all_dates' in data:
            output.append(f"All dates: {data['all_dates']}")
    else:
        output.append(f"Response Text: {res.text}")
except Exception as e:
    output.append(f"Error querying summary dashboard: {e}")

with open("scratch/vercel_api_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("Results written to scratch/vercel_api_res.txt")
