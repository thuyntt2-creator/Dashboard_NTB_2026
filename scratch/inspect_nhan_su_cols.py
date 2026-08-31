import os
import psycopg2
import sys
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
db_url = os.environ.get("DATABASE_URL")

conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("SELECT * FROM ops_nhan_su LIMIT 2;")
colnames = [desc[0] for desc in cur.description]
print("Columns of ops_nhan_su:", repr(colnames))

row = cur.fetchone()
print("First row of ops_nhan_su:", repr(row))

cur.close()
conn.close()
