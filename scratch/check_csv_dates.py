import pandas as pd
import os

csv_files = [
    'aging_raw.csv',
    'ops_gtc.csv',
    'ops_ltc.csv',
    'ops_tts.csv',
    'opr_raw.csv',
    'treo_stuck.csv',
    'buu_cuc_bat_on.csv',
    'vols_tao_don.csv'
]

print("--- DATE INSPECTION FOR LOCAL CSV FILES ---")
for f in csv_files:
    if os.path.exists(f):
        try:
            # read first few rows or load and print date columns
            df = pd.read_csv(f, nrows=5000)
            date_cols = [c for c in df.columns if 'ngày' in c.lower() or 'date' in c.lower() or 'time' in c.lower() or 'thời gian' in c.lower() or 'cập nhật' in c.lower()]
            if not date_cols:
                # search for any date-looking column
                date_cols = [c for c in df.columns if df[c].astype(str).str.contains(r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}').any()]
            
            if date_cols:
                print(f"\nFile: {f}")
                for col in date_cols[:2]:
                    # convert to datetime if possible
                    df[col] = df[col].astype(str).str.strip()
                    unique_vals = sorted(df[col].unique())
                    print(f"  Col '{col}' unique values (up to 5): {unique_vals[-5:]}")
            else:
                print(f"\nFile: {f} (No date columns found, columns: {list(df.columns)})")
        except Exception as e:
            print(f"\nFile: {f} error: {e}")
    else:
        print(f"\nFile: {f} does not exist")
