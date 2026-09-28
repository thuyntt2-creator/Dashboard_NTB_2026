import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

tabs = re.findall(r'id=["\']tab-([^"\']+)["\']', text)
print("Tabs found:", tabs)

m = re.search(r'(<div[^>]*id=["\']tab-overview["\'][^>]*>.*?)(?=<div[^>]*id=["\']tab-|$)', text, re.S)
if m:
    print("Overview HTML excerpt (first 3000 chars):")
    print(m.group(1)[:3000])
