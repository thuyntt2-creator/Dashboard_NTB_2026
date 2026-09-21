import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('data.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# remove window.DASHBOARD_DATA = 
prefix = "window.DASHBOARD_DATA = "
if text.startswith(prefix):
    json_text = text[len(prefix):].rstrip(';\n ')
    try:
        data = json.loads(json_text)
        print("Keys in DASHBOARD_DATA:", len(data.keys()))
        for i, k in enumerate(data.keys()):
            print(f"  {i+1}: {k}")
    except Exception as e:
        print("JSON parse error:", e)
else:
    print("Does not start with prefix")
