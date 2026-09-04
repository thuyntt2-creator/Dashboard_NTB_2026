import urllib.request, json

for repo in ['BAOCAOVANHANHNTB', 'report']:
    url = f'https://api.github.com/repos/trungtran220792-hub/{repo}/deployments'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        print(f'Deployments on {repo}:', len(data))
        for d in data[:3]:
            s_url = d['statuses_url']
            s_req = urllib.request.Request(s_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(s_req) as s_resp:
                s_data = json.loads(s_resp.read().decode())
            target = s_data[0].get('target_url') if s_data else 'None'
            print('  ID:', d['id'], 'Target:', target)
    except Exception as e:
        print(repo, 'error:', e)
