import json
import sys
import os
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SHEET_ID = "1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

def sync_all_tabs_from_google_sheet(sheet_id=SHEET_ID):
    print("="*70)
    print("🚀 BẮT ĐẦU ĐỒNG BỘ GOOGLE SHEET NTB QUA OAUTH 2.0")
    print(f"🔗 Sheet ID: {sheet_id}")
    print("="*70)

    if not os.path.exists('authorized_user.json'):
        print("❌ Không tìm thấy authorized_user.json!")
        return False

    try:
        creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
        service = build('sheets', 'v4', credentials=creds)

        # 1. Fetch metadata
        meta = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        sheet_title = meta.get('properties', {}).get('title', 'report')
        print(f"✅ Đã kết nối thành công đến File Sheet: '{sheet_title}'")

        sheets = meta.get('sheets', [])
        print(f"📊 Tổng số Tab (Sheets): {len(sheets)}")

        synced_count = 0
        for s in sheets:
            props = s.get('properties', {})
            title = props.get('title')
            sheet_id_num = props.get('sheetId')
            
            print(f"\n⬇️ Đang tải Tab: '{title}' (GID: {sheet_id_num})...")
            try:
                res = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=title).execute()
                rows = res.get('values', [])
                if len(rows) > 0:
                    max_cols = max(len(r) for r in rows)
                    padded_rows = [r + [''] * (max_cols - len(r)) for r in rows]
                    df = pd.DataFrame(padded_rows[1:], columns=padded_rows[0])
                    
                    # Clean filename
                    clean_name = title.strip().replace(' ', '_').replace('/', '_')
                    out_file = f"sheet_{clean_name}.csv"
                    df.to_csv(out_file, index=False, encoding='utf-8')
                    print(f"   💾 Đã lưu: {out_file} ({len(df)} dòng, {len(df.columns)} cột)")
                    synced_count += 1
            except Exception as tab_err:
                print(f"   ⚠️ Lỗi tải tab '{title}': {tab_err}")

        print("\n" + "="*70)
        print(f"🎉 ĐỒNG BỘ HOÀN TẤT! Đã lưu {synced_count}/{len(sheets)} tab dữ liệu mới nhất.")
        print("="*70)
        return True

    except Exception as e:
        print(f"❌ Lỗi xác thực hoặc kết nối: {e}")
        return False

if __name__ == '__main__':
    sync_all_tabs_from_google_sheet()
