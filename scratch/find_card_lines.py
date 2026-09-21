import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'GIAO ĐÚNG HẸN' in line or '93.9' in line or 'odr' in line.lower():
        if any(w in line for w in ['Full Hàng', '93.9', 'GIAO ĐÚNG HẸN', 'card', 'stat-']):
            print(f'index.html:{i+1}: {line.strip()[:140]}')

print('--- app.js ---')
with open('app.js', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if '93.9' in line or ('ODR' in line and ('card' in line or 'stat' in line or 'html' in line or 'Full' in line)):
        print(f'app.js:{i+1}: {line.strip()[:140]}')
