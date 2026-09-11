import urllib.request, json

req = urllib.request.Request('https://api.github.com/repos/trungtran220792-hub/ntb-ops-dashboard/deployments', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        deployments = json.loads(resp.read().decode())
        if deployments:
            dep_id = deployments[0]['id']
            status_req = urllib.request.Request(f'https://api.github.com/repos/trungtran220792-hub/ntb-ops-dashboard/deployments/{dep_id}/statuses', headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(status_req) as s_resp:
                statuses = json.loads(s_resp.read().decode())
                for st in statuses:
                    print(st.get('state'), st.get('environment_url'), st.get('log_url'))
except Exception as e:
    print('Error:', e)
