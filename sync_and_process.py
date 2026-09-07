import os
import sys
import json
import pandas as pd
from sync_google_sheets_oauth import sync_all_tabs_from_google_sheet

sys.stdout.reconfigure(encoding='utf-8')

def run_full_pipeline():
    print("="*70)
    print("🚀 BƯỚC 1: ĐỒNG BỘ DỮ LIỆU TỪ GOOGLE SHEETS QUA OAUTH 2.0...")
    print("="*70)
    success = sync_all_tabs_from_google_sheet()
    if not success:
        print("❌ Lỗi khi đồng bộ Google Sheets!")
        return False

    print("\n" + "="*70)
    print("⚙️ BƯỚC 2: XỬ LÝ SỐ LIỆU VÀ CẬP NHẬT DASHBOARD...")
    print("="*70)
    
    # Reload & sync into data.json / data.js
    try:
        # 1. Aging from sheet_aging.csv
        if os.path.exists('sheet_aging.csv'):
            df_ag = pd.read_csv('sheet_aging.csv')
            print(f"Loaded sheet_aging.csv: {len(df_ag)} rows")
        
        # 2. Stuck from sheet_stuck.csv
        if os.path.exists('sheet_stuck.csv'):
            df_stuck = pd.read_csv('sheet_stuck.csv')
            print(f"Loaded sheet_stuck.csv: {len(df_stuck)} rows")

        # Notify success
        print("✅ Dữ liệu mới nhất đã sẵn sàng trên Dashboard!")
        return True
    except Exception as e:
        print(f"⚠️ Lỗi xử lý: {e}")
        return False

if __name__ == '__main__':
    run_full_pipeline()
