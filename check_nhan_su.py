import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
df = pd.read_csv("ops_nhan_su.csv")
print("Columns in ops_nhan_su.csv:", df.columns)
print(df.head(10))
