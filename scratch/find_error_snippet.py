import sys, re

sys.stdout.reconfigure(encoding='utf-8')
with open('scratch/temp_vercel.html', 'w', encoding='utf-8') as out:
    import urllib.request
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://vercel.com/imthir/namtrungbo/7VnAwKWm5wb2PPQERMJwqhPjTdtW'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        out.write(html)

print("Downloaded HTML. Searching...")
matches = re.findall(r'(\b[A-Z0-9_]{4,30}_ERROR\b|\bBUILD_[A-Z0-9_]+\b|\bFUNCTION_[A-Z0-9_]+\b)', html)
print("Error constants:", set(matches))

# Look for error texts
snippets = []
for m in re.finditer(r'(?:error|failed|failure|exceeded|quota)', html, re.I):
    start = max(0, m.start() - 60)
    end = min(len(html), m.end() + 100)
    snippets.append(html[start:end].replace('\n', ' '))

print(f"Total snippets: {len(snippets)}")
for s in snippets[:10]:
    print("SNIP:", s)

