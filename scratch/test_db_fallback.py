import sys
import os
sys.path.insert(0, os.getcwd())
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv(override=True)

# Temporarily rename local CSV files so the app is forced to load from DB
csv_files = [
    'ops_gtc.csv', 'ops_ltc.csv', 'ops_co_cau.csv', 'ops_tts.csv',
    'opr_opr.csv', 'opr_oe.csv', 'opr_raw.csv', 'aging_raw.csv',
    'treo_stuck.csv', 'buu_cuc_bat_on.csv', 'off_tuyen_spe.csv',
    'vols_tao_don.csv', 'co_cau_ntb.csv', 'ODR TTS.csv', 'ops_fd.csv',
    'ops_nhan_su.csv'
]

renamed = []
for f in csv_files:
    if os.path.exists(f):
        os.rename(f, f + ".tmp")
        renamed.append(f)

print(f"Renamed {len(renamed)} local files to force DB load.")

# Simulate Vercel environment
os.environ["VERCEL"] = "1"

try:
    from app import get_dataframes
    print("Loading dataframes from DB...")
    dfs = get_dataframes(force=True)
    print("Success! Dataframes loaded from DB.")
except Exception as e:
    import traceback
    print(f"Error occurred: {e}")
    traceback.print_exc()
finally:
    # Restore original files
    for f in renamed:
        if os.path.exists(f + ".tmp"):
            os.rename(f + ".tmp", f)
    print("Restored all local files.")
