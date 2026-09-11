import urllib.request

for site in ['https://dashboard-ntb-2026.vercel.app/', 'https://namtrungbo.vercel.app/', 'https://namtrungbo2026.vercel.app/']:
    try:
        req = urllib.request.Request(site, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            has_sensor = 'sidebar-hover-sensor' in content
            has_3d_a = 'Khách Hàng Nhóm A' in content
            print(f"{site} -> status: {resp.status}, has_sensor: {has_sensor}, has_3d_a: {has_3d_a}")
    except Exception as e:
        print(f"{site} -> error: {e}")
