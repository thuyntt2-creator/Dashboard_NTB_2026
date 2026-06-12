import subprocess
try:
    res = subprocess.run(["git", "log", "-n", "5", "--oneline"], capture_output=True, text=True, check=True)
    print("Git log:\n", res.stdout)
except Exception as e:
    print("Error running git log:", e)
