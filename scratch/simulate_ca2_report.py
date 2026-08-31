import pandas as pd
import io
import urllib.request
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ss_id = '1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk'

# Load sheets Data, gtc, raw
sheets = [('raw', '910119805'), ('gtc', '1634452132'), ('Data', '0')]
all_rows = []

for s_name, gid in sheets:
    try:
        url = f"https://docs.google.com/spreadsheets/d/{ss_id}/export?format=csv&gid={gid}"
        df = pd.read_csv(url)
        all_rows.append(df)
        print(f"Loaded {s_name}: {len(df)} rows")
    except Exception as e:
        print(f"Error {s_name}: {e}")

df_all = pd.concat(all_rows, ignore_index=True)

# Filter for Ca 2
ca2_df = df_all[df_all['Loại Hàng'].astype(str).str.contains('Ca 2|ca 2', na=False)].copy()

print("\n=== CA 2 DATES & TOTAL VOLUME BY DATE ===")
by_date = ca2_df.groupby('Time')['Volume'].sum().reset_index()
print(by_date.sort_values(by='Time', ascending=False).head(10))

print("\n=== CA 2 VOLUME FOR BẮC BÌNH & HÀM THUẬN NAM BY DATE ===")
bb = ca2_df[ca2_df['Chi tiết'].astype(str).str.contains('Bắc Bình|Hàm Thuận Nam', na=False)]
print(bb.groupby(['Chi tiết', 'Time'])['Volume'].sum().unstack().fillna(0).T.tail(10))
