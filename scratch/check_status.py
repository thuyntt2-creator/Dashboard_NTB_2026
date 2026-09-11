import urllib.request, json, time

for i in range(3):
    try:
        req = urllib.request.Request('https://api.github.com/repos/thuyntt2-creator/namtrungbo/commits/main/status', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"[{i+1}] State: {data.get('state')}")
            for s in data.get('statuses', []):
                print(f"  - {s.get('context')}: {s.get('state')} -> {s.get('target_url')}")
    except Exception as e:
        print('Error:', e)
    time.sleep(3)
