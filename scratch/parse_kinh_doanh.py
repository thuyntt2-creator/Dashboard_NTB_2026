import subprocess
import sys
import os

print("Running scratch/process_bckd_live.py to sync live Kinh Doanh & F30 from BCKD Google Sheet...")
res = subprocess.run([sys.executable, "-X", "utf8", "scratch/process_bckd_live.py"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Errors/Warnings:", res.stderr)
sys.exit(res.returncode)
