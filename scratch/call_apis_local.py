import sys
import os
import json

# Add current working directory to python path
sys.path.append(os.getcwd())

from app import app

# Create test client
client = app.test_client()

responses = {}

with app.test_request_context():
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'
        sess['permissions'] = [
            "tab-dashboard",
            "tab-introduction",
            "tab-ntb-summary",
            "tab-operational",
            "tab-opr",
            "tab-backlog",
            "tab-unstable-po",
            "tab-off-spe",
            "tab-volume-creation",
            "tab-fd",
            "tab-sync"
        ]

    # 1. Get Summary Dashboard
    res_summary = client.get('/api/summary-dashboard')
    if res_summary.status_code == 200:
        responses['summary_dashboard'] = res_summary.get_json()
    else:
        responses['summary_dashboard'] = f"Error {res_summary.status_code}: {res_summary.text}"

    # 2. Get FD data
    res_fd = client.get('/api/fd')
    if res_fd.status_code == 200:
        responses['fd'] = res_fd.get_json()
    else:
        responses['fd'] = f"Error {res_fd.status_code}: {res_fd.text}"

    # 3. Get Unstable PO data
    res_unstable = client.get('/api/unstable-po')
    if res_unstable.status_code == 200:
        responses['unstable_po'] = res_unstable.get_json()
    else:
        responses['unstable_po'] = f"Error {res_unstable.status_code}: {res_unstable.text}"

    # 4. Get Operational data
    res_operational = client.get('/api/operational')
    if res_operational.status_code == 200:
        responses['operational'] = res_operational.get_json()
    else:
        responses['operational'] = f"Error {res_operational.status_code}: {res_operational.text}"

# Save to file
with open("scratch/api_responses.json", "w", encoding="utf-8") as f:
    json.dump(responses, f, indent=4, ensure_ascii=False)

print("Done calling Flask test client!")
