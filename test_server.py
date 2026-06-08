import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "http://127.0.0.1:5000/api/operational"
headers = {
    "Authorization": "Basic YWRtaW46YWRtaW4xMjM="
}

try:
    print("Sending GET request to localhost...")
    res = requests.get(url, headers=headers, timeout=10)
    print("Status code:", res.status_code)
    print("JSON Response:", res.json())
except Exception as e:
    print("Error:", e)
