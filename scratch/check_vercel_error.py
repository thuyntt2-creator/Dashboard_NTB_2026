import urllib.request, re, sys, json

sys.stdout.reconfigure(encoding='utf-8')
headers = {'User-Agent': 'Mozilla/5.0'}
url = 'https://vercel.com/imthir/namtrungbo/7VnAwKWm5wb2PPQERMJwqhPjTdtW'
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        
    print("Page length:", len(html))
    
    # Look for NEXT_DATA or build state
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
    if m:
        data = json.loads(m.group(1))
        page_props = data.get('props', {}).get('pageProps', {})
        dpl = page_props.get('deployment', {})
        print("Deployment state:", dpl.get('state'))
        print("Deployment errorCode:", dpl.get('errorCode'))
        print("Deployment errorMessage:", dpl.get('errorMessage'))
        print("Deployment readyState:", dpl.get('readyState'))
        print("Deployment aliasError:", dpl.get('aliasError'))
        print("Deployment inspector:", dpl.get('inspectorUrl'))
    else:
        # regex search
        for pattern in [r'"errorMessage":"([^"]+)"', r'"errorCode":"([^"]+)"', r'"readyState":"([^"]+)"', r'"state":"([^"]+)"']:
            for match in re.findall(pattern, html):
                print("Found:", pattern, "->", match)
except Exception as e:
    print("Error:", e)

