# -*- coding: utf-8 -*-
import subprocess

for commit in ["4a0a3c29", "43b9eccb", "e506515f", "2a0c1c14", "85e7b338"]:
    res = subprocess.run(["git", "show", f"{commit}:app.js"], capture_output=True, text=True, encoding='utf-8')
    lines = res.stdout.splitlines()
    found = [i for i, line in enumerate(lines) if "renderAgingCustomerChart" in line]
    print(f"Commit {commit}: found at line(s) {found}")
    if found:
        idx = found[0]
        print("\n".join(lines[idx:idx+25]))
        print("="*40)
