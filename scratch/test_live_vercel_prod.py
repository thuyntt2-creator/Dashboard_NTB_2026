import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import requests

session = requests.Session()
login_res = session.post('https://namtrungbo.vercel.app/api/login', json={'username': 'admin', 'password': 'admin123'})
print("Login status:", login_res.status_code, login_res.json() if login_res.status_code == 200 else login_res.text)

res = session.get('https://namtrungbo.vercel.app/api/productivity-realtime')
print("API status:", res.status_code)
try:
    data = res.json()
    if 'records' in data:
        print(f"LIVE VERCEL SUCCESS! Total records: {len(data['records'])}")
        print("First 3 records from LIVE VERCEL:")
        for r in data['records'][:3]:
            print(r)
    else:
        print("LIVE VERCEL Response:", data)
except Exception as e:
    print("Error decoding JSON:", e, res.text[:200])
