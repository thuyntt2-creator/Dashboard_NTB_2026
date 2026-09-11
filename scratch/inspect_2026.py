import urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request('https://namtrungbo2026.vercel.app/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    print('Length:', len(html))
    for line in html.split('\n'):
        if '<title>' in line:
            print('Title:', line.strip())
        if 'nav-tab-kinh-doanh' in line:
            print('Kinh doanh line:', line.strip())
        if 'nav-tab-transport-cost' in line:
            print('Transport line:', line.strip())
        if 'sidebar-hover-sensor' in line:
            print('Sensor found!')
