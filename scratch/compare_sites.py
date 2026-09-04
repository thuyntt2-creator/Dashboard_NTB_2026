import urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')

req1 = urllib.request.Request('https://dashboard-ntb-2026.vercel.app/', headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
with urllib.request.urlopen(req1) as resp:
    h1 = resp.read().decode('utf-8')
    headers1 = dict(resp.getheaders())

req2 = urllib.request.Request('https://namtrungbo.vercel.app/', headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
with urllib.request.urlopen(req2) as resp:
    h2 = resp.read().decode('utf-8')
    headers2 = dict(resp.getheaders())

print("H1 len:", len(h1), "H2 len:", len(h2))
print("x-vercel-id 1:", headers1.get('x-vercel-id'))
print("x-vercel-id 2:", headers2.get('x-vercel-id'))

# Compare titles
def get_title(h):
    s = h.find('<title>')
    e = h.find('</title>')
    return h[s+7:e] if s!=-1 and e!=-1 else 'N/A'

print("Title 1:", get_title(h1))
print("Title 2:", get_title(h2))

# Find differences in script tags or body
import re
scripts1 = re.findall(r'<script[^>]*src=[\'"]([^\'"]+)[\'"]', h1)
scripts2 = re.findall(r'<script[^>]*src=[\'"]([^\'"]+)[\'"]', h2)
print("Scripts 1:", scripts1)
print("Scripts 2:", scripts2)

# Check git commit in HTML if any
for h, name in [(h1, 'dashboard-ntb-2026'), (h2, 'namtrungbo')]:
    m = re.search(r'(commit|version|v\d+)[^<\n]*', h, re.IGNORECASE)
    if m:
        print(f"Version/commit hint in {name}:", m.group(0)[:60])
