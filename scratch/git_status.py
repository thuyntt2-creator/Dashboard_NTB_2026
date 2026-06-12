import subprocess
try:
    res = subprocess.run(["git", "status"], capture_output=True, text=True, check=True)
    print("Git status:\n", res.stdout)
except Exception as e:
    print("Error running git status:", e)
