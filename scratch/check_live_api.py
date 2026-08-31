import urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')

endpoints = [
    '/api/operational',
    '/api/summary-dashboard',
    '/api/trends-dashboard',
    '/api/batch-data'
]

headers = {'User-Agent': 'Mozilla/5.0'}

for ep in endpoints:
    url = f'https://ntb-ops-dashboard-five.vercel.app{ep}'
    print(f"=== Fetching {url} ===")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        print(f"Status Code: {resp.status}")
        if isinstance(data, dict):
            print("Keys:", list(data.keys()))
            if 'overall_ltc' in data:
                print("overall_ltc:", data['overall_ltc'])
            if 'ops' in data and isinstance(data['ops'], dict):
                print("ops.overall_ltc:", data['ops'].get('overall_ltc'))
                print("ops.trend_ltc:", data['ops'].get('trend_ltc')[:2] if data['ops'].get('trend_ltc') else None)
            if 'trend_ltc' in data:
                print("trend_ltc:", data['trend_ltc'][:2] if data['trend_ltc'] else None)
            if 'error' in data:
                print("Error:", data['error'])
        else:
            print("Type:", type(data))
    except Exception as e:
        print(f"Error fetching {ep}: {e}")
    print()
