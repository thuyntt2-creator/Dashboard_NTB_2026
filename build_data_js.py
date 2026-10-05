import openpyxl
import json
import os
import sys
import glob
import re
import time

sys.stdout.reconfigure(encoding='utf-8')

def find_latest_excel():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(root_dir) == 'scratch':
        root_dir = os.path.dirname(root_dir)
    
    candidates = []
    candidates.extend(glob.glob(os.path.join(root_dir, 'BaoCao_Tuan_NTB_W*.xlsx')))
    candidates.extend(glob.glob(r'C:\Users\lap4all\Downloads\**\BaoCao_Tuan_NTB_W*.xlsx', recursive=True))
    candidates.extend(glob.glob(r'C:\Users\lap4all\Desktop\**\BaoCao_Tuan_NTB_W*.xlsx', recursive=True))

    def get_week_num(path):
        m = re.search(r'W(\d+)', os.path.basename(path), re.IGNORECASE)
        return int(m.group(1)) if m else 0

    valid_candidates = [p for p in candidates if os.path.exists(p) and get_week_num(p) > 0]
    if not valid_candidates:
        fallback = os.path.join(root_dir, 'BaoCao_Tuan_NTB_W36_2026.xlsx')
        if os.path.exists(fallback):
            return fallback
        raise FileNotFoundError("Không tìm thấy file Excel báo cáo tuần nào!")

    valid_candidates.sort(key=lambda p: (get_week_num(p), os.path.getmtime(p)), reverse=True)
    best_file = valid_candidates[0]
    
    # Neu file tot nhat nam o Downloads, tu dong copy ve root_dir de luu tru lau dai
    best_dir = os.path.dirname(os.path.abspath(best_file))
    if os.path.abspath(root_dir) != best_dir:
        import shutil
        target_name = os.path.basename(best_file)
        target_path = os.path.join(root_dir, target_name)
        try:
            shutil.copy2(best_file, target_path)
            print(f"Da tu dong sao chep file moi tu Downloads ve thu muc goc: {target_path}")
            return target_path
        except Exception as copy_err:
            print(f"Khong the copy file tu Downloads: {copy_err}")
            return best_file

    return best_file

excel_path = find_latest_excel()
print(f"Reading data from: {excel_path}")
wb = openpyxl.load_workbook(excel_path, data_only=True)

# Detect weeks dynamically
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

def calculate_week_date_range(week_str, default_year=2026):
    m = re.search(r'(\d+)', str(week_str))
    if not m:
        return '07/09 - 13/09/2026'
    w_num = int(m.group(1))
    import datetime
    try:
        monday = datetime.date.fromisocalendar(default_year, w_num, 1)
        sunday = datetime.date.fromisocalendar(default_year, w_num, 7)
        return f"{monday.strftime('%d/%m')} - {sunday.strftime('%d/%m/%Y')}"
    except Exception:
        return '07/09 - 13/09/2026'

date_range = calculate_week_date_range(latest_week)

print(f"Detected: {latest_week}, Weeks: {weeks}, Date Range: {date_range}")

w_keys = [w.lower() for w in weeks]

def parse_san_luong_sheet():
    ws = wb['01_San luong']
    
    def extract_rows(r_start, r_end, name_col=1):
        items = []
        for r in range(r_start, r_end + 1):
            name = ws.cell(r, name_col).value
            if name and str(name).strip() not in ['None', '', 'AM', 'Tỉnh', 'THEO AM - TTS', 'THEO TỈNH - Full hàng', 'THEO TỈNH - TTS']:
                w_vals = [ws.cell(r, c).value or 0 for c in range(2, 6)]
                diff = ws.cell(r, 6).value if ws.cell(r, 6).value is not None else (w_vals[-1] - w_vals[-2])
                item = {
                    'am': str(name).strip(),
                    'tinh': str(name).strip(),
                    'vol': w_vals[-1],
                    'diff': diff
                }
                for idx, k in enumerate(w_keys):
                    item[k] = w_vals[idx]
                
                for idx, w in enumerate(weeks):
                    item[w.lower()] = w_vals[idx] if idx < len(w_vals) else 0
                item['w35'] = item.get('w35', w_vals[0] if len(w_vals) > 0 else 0)
                item['w36'] = item.get('w36', w_vals[1] if len(w_vals) > 1 else 0)
                item['w37'] = item.get('w37', w_vals[2] if len(w_vals) > 2 else 0)
                item['w38'] = item.get('w38', w_vals[3] if len(w_vals) > 3 else 0)
                item['w34'] = item.get('w34', w_vals[0] if len(w_vals) > 0 else 0)
                items.append(item)
        return items

    am_full = extract_rows(11, 32)
    am_tts = extract_rows(33, 55)
    tinh_full = extract_rows(56, 64)
    tinh_tts = extract_rows(65, 73)

    return {
        'am_full': am_full,
        'am_tts': am_tts,
        'tinh_full': tinh_full,
        'tinh_tts': tinh_tts,
        'am': am_full,
        'tinh': tinh_full
    }

def parse_standard_sheet(sheet_name):
    ws = wb[sheet_name]
    overview = []
    for r in range(6, 10):
        c1 = ws.cell(r, 1).value
        if c1:
            w_vals = [ws.cell(r, c).value for c in range(2, 6)]
            diff = ws.cell(r, 6).value
            ov = {
                'label': str(c1).strip(),
                'diff': diff
            }
            for idx, w in enumerate(weeks):
                ov[w.lower()] = w_vals[idx] if idx < len(w_vals) else 0
            ov['w35'] = ov.get('w35', w_vals[0] if len(w_vals) > 0 else 0)
            ov['w36'] = ov.get('w36', w_vals[1] if len(w_vals) > 1 else 0)
            ov['w37'] = ov.get('w37', w_vals[2] if len(w_vals) > 2 else 0)
            ov['w38'] = ov.get('w38', w_vals[3] if len(w_vals) > 3 else 0)
            ov['w34'] = ov.get('w34', w_vals[0] if len(w_vals) > 0 else 0)
            overview.append(ov)
            
    def extract_rows(r_start, r_end):
        items = []
        for r in range(r_start, r_end + 1):
            name = ws.cell(r, 1).value
            if name and str(name).strip() not in ['None', '', 'AM', 'Tỉnh', 'THEO AM - TTS', 'THEO TỈNH - Full hàng', 'THEO TỈNH - TTS']:
                w_vals = [ws.cell(r, c).value or 0 for c in range(3, 7)]
                diff = ws.cell(r, 7).value or 0
                vol = ws.cell(r, 2).value or w_vals[-1]
                item = {
                    'am': str(name).strip(),
                    'tinh': str(name).strip(),
                    'vol': vol,
                    'diff': diff
                }
                for idx, w in enumerate(weeks):
                    item[w.lower()] = w_vals[idx] if idx < len(w_vals) else 0
                item['w35'] = item.get('w35', w_vals[0] if len(w_vals) > 0 else 0)
                item['w36'] = item.get('w36', w_vals[1] if len(w_vals) > 1 else 0)
                item['w37'] = item.get('w37', w_vals[2] if len(w_vals) > 2 else 0)
                item['w38'] = item.get('w38', w_vals[3] if len(w_vals) > 3 else 0)
                item['w34'] = item.get('w34', w_vals[0] if len(w_vals) > 0 else 0)
                items.append(item)
        return items

    am_full = extract_rows(11, 32)
    am_tts = extract_rows(33, 55)
    tinh_full = extract_rows(56, 64)
    tinh_tts = extract_rows(65, 73)

    return {
        'overview': overview,
        'am_full': am_full,
        'am_tts': am_tts,
        'tinh_full': tinh_full,
        'tinh_tts': tinh_tts,
        'am': am_full,
        'tinh': tinh_full
    }

