import time
import urllib.request
import urllib.parse
import json
import re
import concurrent.futures

t0 = time.time()
url = 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit'

headers = {'User-Agent': 'Mozilla/5.0'}
token_data = {
    'refresh_token': '1//0gJt8eR012LtlCgYIARAAGBASNwF-L9IrpYOsOcfOgp5eCzJAypgBRv1e5V_iDaWGw6IH4d_pOTmypYuR31WoKcpeLWi7r5SGZxY',
    'token_uri': 'https://oauth2.googleapis.com/token',
    'client_id': '914783987908-0gknc947mqscj9krsud67ocgmftb2q62.apps.googleusercontent.com',
    'client_secret': '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'
}
data = urllib.parse.urlencode({'grant_type': 'refresh_token', **token_data}).encode('utf-8')
req_t = urllib.request.Request('https://oauth2.googleapis.com/token', data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
with urllib.request.urlopen(req_t, timeout=10) as resp_t:
    headers['Authorization'] = f'Bearer {json.loads(resp_t.read().decode()).get("access_token")}'

req_edit = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req_edit, timeout=10) as r:
    html = r.read().decode('utf-8')

pattern = r'\[\s*\d+\s*,\s*0\s*,\s*\\"?(\d+)\\"?\s*,\s*\[\s*\{\s*\\"?1\\"?\s*:\s*\[\s*\[\s*0\s*,\s*0\s*,\s*\\"?([^\\"\(\]]+)\\"?'
matches = re.findall(pattern, html)
gids = [gid for gid, name in matches[:15]]

def dl(gid):
    u = f'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid={gid}'
    req = urllib.request.Request(u, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return len(resp.read())

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
    results = list(ex.map(dl, gids))

t1 = time.time()
print(f'Downloaded {len(results)} GIDs in {round(t1-t0, 2)} seconds!')
