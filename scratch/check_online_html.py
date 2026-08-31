import urllib.request

url = "https://dashboard-ntb-2026.vercel.app/"
try:
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
    print("Length of HTML:", len(html))
    
    # Check for specific modifications
    checks = [
        "orientation: 'vertical'",
        "hideOverflowingLabels: false",
        "padding: {",
        "foreColor: '#ffffff'"
    ]
    for check in checks:
        present = check in html
        print(f"Presence of '{check}': {present}")
        if present:
            # Find snippet
            idx = html.find(check)
            start = max(0, idx - 100)
            end = min(len(html), idx + 200)
            print(f"Snippet:\n{html[start:end]}\n" + "-"*40)
            
except Exception as e:
    print("Error:", str(e))
