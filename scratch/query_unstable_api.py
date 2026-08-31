import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://dashboard-ntb-2026.vercel.app/api/unstable-po"
out_path = "scratch/unstable_api_res.json"

try:
    print(f"Fetching {url}...")
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    parsed = json.loads(data)
    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=4, ensure_ascii=False)
        
    print("API Query successful!")
    print(f"Total warnings returned: {len(parsed.get('warnings', []))}")
    for i, w in enumerate(parsed.get('warnings', [])):
        print(f" {i+1}: {w.get('kho_giao_name')} - AM: {w.get('AM')} - Tỉnh: {w.get('tinh_giao')} - Tình hình: {w.get('tinh_hinh')}")
except Exception as e:
    print("Error querying API:", e)
