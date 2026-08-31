import urllib.request
import re
import sys
import io
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ss_id = '1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk'
url_html = f'https://docs.google.com/spreadsheets/d/{ss_id}/edit'

req = urllib.request.Request(url_html, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
    
    # Pattern to find sheet names
    sheet_names = re.findall(r'\[\s*\d+\s*,\s*0\s*,\s*\\"?(\d+)\\"?\s*,\s*\[\s*\{\s*\\"?1\\"?\s*:\s*\[\s*\[\s*0\s*,\s*0\s*,\s*\\"?([^\\"\(\]]+)\\"?', html)
    print("Found sheets:")
    for gid, name in sheet_names:
        print(f"  GID: {gid} | Name: {name}")

        # Let's inspect each sheet
        try:
            csv_url = f"https://docs.google.com/spreadsheets/d/{ss_id}/export?format=csv&gid={gid}"
            df = pd.read_csv(csv_url, nrows=5)
            print(f"    Columns ({len(df.columns)}): {list(df.columns)[:5]}...")
        except Exception as ex:
            print(f"    Error reading CSV: {ex}")
except Exception as e:
    print(f"Error fetching HTML: {e}")
