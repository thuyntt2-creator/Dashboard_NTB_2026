import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import sqlalchemy
import pandas as pd

engine = sqlalchemy.create_engine('postgresql://neondb_owner:npg_AyQ9gXpjI7Tt@ep-small-dream-azg9vt9g-pooler.c-3.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')

for tbl in ['ops_gtc', 'ops_ltc', 'odr_tts', 'ops_tts', 'buu_cuc_bat_on']:
    try:
        df = pd.read_sql(f'SELECT * FROM {tbl} LIMIT 5', engine)
        print(f"Table {tbl} columns:", [c for c in df.columns])
        time_col = next((c for c in df.columns if c.lower() in ['time', 'date', 'ngay']), None)
        if time_col:
            df_dates = pd.read_sql(f'SELECT DISTINCT "{time_col}" FROM {tbl}', engine)
            d_list = [str(x).split(' - ')[0] for x in df_dates[time_col].dropna().unique()]
            print(f"  --> {tbl} distinct dates (last 5):", sorted(d_list)[-5:])
    except Exception as e:
        print(f"Table {tbl} error: {e}")
