import os
import sys
import pandas as pd
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv(override=True)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import load_df_from_db, load_vols_tao_don_df

print("Loading vols_tao_don from DB directly...")
df_db = load_df_from_db('vols_tao_don.csv')
if df_db is not None:
    print("Loaded shape from DB:", df_db.shape)
    print("Loaded columns:", df_db.columns.tolist())
    for c in df_db.columns:
        if 'date' in str(c).lower():
            u = sorted(df_db[c].dropna().astype(str).unique())
            print(f"Date values in DB ({len(u)}):", u[-5:])
else:
    print("Failed to load from DB!")
