import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')
df = pd.read_csv('scratch/truythu_raw.csv')

print("Sample 'Số tiền ban đầu' values:")
print(df['Số tiền ban đầu'].dropna().head(30).tolist())

print("\nSample values with dot or comma:")
sample_dots = df[df['Số tiền ban đầu'].astype(str).str.contains(r'\.|\,')]['Số tiền ban đầu'].head(20).tolist()
print(sample_dots)

# Let's see some examples across different columns
for col in ['Số tiền ban đầu', 'Điều chỉnh (+|-)', 'Đã truy thu', 'Cần truy thu thêm', 'Cần hoàn']:
    vals = df[col].dropna().astype(str).unique()[:10]
    print(f"{col} sample unique: {vals}")
