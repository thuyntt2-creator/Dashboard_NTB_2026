import urllib.request, json

for repo in ['thuyntt2-creator/Dashboard_NTB_2026', 'trungtran220792-hub/ntb-ops-dashboard']:
    try:
        req = urllib.request.Request(f'https://api.github.com/repos/{repo}/commits/main/status', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"Repo {repo} State: {data.get('state')}")
            for s in data.get('statuses', []):
                print(f"  - {s.get('context')}: {s.get('state')} -> {s.get('target_url')}")
    except Exception as e:
        print(repo, 'Error:', e)
