import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines with W38: {sum(1 for l in lines if 'W38' in l)}")
for i, l in enumerate(lines):
    if 'W38' in l:
        print(f"L{i+1}: {l.strip()[:100]}")
