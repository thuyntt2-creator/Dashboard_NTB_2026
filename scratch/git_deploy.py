import subprocess
import sys

def run_cmd(args):
    print(f"Running: {' '.join(args)}")
    res = subprocess.run(args, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error: {res.stderr}")
        return False
    print(res.stdout)
    return True

print("Starting git commit and push process...")

# 1. Add app.py
if not run_cmd(["git", "add", "app.py"]):
    sys.exit(1)

# 2. Commit
if not run_cmd(["git", "commit", "-m", "fix: Vercel serverless cache init and sync issue"]):
    # Sometimes it fails if there are no changes, but that's fine
    pass

# 3. Push
if not run_cmd(["git", "push"]):
    sys.exit(1)

print("Git commit and push completed successfully!")
