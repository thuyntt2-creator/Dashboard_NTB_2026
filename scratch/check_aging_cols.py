import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv(override=True)
from sqlalchemy import create_engine

# Check local CSV columns
out = []
csv_path = "aging_raw.csv"
if os.path.exists(csv_path):
    try:
        df_csv = pd.read_csv(csv_path, nrows=5)
        out.append(f"Local CSV columns: {list(df_csv.columns)}")
    except Exception as e:
        out.append(f"Error reading local CSV: {e}")
else:
    out.append("Local CSV does not exist")

# Check DB columns
db_url = os.environ.get("DATABASE_URL")
if db_url:
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    try:
        engine = create_engine(db_url)
        df_db = pd.read_sql("SELECT * FROM aging_raw LIMIT 5", engine)
        out.append(f"DB table columns: {list(df_db.columns)}")
    except Exception as e:
        out.append(f"Error reading DB table: {e}")
else:
    out.append("No DATABASE_URL found")

with open("scratch/check_aging_cols_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("Results saved to scratch/check_aging_cols_res.txt")
