import sys
import os
import psycopg2

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

db_url = "postgresql://neondb_owner:npg_X1CduhiUJ8bo@ep-raspy-dawn-adhrb0b2.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"

try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    # List tables
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    tables = [r[0] for r in cur.fetchall()]
    print("Tables in database:", tables)
    
    # Query latest date in ops_gtc if exists
    if 'ops_gtc' in tables:
        cur.execute('SELECT DISTINCT "Time" FROM ops_gtc;')
        gtc_times = [r[0] for r in cur.fetchall()]
        print("Unique dates in ops_gtc:", gtc_times)
    else:
        print("ops_gtc table not found!")
        
    cur.close()
    conn.close()
except Exception as e:
    print("Error querying database:", e)
