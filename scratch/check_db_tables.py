import os
import sys
import sqlalchemy
import pandas as pd
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv(override=True)

db_url = os.getenv('DATABASE_URL')
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)

engine = sqlalchemy.create_engine(db_url, connect_args={'connect_timeout': 15})
with engine.connect() as conn:
    res = pd.read_sql("SELECT table_name FROM information_schema.tables WHERE table_schema='public'", conn)
    print("Tables in Neon DB:", res['table_name'].tolist())
    
    for t in ['raw_tren10kg', 'ops_heavy_10kg', 'ops_tao_don_10kg']:
        if t in res['table_name'].tolist():
            count = pd.read_sql(f"SELECT count(*) FROM {t}", conn).iloc[0,0]
            df = pd.read_sql(f"SELECT * FROM {t} LIMIT 5", conn)
            print(f"\nTable '{t}': {count} rows, cols={df.columns.tolist()[:8]}")
            for c in df.columns:
                if any(k in str(c).lower() for k in ['date', 'time', 'ngay']):
                    try:
                        dates_df = pd.read_sql(f'SELECT DISTINCT "{c}" FROM {t} ORDER BY "{c}" DESC LIMIT 5', conn)
                        print(f"  Latest in column '{c}': {dates_df[c].tolist()}")
                    except Exception as e:
                        print(f"  Error querying date col {c}: {e}")
        else:
            print(f"\nTable '{t}': NOT FOUND IN NEON DB!")
