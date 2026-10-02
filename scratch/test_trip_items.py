import sys
import os
import requests
import json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fetch_lastmile_productivity import get_ghn_token

token = get_ghn_token()
headers = {'Authorization': token, 'Content-Type': 'application/json'}

trip_codes = [
    '26A21126000ABGF21',
    '26A21126000AKX620',
    '26A21126000PYE419',
    '26A21126000AUYF18',
    '26A21126000QYM916',
    '26A21126000LBGB15',
    '26A21126000X8GJ14',
    '26A21126000CJ6R13',
    '26A21126000AAWN17'
]

for tc in trip_codes:
    r = requests.post('https://nhanh-api.ghn.vn/api/lastmile/trip/get-trip-items',
                      headers=headers, json={"tripCode": tc, "limit": 5000}, timeout=25)
    print(f"Trip {tc}: status={r.status_code}, items_count={len(r.json().get('data') or [])}")
