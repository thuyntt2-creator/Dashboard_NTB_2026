import requests
import time
import json
import re
import concurrent.futures

def get_auth_headers():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    token_data = {
        'refresh_token': '1//0gJt8eR012LtlCgYIARAAGBASNwF-L9IrpYOsOcfOgp5eCzJAypgBRv1e5V_iDaWGw6IH4d_pOTmypYuR31WoKcpeLWi7r5SGZxY',
        'token_uri': 'https://oauth2.googleapis.com/token',
        'client_id': '914783987908-0gknc947mqscj9krsud67ocgmftb2q62.apps.googleusercontent.com',
        'client_secret': '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'
    }
    r = requests.post('https://oauth2.googleapis.com/token', data={'grant_type': 'refresh_token', **token_data}).json()
    headers['Authorization'] = f'Bearer {r.get("access_token")}'
    return headers

headers = get_auth_headers()
url = 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit'
spreadsheet_id = '1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ'

r_edit = requests.get(url, headers=headers)
pattern = r'\[\s*\d+\s*,\s*0\s*,\s*\\"?(\d+)\\"?\s*,\s*\[\s*\{\s*\\"?1\\"?\s*:\s*\[\s*\[\s*0\s*,\s*0\s*,\s*\\"?([^\\"\(\]]+)\\"?'
matches = re.findall(pattern, r_edit.text)

print(f"Found {len(matches)} GIDs.")

def download_gid(gid, name):
    csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}"
    for attempt in range(4):
        try:
            time.sleep(0.2 * (attempt + 1))
            res = requests.get(csv_url, headers=headers, timeout=20)
            if res.status_code == 200 and len(res.content) > 100:
                return True, gid, name, len(res.content)
            elif res.status_code == 429:
                time.sleep(1.5 * (attempt + 1))
        except Exception as e:
            time.sleep(1.5)
    return False, gid, name, 0

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(download_gid, gid, name) for gid, name in matches[:15]]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]

successes = [r for r in results if r[0]]
print(f"SUCCESS: {len(successes)} / {len(results)} downloaded cleanly!")
for s in successes:
    print(f"  GID {s[1]}: {s[3]} bytes")
