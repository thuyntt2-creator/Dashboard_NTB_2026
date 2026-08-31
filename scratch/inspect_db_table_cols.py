import sys
from dotenv import load_dotenv
import os
import sqlalchemy
import pandas as pd

load_dotenv(override=True)
db_url = os.getenv("DATABASE_URL")
if not db_url:
    print("No DATABASE_URL found in .env!")
    sys.exit(1)

# Ensure correct driver for PostgreSQL in SQLAlchemy
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

print(f"Connecting to database: {db_url.split('@')[-1]}")
try:
    engine = sqlalchemy.create_engine(db_url)
    # Query one row from aging_raw
    df = pd.read_sql("SELECT * FROM aging_raw LIMIT 1", engine)
    print("\nColumns in aging_raw table in DB:")
    print(df.columns.tolist())
    print("\nFirst row:")
    print(df.to_dict(orient='records'))
except Exception as e:
    print(f"Error querying database: {e}")
