import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import pandas as pd
import os

files = ['ops_gtc.csv', 'ops_ltc.csv', 'ops_tts.csv', 'co_cau_ntb.csv', 'buu_cuc_bat_on.csv', 'off_tuyen_spe.csv']

for fn in files:
    if not os.path.exists(fn):
        print(f"File {fn} does not exist.")
        continue
    try:
        # read_csv with encoding utf-8 or utf-8-sig
        df_full = pd.read_csv(fn, encoding='utf-8')
        print(f"\n=== {fn} ===")
        print(f"Columns: {list(df_full.columns)}")
        print(f"Shape: {df_full.shape}")
        
        for col in df_full.columns:
            match_count = df_full[col].astype(str).str.contains('NTB', case=False, na=False).sum()
            if match_count > 0:
                print(f"  Column '{col}' has {match_count} matches for 'NTB'")
            
            unique_vals = df_full[col].dropna().unique()
            if len(unique_vals) < 15:
                # convert to string to print safely
                print(f"  Column '{col}' unique values: {[str(x) for x in unique_vals]}")
    except Exception as e:
        print(f"Error reading {fn}: {e}")
