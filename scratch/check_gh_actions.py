import subprocess
import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

res = subprocess.run(['git', 'credential', 'fill'], input='protocol=https\nhost=github.com\n', capture_output=True, text=True)
token = None
for line in res.stdout.splitlines():
    if line.startswith('password='):
        token = line.split('=', 1)[1].strip()

if not token:
    print("No git credential found, trying public request...")
    r = requests.get('https://api.github.com/repos/thuyntt2-creator/namtrungbo/actions/workflows')
else:
    r = requests.get('https://api.github.com/repos/thuyntt2-creator/namtrungbo/actions/workflows', headers={'Authorization': f'token {token}'})

print('Workflows API status:', r.status_code)
if r.status_code == 200:
    workflows = r.json().get('workflows', [])
    for w in workflows:
        print(f"Workflow: {w['name']}, state: {w['state']}, id: {w['id']}, path: {w['path']}")
        
    # Check runs
    runs_res = requests.get('https://api.github.com/repos/thuyntt2-creator/namtrungbo/actions/runs?per_page=10', 
                            headers={'Authorization': f'token {token}'} if token else {})
    if runs_res.status_code == 200:
        runs = runs_res.json().get('workflow_runs', [])
        print("\nRecent Runs:")
        for run in runs:
            print(f"- Run #{run['run_number']}: {run['name']}, event: {run['event']}, status: {run['status']}, conclusion: {run['conclusion']}, created_at: {run['created_at']}")
else:
    print('Response:', r.text)
