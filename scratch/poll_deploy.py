import urllib.request, time

for i in range(10):
    time.sleep(10)
    req = urllib.request.Request('https://dashboard-ntb-2026.vercel.app/', headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache, no-store'})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            has_new = 'tab-heavy-10kg' in html
            print(f'Attempt {i+1}: length={len(html)}, updated={has_new}')
            if has_new:
                print('SUCCESS! Dashboard-ntb-2026 is fully updated!')
                break
    except Exception as e:
        print(f'Attempt {i+1} error:', e)