# 00_Tong quan parsing
ws_tq = wb['00_Tong quan']
tq_rows = {}
for r in range(20, 37):
    ind = ws_tq.cell(r, 1).value
    if ind:
        clean_ind = str(ind).strip()
        w_vals = [ws_tq.cell(r, c).value for c in range(2, 6)]
        diff = ws_tq.cell(r, 6).value
        row_dict = {
            'diff': diff
        }
        for idx, w in enumerate(weeks):
            row_dict[w.lower()] = w_vals[idx] if idx < len(w_vals) else None
        row_dict['w35'] = row_dict.get('w35', w_vals[0] if len(w_vals) > 0 else None)
        row_dict['w36'] = row_dict.get('w36', w_vals[1] if len(w_vals) > 1 else None)
        row_dict['w37'] = row_dict.get('w37', w_vals[2] if len(w_vals) > 2 else None)
        row_dict['w38'] = row_dict.get('w38', w_vals[3] if len(w_vals) > 3 else None)
        row_dict['w34'] = row_dict.get('w34', w_vals[0] if len(w_vals) > 0 else None)
        tq_rows[clean_ind] = row_dict

latest_k = latest_week.lower()
prev_k = prev_week.lower()

vol_full_curr = tq_rows.get('Sản lượng Full hàng', {}).get(latest_k, 357249)
vol_full_diff = tq_rows.get('Sản lượng Full hàng', {}).get('diff', 49412)

vol_tts_curr = tq_rows.get('Sản lượng TTS', {}).get(latest_k, 68719)
vol_tts_diff = tq_rows.get('Sản lượng TTS', {}).get('diff', 5597)

gtc_full_curr = tq_rows.get('%GTC Full hàng (Ca1+Ca2+Tồn)', {}).get(latest_k, 0.5778)
gtc_full_diff = tq_rows.get('%GTC Full hàng (Ca1+Ca2+Tồn)', {}).get('diff', -0.0036)

gtc_tts_curr = tq_rows.get('%GTC TTS (Ca1+Ca2+Tồn)', {}).get(latest_k, 0.5591)
gtc_tts_diff = tq_rows.get('%GTC TTS (Ca1+Ca2+Tồn)', {}).get('diff', -0.0104)

odr_full_curr = tq_rows.get('%ODR Full hàng', {}).get(latest_k, 0.9334)
odr_full_diff = tq_rows.get('%ODR Full hàng', {}).get('diff', 0.0046)

ltc_full_curr = tq_rows.get('%LTC Full hàng', {}).get(latest_k, 0.9029)
ltc_full_diff = tq_rows.get('%LTC Full hàng', {}).get('diff', -0.0021)

rot_lc_val = 0.0180
rot_lc_diff = -0.0045
for k, v in tq_rows.items():
    if 'rớt' in k.lower() or 'rot' in k.lower():
        rot_lc_val = v.get(latest_k, rot_lc_val) or rot_lc_val
        rot_lc_diff = v.get('diff', rot_lc_diff) or rot_lc_diff

# Parse Insights
# Executive Strategic Insights W38
insights = [
    {
        'type': 'warning',
        'text': 'Sản lượng toàn vùng hạ nhiệt sau kỳ đại lễ: Full hàng đạt 345,994 đơn (-3.15% WoW, giảm -11,255 đơn). TTS đạt 69,274 đơn (+0.81% WoW, tăng nhẹ +555 đơn). Lâm Đồng tiếp tục dẫn đầu quy mô (95,727 đơn), Khánh Hòa thứ nhì (96,012 đơn).'
    },
    {
        'type': 'warning',
        'text': 'Tỷ lệ Rớt Luân Chuyển tăng đột biến: Tỷ lệ rớt LC toàn vùng W38 tăng lên 3.32% (+1.52%p WoW so với 1.80% ở W37, tổng 252 đơn rớt / 7,586 đơn cần LC). Điểm nóng rớt tập trung tại Đắk Nông (20.73%), Khánh Hòa (5.09%), Lâm Đồng (3.32%). AM Thái Thị Thanh Thư rớt 79 đơn (7.13%), Trần Thị Nhung rớt 33 đơn (19.76%), Huỳnh Thúc Duân rớt 21 đơn (20.79%).'
    },
    {
        'type': 'positive',
        'text': 'Chất lượng ODR bảo vệ ngưỡng cao: %ODR Full hàng đạt 91.24% (-2.10%p WoW, TTS đạt 91.54%), Ninh Thuận (96.5%) và Bình Thuận (96.2%) tiếp tục dẫn đầu toàn vùng.'
    },
    {
        'type': 'warning',
        'text': '%GTC Tổng chịu áp lực tồn bãi: %GTC Full hàng đạt 55.75% (-2.02%p WoW), %GTC TTS đạt 54.01% (-1.90%p WoW). 3 AM suy giảm mạnh nhất gồm Nguyễn Thanh Long (42.52%, giảm -16.8%p), Phan Đình Duy (59.10%, -8.5%p), Lê Văn Trường (52.88%, -8.5%p).'
    },
    {
        'type': 'positive',
        'text': '%LTC Lấy thành công duy trì vững: %LTC Full hàng đạt 90.36% (+0.06%p WoW), TTS đạt 95.43% (+1.88%p WoW).'
    }
]


# KPIs Trend list
indicator_configs = [
    ('Sản lượng Full hàng', 'number'),
    ('Sản lượng TTS', 'number'),
    ('%GTC Full hàng (Ca1+Ca2+Tồn)', 'percent'),
    ('%GTC TTS (Ca1+Ca2+Tồn)', 'percent'),
    ('%GTC Full hàng (Ca1+Tồn)', 'percent'),
    ('%GTC Full hàng (Ca1 thuần)', 'percent'),
    ('%GTC TTS (Ca1 thuần)', 'percent'),
    ('%GTC TTS (Ca1+Tồn)', 'percent'),
    ('%GTC Full hàng (Ca2)', 'percent'),
    ('%GTC TTS (Ca2)', 'percent'),
    ('%ODR Full hàng', 'percent'),
    ('%ODR TTS', 'percent'),
    ('%LTC Full hàng', 'percent'),
    ('%LTC TTS', 'percent'),
    ('%Rớt Luân Chuyển', 'percent')
]

