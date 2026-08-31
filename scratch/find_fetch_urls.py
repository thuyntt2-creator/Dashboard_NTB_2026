import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('templates/index.html', encoding='utf-8') as f:
    html = f.read()

matches = re.findall(r'/api/[a-zA-Z0-9_\-/]+', html)
print('API URLs found in index.html:')
for m in sorted(set(matches)):
    print(' ', m)
