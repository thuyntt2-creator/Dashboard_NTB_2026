import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

df_w38 = pd.read_csv(r'C:\Users\lap4all\Downloads\w38.csv', low_memory=False)
print("Columns in w38.csv:", df_w38.columns.tolist())
print(f"Total rows: {len(df_w38)}")

# Check if there are provinces or places
places = df_w38['Nơi vi phạm'].dropna().unique()
print(f"Unique places: {len(places)}")
print("Sample places:", places[:15])

# Compare with sheet_truythu.csv (W39)
df_w39 = pd.read_csv('sheet_truythu.csv', low_memory=False)
places_w39 = df_w39['Nơi vi phạm'].dropna().unique()
print(f"\nUnique places in W39: {len(places_w39)}")

# Check how many places overlap
overlap = set(places).intersection(set(places_w39))
print(f"Places overlap: {len(overlap)}")
