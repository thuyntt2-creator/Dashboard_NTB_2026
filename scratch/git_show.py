import subprocess
try:
    res = subprocess.run(["git", "show", "bc2ac4f", "--stat"], capture_output=True, text=True, check=True)
    print("Git show bc2ac4f --stat:\n", res.stdout)
    res_diff = subprocess.run(["git", "diff", "bc2ac4f^..bc2ac4f", "--", "app.py"], capture_output=True, text=True, check=True)
    print("Git diff in app.py:\n", res_diff.stdout[:1000])
except Exception as e:
    print("Error running git show:", e)