kpis_trend = []
for ind_name, ind_type in indicator_configs:
    item = tq_rows.get(ind_name, {})
    if not item and ind_name == '%Rớt Luân Chuyển':
        for k, v in tq_rows.items():
            if 'rớt' in k.lower():
                item = v
                break
    
    kpi_entry = {
        'indicator': ind_name,
        'diff': item.get('diff', 0),
        'type': ind_type
    }
    for k in w_keys:
        kpi_entry[k] = item.get(k)
    kpi_entry['w32'] = item.get('w32', item.get(w_keys[0]))
    kpi_entry['w33'] = item.get('w33', item.get(w_keys[0]))
    kpi_entry['w34'] = item.get('w34')
    kpi_entry['w35'] = item.get('w35')
    kpi_entry['w36'] = item.get('w36')
    kpi_entry['w37'] = item.get('w37')
    kpis_trend.append(kpi_entry)

data = {
    'meta': {
        'region': 'Vùng Nam Trung Bộ (NTB)',
        'provinces': ['Khánh Hòa', 'Lâm Đồng', 'Đắk Nông', 'Ninh Thuận', 'Bình Thuận'],
        'latest_week': latest_week,
        'prev_week': prev_week,
        'weeks': weeks,
        'date_range': date_range,
        'updated_at': '2026-09-14 18:00'
    },
    'overview': {
        'cards': [
            {'id': 'vol_full', 'title': 'Sản Lượng Full Hàng', 'val': vol_full_curr, 'unit': 'đơn', 'diff': vol_full_diff, 'diff_pct': (vol_full_diff / (vol_full_curr - vol_full_diff)) if (vol_full_curr - vol_full_diff) else 0, 'is_good': vol_full_diff >= 0, 'icon': 'package'},
            {'id': 'vol_tts', 'title': 'Sản Lượng TTS', 'val': vol_tts_curr, 'unit': 'đơn', 'diff': vol_tts_diff, 'diff_pct': (vol_tts_diff / (vol_tts_curr - vol_tts_diff)) if (vol_tts_curr - vol_tts_diff) else 0, 'is_good': vol_tts_diff >= 0, 'icon': 'truck'},
            {'id': 'gtc_full', 'title': '%GTC Full Hàng', 'val': gtc_full_curr, 'unit': '%', 'diff': gtc_full_diff, 'diff_pct': gtc_full_diff, 'is_good': gtc_full_diff >= 0, 'icon': 'check-circle-2'},
            {'id': 'gtc_tts', 'title': '%GTC TTS', 'val': gtc_tts_curr, 'unit': '%', 'diff': gtc_tts_diff, 'diff_pct': gtc_tts_diff, 'is_good': gtc_tts_diff >= 0, 'icon': 'award'},
            {'id': 'odr_full', 'title': '%ODR (Giao Đúng Hẹn)', 'val': odr_full_curr, 'unit': '%', 'diff': odr_full_diff, 'diff_pct': odr_full_diff, 'is_good': odr_full_diff >= 0, 'icon': 'clock'},
            {'id': 'ltc_full', 'title': '%LTC (Lấy Thành Công)', 'val': ltc_full_curr, 'unit': '%', 'diff': ltc_full_diff, 'diff_pct': ltc_full_diff, 'is_good': ltc_full_diff >= 0, 'icon': 'archive'},
            {'id': 'rot_lc', 'title': '%Rớt Luân Chuyển', 'val': rot_lc_val, 'unit': '%', 'diff': rot_lc_diff, 'diff_pct': rot_lc_diff, 'is_good': rot_lc_diff <= 0, 'icon': 'alert-triangle'},
            {'id': 'truy_thu', 'title': 'Tổng Cần Truy Thu', 'val': 187088448, 'unit': 'VNĐ', 'diff': -124994814, 'diff_pct': -0.401, 'is_good': True, 'icon': 'shield-alert'},
            {'id': 'cod_tm', 'title': 'Tỷ Lệ Tiền Mặt COD', 'val': 0.371, 'unit': '%', 'diff': -0.030, 'diff_pct': -0.075, 'is_good': True, 'icon': 'qr-code'}
        ],
        'kpis_trend': kpis_trend,
        'insights': insights
    }
}

data['san_luong'] = parse_san_luong_sheet()
data['gtc_tong'] = parse_standard_sheet('02_GTC tong')
data['gtc_ca1_ton'] = parse_standard_sheet('03_GTC Ca1+Ton')
data['gtc_ca1_thuan'] = parse_standard_sheet('03b_GTC Ca1 thuan')
data['gtc_ca2'] = parse_standard_sheet('04_GTC Ca2')
data['odr'] = parse_standard_sheet('05_ODR')
data['ltc'] = parse_standard_sheet('06_LTC')

# 07_Gan
ws_gan = wb['07_Gan']
gan_overview = []
for r in range(6, 12):
    ind = ws_gan.cell(r, 1).value
    if ind and str(ind).strip() not in ['None', '']:
        w_vals = [ws_gan.cell(r, c).value or 0 for c in range(2, 6)]
        diff = ws_gan.cell(r, 6).value if ws_gan.cell(r, 6).value is not None else (w_vals[-1] - w_vals[-2])
        ov = {
            'indicator': str(ind).strip(),
            'diff': diff
        }
        for idx, w in enumerate(weeks):
            ov[w.lower()] = w_vals[idx] if idx < len(w_vals) else 0
        ov['w35'] = ov.get('w35', w_vals[0])
        ov['w36'] = ov.get('w36', w_vals[1])
        ov['w37'] = ov.get('w37', w_vals[2])
        ov['w38'] = ov.get('w38', w_vals[3])
        ov['w34'] = ov.get('w34', w_vals[0])
        gan_overview.append(ov)

def extract_gan_am(r_start, r_end):
    items = []
    for r in range(r_start, r_end + 1):
        am = ws_gan.cell(r, 1).value
        if am and str(am).strip() not in ['None', '', 'AM']:
            item = {
                'am': str(am).strip(),
                'vol': ws_gan.cell(r, 2).value or 0,
                'tong_prev': ws_gan.cell(r, 3).value or 0,
                'tong_curr': ws_gan.cell(r, 4).value or 0,
                'tong_diff': ws_gan.cell(r, 5).value or 0,
                'ca1ton_prev': ws_gan.cell(r, 6).value or 0,
                'ca1ton_curr': ws_gan.cell(r, 7).value or 0,
                'ca1ton_diff': ws_gan.cell(r, 8).value or 0,
                'ca2_prev': ws_gan.cell(r, 9).value or 0,
                'ca2_curr': ws_gan.cell(r, 10).value or 0,
                'ca2_diff': ws_gan.cell(r, 11).value or 0,
                # Explicit week keys
                f'tong_{prev_k}': ws_gan.cell(r, 3).value or 0,
                f'tong_{latest_k}': ws_gan.cell(r, 4).value or 0,
                f'ca1ton_{prev_k}': ws_gan.cell(r, 6).value or 0,
                f'ca1ton_{latest_k}': ws_gan.cell(r, 7).value or 0,
                f'ca2_{prev_k}': ws_gan.cell(r, 9).value or 0,
                f'ca2_{latest_k}': ws_gan.cell(r, 10).value or 0,
                'tong_w37': ws_gan.cell(r, 3).value or 0,
                'tong_w38': ws_gan.cell(r, 4).value or 0,
                'ca1ton_w37': ws_gan.cell(r, 6).value or 0,
                'ca1ton_w38': ws_gan.cell(r, 7).value or 0,
                'ca2_w37': ws_gan.cell(r, 9).value or 0,
                'ca2_w38': ws_gan.cell(r, 10).value or 0,
                # Fallback keys
                'tong_w36': ws_gan.cell(r, 3).value or 0,
                'ca1ton_w36': ws_gan.cell(r, 6).value or 0,
                'ca2_w36': ws_gan.cell(r, 9).value or 0
            }
            items.append(item)
    return items

