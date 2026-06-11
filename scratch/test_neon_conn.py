import os
import sys
import pandas as pd
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(override=True)

from app import get_db_engine, save_df_to_db, load_df_from_db

def test_neon():
    print("Testing connection to Neon PostgreSQL...")
    print("DATABASE_URL:", os.environ.get("DATABASE_URL"))
    
    engine = get_db_engine()
    if engine is None:
        print("FAIL: Database engine could not be initialized.")
        sys.exit(1)
        
    print("Engine initialized. Testing write...")
    df = pd.DataFrame([{"id": 1, "status": "Neon is working!"}])
    success = save_df_to_db(df, "test_neon_conn.csv")
    if not success:
        print("FAIL: Could not write to Neon database.")
        sys.exit(1)
        
    print("Write succeeded. Testing read...")
    loaded_df = load_df_from_db("test_neon_conn.csv")
    if loaded_df is None or loaded_df.empty:
        print("FAIL: Could not read back from Neon database.")
        sys.exit(1)
        
    print("Read succeeded! Content:")
    print(loaded_df)
    print("\nSUCCESS! Your Neon PostgreSQL database is fully compatible and working!")

if __name__ == "__main__":
    test_neon()
