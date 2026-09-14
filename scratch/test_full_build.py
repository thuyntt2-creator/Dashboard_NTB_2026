import openpyxl
import json
import os
import sys
import glob
import re

sys.stdout.reconfigure(encoding='utf-8')

def find_latest_excel():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(root_dir) == 'scratch':
        root_dir = os.path.dirname(root_dir)
    
    candidates = []
    candidates.extend(glob.glob(os.path.join(root_dir, 'BaoCao_Tuan_NTB_W*.xlsx')))
    candidates.extend(glob.glob(r'C:\Users\lap4all\Downloads\BaoCao_AM_Project_*\BaoCao_AM_Project\output\BaoCao_Tuan_NTB_W*.xlsx'))
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

    valid_candidates.sort(key=lambda p: (get_week_num(p), os.path.getmtime(p)), reverse=True)
    return valid_candidates[0]

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

date_range_map = {
    'W35': '24/08 - 30/08/2026',
    'W36': '31/08 - 06/09/2026',
    'W37': '07/09 - 13/09/2026',
    'W38': '14/09 - 20/09/2026',
    'W39': '21/09 - 27/09/2026',
}
date_range = date_range_map.get(latest_week, '07/09 - 13/09/2026')

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
                
                # Compatibility fallbacks
                item['w32'] = w_vals[0]
                item['w33'] = w_vals[0]
                item['w34'] = w_vals[0] if weeks[0] == 'W34' else (w_vals[1] if weeks[1] == 'W34' else w_vals[0])
                item['w35'] = w_vals[1] if weeks[1] == 'W35' else (w_vals[2] if weeks[2] == 'W35' else w_vals[1])
                item['w36'] = w_vals[2] if weeks[2] == 'W36' else (w_vals[3] if len(weeks) > 3 and weeks[3] == 'W36' else w_vals[2])
                item['w37'] = w_vals[3] if len(weeks) > 3 and weeks[3] == 'W37' else w_vals[-1]
                items.append(item)
        return items

    am_full = extract_rows(12, 30)
    am_tts = extract_rows(34, 52)
    tinh_full = extract_rows(56, 61)
    tinh_tts = extract_rows(65, 70)

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
            for idx, k in enumerate(w_keys):
                ov[k] = w_vals[idx]
            ov['w32'] = w_vals[0]
            ov['w33'] = w_vals[0]
            ov['w34'] = w_vals[0] if weeks[0] == 'W34' else w_vals[1]
            ov['w35'] = w_vals[1] if weeks[1] == 'W35' else w_vals[2]
            ov['w36'] = w_vals[2] if weeks[2] == 'W36' else w_vals[3]
            ov['w37'] = w_vals[3] if len(weeks) > 3 else w_vals[-1]
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
                for idx, k in enumerate(w_keys):
                    item[k] = w_vals[idx]
                item['w32'] = w_vals[0]
                item['w33'] = w_vals[0]
                item['w34'] = w_vals[0] if weeks[0] == 'W34' else w_vals[1]
                item['w35'] = w_vals[1] if weeks[1] == 'W35' else w_vals[2]
                item['w36'] = w_vals[2] if weeks[2] == 'W36' else w_vals[3]
                item['w37'] = w_vals[3] if len(weeks) > 3 else w_vals[-1]
                items.append(item)
        return items

    am_full = extract_rows(12, 30)
    am_tts = extract_rows(34, 52)
    tinh_full = extract_rows(56, 61)
    tinh_tts = extract_rows(65, 70)

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
        for idx, k in enumerate(w_keys):
            row_dict[k] = w_vals[idx]
        row_dict['w32'] = w_vals[0]
        row_dict['w33'] = w_vals[0]
        row_dict['w34'] = w_vals[0] if weeks[0] == 'W34' else w_vals[1]
        row_dict['w35'] = w_vals[1] if weeks[1] == 'W35' else w_vals[2]
        row_dict['w36'] = w_vals[2] if weeks[2] == 'W36' else w_vals[3]
        row_dict['w37'] = w_vals[3] if len(weeks) > 3 else w_vals[-1]
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
insights = []
for r in range(37, 45):
    txt = ws_tq.cell(r, 1).value
    if txt and str(txt).strip():
        c_txt = str(txt).strip().lstrip('•').strip()
        if not c_txt or 'ĐIỂM NỔI BẬT' in c_txt.upper():
            continue
        i_type = 'highlight'
        if 'cải thiện' in c_txt.lower() or 'tăng' in c_txt.lower() or 'cao nhất' in c_txt.lower():
            i_type = 'positive'
        elif 'giảm mạnh' in c_txt.lower() or 'thấp nhất' in c_txt.lower() or 'cần rà soát' in c_txt.lower():
            i_type = 'warning'
        insights.append({'type': i_type, 'text': c_txt})