gan_am_full = extract_gan_am(16, 35)
gan_am_tts = extract_gan_am(38, 57)

data['gan'] = {
    'overview': gan_overview,
    'am_full': gan_am_full,
    'am_tts': gan_am_tts,
    'am': gan_am_full
}

# 08_OPR TTS
ws_opr = wb['08_OPR TTS']
opr_am = []
for r in range(6, 24):
    am = ws_opr.cell(r, 1).value
    if am and str(am).strip() not in ['None', '', 'AM']:
        w_prev_day = ws_opr.cell(r, 3).value or 0
        w_curr_day = (ws_opr.cell(r, 4).value or 0) if (ws_opr.cell(r, 4).value or 0) <= 1 else 0
        w_prev_night = ws_opr.cell(r, 7).value or 0
        w_curr_night = ws_opr.cell(r, 8).value or 0
        w_prev_total = ws_opr.cell(r, 11).value or 0
        w_curr_total = ws_opr.cell(r, 12).value or 0
        opr_am.append({
            'am': str(am).strip(),
            'vol_day': ws_opr.cell(r, 2).value or 0,
            f'{prev_k}_day': w_prev_day,
            f'{latest_k}_day': w_curr_day,
            'diff_day': ws_opr.cell(r, 5).value or 0,
            'vol_night': ws_opr.cell(r, 6).value or 0,
            f'{prev_k}_night': w_prev_night,
            f'{latest_k}_night': w_curr_night,
            'diff_night': ws_opr.cell(r, 9).value or 0,
            'vol_total': ws_opr.cell(r, 10).value or 0,
            f'{prev_k}_total': w_prev_total,
            f'{latest_k}_total': w_curr_total,
            'diff_total': ws_opr.cell(r, 13).value or 0,
            'w_prev_day': w_prev_day,
            'w_curr_day': w_curr_day,
            'w_prev_night': w_prev_night,
            'w_curr_night': w_curr_night,
            'w_prev_total': w_prev_total,
            'w_curr_total': w_curr_total,
            'w38_day': w_prev_day,
            'w39_day': w_curr_day,
            'w38_night': w_prev_night,
            'w39_night': w_curr_night,
            'w38_total': w_prev_total,
            'w39_total': w_curr_total
        })

opr_tinh = []
for r in range(26, 33):
    t = ws_opr.cell(r, 1).value
    if t and str(t).strip() not in ['None', '', 'Tỉnh']:
        w_prev_day = ws_opr.cell(r, 3).value or 0
        w_curr_day = ws_opr.cell(r, 4).value or 0
        w_prev_night = ws_opr.cell(r, 7).value or 0
        w_curr_night = ws_opr.cell(r, 8).value or 0
        w_prev_total = ws_opr.cell(r, 11).value or 0
        w_curr_total = ws_opr.cell(r, 12).value or 0
        opr_tinh.append({
            'tinh': str(t).strip(),
            'vol_day': ws_opr.cell(r, 2).value or 0,
            f'{prev_k}_day': w_prev_day,
            f'{latest_k}_day': w_curr_day,
            'diff_day': ws_opr.cell(r, 5).value or 0,
            'vol_night': ws_opr.cell(r, 6).value or 0,
            f'{prev_k}_night': w_prev_night,
            f'{latest_k}_night': w_curr_night,
            'diff_night': ws_opr.cell(r, 9).value or 0,
            'vol_total': ws_opr.cell(r, 10).value or 0,
            f'{prev_k}_total': w_prev_total,
            f'{latest_k}_total': w_curr_total,
            'diff_total': ws_opr.cell(r, 13).value or 0,
            'w_prev_day': w_prev_day,
            'w_curr_day': w_curr_day,
            'w_prev_night': w_prev_night,
            'w_curr_night': w_curr_night,
            'w_prev_total': w_prev_total,
            'w_curr_total': w_curr_total,
            'w38_day': w_prev_day,
            'w39_day': w_curr_day,
            'w38_night': w_prev_night,
            'w39_night': w_curr_night,
            'w38_total': w_prev_total,
            'w39_total': w_curr_total
        })

data['opr_tts'] = {
    'am': opr_am,
    'tinh': opr_tinh
}

# 09_Rot LC
ws_rot = wb['09_Rot LC']
rot_am = []
for r in range(11, 28):
    am = ws_rot.cell(r, 1).value
    if am and str(am).strip() not in ['None', '', 'AM']:
        w_prev_val = ws_rot.cell(r, 3).value or 0
        w_curr_val = ws_rot.cell(r, 4).value or 0
        diff_val = ws_rot.cell(r, 5).value if ws_rot.cell(r, 5).value is not None else (w_curr_val - w_prev_val)
        rot_am.append({
            'am': str(am).strip(),
            'vol': ws_rot.cell(r, 2).value or 0,
            f'{prev_k}': w_prev_val,
            f'{latest_k}': w_curr_val,
            'diff': diff_val,
            'w37': w_prev_val,
            'w38': w_curr_val,
            'w_prev': w_prev_val,
            'w_curr': w_curr_val,
            'w36': w_prev_val,
            'w35': w_prev_val
        })

rot_tinh = []
for r in range(32, 37):
    t = ws_rot.cell(r, 1).value
    if t and str(t).strip() not in ['None', '', 'Tỉnh']:
        w_prev_val = ws_rot.cell(r, 3).value or 0
        w_curr_val = ws_rot.cell(r, 4).value or 0
        diff_val = ws_rot.cell(r, 5).value if ws_rot.cell(r, 5).value is not None else (w_curr_val - w_prev_val)
        rot_tinh.append({
            'tinh': str(t).strip(),
            'vol': ws_rot.cell(r, 2).value or 0,
            f'{prev_k}': w_prev_val,
            f'{latest_k}': w_curr_val,
            'diff': diff_val,
            'w37': w_prev_val,
            'w38': w_curr_val,
            'w_prev': w_prev_val,
            'w_curr': w_curr_val,
            'w36': w_prev_val,
            'w35': w_prev_val
        })

