import openpyxl
import json
import os
import sys
import glob
import re

sys.stdout.reconfigure(encoding='utf-8')

def find_latest_excel():
    cwd = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(cwd) if os.path.basename(cwd) == 'scratch' else cwd
    
    candidates = []
    # 1. Root dir
    candidates.extend(glob.glob(os.path.join(root_dir, 'BaoCao_Tuan_NTB_W*.xlsx')))
    # 2. Downloads AM projects
    candidates.extend(glob.glob(r'C:\Users\lap4all\Downloads\BaoCao_AM_Project_*\BaoCao_AM_Project\output\BaoCao_Tuan_NTB_W*.xlsx'))
    # 3. Downloads root
    candidates.extend(glob.glob(r'C:\Users\lap4all\Downloads\BaoCao_Tuan_NTB_W*.xlsx'))

    def get_week_num(path):
        m = re.search(r'W(\d+)', os.path.basename(path), re.IGNORECASE)
        return int(m.group(1)) if m else 0

    valid_candidates = [p for p in candidates if os.path.exists(p) and get_week_num(p) > 0]
    if not valid_candidates:
        fallback = os.path.join(root_dir, 'BaoCao_Tuan_NTB_W36_2026.xlsx')
        if os.path.exists(fallback):
            return fallback
        raise FileNotFoundError("Không tìm thấy file Excel báo cáo tuần nào!")

    # Sort by week number descending, then by mtime descending
    valid_candidates.sort(key=lambda p: (get_week_num(p), os.path.getmtime(p)), reverse=True)
    return valid_candidates[0]

excel_path = find_latest_excel()
print(f"Reading data from: {excel_path}")
wb = openpyxl.load_workbook(excel_path, data_only=True)

# Detect weeks dynamically from sheet 01_San luong
ws_sl = wb['01_San luong']
weeks = []
for c in range(2, 6):
    val = ws_sl.cell(11, c).value
    if val:
        weeks.append(str(val).strip())
if not weeks or len(weeks) < 4:
    weeks = ['W34', 'W35', 'W36', 'W37']

latest_week = weeks[-1]
prev_week = weeks[-2]

date_range_map = {
    'W35': '24/08 - 30/08/2026',
    'W36': '31/08 - 06/09/2026',
    'W37': '07/09 - 13/09/2026',
    'W38': '14/09 - 20/09/2026',
    'W39': '21/09 - 27/09/2026',
}
date_range = date_range_map.get(latest_week, '07/09 - 13/09/2026')

print(f"Detected: {latest_week}, Weeks: {weeks}, Date Range: {date_range}")