if not insights:
    insights = [
        {'type': 'highlight', 'text': f'Sản lượng Full hàng {latest_week} đạt {vol_full_curr:,} đơn (tăng {vol_full_diff:,} so với {prev_week}).'},
        {'type': 'positive', 'text': f'%ODR toàn vùng đạt {(odr_full_curr*100):.1f}%, giữ vững phong độ chuẩn ≥92%.'},
        {'type': 'warning', 'text': f'%GTC toàn vùng đạt {(gtc_full_curr*100):.1f}%, cần đẩy mạnh giải phóng tồn kho.'}
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
            {'id': 'cod_tm', 'title': 'Tỷ Lệ COD Tiền Mặt', 'val': 0.396, 'unit': '%', 'diff': 0.011, 'diff_pct': 0.030, 'is_good': False, 'icon': 'banknote'},
            {'id': 'truy_thu', 'title': 'Tổng Cần Truy Thu', 'val': 174663624, 'unit': 'VNĐ', 'diff': -21200000, 'diff_pct': -0.108, 'is_good': True, 'icon': 'shield-alert'}
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
        ov = {
            'indicator': str(ind).strip(),
            'diff': ws_gan.cell(r, 6).value or 0
        }
        for idx, k in enumerate(w_keys):
            ov[k] = w_vals[idx]
        ov['w32'] = w_vals[0]
        ov['w33'] = w_vals[0]
        ov['w34'] = w_vals[0] if weeks[0] == 'W34' else w_vals[1]
        ov['w35'] = w_vals[1] if weeks[1] == 'W35' else w_vals[2]
        ov['w36'] = w_vals[2] if weeks[2] == 'W36' else w_vals[3]
        ov['w37'] = w_vals[3] if len(weeks) > 3 else w_vals[-1]
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
                # Compatibility fallbacks
                'tong_w35': ws_gan.cell(r, 3).value or 0,
                'tong_w36': ws_gan.cell(r, 4).value or 0,
                'ca1ton_w35': ws_gan.cell(r, 6).value or 0,
                'ca1ton_w36': ws_gan.cell(r, 7).value or 0,
                'ca2_w35': ws_gan.cell(r, 9).value or 0,
                'ca2_w36': ws_gan.cell(r, 10).value or 0,
                'tong_w34': ws_gan.cell(r, 3).value or 0,
                'ca1ton_w34': ws_gan.cell(r, 6).value or 0,
                'ca2_w34': ws_gan.cell(r, 9).value or 0
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
            # Compatibility
            'w35_day': w_prev_day,
            'w36_day': w_curr_day,
            'w37_day': w_curr_day,
            'w35_night': w_prev_night,
            'w36_night': w_curr_night,
            'w37_night': w_curr_night,
            'w35_total': w_prev_total,
            'w36_total': w_curr_total,
            'w37_total': w_curr_total,
            'w34_day': w_prev_day,
            'w34_night': w_prev_night,
            'w34_total': w_prev_total
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
            # Compatibility
            'w35_day': w_prev_day,
            'w36_day': w_curr_day,
            'w37_day': w_curr_day,
            'w35_night': w_prev_night,
            'w36_night': w_curr_night,
            'w37_night': w_curr_night,
            'w35_total': w_prev_total,
            'w36_total': w_curr_total,
            'w37_total': w_curr_total,
            'w34_day': w_prev_day,
            'w34_night': w_prev_night,
            'w34_total': w_prev_total
        })

data['opr_tts'] = {
    'am': opr_am,
    'tinh': opr_tinh
}

# 09_Rot LC
ws_rot = wb['09_Rot LC']
rot_am = []
for r in range(11, 30):
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
            'w35': w_prev_val,
            'w36': w_curr_val,
            'w37': w_curr_val,
            'w34': w_prev_val
        })

rot_tinh = []
for r in range(32, 39):
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
            'w35': w_prev_val,
            'w36': w_curr_val,
            'w37': w_curr_val,
            'w34': w_prev_val
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

data['rot_lc'] = {
    'am': rot_am,
    'tinh': rot_tinh,
    'top_bc': rot_top_bc,
    'bc': rot_top_bc
}

