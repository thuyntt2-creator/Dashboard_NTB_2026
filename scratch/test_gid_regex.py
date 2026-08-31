import urllib.request
import urllib.parse
import json
import re

def get_auth_headers():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    token_data = {
        'refresh_token': '1//0gJt8eR012LtlCgYIARAAGBASNwF-L9IrpYOsOcfOgp5eCzJAypgBRv1e5V_iDaWGw6IH4d_pOTmypYuR31WoKcpeLWi7r5SGZxY',
        'token_uri': 'https://oauth2.googleapis.com/token',
        'client_id': '914783987908-0gknc947mqscj9krsud67ocgmftb2q62.apps.googleusercontent.com',
        'client_secret': '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',
        'scopes': ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'],
        'universe_domain': 'googleapis.com'
    }
    data = urllib.parse.urlencode({
        'grant_type': 'refresh_token',
        'client_id': token_data['client_id'],
        'client_secret': token_data['client_secret'],
        'refresh_token': token_data['refresh_token']
    }).encode('utf-8')
    req_t = urllib.request.Request(token_data['token_uri'], data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    with urllib.request.urlopen(req_t, timeout=15) as resp_t:
        access_token = json.loads(resp_t.read().decode('utf-8')).get('access_token')
        headers['Authorization'] = f'Bearer {access_token}'
    return headers

headers = get_auth_headers()
url = 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit'
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode('utf-8')

pattern = r'\[\s*\d+\s*,\s*0\s*,\s*\\"?(\d+)\\"?\s*,\s*\[\s*\{\s*\\"?1\\"?\s*:\s*\[\s*\[\s*0\s*,\s*0\s*,\s*\\"?([^\\"\(\]]+)\\"?'
matches = re.findall(pattern, html)
print('Matches count:', len(matches))
for gid, name in matches[:10]:
    print(f'GID: {gid}, Name: {name}')
