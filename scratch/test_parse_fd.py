import csv
import re
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def clean_pct(val):
    if not val:
        return 0.0
    val_str = str(val).strip()
    val_str = val_str.replace('%', '').replace(',', '.')
    # Remove arrows
    val_str = val_str.replace('▲', '').replace('▼', '').strip()
    try:
        return float(val_str)
    except:
        return 0.0

def clean_num(val):
    if not val:
        return 0.0
    val_str = str(val).strip().replace(',', '')
    try:
        return float(val_str)
    except:
        return 0.0

def parse_fd_csv(filepath):
    if not os.path.exists(filepath):
        return {"error": "File not found"}
        
    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        lines = list(reader)
        
    if len(lines) == 0:
        return {"error": "File is empty"}
        
    # 1. Parse Date from line 0
    date_str = ""
    line0 = lines[0]
    if len(line0) > 1 and "N =" in line0[1]:
        match = re.search(r'N\s*=\s*(\d{2}/\d{2}/\d{4})', line0[1])
        if match:
            date_str = match.group(1)
            
    # 2. Split sections
    sec_po_rows = []
    sec_am_rows = []
    sec_prov_rows = []
    
    current_section = None # 'po', 'am', 'prov'
    
    for idx, line in enumerate(lines):
        if len(line) == 0 or not line[0].strip():
            continue
            
        first_cell = line[0].strip()
        
        if '🏪 TẤT CẢ BƯU CỤC' in first_cell:
            current_section = 'po'
            continue
        elif '👤 THEO AM' in first_cell:
            current_section = 'am'
            continue
        elif '🗺️ THEO TỈNH' in first_cell:
            current_section = 'prov'
            continue
            
        # Skip headers
        if first_cell in ['Bưu Cục', 'AM', 'Tỉnh'] and line[1].strip() in ['AM', '%FD (N)', '']:
            continue
            
        # Parse data based on section
        if current_section == 'po':
            # Schema: Bưu cục, AM, %FD (N), %FD (N-1), vs N-1, %FD (N-7), vs N-7, Vol giao, Vol trả, Tỷ trọng trả
            if len(line) >= 10:
                sec_po_rows.append({
                    'post_office': line[0].strip(),
                    'am': line[1].strip(),
                    'fd_n': clean_pct(line[2]),
                    'fd_n1': clean_pct(line[3]),
                    'vs_n1': clean_pct(line[4]) * (-1 if '▼' in line[4] else 1),
                    'fd_n7': clean_pct(line[5]),
                    'vs_n7': clean_pct(line[6]) * (-1 if '▼' in line[6] else 1),
                    'vol_giao': clean_num(line[7]),
                    'vol_tra': clean_num(line[8]),
                    'ty_trong_tra': clean_pct(line[9])
                })
        elif current_section == 'am':
            # Schema: AM, %FD (N), %FD (N-1), vs N-1, %FD (N-7), vs N-7, Vol trả, Tỷ trọng trả
            if len(line) >= 8:
                sec_am_rows.append({
                    'am': line[0].strip(),
                    'fd_n': clean_pct(line[1]),
                    'fd_n1': clean_pct(line[2]),
                    'vs_n1': clean_pct(line[3]) * (-1 if '▼' in line[3] else 1),
                    'fd_n7': clean_pct(line[4]),
                    'vs_n7': clean_pct(line[5]) * (-1 if '▼' in line[5] else 1),
                    'vol_tra': clean_num(line[6]),
                    'ty_trong_tra': clean_pct(line[7])
                })
        elif current_section == 'prov':
            # Schema: Tỉnh, %FD (N), %FD (N-1), vs N-1, %FD (N-7), vs N-7
            if len(line) >= 6:
                sec_prov_rows.append({
                    'province': line[0].strip(),
                    'fd_n': clean_pct(line[1]),
                    'fd_n1': clean_pct(line[2]),
                    'vs_n1': clean_pct(line[3]) * (-1 if '▼' in line[3] else 1),
                    'fd_n7': clean_pct(line[4]),
                    'vs_n7': clean_pct(line[5]) * (-1 if '▼' in line[5] else 1)
                })

    # Find "Tổng NTB" in provinces
    kpi_fd = {
        'fd_n': 0.0,
        'fd_n1': 0.0,
        'vs_n1': 0.0,
        'fd_n7': 0.0,
        'vs_n7': 0.0
    }
    
    # Extract "Tổng NTB" to separate object and filter it out of province list
    provinces_clean = []
    for r in sec_prov_rows:
        if r['province'] == 'Tổng NTB':
            kpi_fd = {
                'fd_n': r['fd_n'],
                'fd_n1': r['fd_n1'],
                'vs_n1': r['vs_n1'],
                'fd_n7': r['fd_n7'],
                'vs_n7': r['vs_n7']
            }
        else:
            provinces_clean.append(r)
            
    return {
        'date': date_str,
        'kpi': kpi_fd,
        'po': sec_po_rows,
        'am': sec_am_rows,
        'province': provinces_clean
    }

res = parse_fd_csv('ops_fd.csv')
print("\nParsed successfully!")
print("Date:", res['date'])
print("KPI:", res['kpi'])
print("Provinces count:", len(res['province']))
print("First province:", res['province'][0] if res['province'] else "None")
print("AM count:", len(res['am']))
print("First AM:", res['am'][0] if res['am'] else "None")
print("PO count:", len(res['po']))
print("First PO:", res['po'][0] if res['po'] else "None")
