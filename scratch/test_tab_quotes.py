import sys, json, urllib.parse, urllib.request, requests
sys.stdout.reconfigure(encoding='utf-8')

with open('authorized_user.json', 'r', encoding='utf-8') as f:
    t_data = json.load(f)
data = urllib.parse.urlencode({
    'grant_type': 'refresh_token',
    'client_id': t_data['client_id'],
    'client_secret': t_data['client_secret'],
    'refresh_token': t_data['refresh_token']
}).encode('utf-8')
req = urllib.request.Request(t_data['token_uri'], data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
res = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
token = res.get('access_token')
headers = {'Authorization': f'Bearer {token}'}

sheets = [
    ('Cong Dinh', '1uRoMDGPI0rJI5pqK4VA0QVfNj9B2vh9heNr9ow4MXaw', 'Chuyến Ghép/Tăng cường GXT'),
    ('NAK', '1_fDiARRteAUNEyas9tw9vvSDCppCudj_jxvqDrH8jug', 'Chuyến Ghép/Tăng cường GXT'),
    ('Manh Cuong', '1xQtd7DUZ9JVctuV7VChwR1AMy9KPCOy6cz2YFTOVXuo', 'Chuyến Ghép/Tăng cường GXT'),
    ('Lam Ngoc Thanh', '1VeYu4_Gs78E_sLRTx-Pq4PoDBmYR9oT8Ch6oDM_E2sM', 'Chuyến Ghép/Tăng cường GXT')
]

for name, sid, tab in sheets:
    encoded_tab = urllib.parse.quote(tab, safe='')
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/'{encoded_tab}'!A1:N20"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        rows = r.json().get('values', [])
        valid = [r for r in rows if any(r)]
        print(f'{name} ({tab}) non-empty rows: {len(valid)}')
        if len(valid) > 1:
            print('  Sample:', valid[1][:6])
    else:
        print(f'{name} ({tab}) HTTP {r.status_code} - {r.text[:100]}')