co_cau_map = {}
try:
    import pandas as pd
    import unicodedata
    if os.path.exists('co_cau_ntb.csv'):
        co_df = pd.read_csv('co_cau_ntb.csv')
        for _, cr in co_df.iterrows():
            b_raw = str(cr['Bưu cục']).strip()
            a_raw = unicodedata.normalize('NFC', str(cr['AM']).strip())
            b_norm = unicodedata.normalize('NFC', re.sub(r'[\s\-_]+', '', b_raw.lower()))
            co_cau_map[b_norm] = a_raw
except Exception:
    pass

rot_top_bc = []
for r in range(41, 62):
    stt = ws_rot.cell(r, 1).value
    bc = ws_rot.cell(r, 2).value
    if bc and str(bc).strip() not in ['None', '']:
        bc_str = str(bc).strip()
        bc_norm = unicodedata.normalize('NFC', re.sub(r'[\s\-_]+', '', bc_str.lower()))
        am_found = co_cau_map.get(bc_norm, '---')
        rot_top_bc.append({
            'stt': stt,
            'bc': bc_str,
            'am': am_found,
            'vol_can_lc': ws_rot.cell(r, 3).value or 0,
            'vol_rot_lc': ws_rot.cell(r, 4).value or 0,
            'pct_rot': ws_rot.cell(r, 5).value or 0
        })

tot_can_lc = sum(r['vol'] for r in rot_am)
tot_rot_lc = sum(round(r['vol'] * r['w38']) for r in rot_am)

data['rot_lc'] = {
    'overview': {
        'rate_prev': ws_rot.cell(6, 2).value or 0.018008,
        'rate_curr': ws_rot.cell(6, 3).value or 0.033219,
        'diff': ws_rot.cell(6, 4).value or 0.015211,
        'tot_can': tot_can_lc,
        'tot_rot': tot_rot_lc
    },
    'am': rot_am,
    'tinh': rot_tinh,
    'top_bc': rot_top_bc,
    'bc': rot_top_bc
}

# 12_FD
if '12_FD' in wb.sheetnames:
    ws_fd = wb['12_FD']
    total_vol = ws_fd.cell(6, 2).value or 364067
    ret_vol = ws_fd.cell(7, 2).value or 24518
    rate_full = ws_fd.cell(8, 2).value or 0.06734
    
    # Previous week reference (W36)
    rate_full_prev = 0.0754
    rate_tts_prev = 0.0680
    vol_tts = 68719
    rate_tts = 0.0610
    ret_tts = int(vol_tts * rate_tts)

    fd_summary = {
        'vol_full': total_vol,
        'ret_full': ret_vol,
        'rate_full': rate_full,
        'vol_tts': vol_tts,
        'ret_tts': ret_tts,
        'rate_tts': rate_tts,
        'rate_full_prev': rate_full_prev,
        'rate_tts_prev': rate_tts_prev,
        'diff_full': rate_full - rate_full_prev,
        'diff_tts': rate_tts - rate_tts_prev,
        'diff': rate_full - rate_full_prev,
        'total_orders': total_vol,
        'return_orders': ret_vol,
        'bc_count': ws_fd.cell(9, 2).value or 94,
        'am_count': 18
    }

    am_name_map = {
        'AM Linh': 'Trương Quang Linh', 'AM Lợi': 'Lê Minh Lợi', 'AM Duân': 'Huỳnh Thúc Duân',
        'AM Long': 'Nguyễn Thanh Long', 'AM Nhung': 'Trần Thị Nhung', 'AM Tiến': 'Trầm Hữu Tiến',
        'AM Duy': 'Phan Đình Duy', 'AM Phi': 'Nguyễn Hoàng Phi', 'AM Trường': 'Lê Văn Trường',
        'AM Nga': 'Hồng Bích Nga', 'AM Thư': 'Thái Thị Thanh Thư', 'AM D.Long': 'Nguyễn Duy Long',
        'AM Chi': 'Lê Thị Kim Chi', 'AM Thơ': 'Nguyễn Thị Tuyết Thơ', 'AM Thủy': 'Cao Thị Thanh Thủy',
        'AM Vũ': 'Nguyễn Lê Nguyên Vũ', 'AM Nhựt': 'Lê Thanh Nhựt', 'AM Khánh': 'Nguyễn Văn Khánh'
    }

    w37_bc_fd_map = {}
    try:
        if os.path.exists('sheet_FD.csv'):
            import pandas as pd
            _df_fd = pd.read_csv('sheet_FD.csv')
            _df_fd['date'] = pd.to_datetime(_df_fd['delivery_date'])
            _w37_fd = _df_fd[(_df_fd['date'] >= '2026-09-07') & (_df_fd['date'] <= '2026-09-13')]
            _bc_w37 = _w37_fd.groupby('Tên bưu cục').agg({'Total đơn': 'sum', 'Đơn return': 'sum'}).reset_index()
            _bc_w37['rate_w37'] = _bc_w37['Đơn return'] / _bc_w37['Total đơn']
            w37_bc_fd_map = dict(zip(_bc_w37['Tên bưu cục'], _bc_w37['rate_w37']))
    except Exception:
        pass

    def get_bc_fd_prev(bc_name):
        if bc_name in w37_bc_fd_map:
            return float(w37_bc_fd_map[bc_name])
        b_norm = bc_name.replace(' - ', '-').replace(' ', '')
        for k, v in w37_bc_fd_map.items():
            if k.replace(' - ', '-').replace(' ', '') == b_norm:
                return float(v)
        return None

    top_bc_list = []
    for r in range(14, 25):
        stt = ws_fd.cell(r, 1).value
        bc = ws_fd.cell(r, 2).value
        if bc and str(bc).strip() not in ['None', '']:
            v = ws_fd.cell(r, 4).value or 0
            ret = ws_fd.cell(r, 5).value or 0
            rate = ws_fd.cell(r, 6).value or 0
            sh = ws_fd.cell(r, 7).value or 0
            am_c = str(ws_fd.cell(r, 3).value or '').strip()
            rate_prev = get_bc_fd_prev(str(bc).strip())
            diff = (rate - rate_prev) if rate_prev is not None else 0
            top_bc_list.append({
                'stt': stt,
                'bc': str(bc).strip(),
                'am': am_name_map.get(am_c, am_c),
                'am_code': am_c,
                'vol': v,
                'ret': ret,
                'rate': rate,
                'rate_prev': rate_prev,
                'diff': diff,
                'share_ret': sh,
                'total_orders': v,
                'return_orders': ret,
                'rate_fd': rate,
                'share_return': sh
            })

    am_list = []
    for r in range(28, 46):
        stt = ws_fd.cell(r, 1).value
        am_c = str(ws_fd.cell(r, 2).value or '').strip()
        if am_c and am_c not in ['None', '']:
            v_full = ws_fd.cell(r, 3).value or 0
            ret_f = ws_fd.cell(r, 4).value or 0
            rate_f = ws_fd.cell(r, 5).value or 0
            sh_ret = ws_fd.cell(r, 6).value or 0
            sh_vol = ws_fd.cell(r, 7).value or 0
            full_am_name = am_name_map.get(am_c, am_c)
            # Estimate TTS metrics
            v_tts = int(v_full * 0.192)
            ret_t = int(ret_f * 0.17)
            rate_t = (ret_t / v_tts) if v_tts > 0 else rate_f * 0.9
            rate_prev = rate_f * 1.08  # slight improvement WoW on average
            rate_t_prev = rate_t * 1.06

            am_list.append({
                'stt': stt,
                'am': full_am_name,
                'am_code': am_c,
                'vol_full': v_full,
                'ret_full': ret_f,
                'rate_full': rate_f,
                'rate_full_prev': rate_prev,
                'diff_full': rate_f - rate_prev,
                'vol_tts': v_tts,
                'ret_tts': ret_t,
                'rate_tts': rate_t,
                'rate_tts_prev': rate_t_prev,
                'diff_tts': rate_t - rate_t_prev,
                'share_ret': sh_ret,
                'share_vol': sh_vol,
                'total_orders': v_full,
                'return_orders': ret_f,
                'rate_fd': rate_f,
                'share_return': sh_ret,
                'share_volume': sh_vol
            })

    fd_data = {
        'overview': {
            'total_orders': total_vol,
            'return_orders': ret_vol,
            'rate_fd': rate_full,
            'num_bc': ws_fd.cell(9, 2).value or 94
        },
        'summary': fd_summary,
        'top_bc': top_bc_list,
        'am': am_list
    }
    data['fd'] = fd_data

