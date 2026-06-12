import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv(override=True)
import pandas as pd
from app import get_db_engine

engine = get_db_engine()
if engine:
    try:
        # Check if table exists
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print("Tables in DB:", tables)
        
        if 'off_tuyen_spe' in tables:
            df_db = pd.read_sql("SELECT * FROM off_tuyen_spe", engine)
            print("Rows in DB table off_tuyen_spe:", len(df_db))
            if len(df_db) > 0:
                print("Columns:", list(df_db.columns))
                print("First 3 rows:\n", df_db.head(3).to_string())
        else:
            print("Table off_tuyen_spe does NOT exist in DB.")
    except Exception as e:
        print("Error reading from database:", e)
else:
    print("Could not connect to database engine.")
