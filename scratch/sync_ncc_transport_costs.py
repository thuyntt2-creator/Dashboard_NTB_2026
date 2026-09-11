import os
import sys
import json
import re
import datetime
import urllib.parse
import urllib.request
import requests

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("=== ĐỒNG BỘ CHI PHÍ VẬN TẢI & KTC TỪ 7 GOOGLE SHEETS NCC ===")
print("=" * 60)

# 1. Acquire OAuth Token
token = None
candidate_token_paths = [
    os.path.join(os.path.dirname(__file__), 'authorized_user.json'),
    r'authorized_user.json',
    r'C:\Users\lap4all\Documents\Auto report\authorized_user.json',
    r'C:\Users\lap4all\Desktop\Backlog_Automation\authorized_user.json',
]

for tp in candidate_token_paths:
    if os.path.exists(tp):
        try:
            with open(tp, 'r', encoding='utf-8') as f:
                t_data = json.load(f)
            data = urllib.parse.urlencode({
                'grant_type': 'refresh_token',
                'client_id': t_data['client_id'],
                'client_secret': t_data['client_secret'],
                'refresh_token': t_data['refresh_token']
            }).encode('utf-8')
            req = urllib.request.Request(t_data['token_uri'], data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
            res = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
            token = res.get('access_token')
            if token:
                print(f"✅ Đã lấy OAuth access token từ: {tp}")
                break
        except Exception as e:
            pass

if not token:
    print("❌ Lỗi: Không thể làm mới Google OAuth Token. Vui lòng kiểm tra authorized_user.json!")
    sys.exit(1)

headers = {'Authorization': f'Bearer {token}'}

def get_tab_rows(s_id, tab_name, r_range='A1:P350'):
    try:
        encoded = urllib.parse.quote(tab_name)
        val_url = f"https://sheets.googleapis.com/v4/spreadsheets/{s_id}/values/'{encoded}'!{r_range}"
        r = requests.get(val_url, headers=headers, timeout=18)
        if r.status_code == 200:
            return r.json().get('values', [])
    except Exception as e:
        print(f"⚠️ Lỗi fetch tab {tab_name} ({s_id}): {e}")
    return []

def parse_num(v):
    if v is None:
        return 0.0
    s = str(v).replace('đ', '').replace('Đ', '').replace(' ', '').strip()
    if not s or s == '-' or s == '0.00':
        return 0.0
    # Handle dot vs comma separator
    # E.g. "1.014.687" or "101.075.930 đ" or "796723,2"
    if ',' in s and '.' in s:
        # e.g. 1,014,687.50 or 1.014.687,50
        if s.find('.') < s.find(','):
            s = s.replace('.', '').replace(',', '.')
        else:
            s = s.replace(',', '')
    elif '.' in s:
        # Check if dot is thousands separator
        parts = s.split('.')
        if len(parts) > 1 and all(len(p) == 3 for p in parts[1:]):
            s = s.replace('.', '')
    elif ',' in s:
        # Check if comma is decimal or thousands
        parts = s.split(',')
        if len(parts) > 1 and len(parts[-1]) <= 2:
            s = s.replace(',', '.')
        else:
            s = s.replace(',', '')
    try:
        return float(s)
    except Exception:
        return 0.0

def extract_ktc(route_text):
    t = str(route_text).lower()
    if 'bảo lộc' in t or 'bao loc' in t:
        return 'KTC Bảo Lộc'
    elif 'đức trọng' in t or 'duc trong' in t:
        return 'KTC Đức Trọng'
    elif 'đắk nông' in t or 'dak nong' in t or 'gia nghĩa' in t:
        return 'KTC Đắk Nông'
    elif 'bắc nha trang' in t or 'bac nha trang' in t:
        return 'KTC Bắc Nha Trang'
    elif 'nam nha trang' in t or 'nam nha trang' in t:
        return 'KTC Nam Nha Trang'
    elif 'khánh hòa' in t or 'nha trang' in t or 'diên khánh' in t:
        return 'KTC Khánh Hòa'
    elif 'phan thiết' in t or 'bình thuận' in t:
        return 'KTC Bình Thuận'
    elif 'ninh thuận' in t or 'phan rang' in t:
        return 'KTC Ninh Thuận'
    return 'KTC Đắk Nông' if 'dno' in t else 'KTC Liên Tỉnh'

all_trips = []

# ==============================================================================
# 1. CÔNG ĐỊNH
# ==============================================================================
print("Đang quét: NCC Công Định...")
rows_cd = get_tab_rows('1uRoMDGPI0rJI5pqK4VA0QVfNj9B2vh9heNr9ow4MXaw', 'CĐ', 'A1:P250')
cd_count = 0
for r in rows_cd[2:]:
    if len(r) >= 12 and r[1].strip() and '/' in str(r[1]):
        cost = parse_num(r[11])
        if cost > 0:
            ghi_chu = r[14].strip() if len(r) > 14 else ''
            hinh_thuc = r[4].strip() if len(r) > 4 else ''
            is_surge = 'tăng cường' in ghi_chu.lower() or 'tăng cường' in hinh_thuc.lower()
            all_trips.append({
                'id': f"CD_{cd_count+1}",
                'ncc': 'Công Định',
                'date': r[1].strip(),
                'truck': r[2].strip() if len(r) > 2 else '',
                'capacity': r[3].strip() if len(r) > 3 else '1.9T',
                'cost_type': hinh_thuc,
                'type': 'Tăng cường' if is_surge else 'Cố định',
                'route': r[5].strip() if len(r) > 5 else '',
                'ktc': extract_ktc(r[5] if len(r) > 5 else ''),
                'km': parse_num(r[6]) if len(r) > 6 else 0,
                'cost': cost,
                'trip_code': r[13].strip() if len(r) > 13 else f"CD_{cd_count+1}",
                'ontime': r[10].strip() if len(r) > 10 else '100%'
            })
            cd_count += 1
print(f" -> Công Định: {cd_count} chuyến xe.")

# ==============================================================================
# 2. TỐT VÀ RẺ
# ==============================================================================
print("Đang quét: NCC Tốt và Rẻ...")
rows_tr = get_tab_rows('1SuhbzeBJBnASyMT4nW9o5kiHOEW7zkBLGA-LmN8jpNU', 'TR', 'A1:P250')
tr_count = 0
for r in rows_tr[2:]:
    if len(r) >= 12 and r[1].strip() and '/' in str(r[1]):
        cost = parse_num(r[11])
        if cost > 0:
            ghi_chu = r[14].strip() if len(r) > 14 else ''
            hinh_thuc = r[4].strip() if len(r) > 4 else ''
            is_surge = 'tăng cường' in ghi_chu.lower() or 'tăng cường' in hinh_thuc.lower()
            all_trips.append({
                'id': f"TR_{tr_count+1}",
                'ncc': 'Tốt và Rẻ',
                'date': r[1].strip(),
                'truck': r[2].strip() if len(r) > 2 else '',
                'capacity': r[3].strip() if len(r) > 3 else '1.9T',
                'cost_type': hinh_thuc,
                'type': 'Tăng cường' if is_surge else 'Cố định',
                'route': r[5].strip() if len(r) > 5 else '',
                'ktc': extract_ktc(r[5] if len(r) > 5 else ''),
                'km': parse_num(r[6]) if len(r) > 6 else 0,
                'cost': cost,
                'trip_code': r[13].strip() if len(r) > 13 else f"TR_{tr_count+1}",
                'ontime': r[10].strip() if len(r) > 10 else '100%'
            })
            tr_count += 1
print(f" -> Tốt và Rẻ: {tr_count} chuyến xe.")

# ==============================================================================
# 3. NAK
# ==============================================================================
print("Đang quét: NCC NAK...")
rows_nak = get_tab_rows('1_fDiARRteAUNEyas9tw9vvSDCppCudj_jxvqDrH8jug', 'DATA', 'A1:P300')
nak_count = 0
for r in rows_nak[1:]:
    if len(r) >= 12 and r[1].strip() and '/' in str(r[1]):
        cost = parse_num(r[11])
        if cost > 0:
            ghi_chu = r[14].strip() if len(r) > 14 else ''
            hinh_thuc = r[4].strip() if len(r) > 4 else ''
            is_surge = 'tăng cường' in ghi_chu.lower() or 'tăng cường' in hinh_thuc.lower()
            all_trips.append({
                'id': f"NAK_{nak_count+1}",
                'ncc': 'NAK',
                'date': r[1].strip(),
                'truck': r[2].strip() if len(r) > 2 else '',
                'capacity': r[3].strip() if len(r) > 3 else '1.9T',
                'cost_type': hinh_thuc,
                'type': 'Tăng cường' if is_surge else 'Cố định',
                'route': r[5].strip() if len(r) > 5 else '',
                'ktc': extract_ktc(r[5] if len(r) > 5 else ''),
                'km': parse_num(r[6]) if len(r) > 6 else 0,
                'cost': cost,
                'trip_code': r[13].strip() if len(r) > 13 else f"NAK_{nak_count+1}",
                'ontime': r[10].strip() if len(r) > 10 else '100%'
            })
            nak_count += 1
print(f" -> NAK: {nak_count} chuyến xe.")

# ==============================================================================
# 4. LÂM NGỌC THÀNH
# ==============================================================================
print("Đang quét: NCC Lâm Ngọc Thành...")
rows_lnt = get_tab_rows('1VeYu4_Gs78E_sLRTx-Pq4PoDBmYR9oT8Ch6oDM_E2sM', 'DNO_01', 'A1:P250')
lnt_count = 0
for r in rows_lnt[6:]:
    if len(r) >= 12 and r[1].strip() and '/' in str(r[1]):
        cost = parse_num(r[11])
        if cost > 0:
            ghi_chu = r[14].strip() if len(r) > 14 else ''
            hinh_thuc = r[4].strip() if len(r) > 4 else ''
            is_surge = 'tăng cường' in ghi_chu.lower() or 'tăng cường' in hinh_thuc.lower()
            all_trips.append({
                'id': f"LNT_{lnt_count+1}",
                'ncc': 'Lâm Ngọc Thành',
                'date': r[1].strip(),
                'truck': r[2].strip() if len(r) > 2 else '',
                'capacity': r[3].strip() if len(r) > 3 else '3.5T',
                'cost_type': hinh_thuc,
                'type': 'Tăng cường' if is_surge else 'Cố định',
                'route': r[5].strip() if len(r) > 5 else '',
                'ktc': extract_ktc(r[5] if len(r) > 5 else ''),
                'km': parse_num(r[6]) if len(r) > 6 else 0,
                'cost': cost,
                'trip_code': r[13].strip() if len(r) > 13 else f"LNT_{lnt_count+1}",
                'ontime': r[10].strip() if len(r) > 10 else '100%'
            })
            lnt_count += 1
print(f" -> Lâm Ngọc Thành: {lnt_count} chuyến xe.")

# ==============================================================================
# 5. TRÂM HOÁ
# ==============================================================================
print("Đang quét: NCC Trâm Hoá...")
rows_th = get_tab_rows('1lt4NC2Ih_rqgsO8O7-qYTki17fPnjGwdB5EpTl116qg', 'TH', 'A1:P250')
th_count = 0
for r in rows_th[2:]:
    if len(r) >= 12 and r[1].strip() and '/' in str(r[1]):
        cost = parse_num(r[11])
        if cost > 0:
            ghi_chu = r[14].strip() if len(r) > 14 else ''
            hinh_thuc = r[4].strip() if len(r) > 4 else ''
            is_surge = 'tăng cường' in ghi_chu.lower() or 'tăng cường' in hinh_thuc.lower()
            all_trips.append({
                'id': f"TH_{th_count+1}",
                'ncc': 'Trâm Hoá',
                'date': r[1].strip(),
                'truck': r[2].strip() if len(r) > 2 else '',
                'capacity': r[3].strip() if len(r) > 3 else '3.5T',
                'cost_type': hinh_thuc,
                'type': 'Tăng cường' if is_surge else 'Cố định',
                'route': r[5].strip() if len(r) > 5 else '',
                'ktc': extract_ktc(r[5] if len(r) > 5 else ''),
                'km': parse_num(r[6]) if len(r) > 6 else 0,
                'cost': cost,
                'trip_code': r[13].strip() if len(r) > 13 else f"TH_{th_count+1}",
                'ontime': r[10].strip() if len(r) > 10 else '100%'
            })
            th_count += 1

# Tab xe tăng cường Trâm Hoá (nếu có)
rows_th_tc = get_tab_rows('1lt4NC2Ih_rqgsO8O7-qYTki17fPnjGwdB5EpTl116qg', 'Chuyến Ghép/Tăng cường GXT', 'A1:P100')
for r in rows_th_tc[1:]:
    if len(r) >= 6:
        cost = parse_num(r[4] if len(r) > 4 else 0)
        if cost > 0:
            all_trips.append({
                'id': f"TH_TC_{th_count+1}",
                'ncc': 'Trâm Hoá',
                'date': r[0].strip() if '/' in str(r[0]) else 'Tháng 8/2026',
                'truck': r[1].strip() if len(r) > 1 else '',
                'capacity': 'Tăng Cường',
                'cost_type': 'Cost/Chuyến',
                'type': 'Tăng cường',
                'route': r[2].strip() if len(r) > 2 else '',
                'ktc': extract_ktc(r[2] if len(r) > 2 else ''),
                'km': 0,
                'cost': cost,
                'trip_code': f"TCTC_{th_count+1}",
                'ontime': '100%'
            })
            th_count += 1
print(f" -> Trâm Hoá: {th_count} chuyến xe.")

# ==============================================================================
# 6. MẠNH CƯỜNG (KTC & TUYẾN)
# ==============================================================================
print("Đang quét: NCC Mạnh Cường...")
rows_mc = get_tab_rows('1xQtd7DUZ9JVctuV7VChwR1AMy9KPCOy6cz2YFTOVXuo', 'MCKH', 'A1:P250')
mc_count = 0
for r in rows_mc[2:]:
    if len(r) >= 12 and r[1].strip() and '/' in str(r[1]):
        cost = parse_num(r[11])
        if cost > 0:
            ghi_chu = r[14].strip() if len(r) > 14 else ''
            hinh_thuc = r[4].strip() if len(r) > 4 else ''
            is_surge = 'tăng cường' in ghi_chu.lower() or 'tăng cường' in hinh_thuc.lower()
            all_trips.append({
                'id': f"MC_{mc_count+1}",
                'ncc': 'Mạnh Cường',
                'date': r[1].strip(),
                'truck': r[2].strip() if len(r) > 2 else '',
                'capacity': r[3].strip() if len(r) > 3 else '5.0T',
                'cost_type': hinh_thuc,
                'type': 'Tăng cường' if is_surge else 'Cố định',
                'route': r[5].strip() if len(r) > 5 else '',
                'ktc': extract_ktc(r[5] if len(r) > 5 else ''),
                'km': parse_num(r[6]) if len(r) > 6 else 0,
                'cost': cost,
                'trip_code': r[13].strip() if len(r) > 13 else f"MC_{mc_count+1}",
                'ontime': r[10].strip() if len(r) > 10 else '100%'
            })
            mc_count += 1
print(f" -> Mạnh Cường: {mc_count} chuyến xe.")

# ==============================================================================
# 7. MẠNH CƯỜNG - BCCK (HỢP ĐỒNG THÁNG CỐ ĐỊNH)
# ==============================================================================
print("Đang quét: NCC Mạnh Cường - BCCK...")
rows_mcbcck = get_tab_rows('16UfCMPOOMJM3cS3h2wG4TPyGFgq-arrYd_qnShA_Id0', 'XUẤT HĐ.', 'A1:L50')
mcbcck_count = 0
for r in rows_mcbcck[1:]:
    if len(r) >= 11 and r[0].strip() and ('-' in str(r[0]) or 'C' in str(r[0])):
        cost = parse_num(r[10])
        if cost > 0:
            # 1 xe hợp đồng tháng chạy trung bình 30 chuyến/tháng
            all_trips.append({
                'id': f"MC_BCCK_{mcbcck_count+1}",
                'ncc': 'Mạnh Cường (BCCK)',
                'date': 'Hàng ngày',
                'truck': r[0].strip(),
                'capacity': 'Bưu cục CK',
                'cost_type': 'Cost/tháng',
                'type': 'Cố định',
                'route': r[1].strip() if len(r) > 1 else '',
                'ktc': extract_ktc(r[1] if len(r) > 1 else ''),
                'km': 0,
                'cost': cost,
                'trip_code': f"HĐ_BCCK_{mcbcck_count+1}",
                'ontime': '100%',
                'trips_equivalent': 30
            })
            mcbcck_count += 1
print(f" -> Mạnh Cường BCCK: {mcbcck_count} xe hợp đồng cố định.")

# ==============================================================================
# TÍNH TOÁN 4 NHÓM CHỈ SỐ THEO YÊU CẦU CỦA SẾP
# ==============================================================================
print("\nĐang tính toán các chỉ số quản trị chi phí vận tải...")

# 1. Từng KTC (Kho Trung Chuyển)
ktc_dict = {}
for t in all_trips:
    ktc = t['ktc']
    if ktc not in ktc_dict:
        ktc_dict[ktc] = {
            'ktc': ktc,
            'total_cost': 0.0,
            'total_trips': 0,
            'fixed_cost': 0.0,
            'surge_cost': 0.0,
            'nccs': set(),
            'trucks': set()
        }
    cost = t['cost']
    trips = t.get('trips_equivalent', 1)
    ktc_dict[ktc]['total_cost'] += cost
    ktc_dict[ktc]['total_trips'] += trips
    if t['type'] == 'Cố định':
        ktc_dict[ktc]['fixed_cost'] += cost
    else:
        ktc_dict[ktc]['surge_cost'] += cost
    ktc_dict[ktc]['nccs'].add(t['ncc'])
    if t['truck']:
        ktc_dict[ktc]['trucks'].add(t['truck'])

ktc_list = []
for k, v in sorted(ktc_dict.items(), key=lambda x: x[1]['total_cost'], reverse=True):
    total_c = v['total_cost']
    trips = v['total_trips']
    avg_trip = (total_c / trips) if trips > 0 else 0
    surge_pct = (v['surge_cost'] / total_c * 100) if total_c > 0 else 0
    ktc_list.append({
        'ktc': k,
        'total_cost': round(total_c / 1e6, 2), # Triệu VNĐ
        'total_cost_raw': total_c,
        'total_trips': trips,
        'cost_per_trip': round(avg_trip / 1e6, 2), # Triệu VNĐ / chuyến
        'cost_per_trip_raw': avg_trip,
        'fixed_cost': round(v['fixed_cost'] / 1e6, 2),
        'surge_cost': round(v['surge_cost'] / 1e6, 2),
        'surge_pct': round(surge_pct, 1),
        'primary_ncc': ", ".join(list(v['nccs'])[:2]),
        'truck_count': len(v['trucks'])
    })

# 2. Từng NCC (Nhà Cung Cấp)
ncc_dict = {}
for t in all_trips:
    ncc = t['ncc']
    if ncc not in ncc_dict:
        ncc_dict[ncc] = {
            'ncc': ncc,
            'total_cost': 0.0,
            'total_trips': 0,
            'fixed_cost': 0.0,
            'surge_cost': 0.0,
            'ktcs': set(),
            'trucks': set()
        }
    cost = t['cost']
    trips = t.get('trips_equivalent', 1)
    ncc_dict[ncc]['total_cost'] += cost
    ncc_dict[ncc]['total_trips'] += trips
    if t['type'] == 'Cố định':
        ncc_dict[ncc]['fixed_cost'] += cost
    else:
        ncc_dict[ncc]['surge_cost'] += cost
    ncc_dict[ncc]['ktcs'].add(t['ktc'])
    if t['truck']:
        ncc_dict[ncc]['trucks'].add(t['truck'])

ncc_list = []
for k, v in sorted(ncc_dict.items(), key=lambda x: x[1]['total_cost'], reverse=True):
    total_c = v['total_cost']
    trips = v['total_trips']
    avg_trip = (total_c / trips) if trips > 0 else 0
    surge_pct = (v['surge_cost'] / total_c * 100) if total_c > 0 else 0
    ncc_list.append({
        'ncc': k,
        'total_cost': round(total_c / 1e6, 2), # Triệu VNĐ
        'total_cost_raw': total_c,
        'total_trips': trips,
        'cost_per_trip': round(avg_trip / 1e6, 2), # Triệu VNĐ / chuyến
        'cost_per_trip_raw': avg_trip,
        'fixed_cost': round(v['fixed_cost'] / 1e6, 2),
        'surge_cost': round(v['surge_cost'] / 1e6, 2),
        'surge_pct': round(surge_pct, 1),
        'truck_count': len(v['trucks']),
        'active_ktcs': ", ".join(list(v['ktcs']))
    })

# 3. Tăng cường vs Cố định
total_region_cost = sum(t['cost'] for t in all_trips)
total_region_trips = sum(t.get('trips_equivalent', 1) for t in all_trips)
total_fixed_cost = sum(t['cost'] for t in all_trips if t['type'] == 'Cố định')
total_surge_cost = sum(t['cost'] for t in all_trips if t['type'] != 'Cố định')
total_fixed_trips = sum(t.get('trips_equivalent', 1) for t in all_trips if t['type'] == 'Cố định')
total_surge_trips = sum(t.get('trips_equivalent', 1) for t in all_trips if t['type'] != 'Cố định')

surge_fixed_summary = {
    'fixed_cost': round(total_fixed_cost / 1e6, 2),
    'fixed_cost_pct': round((total_fixed_cost / total_region_cost * 100) if total_region_cost > 0 else 0, 1),
    'fixed_trips': total_fixed_trips,
    'surge_cost': round(total_surge_cost / 1e6, 2),
    'surge_cost_pct': round((total_surge_cost / total_region_cost * 100) if total_region_cost > 0 else 0, 1),
    'surge_trips': total_surge_trips,
    'eval': 'An toàn (<20% chi phí xe tăng cường)' if (total_surge_cost / total_region_cost) < 0.2 else 'Cần kiểm soát chi phí xe tăng cường'
}

# 4. Tổng vùng Nam Trung Bộ
region_summary = {
    'total_cost': round(total_region_cost / 1e6, 2), # Triệu VNĐ
    'total_cost_formatted': f"{total_region_cost:,.0f} đ".replace(',', '.'),
    'total_trips': total_region_trips,
    'avg_cost_per_trip': round((total_region_cost / total_region_trips / 1e6), 2) if total_region_trips > 0 else 0,
    'avg_cost_per_trip_formatted': f"{(total_region_cost / total_region_trips):,.0f} đ/chuyến".replace(',', '.') if total_region_trips > 0 else "0 đ",
    'ncc_count': len(ncc_dict),
    'ktc_count': len(ktc_dict),
    'total_trucks': len(set(t['truck'] for t in all_trips if t['truck'])),
    'last_updated': datetime.datetime.now().strftime("%H:%M - %d/%m/%Y")
}

import re

def normalize_date(d_str):
    if not d_str:
        return 'N/A', ''
    s = str(d_str).strip()
    m = re.search(r'(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})', s)
    if m:
        day, mon, yr = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return f"{day:02d}/{mon:02d}/{yr}", f"{yr:04d}-{mon:02d}-{day:02d}"
    return s, ''

# Include all trips with standardized date_iso for interactive frontend filtering
all_trips_formatted = []
for t in all_trips:
    d_disp, d_iso = normalize_date(t.get('date'))
    all_trips_formatted.append({
        'ncc': t['ncc'],
        'date': d_disp,
        'date_iso': d_iso,
        'truck': t['truck'],
        'capacity': t.get('capacity', ''),
        'route': t['route'],
        'ktc': t['ktc'],
        'type': t['type'],
        'cost_str': f"{t['cost']:,.0f} đ".replace(',', '.'),
        'cost': t['cost'],
        'trips_equivalent': t.get('trips_equivalent', 1),
        'trip_code': t['trip_code'],
        'ontime': t.get('ontime', '100%')
    })

payload = {
    'region': region_summary,
    'surge_fixed': surge_fixed_summary,
    'ktcs': ktc_list,
    'nccs': ncc_list,
    'trips': all_trips_formatted,
    'all_trips_count': len(all_trips)
}

# Save output JSON in scratch/transport_costs.json and transport_costs.json
scratch_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(scratch_dir, 'transport_costs.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

root_out_path = os.path.join(os.path.dirname(scratch_dir), 'transport_costs.json')
with open(root_out_path, 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 60)
print(f"🎉 HOÀN TẤT ĐỒNG BỘ CHI PHÍ VẬN TẢI!")
print(f"• Tổng chi phí toàn vùng: {region_summary['total_cost']} Triệu VNĐ ({region_summary['total_cost_formatted']})")
print(f"• Tổng số chuyến xe: {region_summary['total_trips']} chuyến")
print(f"• Chi phí bình quân/chuyến: {region_summary['avg_cost_per_trip']} Tr ₫ ({region_summary['avg_cost_per_trip_formatted']})")
print(f"• Tỷ trọng Tăng Cường: {surge_fixed_summary['surge_cost_pct']}% | Cố Định: {surge_fixed_summary['fixed_cost_pct']}%")
print(f"• Số NCC: {region_summary['ncc_count']} NCC | Số KTC: {region_summary['ktc_count']} KTC")
print(f"• File cache đã lưu: {out_path}")
print("=" * 60)
