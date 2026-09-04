import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import csv
import json
import subprocess
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

spreadsheet_id = "1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ"
tab_name = "FD "

print(f"Fetching '{tab_name}' from {spreadsheet_id}...")
res = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range=f"'{tab_name}'!A1:W200"
).execute()

rows = res.get('values', [])
print(f"Retrieved {len(rows)} rows from Google Sheets.")

if not rows:
    print("Error: No rows returned!")
    sys.exit(1)

# Write to ops_fd.csv
with open('ops_fd.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for r in rows:
        writer.writerow(r)

print(f"Successfully updated ops_fd.csv ({len(rows)} rows).")

# Print check
for i, r in enumerate(rows[3:8]):
    print(f"Row {i+4}: {r[:3]}")

# Update Neon Database
print("\nUpdating Neon DB table ops_fd...")
p_db = subprocess.run([sys.executable, r"scratch\bootstrap_new_db.py"], capture_output=True, text=True, timeout=120)
print(f"DB Update exit code: {p_db.returncode}")
if p_db.stdout:
    for line in p_db.stdout.splitlines():
        if 'ops_fd' in line:
            print(" ", line)

# Git commit and push to Vercel
print("\nGit commit and push...")
subprocess.run(["git", "add", "ops_fd.csv", "scratch/"], capture_output=True)
p_commit = subprocess.run(["git", "commit", "-m", "Fix FD data: update real return orders and %FD"], capture_output=True, text=True)
print(f"Commit output: {p_commit.stdout.strip() if p_commit.stdout else p_commit.stderr.strip()}")

p_push = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True, timeout=60)
print(f"Push code: {p_push.returncode}")
if p_push.stderr:
    print(f"Push log: {p_push.stderr.strip()}")
if p_push.stdout:
    print(f"Push stdout: {p_push.stdout.strip()}")

print("\n=== All Done! ===")
