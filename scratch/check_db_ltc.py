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
        df_db = pd.read_sql("SELECT * FROM ops_ltc WHERE \"Time\" = '2026-06-10 - Thứ 4'", engine)
        print("Rows in DB:", len(df_db))
        print("Columns in DB:", list(df_db.columns))
        
        # Filter out Grand Total
        df_details = df_db[df_db['Cấp quản lý'] != 'Grand Total'].copy()
        
        # Parse numeric columns
        df_details['Volume_num'] = pd.to_numeric(df_details['Volume'], errors='coerce').fillna(0)
        df_details['Success_num'] = pd.to_numeric(df_details['Sản Lượng Lấy Thành Công'], errors='coerce').fillna(0)
        
        print("\n--- Database details for 2026-06-10 ---")
        print("Sum of Volume (as read/stored):", df_details['Volume'].dtype, "Sum:", df_details['Volume_num'].sum())
        print("Sum of Sản Lượng Lấy Thành Công (as read/stored):", df_details['Sản Lượng Lấy Thành Công'].dtype, "Sum:", df_details['Success_num'].sum())
        
        # Let's inspect rows where Volume is null or empty, or where Success > Volume
        print("\nRows in DB where Volume is null or not numeric:")
        null_vol = df_details[pd.to_numeric(df_details['Volume'], errors='coerce').isna()]
        print(null_vol[['Chi tiết', 'Ca', 'Volume', 'Sản Lượng Lấy Thành Công']])
        
        # Show some example rows of the database to see the format
        print("\nFirst 5 rows from DB details:")
        print(df_details[['Chi tiết', 'Ca', 'Volume', 'Sản Lượng Lấy Thành Công', 'Volume_num', 'Success_num']].head(5).to_string())
        
    except Exception as e:
        print("Error reading from database:", e)
else:
    print("Could not connect to database engine.")
