import pandas as pd
import io
import urllib.request
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ss_id = '1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk'

sheets = [
    ('raw', '910119805'),
    ('gtc', '1634452132'),
    ('trên 10kg', '1044003167')
]

for name, gid in sheets:
    try:
        url = f"https://docs.google.com/spreadsheets/d/{ss_id}/export?format=csv&gid={gid}"
        df = pd.read_csv(url)
        if 'Loại Hàng' in df.columns:
            ca2 = df[df['Loại Hàng'].astype(str).str.contains('Ca 2|ca 2|Ca2', na=False)]
            print(f"=== Sheet '{name}' ===")
            print(f"  Ca 2 row count: {len(ca2)}")
            if len(ca2) > 0:
                print(f"  Ca 2 dates: {sorted(list(ca2['Time'].dropna().unique()))}")
                print(f"  Ca 2 Volume sum: {ca2['Volume'].sum() if 'Volume' in ca2.columns else 'No Vol'}")
                print(f"  Sample Ca 2 rows:\n{ca2[['Chi tiết', 'Loại Hàng', 'Time', 'Volume', '% Gán', '% GTC']].head(5)}")
    except Exception as e:
        print(f"Error in {name}: {e}")
