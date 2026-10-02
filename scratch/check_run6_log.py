import requests
import subprocess
import sys
sys.stdout.reconfigure(encoding='utf-8')

res = subprocess.run(['git', 'credential', 'fill'], input='protocol=https\nhost=github.com\n', capture_output=True, text=True)
token = None
for line in res.stdout.splitlines():
    if line.startswith('password='):
        token = line.split('=', 1)[1].strip()

headers = {'Authorization': f'token {token}'} if token else {}
# Get run 6 jobs
r = requests.get('https://api.github.com/repos/thuyntt2-creator/namtrungbo/actions/runs/371024602/jobs', headers=headers)
# wait, run ID for run 6: let's get latest run
runs_res = requests.get('https://api.github.com/repos/thuyntt2-creator/namtrungbo/actions/runs?per_page=3', headers=headers)
latest_run = runs_res.json()['workflow_runs'][0]
print(f"Run ID: {latest_run['id']}, Name: {latest_run['name']}")

jobs_res = requests.get(f"https://api.github.com/repos/thuyntt2-creator/namtrungbo/actions/runs/{latest_run['id']}/jobs", headers=headers)
jobs = jobs_res.json().get('jobs', [])
for job in jobs:
    print(f"Job: {job['name']}, status: {job['status']}, conclusion: {job['conclusion']}")
    for step in job.get('steps', []):
        print(f"  Step: {step['name']}, conclusion: {step['conclusion']}")

# Get job logs
job_id = jobs[0]['id']
log_res = requests.get(f"https://api.github.com/repos/thuyntt2-creator/namtrungbo/actions/jobs/{job_id}/logs", headers=headers)
lines = log_res.text.splitlines()
print(f"\nTotal log lines: {len(lines)}")
for l in lines:
    if 'Xuân Hương' in l or 'Xuân Trường' in l or 'Đã đọc tổng cộng' in l or 'Lê Văn Trường' in l:
        print(l)
