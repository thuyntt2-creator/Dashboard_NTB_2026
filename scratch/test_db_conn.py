import os
from dotenv import load_dotenv
load_dotenv(override=True)
import time
from sqlalchemy import create_engine, text

db_url = os.environ.get("DATABASE_URL")
print("DATABASE_URL:", db_url[:40] if db_url else "None")

if not db_url:
    print("No DATABASE_URL found")
    exit()

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

try:
    print("Creating engine...")
    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    
    print("Testing connection (ping)...")
    start = time.time()
    with engine.connect() as conn:
        res = conn.execute(text("SELECT 1"))
        print(f"Connection OK! Ping time: {time.time() - start:.2f}s")
        
        # List tables
        print("Listing tables...")
        tables_res = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
        tables = [r[0] for r in tables_res]
        print("Tables in database:", tables)
        
        for table in tables:
            start_table = time.time()
            count_res = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = count_res.scalar()
            print(f"  Table: {table} -> Count: {count} (Time: {time.time() - start_table:.2f}s)")
            
except Exception as e:
    print("Database test failed with exception:", e)
