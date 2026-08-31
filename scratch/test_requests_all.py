import requests
import time
import concurrent.futures
import re

t0 = time.time()
res_token = requests.post('https://oauth2.googleapis.com/token', data={
    'grant_type': 'refresh_token',
    'client_id': '914783987908-0gknc947mqscj9krsud67ocgmftb2q62.apps.googleusercontent.com',
    'client_secret': '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',
    'refresh_token': '1//0gJt8eR012LtlCgYIARAAGBASNwF-L9IrpYOsOcfOgp5eCzJAypgBRv1e5V_iDaWGw6IH4d_pOTmypYuR31WoKcpeLWi7r5SGZxY'
}).json()

headers = {'Authorization': f'Bearer {res_token["access_token"]}', 'User-Agent': 'Mozilla/5.0'}

# Fetch edit HTML to extract GIDs
edit_url = 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit'
r_edit = requests.get(edit_url, headers=headers)

pattern = r'\[\s*\d+\s*,\s*0\s*,\s*\\"?(\d+)\\"?\s*,\s*\[\s*\{\s*\\"?1\\"?\s*:\s*\[\s*\[\s*0\s*,\s*0\s*,\s*\\"?([^\\"\(\]]+)\\"?'
matches = re.findall(pattern, r_edit.text)
print('Found GIDs count:', len(matches))

def download_one(args):
    gid, name = args
    u = f'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid={gid}'
    r = requests.get(u, headers=headers, timeout=20)
    return (gid, name, r.status_code, len(r.content))

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
    results = list(ex.map(download_one, matches[:15]))

t1 = time.time()
print(f'Downloaded {len(results)} GIDs with requests in {round(t1-t0, 2)}s!')
for gid, name, status, length in results:
    print(f'  GID {gid} ({name}): Status {status}, Size {length} bytes')
