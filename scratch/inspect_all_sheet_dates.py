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
    print("=== INSPECTING ALL SHEETS FOR DATES & LOẠI HÀNG ===")
    for gid, name in sheet_names:
        try:
            csv_url = f"https://docs.google.com/spreadsheets/d/{ss_id}/export?format=csv&gid={gid}"
            df = pd.read_csv(csv_url)
            loai_col = [c for c in df.columns if 'loại' in c.lower() or 'ca' in c.lower()]
            time_col = [c for c in df.columns if 'time' in c.lower() or 'ngày' in c.lower() or 'thời gian' in c.lower()]
            
            l_val = df[loai_col[0]].unique() if loai_col else 'No loai col'
            t_val = sorted(list(df[time_col[0]].dropna().unique())) if time_col else 'No time col'
            max_t = t_val[-1] if isinstance(t_val, list) and t_val else 'None'
            
            print(f"Sheet '{name}' (GID {gid}) -> Rows: {len(df)} | Max Date: {max_t} | Categories: {l_val}")
        except Exception as ex:
            print(f"Sheet '{name}' (GID {gid}) -> Error: {ex}")
except Exception as e:
    print(f"Error fetching HTML: {e}")
