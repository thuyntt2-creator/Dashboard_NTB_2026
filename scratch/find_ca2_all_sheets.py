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
    
    sheet_names = re.findall(r'\[\s*\d+\s*,\s*0\s*,\s*\\"?(\d+)\\"?\s*,\s*\[\s*\{\s*\\"?1\\"?\s*:\s*\[\s*\[\s*0\s*,\s*0\s*,\s*\\"?([^\\"\(\]]+)\\"?', html)
    print("=== SEARCHING FOR CA 2 ACROSS ALL SHEETS ===")
    for gid, name in sheet_names:
        try:
            csv_url = f"https://docs.google.com/spreadsheets/d/{ss_id}/export?format=csv&gid={gid}"
            df = pd.read_csv(csv_url)
            # Find any column that contains 'loại' or 'ca'
            ca_cols = [c for c in df.columns if any(k in c.lower() for k in ['loại', 'ca', 'hàng'])]
            for col in ca_cols:
                vals = df[col].astype(str).unique()
                ca2_matches = [v for v in vals if 'ca 2' in v.lower() or 'ca2' in v.lower()]
                if ca2_matches:
                    print(f"\nSheet '{name}' (GID {gid}) -> HAS CA 2 in column '{col}'! Matches: {ca2_matches}")
                    print(f"  Total Rows: {len(df)}, Cols: {list(df.columns)}")
                    sub = df[df[col].astype(str).str.lower().str.contains('ca 2|ca2', na=False)]
                    print(f"  Ca 2 rows count: {len(sub)}")
                    print(f"  Ca 2 Max Date: {sub['Time'].max() if 'Time' in sub.columns else 'No Time col'}")
                    print(f"  Ca 2 Volume describe: {sub['Volume'].describe().to_dict() if 'Volume' in sub.columns else 'No Vol'}")
        except Exception as ex:
            pass
except Exception as e:
    print(f"Error fetching HTML: {e}")
