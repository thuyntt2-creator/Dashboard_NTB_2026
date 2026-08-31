import sys
import requests
from requests.auth import HTTPBasicAuth

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://ntb-ops-dashboard-five.vercel.app/api/send-telegram-ai-briefing"
auth = HTTPBasicAuth('admin', 'admin123')

print("Triggering AI Briefing on Vercel...")
try:
    res = requests.post(url, auth=auth, json={}, timeout=30)
    print("Response Code:", res.status_code)
    print("Response JSON:", res.json())
except Exception as e:
    print("Error triggering AI briefing:", e)
