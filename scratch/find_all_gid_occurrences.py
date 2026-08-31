with open("scratch/raw_sheet.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
matches = [m.start() for m in re.finditer("843153285", html)]
print(f"Found {len(matches)} occurrences of 843153285:")
for i, m in enumerate(matches):
    print(f"\nMatch {i+1} at index {m}:")
    print(html[max(0, m - 100): min(len(html), m + 150)])
