import sys, os, time, requests
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fetch_lastmile_productivity import get_ghn_token, get_today_info

today_int, _, _, _ = get_today_info()
token = get_ghn_token()
headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}

alert_wid_map = {
    '(LDO) Đức Trọng 1': '22389000',
    '(LDO) Tân Hà Lâm Hà': '22425000',
    '(KHO) Tây Nha Trang': '20320000',
    '(KHO) Bắc Cam Ranh': '21479000',
    '(LDO) Lang Biang - Đà Lạt 1': '22051000',
    '(LDO) Lang Biang - Đà Lạt 2': '21687000',
    '(DNO) Quảng Khê': '21364000',
    '(DNO) Đức An': '21477000',
    '(LDO) Hòa Ninh': '22759000',
    '(LDO) D\'Ran': '23189000',
    '(KHO) CK Diên Điền': '23098000'
}

def fetch_single_hub(bc, wid):
    trips = []
    for st in ['ON_TRIP', 'FINISHED']:
        p = {'hub_id': wid, 'status': st, 'offset': 0, 'limit': 100, 'reverse': 1}
        try:
            r = requests.post('https://nhanh-api.ghn.vn/api/lastmile/trip/get-trip-list-by-hub', headers=headers, json=p, timeout=10)
            if r.status_code == 200:
                for t in r.json().get('data') or []:
                    if t.get('startDateIndex') == today_int or t.get('createDateIndex') == today_int:
                        trips.append(t)
        except: pass
    
    total_gtc = 0
    for t in trips:
        code = t.get('tripCode')
        if not t.get('driverId'): continue
        try:
            r = requests.post('https://nhanh-api.ghn.vn/api/lastmile/trip/get-trip-items', headers=headers, json={'tripCode': code, 'limit': 5000}, timeout=15)
            if r.status_code == 200:
                for it in r.json().get('data') or []:
                    if it.get('type') == 'DELIVER' and it.get('isSucceeded'):
                        total_gtc += 1
        except: pass
    return bc, total_gtc, len(trips)

t0 = time.time()
print('Testing multi-threaded API fetch for 11 alert hubs...')
results = {}
with ThreadPoolExecutor(max_workers=11) as executor:
    futures = {executor.submit(fetch_single_hub, bc, wid): bc for bc, wid in alert_wid_map.items()}
    for f in as_completed(futures):
        bc, gtc, n_trips = f.result()
        results[bc] = (gtc, n_trips)
        print(f'{bc}: {gtc} GTC ({n_trips} chuyến)')

print(f'Total time: {time.time()-t0:.2f}s')
