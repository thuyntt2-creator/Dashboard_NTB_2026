import pandas as pd
import sqlalchemy
import os
import sys
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv(override=True)

df_local = pd.read_csv('vols_tao_don.csv', low_memory=False)
col_d = next(c for c in df_local.columns if 'date' in c.lower())
print('Local vols_tao_don.csv dates:', sorted(df_local[col_d].dropna().astype(str).unique())[-5:])

db_url = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://', 1)
engine = sqlalchemy.create_engine(db_url)
with engine.connect() as conn:
    df_db = pd.read_sql('SELECT * FROM vols_tao_don LIMIT 5', conn)
    print('DB cols:', df_db.columns.tolist())
    col_db_d = next(c for c in df_db.columns if 'date' in c.lower())
    df_dates = pd.read_sql(f'SELECT DISTINCT "{col_db_d}" FROM vols_tao_don', conn)
    print('Neon DB vols_tao_don dates:', sorted(df_dates[col_db_d].dropna().astype(str).unique())[-5:])
