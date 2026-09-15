import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'class="exec-banner' in line:
        content = ''.join(lines[i:min(i+20, len(lines))])
        print(f"--- Line {i+1} ---")
        h3 = re.search(r'<h3[^>]*>(.*?)</h3>', content, re.DOTALL)
        if h3:
            print("TITLE:", h3.group(1).strip())
        p = re.search(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
        if p:
            print("TEXT:", p.group(1).strip()[:250])
        print()
