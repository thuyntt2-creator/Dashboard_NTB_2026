import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

matches = re.findall(r'@app\.route\([^\)]+\)', content)
for m in matches:
    print(m)
