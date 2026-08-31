import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import os
import sqlalchemy
import pandas as pd
from dotenv import load_dotenv

load_dotenv(override=True)

db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

engine = sqlalchemy.create_engine(db_url)
df = pd.read_sql("SELECT * FROM ops_productivity_realtime", engine)
print(f"Postgres ops_productivity_realtime row count: {len(df)}")
print(f"Columns in DB: {df.columns.tolist()}")
print("\nFirst 10 rows:")
print(df.head(10))
