import pandas as pd
import io
import urllib.request
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ss_id = '1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk'

sheets = [
    ('Data', '0'),
    ('raw', '910119805'),
    ('gtc', '1634452132'),
    ('rawGTCTTS', '1006637898'),
    ('GTC ca1 TTS', '1851125447')
]

for name, gid in sheets:
    try:
        url = f"https://docs.google.com/spreadsheets/d/{ss_id}/export?format=csv&gid={gid}"
        df = pd.read_csv(url)
        dates = sorted(list(df['Time'].dropna().unique()))
        cats = df['Loại Hàng'].unique() if 'Loại Hàng' in df.columns else 'No Loại Hàng'
        print(f"Sheet '{name}' (GID {gid}):")
        print(f"  Rows: {len(df)}")
        print(f"  Min Date: {dates[0] if dates else 'None'} | Max Date: {dates[-1] if dates else 'None'}")
        print(f"  Categories: {cats}")
    except Exception as e:
        print(f"Sheet '{name}' Error: {e}")
