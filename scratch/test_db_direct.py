import os
import sys
import sqlalchemy
from dotenv import load_dotenv

load_dotenv(override=True)

db_url = os.getenv("DATABASE_URL")
print(f"Testing connection to DATABASE_URL: {db_url.split('@')[-1] if db_url else 'None'}", flush=True)

if not db_url:
    print("No DATABASE_URL found in .env!", flush=True)
    sys.exit(1)

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

try:
    engine = sqlalchemy.create_engine(db_url, connect_args={'connect_timeout': 10})
    with engine.connect() as conn:
        res = conn.execute(sqlalchemy.text("SELECT version();"))
        row = res.fetchone()
        print("DATABASE CONNECTION SUCCESSFUL!", flush=True)
        print("PostgreSQL Version:", row[0] if row else "Unknown", flush=True)
except Exception as e:
    print(f"DATABASE CONNECTION FAILED: {e}", flush=True)