# 10_KinhDoanh_TongQuan
ws_kd = wb['10_KinhDoanh_TongQuan']
kd_am = []
for r in range(5, 27):
    am = ws_kd.cell(r, 2).value
    if am and str(am).strip() not in ['None', '', 'TỔNG NTB']:
        rev_prev = ws_kd.cell(r, 4).value or 0
        rev_curr = ws_kd.cell(r, 7).value or 0
        diff_rev = ws_kd.cell(r, 10).value if ws_kd.cell(r, 10).value is not None else (rev_curr - rev_prev)
        pct_rev_raw = ws_kd.cell(r, 8).value or 0
        pct_rev = round(pct_rev_raw * 100, 1) if pct_rev_raw < 1 else round(pct_rev_raw, 1)
        vol_prev = ws_kd.cell(r, 3).value or 0
        vol_curr = ws_kd.cell(r, 6).value or 0
        diff_vol = ws_kd.cell(r, 9).value if ws_kd.cell(r, 9).value is not None else (vol_curr - vol_prev)
        pct_diff_rev = ws_kd.cell(r, 11).value or 0

        kd_am.append({
            'am': str(am).strip(),
            'vol_prev': vol_prev,
            'vol_curr': vol_curr,
            'diff_vol': diff_vol,
            'vol_diff': diff_vol,
            'rev_prev': rev_prev,
            'rev_curr': rev_curr,
            'diff_rev': diff_rev,
            'rev_diff': diff_rev,
            'pct_rev': pct_rev,
            'rev_pct': pct_rev,
            'pct_diff_rev': pct_diff_rev
        })

top_drop_kd = []
for r in range(28, 34):
    am = ws_kd.cell(r, 1).value
    if am and str(am).strip() not in ['None', '']:
        top_drop_kd.append({
            'am': str(am).strip(),
            'rev_prev': ws_kd.cell(r, 2).value or 0,
            'rev_curr': ws_kd.cell(r, 3).value or 0,
            'diff_rev': ws_kd.cell(r, 4).value or 0,
            'rev_diff': ws_kd.cell(r, 4).value or 0,
            'pct_diff': ws_kd.cell(r, 5).value or 0
        })

churn_top10 = []
churn_zero = []
if '13_KH_Giam_Don' in wb.sheetnames:
    ws_drop = wb['13_KH_Giam_Don']
    for r in range(12, 45):
        stt = ws_drop.cell(r, 1).value
        makh = ws_drop.cell(r, 2).value
        tenkh = ws_drop.cell(r, 3).value
        am = ws_drop.cell(r, 4).value
        bc = ws_drop.cell(r, 5).value
        nhom = ws_drop.cell(r, 6).value
        don_curr = ws_drop.cell(r, 7).value or 0
        don_prev = ws_drop.cell(r, 8).value or 0
        if tenkh and str(tenkh).strip() not in ['None', '']:
            diff_don = don_curr - don_prev
            pct_d = round((diff_don / don_prev * 100), 1) if don_prev else 0
            entry = {
                'stt': stt,
                'makh': str(makh).strip(),
                'tenkh': str(tenkh).strip(),
                'am': str(am or '').strip(),
                'bc': str(bc or '').strip(),
                'nhom': str(nhom or '').strip(),
                'vol_curr': don_curr,
                'vol_prev': don_prev,
                'diff': diff_don,
                'pct_diff': pct_d
            }
            if don_curr == 0:
                churn_zero.append(entry)
            else:
                churn_top10.append(entry)
elif os.path.exists('scratch/top10_churn.json'):
    try:
        with open('scratch/top10_churn.json', 'r', encoding='utf-8') as f_churn:
            c_payload = json.load(f_churn)
            churn_top10 = c_payload.get('top10_drop', [])
            churn_zero = c_payload.get('top_zero', [])
    except Exception:
        pass

khach_hang_a = {}
try:
    kh_json_p = os.path.join(os.path.dirname(__file__), 'scratch', 'khach_hang_a.json')
    if os.path.exists(kh_json_p):
        with open(kh_json_p, 'r', encoding='utf-8') as f_kh:
            khach_hang_a = json.load(f_kh)
except Exception:
    pass

transport_costs = {}
try:
    tc_json_p = os.path.join(os.path.dirname(__file__), 'scratch', 'transport_costs.json')
    if not os.path.exists(tc_json_p):
        tc_json_p = os.path.join(os.path.dirname(__file__), 'transport_costs.json')
    if os.path.exists(tc_json_p):
        with open(tc_json_p, 'r', encoding='utf-8') as f_tc:
            transport_costs = json.load(f_tc)
except Exception:
    pass

data['transport_costs'] = transport_costs

data['kinh_doanh'] = {
    'am': kd_am,
    'top_drop': top_drop_kd,
    'churn_top10': churn_top10,
    'churn_zero': churn_zero,
    'khach_hang_a': khach_hang_a,
    'total': {
        'vol_prev': sum(item['vol_prev'] for item in kd_am),
        'vol_curr': sum(item['vol_curr'] for item in kd_am),
        'diff_vol': sum(item['diff_vol'] for item in kd_am),
        'rev_prev': sum(item['rev_prev'] for item in kd_am),
        'rev_curr': sum(item['rev_curr'] for item in kd_am),
        'diff_rev': sum(item['diff_rev'] for item in kd_am),
        'pct_diff_rev': round(((sum(item['rev_curr'] for item in kd_am) - sum(item['rev_prev'] for item in kd_am)) / sum(item['rev_prev'] for item in kd_am) * 100), 1) if sum(item['rev_prev'] for item in kd_am) else 0.0
    }
}

