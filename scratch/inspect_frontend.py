import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

html_path = "templates/index.html"
with open(html_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "nav-tab" in line or "permissions" in line or "role" in line:
        if idx > 3600: # Usually JS starts later in the file
            print(f"Line {idx+1}: {line.strip()}")
