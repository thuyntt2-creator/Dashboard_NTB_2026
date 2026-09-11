import urllib.request

req = urllib.request.Request('https://ntb-ops-dashboard-8extsce7p-trungtran220792-hubs-projects.vercel.app', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    print('Length:', len(html))
    print('Has sidebar-hover-sensor:', 'sidebar-hover-sensor' in html)
    print('Has sidebar-toggle-btn:', 'sidebar-toggle-btn' in html)
    print('First 200 chars:', html[:200])