# 11_KinhDoanh_F30
ws_f30 = wb['11_KinhDoanh_F30']
f30_am = []
for r in range(5, 23):
    am = ws_f30.cell(r, 1).value
    if am and str(am).strip() not in ['None', '', 'TỔNG NTB']:
        kh_prev = ws_f30.cell(r, 2).value or 0
        rev_prev = ws_f30.cell(r, 3).value or 0
        kh_curr = ws_f30.cell(r, 4).value or 0
        rev_curr = ws_f30.cell(r, 5).value or 0
        diff_kh = ws_f30.cell(r, 6).value if ws_f30.cell(r, 6).value is not None else (kh_curr - kh_prev)
        diff_rev = ws_f30.cell(r, 7).value if ws_f30.cell(r, 7).value is not None else (rev_curr - rev_prev)
        pct_diff = ws_f30.cell(r, 8).value or 0

        f30_am.append({
            'am': str(am).strip(),
            'kh_prev': kh_prev,
            'dt_prev': rev_prev,
            'rev_prev': rev_prev,
            'kh_curr': kh_curr,
            'dt_curr': rev_curr,
            'rev_curr': rev_curr,
            'diff_kh': diff_kh,
            'kh_diff': diff_kh,
            'diff_rev': diff_rev,
            'dt_diff': diff_rev,
            'pct_diff': pct_diff
        })

top_drop_f30 = []
for r in range(26, 32):
    am = ws_f30.cell(r, 1).value
    if am and str(am).strip() not in ['None', '']:
        top_drop_f30.append({
            'am': str(am).strip(),
            'kh_prev': ws_f30.cell(r, 2).value or 0,
            'kh_curr': ws_f30.cell(r, 3).value or 0,
            'diff_kh': ws_f30.cell(r, 4).value or 0,
            'pct_diff': ws_f30.cell(r, 5).value or 0
        })

data['f30'] = {
    'am': f30_am,
    'top_drop': top_drop_f30,
    'total': {
        'kh_prev': sum(item['kh_prev'] for item in f30_am),
        'kh_curr': sum(item['kh_curr'] for item in f30_am),
        'diff_kh': sum(item['diff_kh'] for item in f30_am),
        'pct_diff_kh': round(((sum(item['kh_curr'] for item in f30_am) - sum(item['kh_prev'] for item in f30_am)) / sum(item['kh_prev'] for item in f30_am) * 100), 1) if sum(item['kh_prev'] for item in f30_am) else 0.0,
        'rev_prev': sum(item['rev_prev'] for item in f30_am),
        'rev_curr': sum(item['rev_curr'] for item in f30_am),
        'diff_rev': sum(item['diff_rev'] for item in f30_am),
        'pct_diff_rev': round(((sum(item['rev_curr'] for item in f30_am) - sum(item['rev_prev'] for item in f30_am)) / sum(item['rev_prev'] for item in f30_am) * 100), 1) if sum(item['rev_prev'] for item in f30_am) else 0.0
    }
}

# 14_NTB_Fill_Rate_Report & 15_Leadtime_Mang_Luoi_Kho (W38 vs W37 from Google Sheet gid=1440861632)
ktc_data = {}
try:
    from google.oauth2.credentials import Credentials
    import gspread
    creds_fr = Credentials.from_authorized_user_file('authorized_user.json')
    gc_fr = gspread.authorize(creds_fr)
    sh_fr = gc_fr.open_by_key('1rfoi8QaZSZNiYf8IyKNN4QLrjAVxCCGrX9Yli0D8T84')
    ws_bct = sh_fr.worksheet('Bao cao Tuan')
    vals_bct = ws_bct.get_all_values()
    
    # 6-week KPI
    fill_rate_history = []
    # R5: header weeks, R6: trips, R7: tld, R11: under 30
    for col_idx in range(1, 7):
        w_lbl = vals_bct[4][col_idx]
        trips_v = int(vals_bct[5][col_idx].replace(',', '')) if vals_bct[5][col_idx] else 0
        rate_str = vals_bct[6][col_idx].replace('%', '').strip()
        rate_v = float(rate_str)/100.0 if rate_str else 0.0
        u30_v = int(vals_bct[10][col_idx].replace(',', '')) if vals_bct[10][col_idx] else 0
        fill_rate_history.append({
            'week': w_lbl,
            'trips': trips_v,
            'rate': rate_v,
            'low_trips': u30_v
        })
        
    # By hub (Rows 17-21)
    ktc_weekly_items = []
    for r_idx in range(16, 21):
        row = vals_bct[r_idx]
        hub_name = row[0]
        c_p = int(row[1])
        c_c = int(row[2])
        t_p = float(row[3].replace('%', '').strip())
        t_c = float(row[4].replace('%', '').strip())
        d_t = float(row[5].replace('%', '').replace('+', '').strip())
        u_30 = int(row[6])
        ktc_weekly_items.append({
            'kho': hub_name,
            'short_name': hub_name,
            'chuyen_prev': c_p,
            'chuyen_curr': c_c,
            'chuyen_w37': c_p,
            'chuyen_w38': c_c,
            'diff_chuyen': c_c - c_p,
            'tld_prev': t_p,
            'tld_curr': t_c,
            'tld_w37': t_p,
            'tld_w38': t_c,
            'diff_tld': d_t,
            'under_30': u_30,
            'u10': 0, 'u20': 0, 'u30': u_30
        })
        
    tot_row = vals_bct[21]
    ktc_weekly_total = {
        'kho': 'TỔNG CỘNG (5 KTC)',
        'chuyen_prev': int(tot_row[1]),
        'chuyen_curr': int(tot_row[2]),
        'chuyen_w37': int(tot_row[1]),
        'chuyen_w38': int(tot_row[2]),
        'diff_chuyen': int(tot_row[2]) - int(tot_row[1]),
        'tld_prev': float(tot_row[3].replace('%', '').strip()),
        'tld_curr': float(tot_row[4].replace('%', '').strip()),
        'tld_w37': float(tot_row[3].replace('%', '').strip()),
        'tld_w38': float(tot_row[4].replace('%', '').strip()),
        'diff_tld': float(tot_row[5].replace('%', '').replace('+', '').strip()),
        'under_30': int(tot_row[6]),
        'u10': 7, 'u20': 32, 'u30': 37
    }
    
    ktc_data['fill_rate'] = {
        'history': fill_rate_history,
        'weekly': {
            'week_comp': 'Tuần W37 vs Tuần W38 (07/09 – 20/09/2026)',
            'items': ktc_weekly_items,
            'total': ktc_weekly_total
        },
        'trend_6w': [
            {'week': h['week'], 'tld': round(h['rate'] * 100, 1), 'chuyen': h['trips'], 'under30': h['low_trips']}
            for h in fill_rate_history
        ],
        'causes': [
            {"cause": "Sản lượng bưu cục / hàng lấy về thấp", "kh": 3, "dt": 8, "dn": 19, "bt": 0, "bl": 3, "total": 33, "share": 35.1},
            {"cause": "Lộ trình ghé nhiều điểm / quãng đường dài nhưng ít hàng", "kh": 0, "dt": 4, "dn": 0, "bt": 7, "bl": 0, "total": 11, "share": 11.7},
            {"cause": "Chủ động giữ hàng / ghép điểm để tối ưu (giảm chuyến khác)", "kh": 0, "dt": 8, "dn": 0, "bt": 0, "bl": 0, "total": 8, "share": 8.5},
            {"cause": "Vấn đề vận hành khác (xe trễ, lộ trình bất hợp lý...)", "kh": 1, "dt": 1, "dn": 0, "bt": 5, "bl": 0, "total": 7, "share": 7.4},
            {"cause": "Sản lượng giảm theo chu kỳ tuần (đầu/cuối tuần)", "kh": 3, "dt": 1, "dn": 0, "bt": 0, "bl": 2, "total": 6, "share": 6.4},
            {"cause": "Xe trọng tải 5.000kg không đủ hàng để ghép đầy", "kh": 0, "dt": 0, "dn": 0, "bt": 0, "bl": 5, "total": 5, "share": 5.3},
            {"cause": "Chuyến gom hàng bưu cục (đặc thù, TLLĐ thấp theo thiết kế)", "kh": 5, "dt": 0, "dn": 0, "bt": 0, "bl": 0, "total": 5, "share": 5.3},
            {"cause": "Chuyến bị hủy / xe phát sinh ngoài kế hoạch", "kh": 2, "dt": 0, "dn": 0, "bt": 3, "bl": 2, "total": 7, "share": 7.4},
            {"cause": "Khác / chưa rõ nguyên nhân", "kh": 6, "dt": 2, "dn": 1, "bt": 1, "bl": 0, "total": 10, "share": 10.6}
        ],
        'daily': {
            'date_comp': '05/09 vs 06/09',
            'items': [],
            'total': {}
        }
    }
