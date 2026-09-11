import urllib.request, json

req = urllib.request.Request('https://api.github.com/repos/trungtran220792-hub/ntb-ops-dashboard/deployments', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        deployments = json.loads(resp.read().decode())
        for d in deployments[:5]:
            print(f"ID: {d['id']}, SHA: {d['sha']}, Created: {d['created_at']}")
except Exception as e:
    print('Error:', e)
