import sys, pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv("scratch/raw_tren10kg.csv", header=None)

print("Row 0 (Header row):")
for i, col_val in enumerate(df.iloc[0]):
    print(f"Col {i} ({chr(65+i) if i < 26 else 'A'+chr(65+i-26)}): {col_val}")

print("\n--- SECTION 1 (A:U) (Cols 0..20) ---")
print("Headers:", df.iloc[0, 0:21].tolist())
print("Sample Row 1:", df.iloc[1, 0:21].tolist())

print("\n--- SECTION 2 (W:AD) (Cols 22..29) ---")
print("Headers:", df.iloc[0, 22:30].tolist())
print("Sample Row 1:", df.iloc[1, 22:30].tolist())