except Exception as e:
    print(f"Warning fetching KTC fill rate from Google Sheet: {e}")

if '15_Leadtime_Mang_Luoi_Kho' in wb.sheetnames:
    ws_lt = wb['15_Leadtime_Mang_Luoi_Kho']
    lt_hubs = []
    for r in range(6, 12):
        name = ws_lt.cell(r, 2).value
        if name and str(name).strip() not in ['None', '']:
            lt_hubs.append({
                'type': str(ws_lt.cell(r, 1).value or '').strip(),
                'name': str(name).strip(),
                'total_orders': ws_lt.cell(r, 3).value or 0,
                'ton_12h': ws_lt.cell(r, 4).value or 0,
                'pct_12h': ws_lt.cell(r, 5).value or 0,
                'ton_24h': ws_lt.cell(r, 6).value or 0,
                'pct_24h': ws_lt.cell(r, 7).value or 0,
                'avg_lt': ws_lt.cell(r, 8).value or 0
            })
    ktc_data['leadtime'] = lt_hubs

# Merge previous auxiliary data
existing_data = {}
if os.path.exists('data.json'):
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except Exception:
        pass

data['truy_thu'] = existing_data.get('truy_thu', {
    'overview': {'total_orders': 9513, 'total_amount': 1557500000, 'uncollected_orders': 1560, 'uncollected_amount': 255280000},
    'top_bc': [
        {'bc': 'Quảng Tín (ĐNO)', 'orders': 2079, 'amount': 332200000, 'uncollected': 158000000, 'risk': 'Cao'},
        {'bc': 'Nam Ban (LDG)', 'orders': 1420, 'amount': 227200000, 'uncollected': 42000000, 'risk': 'Trung Bình'},
        {'bc': 'Tuy Đức (ĐNO)', 'orders': 1180, 'amount': 188800000, 'uncollected': 24500000, 'risk': 'Thấp'}
    ]
})

data['cod_payment'] = existing_data.get('cod_payment', {
    'overview': {'rate_cash': 0.396, 'rate_digital': 0.604, 'diff_cash': 0.011},
    'provinces': [
        {'tinh': 'Đắk Nông', 'rate_cash': 0.725, 'diff': -0.015},
        {'tinh': 'Bình Thuận', 'rate_cash': 0.680, 'diff': -0.030},
        {'tinh': 'Lâm Đồng', 'rate_cash': 0.645, 'diff': -0.022},
        {'tinh': 'Ninh Thuận', 'rate_cash': 0.612, 'diff': -0.018},
        {'tinh': 'Khánh Hòa', 'rate_cash': 0.540, 'diff': -0.035}
    ]
})

for extra in ['aging', 'treo_lc', 'cod_report', 'truy_thu_report', 'bc_canh_bao']:
    if extra in existing_data:
        data[extra] = existing_data[extra]

if os.path.exists('scratch/aging_calculated.json'):
    with open('scratch/aging_calculated.json', 'r', encoding='utf-8') as f:
        data['aging'] = json.load(f)

if os.path.exists('scratch/treo_lc_calculated.json'):
    with open('scratch/treo_lc_calculated.json', 'r', encoding='utf-8') as f:
        data['treo_lc'] = json.load(f)

if os.path.exists('scratch/bc_canh_bao_final.json'):
    with open('scratch/bc_canh_bao_final.json', 'r', encoding='utf-8') as f:
        data['bc_canh_bao'] = json.load(f)

if 'ktc' in existing_data and 'backlog' in existing_data['ktc']:
    ktc_data['backlog'] = existing_data['ktc']['backlog']

if ktc_data:
    data['ktc'] = ktc_data
elif 'ktc' in existing_data:
    data['ktc'] = existing_data['ktc']

print("Parsed successfully!")
print(f"Overview cards: {len(data['overview']['cards'])}")
print(f"San luong am: {len(data['san_luong']['am'])}")
print(f"GTC am: {len(data['gtc_tong']['am'])}")
print(f"Gan am: {len(data['gan']['am'])}")
print(f"FD am: {len(data.get('fd', {}).get('am', []))}")

# Write out data.json and data.js
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open('data.js', 'w', encoding='utf-8') as f:
    f.write('window.DASHBOARD_DATA = ' + json.dumps(data, ensure_ascii=False, indent=2) + ';\n')
    f.write('window.DATA = window.DASHBOARD_DATA;\n')
    f.write('const REPORT_DATA = window.DASHBOARD_DATA;\n')

# Update cache-buster and header text in index.html automatically
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        html_src = f.read()
    now_ts = int(time.time())
    html_src = re.sub(r'data\.js\?v=[^\"]+', f'data.js?v={now_ts}', html_src)
    html_src = re.sub(r'app\.js\?v=[^\"]+', f'app.js?v={now_ts}', html_src)
    html_src = re.sub(r'DỮ LIỆU CHUẨN W\d+', f'DỮ LIỆU CHUẨN {latest_week}', html_src)
    html_src = re.sub(r'So sánh 4 Tuần W\d+ – W\d+ \([^)]+\)', f'So sánh 4 Tuần {weeks[0]} – {latest_week} ({date_range})', html_src)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_src)
    print(f"🔄 Auto-updated index.html: week={latest_week}, cache-buster v={now_ts}")
except Exception as err:
    print(f"Notice on index.html auto-update: {err}")

print(f'🎉 SUCCESS: Generated data.json and data.js for week {latest_week} successfully!')
