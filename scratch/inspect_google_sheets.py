import sys
import urllib.request
import re
import pandas as pd
import io

sys.stdout.reconfigure(encoding='utf-8')

url = "https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/edit"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'

print("1. Fetching spreadsheet edit page...")
req = urllib.request.Request(url, headers={'User-Agent': user_agent})
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        html = r.read().decode('utf-8')
except Exception as e:
    print(f"Error fetching Google Sheet: {e}")
    sys.exit(1)

# Find GIDs and Names
pattern = r'\[\s*\d+\s*,\s*0\s*,\s*\\"?(\d+)\\"?\s*,\s*\[\s*\{\s*\\"?1\\"?\s*:\s*\[\s*\[\s*0\s*,\s*0\s*,\s*\\"?([^\\"\(\]]+)\\"?'
matches = re.findall(pattern, html)
print(f"Found {len(matches)} tabs:")
gid_map = {}
for gid, name in matches:
    name_clean = name.strip()
    gid_map[name_clean.lower()] = (gid, name_clean)
    print(f"  - {name_clean}: {gid}")

# Find aging GID
target_gid = None
target_name = None
for name_lower, (gid, orig_name) in gid_map.items():
    if any(x in name_lower for x in ["aging trên 5 ngày", "aging tren 5 ngay", "đơn giao aging trên 5 ngày", "don giao aging tren 5 ngay"]):
        target_gid = gid
        target_name = orig_name
        break

if not target_gid:
    print("Could not find aging tab in sheet mappings!")
    sys.exit(1)

print(f"\n2. Downloading aging tab '{target_name}' (GID: {target_gid})...")
csv_url = f"https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid={target_gid}"
req_csv = urllib.request.Request(csv_url, headers={'User-Agent': user_agent})
try:
    with urllib.request.urlopen(req_csv, timeout=30) as response:
        content = response.read()
    
    # Load into DataFrame and print headers
    df = pd.read_csv(io.BytesIO(content))
    print("\nCSV Columns:")
    print(df.columns.tolist())
    print("\nFirst row preview:")
    if len(df) > 0:
        print(df.iloc[0].to_dict())
    else:
        print("Empty sheet!")
except Exception as e:
    print(f"Error downloading or parsing CSV: {e}")
