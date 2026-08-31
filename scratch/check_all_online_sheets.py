import urllib.request, io, sys, re
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')

gids = {
    'ops_gtc': '0',
    'ops_ltc': '1365110988',
    'ops_tts': '620800887',
    'ops_co_cau': '1666412390'
}

for name, gid in gids.items():
    url = f'https://docs.google.com/spreadsheets/d/1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk/export?format=csv&gid={gid}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            df = pd.read_csv(io.BytesIO(resp.read()))
        print(f"=== Sheet: {name} (gid={gid}) ===")
        print("Columns:", list(df.columns))
        print("First row values:")
        for c in df.columns:
            val = df.iloc[0][c] if len(df) > 0 else 'N/A'
            print(f"  {c}: {val}")
        print()
    except Exception as e:
        print(f"Error loading {name}: {e}")
