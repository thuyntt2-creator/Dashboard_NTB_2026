import sys
import os
import requests
import json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fetch_lastmile_productivity import get_ghn_token, get_today_info

token = get_ghn_token()
headers = {'Authorization': token, 'Content-Type': 'application/json'}
today_int, date_str_vn, time_str, _ = get_today_info()
print('today_int:', today_int)

hub_id = '21126000'
for st in ['ON_TRIP', 'FINISHED', 'NEW']:
    r = requests.post('https://nhanh-api.ghn.vn/api/lastmile/trip/get-trip-list-by-hub',
                      headers=headers, json={'hub_id': hub_id, 'status': st, 'offset': 0, 'limit': 100, 'reverse': 1})
    data = r.json().get('data') or []
    print(f'Status {st}: found {len(data)} trips')
    for t in data[:12]:
        print(f"  Trip: {t.get('tripCode')}, Driver: {t.get('driverId')}_{t.get('driverName')}, start: {t.get('startDateIndex')}, create: {t.get('createDateIndex')}, pick: {t.get('pickCount')}, deliver: {t.get('deliverCount')}")
