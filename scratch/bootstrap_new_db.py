import os
import sys
import sqlalchemy
import pandas as pd
from dotenv import load_dotenv

load_dotenv(override=True)

db_url = os.getenv("DATABASE_URL")
if len(sys.argv) > 1 and sys.argv[1].strip():
    db_url = sys.argv[1].strip()

if not db_url:
    print("No DATABASE_URL provided!", flush=True)
    sys.exit(1)

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

print(f"Connecting to DB: {db_url.split('@')[-1]}", flush=True)

try:
    engine = sqlalchemy.create_engine(db_url, connect_args={'connect_timeout': 15})
    
    csv_files = [
        "ops_gtc.csv",
        "ops_ltc.csv",
        "ops_co_cau.csv",
        "co_cau_ntb.csv",
        "ops_tts.csv",
        "opr_opr.csv",
        "opr_oe.csv",
        "opr_raw.csv",
        "aging_raw.csv",
        "treo_stuck.csv",
        "buu_cuc_bat_on.csv",
        "off_tuyen_spe.csv",
        "vols_tao_don.csv",
        "ODR TTS.csv",
        "ops_fd.csv",
        "ops_productivity_realtime.csv",
        "ops_nhan_su.csv",
        "ops_heavy_10kg.csv",
        "ops_tao_don_10kg.csv",
        "raw_tren10kg.csv"
    ]
    
    imported_count = 0
    for filename in csv_files:
        if os.path.exists(filename) and os.path.getsize(filename) > 10:
            table_name = filename.lower().replace(".csv", "").replace(" ", "_")
            print(f"Importing {filename} -> table '{table_name}'...", flush=True)
            try:
                try:
                    df = pd.read_csv(filename, encoding='utf-8')
                except Exception:
                    df = pd.read_csv(filename, encoding='latin-1')
                
                df.to_sql(table_name, engine, if_exists="replace", index=False, chunksize=1000)
                imported_count += 1
                print(f"  --> Successfully imported {len(df)} rows into '{table_name}'", flush=True)
            except Exception as e:
                print(f"  --> Error importing {filename}: {e}", flush=True)

    print(f"\nBOOTSTRAP COMPLETE! Imported {imported_count} tables into new Neon DB.", flush=True)
except Exception as e:
    print(f"\nDB Connection Error: {e}", flush=True)
