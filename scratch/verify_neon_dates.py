import os
import sqlalchemy
import pandas as pd
from dotenv import load_dotenv

load_dotenv(override=True)

db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

engine = sqlalchemy.create_engine(db_url)
for table in ['ops_gtc', 'ops_ltc', 'odr_tts']:
    try:
        with engine.connect() as conn:
            query = f'SELECT "Time", count(*) as total_rows FROM {table} GROUP BY "Time" ORDER BY "Time" DESC LIMIT 5'
            df = pd.read_sql(query, conn)
            print(f"=== Table {table} ===")
            print(df.to_string(index=False))
            print()
    except Exception as e:
        print(f"Table {table} error: {e}")
