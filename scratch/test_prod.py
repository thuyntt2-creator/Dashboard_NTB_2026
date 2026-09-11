import urllib.request

for url in [
    'https://ntb-ops-dashboard-trungtran220792-hubs-projects.vercel.app',
    'https://ntb-ops-dashboard-git-main-trungtran220792-hubs-projects.vercel.app'
]:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            print(url)
            print('  Length:', len(html))
            print('  Has sensor:', 'sidebar-hover-sensor' in html)
            print('  Has login:', 'login-container' in html)
            print('  Has title:', 'GIỚI THIỆU VÙNG NAM TRUNG BỘ' in html)
    except Exception as e:
        print(url, e)
