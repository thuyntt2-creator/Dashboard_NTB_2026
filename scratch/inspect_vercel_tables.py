import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_url = os.environ.get("DATABASE_URL")
print("Connecting to:", db_url)

conn = psycopg2.connect(db_url)
cur = conn.cursor()

# Get all tables
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
tables = cur.fetchall()
print("Tables in database:")
for t in tables:
    table_name = t[0]
    cur.execute(f"SELECT COUNT(*) FROM {table_name};")
    count = cur.fetchone()[0]
    print(f"  - {table_name}: {count} rows")

cur.close()
conn.close()
