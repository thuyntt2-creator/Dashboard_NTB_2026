import urllib.request, re, unicodedata, sys
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/edit'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        html = r.read().decode('utf-8')

    pattern = r'\[\s*\d+\s*,\s*0\s*,\s*\\"?(\d+)\\"?\s*,\s*\[\s*\{\s*\\"?1\\"?\s*:\s*\[\s*\[\s*0\s*,\s*0\s*,\s*\\"?([^\\"\(\]]+)\\"?'
    matches = re.findall(pattern, html)
    print('Found tabs:')
    for gid, name in matches:
        print(f'  GID {gid}: {name}')
except Exception as e:
    print(f'Error: {e}')
