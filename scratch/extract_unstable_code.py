import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

import re

# Let's find def process_unstable_po(): and extract the function body
start_match = re.search(r"def process_unstable_po\(\):", content)
if start_match:
    start_idx = start_match.start()
    # Let's read 150 lines from start_idx
    lines = content[start_idx:].splitlines()
    with open("scratch/unstable_po_code.txt", "w", encoding="utf-8") as out:
        for line in lines[:100]:
            out.write(line + "\n")
    print("Code extracted successfully!")
else:
    print("Function process_unstable_po not found!")
