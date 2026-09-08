import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv('sheet_truythu.csv', nrows=5000, low_memory=False)
print("Columns in sheet_truythu.csv:", df.columns.tolist())

# Check for date or week columns
date_cols = [c for c in df.columns if any(k in c.lower() for k in ['tuần', 'week', 'ngày', 'date', 'thời gian', 'kỳ'])]
print("Potential Date/Week columns:", date_cols)

for c in date_cols:
    print(f"\nUnique values in {c}:")
    print(df[c].value_counts().head(10))

# Let's inspect the entire file's unique values for these date columns
df_full = pd.read_csv('sheet_truythu.csv', usecols=date_cols, low_memory=False)
for c in date_cols:
    print(f"\nFULL FILE unique values in {c}:")
    print(df_full[c].value_counts().head(15))
