import subprocess
import requests

res = subprocess.run(['git', 'credential', 'fill'], input='protocol=https\nhost=github.com\n', capture_output=True, text=True)
token = None
for line in res.stdout.splitlines():
    if line.startswith('password='):
        token = line.split('=', 1)[1].strip()

workflow_id = 371024602
headers = {'Authorization': f'token {token}'} if token else {}
r = requests.put(f'https://api.github.com/repos/thuyntt2-creator/namtrungbo/actions/workflows/{workflow_id}/enable', headers=headers)
print('Enable status:', r.status_code)

# Check workflow state after enable
r_check = requests.get(f'https://api.github.com/repos/thuyntt2-creator/namtrungbo/actions/workflows/{workflow_id}', headers=headers)
print('Workflow state now:', r_check.json().get('state'))
