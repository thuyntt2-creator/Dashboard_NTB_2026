import time
import subprocess
import sys
import os

cwd = r"c:\Users\lap4all\Desktop\New folder"
print("Auto sync background loop started. Will sync every 30 minutes.", flush=True)

while True:
    try:
        subprocess.run([sys.executable, os.path.join(cwd, "auto_sync_and_push.py")], cwd=cwd)
    except Exception as e:
        print(f"Error in sync loop: {e}", flush=True)
    # Sleep 30 minutes (1800 seconds)
    time.sleep(1800)
