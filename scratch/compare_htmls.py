import sys, glob, re
sys.stdout.reconfigure(encoding='utf-8')

f1 = glob.glob('scratch/db_s*.html')[0]
f2 = 'scratch/db_moi.html'

with open(f1, encoding='utf-8') as f:
    s1 = f.read()
with open(f2, encoding='utf-8') as f:
    s2 = f.read()

print('Len 1 (sếp):', len(s1))
print('Len 2 (mới):', len(s2))

tabs1 = re.findall(r'id=[\'"](tab-[^\'"]+)[\'"]', s1)
tabs2 = re.findall(r'id=[\'"](tab-[^\'"]+)[\'"]', s2)
print('Tabs in 1:', tabs1)
print('Tabs in 2:', tabs2)

# Check differences in tabs
diff_tabs = set(tabs2) - set(tabs1)
print('New tabs in 2:', diff_tabs)

# Check git commit in response header
import urllib.request
for u in ['https://dashboard-ntb-2026.vercel.app/', 'https://namtrungbo.vercel.app/']:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
    with urllib.request.urlopen(req) as resp:
        print(f'=== Headers for {u} ===')
        for k, v in resp.getheaders():
            if 'vercel' in k.lower() or 'cache' in k.lower() or 'age' in k.lower() or 'etag' in k.lower():
                print(f'  {k}: {v}')
