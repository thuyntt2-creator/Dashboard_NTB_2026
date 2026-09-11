import urllib.request

for url in [
    'https://ntb-ops-dashboard.vercel.app',
    'https://ntb-ops-dashboard-8extsce7p-trungtran220792-hubs-projects.vercel.app'
]:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            has_sensor = 'sidebar-hover-sensor' in content
            has_3d_a = 'Khách Hàng Nhóm A' in content
            print(f"{url} -> status {resp.status} | has_sensor: {has_sensor} | has_3d_a: {has_3d_a}")
    except Exception as e:
        print(f"{url} -> Error: {e}")