# 12_FD
if '12_FD' in wb.sheetnames:
    ws_fd = wb['12_FD']
    fd_data = {
        'overview': {
            'total_orders': ws_fd.cell(6, 2).value or 364067,
            'return_orders': ws_fd.cell(7, 2).value or 24518,
            'rate_fd': ws_fd.cell(8, 2).value or 0.0673,
            'num_bc': ws_fd.cell(9, 2).value or 94
        },
        'top_bc': [],
        'am': []
    }
    for r in range(14, 25):
        stt = ws_fd.cell(r, 1).value
        bc = ws_fd.cell(r, 2).value
        if bc and str(bc).strip() not in ['None', '']:
            fd_data['top_bc'].append({
                'stt': stt,
                'bc': str(bc).strip(),
                'am': str(ws_fd.cell(r, 3).value or '').strip(),
                'total_orders': ws_fd.cell(r, 4).value or 0,
                'return_orders': ws_fd.cell(r, 5).value or 0,
                'rate_fd': ws_fd.cell(r, 6).value or 0,
                'share_return': ws_fd.cell(r, 7).value or 0
            })
    for r in range(28, 48):
        stt = ws_fd.cell(r, 1).value
        am = ws_fd.cell(r, 2).value
        if am and str(am).strip() not in ['None', '']:
            fd_data['am'].append({
                'stt': stt,
                'am': str(am).strip(),
                'total_orders': ws_fd.cell(r, 3).value or 0,
                'return_orders': ws_fd.cell(r, 4).value or 0,
                'rate_fd': ws_fd.cell(r, 5).value or 0,
                'share_return': ws_fd.cell(r, 6).value or 0,
                'share_volume': ws_fd.cell(r, 7).value or 0
            })
    data['fd'] = fd_data
elif os.path.exists('scratch/fd_processed.json'):
    try:
        with open('scratch/fd_processed.json', 'r', encoding='utf-8') as f_fd:
            data['fd'] = json.load(f_fd)
    except Exception:
        pass

# 10_KinhDoanh_TongQuan
ws_kd = wb['10_KinhDoanh_TongQuan']
kd_am = []
for r in range(5, 25):
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
        'pct_diff_rev': ((sum(item['rev_curr'] for item in kd_am) - sum(item['rev_prev'] for item in kd_am)) / sum(item['rev_prev'] for item in kd_am)) if sum(item['rev_prev'] for item in kd_am) else 0
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
        'rev_prev': sum(item['rev_prev'] for item in f30_am),
        'rev_curr': sum(item['rev_curr'] for item in f30_am),
        'diff_rev': sum(item['diff_rev'] for item in f30_am),
        'pct_diff_rev': ((sum(item['rev_curr'] for item in f30_am) - sum(item['rev_prev'] for item in f30_am)) / sum(item['rev_prev'] for item in f30_am)) if sum(item['rev_prev'] for item in f30_am) else 0
    }
}

# 14_NTB_Fill_Rate_Report & 15_Leadtime_Mang_Luoi_Kho
ktc_data = {}
if '14_NTB_Fill_Rate_Report' in wb.sheetnames:
    ws_fr = wb['14_NTB_Fill_Rate_Report']
    fill_rate_history = []
    for c in range(2, 8):
        week_label = ws_fr.cell(5, c).value
        if week_label:
            fill_rate_history.append({
                'week': str(week_label).strip(),
                'trips': ws_fr.cell(6, c).value or 0,
                'rate': ws_fr.cell(7, c).value or 0,
                'low_trips': ws_fr.cell(11, c).value or 0
            })
    
    ktc_by_hub = []
    for r in range(16, 25):
        hub_name = ws_fr.cell(r, 1).value
        if hub_name and str(hub_name).strip() not in ['None', '']:
            ktc_by_hub.append({
                'hub': str(hub_name).strip(),
                'trips_prev': ws_fr.cell(r, 2).value or 0,
                'trips_curr': ws_fr.cell(r, 3).value or 0,
                'rate_prev': ws_fr.cell(r, 4).value or 0,
                'rate_curr': ws_fr.cell(r, 5).value or 0,
                'diff_rate': ws_fr.cell(r, 6).value or 0,
                'low_trips': ws_fr.cell(r, 7).value or 0
            })
    ktc_data['fill_rate'] = {
        'history': fill_rate_history,
        'by_hub': ktc_by_hub
    }

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

for extra in ['aging', 'treo_lc', 'cod_report', 'truy_thu_report']:
    if extra in existing_data:
        data[extra] = existing_data[extra]

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
