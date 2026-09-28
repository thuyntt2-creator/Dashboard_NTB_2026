import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    text = f.read()

for i, m in enumerate(re.finditer(r'.{0,40}W35.{0,40}', text)):
    print(f"{i+1}: {m.group(0).strip().replace(chr(10), ' ')}")
