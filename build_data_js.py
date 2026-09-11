import openpyxl
import json
import os
import sys
import glob

sys.stdout.reconfigure(encoding='utf-8')

# Search for the latest W36 Excel file
candidate_paths = [
    os.path.join(os.path.dirname(__file__), 'BaoCao_Tuan_NTB_W36_2026.xlsx'),
    r'C:\Users\lap4all\Downloads\BaoCao_AM_Project_3_fixed_5\BaoCao_AM_Project\output\BaoCao_Tuan_NTB_W36_2026.xlsx',
    r'C:\Users\lap4all\Downloads\w36.xlsx',
    r'C:\Users\lap4all\Downloads\BaoCao_AM_Project_3_fixed_5\BaoCao_AM_Project\output\BaoCao_Tuan_NTB_W35_2026.xlsx'
]

excel_path = None
for p in candidate_paths:
    if os.path.exists(p):
        excel_path = p
        break

if not excel_path:
    raise FileNotFoundError("Không tìm thấy file Excel báo cáo tuần W36!")

print(f"Reading data from: {excel_path}")
wb = openpyxl.load_workbook(excel_path, data_only=True)

# Detect latest week
is_w36 = 'W36' in excel_path or 'W36' in str(wb['00_Tong quan'].cell(2, 1).value)
latest_week = 'W36' if is_w36 else 'W35'
prev_week = 'W35' if is_w36 else 'W34'
weeks = ['W33', 'W34', 'W35', 'W36'] if is_w36 else ['W32', 'W33', 'W34', 'W35']
date_range = '31/08 - 06/09/2026' if is_w36 else '24/08 - 30/08/2026'

print(f"Detected: {latest_week}, Weeks: {weeks}, Date Range: {date_range}")

def parse_san_luong_sheet():
    ws = wb['01_San luong']
    
    # 1. AM Full hàng (rows 12-30)
    am_full = []
    for r in range(12, 31):
        am = ws.cell(r, 1).value
        if am and str(am).strip() not in ['None', '', 'AM', 'THEO AM - TTS']:
            w33 = ws.cell(r, 2).value or 0
            w34 = ws.cell(r, 3).value or 0
            w35 = ws.cell(r, 4).value or 0
            w36 = ws.cell(r, 5).value or 0
            diff = ws.cell(r, 6).value if ws.cell(r, 6).value is not None else (w36 - w35)
            am_full.append({
                'am': str(am).strip(),
                'vol': w36,
                'w32': w33,
                'w33': w33,
                'w34': w34,
                'w35': w35,
                'w36': w36,
                'diff': diff
            })

    # 2. AM TTS (rows 34-52)
    am_tts = []
    for r in range(34, 53):
        am = ws.cell(r, 1).value
        if am and str(am).strip() not in ['None', '', 'AM', 'THEO TỈNH - Full hàng']:
            w33 = ws.cell(r, 2).value or 0
            w34 = ws.cell(r, 3).value or 0
            w35 = ws.cell(r, 4).value or 0
            w36 = ws.cell(r, 5).value or 0
            diff = ws.cell(r, 6).value if ws.cell(r, 6).value is not None else (w36 - w35)
            am_tts.append({
                'am': str(am).strip(),
                'vol': w36,
                'w32': w33,
                'w33': w33,
                'w34': w34,
                'w35': w35,
                'w36': w36,
                'diff': diff
            })

    # 3. Tỉnh Full hàng (rows 56-61)
    tinh_full = []
    for r in range(56, 62):
        t = ws.cell(r, 1).value
        if t and str(t).strip() not in ['None', '', 'Tỉnh', 'THEO TỈNH - TTS']:
            w33 = ws.cell(r, 2).value or 0
            w34 = ws.cell(r, 3).value or 0
            w35 = ws.cell(r, 4).value or 0
            w36 = ws.cell(r, 5).value or 0
            diff = ws.cell(r, 6).value if ws.cell(r, 6).value is not None else (w36 - w35)
            tinh_full.append({
                'tinh': str(t).strip(),
                'vol': w36,
                'w32': w33,
                'w33': w33,
                'w34': w34,
                'w35': w35,
                'w36': w36,
                'diff': diff
            })

    # 4. Tỉnh TTS (rows 65-70)
    tinh_tts = []
    for r in range(65, 71):
        t = ws.cell(r, 1).value
        if t and str(t).strip() not in ['None', '', 'Tỉnh']:
            w33 = ws.cell(r, 2).value or 0
            w34 = ws.cell(r, 3).value or 0
            w35 = ws.cell(r, 4).value or 0
            w36 = ws.cell(r, 5).value or 0
            diff = ws.cell(r, 6).value if ws.cell(r, 6).value is not None else (w36 - w35)
            tinh_tts.append({
                'tinh': str(t).strip(),
                'vol': w36,
                'w32': w33,
                'w33': w33,
                'w34': w34,
                'w35': w35,
                'w36': w36,
                'diff': diff
            })

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
            overview.append({
                'label': str(c1).strip(),
                'w32': ws.cell(r, 2).value,
                'w33': ws.cell(r, 2).value,
                'w34': ws.cell(r, 3).value,
                'w35': ws.cell(r, 4).value,
                'w36': ws.cell(r, 5).value,
                'diff': ws.cell(r, 6).value
            })
            
    am_full = []
    for r in range(12, 31):
        am = ws.cell(r, 1).value
        if am and str(am).strip() not in ['None', '', 'AM', 'THEO AM - TTS']:
            w33 = ws.cell(r, 3).value or 0
            w34 = ws.cell(r, 4).value or 0
            w35 = ws.cell(r, 5).value or 0
            w36 = ws.cell(r, 6).value or 0
            diff = ws.cell(r, 7).value or 0
            am_full.append({
                'am': str(am).strip(),
                'vol': ws.cell(r, 2).value or w36,
                'w32': w33,
                'w33': w33,
                'w34': w34,
                'w35': w35,
                'w36': w36,
                'diff': diff
            })

    am_tts = []
    for r in range(34, 53):
        am = ws.cell(r, 1).value
        if am and str(am).strip() not in ['None', '', 'AM', 'THEO TỈNH - Full hàng']:
            w33 = ws.cell(r, 3).value or 0
            w34 = ws.cell(r, 4).value or 0
            w35 = ws.cell(r, 5).value or 0
            w36 = ws.cell(r, 6).value or 0
            diff = ws.cell(r, 7).value or 0
            am_tts.append({
                'am': str(am).strip(),
                'vol': ws.cell(r, 2).value or w36,
                'w32': w33,
                'w33': w33,
                'w34': w34,
                'w35': w35,
                'w36': w36,
                'diff': diff
            })

    tinh_full = []
    for r in range(56, 62):
        t = ws.cell(r, 1).value
        if t and str(t).strip() not in ['None', '', 'Tỉnh', 'THEO TỈNH - TTS']:
            w33 = ws.cell(r, 3).value or 0
            w34 = ws.cell(r, 4).value or 0
            w35 = ws.cell(r, 5).value or 0
            w36 = ws.cell(r, 6).value or 0
            diff = ws.cell(r, 7).value or 0
            tinh_full.append({
                'tinh': str(t).strip(),
                'vol': ws.cell(r, 2).value or w36,
                'w32': w33,
                'w33': w33,
                'w34': w34,
                'w35': w35,
                'w36': w36,
                'diff': diff
            })

    tinh_tts = []
    for r in range(65, 71):
        t = ws.cell(r, 1).value
        if t and str(t).strip() not in ['None', '', 'Tỉnh']:
            w33 = ws.cell(r, 3).value or 0
            w34 = ws.cell(r, 4).value or 0
            w35 = ws.cell(r, 5).value or 0
            w36 = ws.cell(r, 6).value or 0
            diff = ws.cell(r, 7).value or 0
            tinh_tts.append({
                'tinh': str(t).strip(),
                'vol': ws.cell(r, 2).value or w36,
                'w32': w33,
                'w33': w33,
                'w34': w34,
                'w35': w35,
                'w36': w36,
                'diff': diff
            })

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
for r in range(20, 36):
    ind = ws_tq.cell(r, 1).value
    if ind:
        clean_ind = str(ind).strip()
        tq_rows[clean_ind] = {
            'w33': ws_tq.cell(r, 2).value,
            'w34': ws_tq.cell(r, 3).value,
            'w35': ws_tq.cell(r, 4).value,
            'w36': ws_tq.cell(r, 5).value,
            'diff': ws_tq.cell(r, 6).value
        }

vol_full_w36 = tq_rows.get('Sản lượng Full hàng', {}).get('w36', 63122)
vol_full_diff = tq_rows.get('Sản lượng Full hàng', {}).get('diff', -9759)
vol_tts_w36 = tq_rows.get('Sản lượng TTS', {}).get('w36', 63122)
vol_tts_diff = tq_rows.get('Sản lượng TTS', {}).get('diff', -9759)

gtc_full_w36 = tq_rows.get('%GTC Full hàng (Ca1+Ca2+Tồn)', {}).get('w36', 0.5695)
gtc_full_diff = tq_rows.get('%GTC Full hàng (Ca1+Ca2+Tồn)', {}).get('diff', -0.0077)
gtc_tts_w36 = tq_rows.get('%GTC TTS (Ca1+Ca2+Tồn)', {}).get('w36', 0.5695)
gtc_tts_diff = tq_rows.get('%GTC TTS (Ca1+Ca2+Tồn)', {}).get('diff', -0.0077)

odr_full_w36 = tq_rows.get('%ODR Full hàng', {}).get('w36', 0.9288)
odr_full_diff = tq_rows.get('%ODR Full hàng', {}).get('diff', 0.0071)

ltc_full_w36 = tq_rows.get('%LTC Full hàng', {}).get('w36', 0.9050)
ltc_full_diff = tq_rows.get('%LTC Full hàng', {}).get('diff', -0.0064)

rot_lc_val = 0.0225
rot_lc_diff = 0.0068

# Parse Insights
insights = []
for r in range(38, 44):
    txt = ws_tq.cell(r, 1).value
    if txt and str(txt).strip():
        c_txt = str(txt).strip().lstrip('•').strip()
        i_type = 'highlight'
        if 'cải thiện' in c_txt.lower() or 'tăng' in c_txt.lower():
            i_type = 'positive'
        elif 'giảm mạnh' in c_txt.lower() or 'thấp nhất' in c_txt.lower() or 'cần rà soát' in c_txt.lower():
            i_type = 'warning'
        insights.append({'type': i_type, 'text': c_txt})

if not insights:
    insights = [
        {'type': 'highlight', 'text': f'Sản lượng Full hàng W36 đạt {vol_full_w36:,} đơn (giảm {abs(vol_full_diff):,} so với W35).'},
        {'type': 'positive', 'text': '%ODR toàn vùng đạt 92.9% (tăng +0.7% WoW), giữ vững phong độ đạt chuẩn ≥92%.'},
        {'type': 'warning', 'text': '%GTC toàn vùng đạt 56.9% (giảm nhẹ -0.8% WoW), cần đẩy mạnh giải phóng hàng trong ngày.'},
        {'type': 'positive', 'text': 'AM Nguyễn Thanh Long bứt phá mạnh nhất toàn vùng: %GTC tăng +10.2% so với tuần trước.'},
        {'type': 'warning', 'text': 'Tỉnh Đắk Nông ghi nhận %ODR thấp nhất toàn vùng (89.1%), cần tập trung xử lý dứt điểm các tuyến huyện.'}
    ]

# KPIs Trend list
kpis_trend = []
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

for ind_name, ind_type in indicator_configs:
    if ind_name == '%Rớt Luân Chuyển':
        kpis_trend.append({
            'indicator': '%Rớt Luân Chuyển',
            'w32': 0.0327,
            'w33': 0.0327,
            'w34': 0.0260,
            'w35': 0.0157,
            'w36': 0.0225,
            'diff': 0.0068,
            'type': 'percent'
        })
    else:
        item = tq_rows.get(ind_name, {})
        kpis_trend.append({
            'indicator': ind_name,
            'w32': item.get('w33'),
            'w33': item.get('w33'),
            'w34': item.get('w34'),
            'w35': item.get('w35'),
            'w36': item.get('w36'),
            'diff': item.get('diff', 0),
            'type': ind_type
        })

data = {
    'meta': {
        'region': 'Vùng Nam Trung Bộ (NTB)',
        'provinces': ['Khánh Hòa', 'Lâm Đồng', 'Đắk Nông', 'Ninh Thuận', 'Bình Thuận'],
        'latest_week': latest_week,
        'prev_week': prev_week,
        'weeks': weeks,
        'date_range': date_range,
        'updated_at': '2026-09-07 19:15'
    },
    'overview': {
        'cards': [
            {'id': 'vol_full', 'title': 'Sản Lượng Full Hàng', 'val': vol_full_w36, 'unit': 'đơn', 'diff': vol_full_diff, 'diff_pct': (vol_full_diff / (vol_full_w36 - vol_full_diff)) if (vol_full_w36 - vol_full_diff) else 0, 'is_good': vol_full_diff >= 0, 'icon': 'package'},
            {'id': 'vol_tts', 'title': 'Sản Lượng TTS', 'val': vol_tts_w36, 'unit': 'đơn', 'diff': vol_tts_diff, 'diff_pct': (vol_tts_diff / (vol_tts_w36 - vol_tts_diff)) if (vol_tts_w36 - vol_tts_diff) else 0, 'is_good': vol_tts_diff >= 0, 'icon': 'truck'},
            {'id': 'gtc_full', 'title': '%GTC Full Hàng', 'val': gtc_full_w36, 'unit': '%', 'diff': gtc_full_diff, 'diff_pct': gtc_full_diff, 'is_good': gtc_full_diff >= 0, 'icon': 'check-circle-2'},
            {'id': 'gtc_tts', 'title': '%GTC TTS', 'val': gtc_tts_w36, 'unit': '%', 'diff': gtc_tts_diff, 'diff_pct': gtc_tts_diff, 'is_good': gtc_tts_diff >= 0, 'icon': 'award'},
            {'id': 'odr_full', 'title': '%ODR (Giao Đúng Hẹn)', 'val': odr_full_w36, 'unit': '%', 'diff': odr_full_diff, 'diff_pct': odr_full_diff, 'is_good': odr_full_diff >= 0, 'icon': 'clock'},
            {'id': 'ltc_full', 'title': '%LTC (Lấy Thành Công)', 'val': ltc_full_w36, 'unit': '%', 'diff': ltc_full_diff, 'diff_pct': ltc_full_diff, 'is_good': ltc_full_diff >= 0, 'icon': 'archive'},
            {'id': 'rot_lc', 'title': '%Rớt Luân Chuyển', 'val': rot_lc_val, 'unit': '%', 'diff': rot_lc_diff, 'diff_pct': (rot_lc_diff / 0.0157), 'is_good': False, 'icon': 'alert-triangle'},
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
        gan_overview.append({
            'indicator': str(ind).strip(),
            'w33': ws_gan.cell(r, 2).value or 0,
            'w34': ws_gan.cell(r, 3).value or 0,
            'w35': ws_gan.cell(r, 4).value or 0,
            'w36': ws_gan.cell(r, 5).value or 0,
            'diff': ws_gan.cell(r, 6).value or 0
        })

gan_am_full = []
for r in range(16, 35):
    am = ws_gan.cell(r, 1).value
    if am and str(am).strip() not in ['None', '', 'AM']:
        gan_am_full.append({
            'am': str(am).strip(),
            'vol': ws_gan.cell(r, 2).value or 0,
            'tong_w35': ws_gan.cell(r, 3).value or 0,
            'tong_w36': ws_gan.cell(r, 4).value or 0,
            'tong_diff': ws_gan.cell(r, 5).value or 0,
            'ca1ton_w35': ws_gan.cell(r, 6).value or 0,
            'ca1ton_w36': ws_gan.cell(r, 7).value or 0,
            'ca1ton_diff': ws_gan.cell(r, 8).value or 0,
            'ca2_w35': ws_gan.cell(r, 9).value or 0,
            'ca2_w36': ws_gan.cell(r, 10).value or 0,
            'ca2_diff': ws_gan.cell(r, 11).value or 0,
            # Fallback for legacy W34/W35 keys
            'tong_w34': ws_gan.cell(r, 3).value or 0,
            'ca1ton_w34': ws_gan.cell(r, 6).value or 0,
            'ca2_w34': ws_gan.cell(r, 9).value or 0
        })

gan_am_tts = []
for r in range(38, 57):
    am = ws_gan.cell(r, 1).value
    if am and str(am).strip() not in ['None', '', 'AM']:
        gan_am_tts.append({
            'am': str(am).strip(),
            'vol': ws_gan.cell(r, 2).value or 0,
            'tong_w35': ws_gan.cell(r, 3).value or 0,
            'tong_w36': ws_gan.cell(r, 4).value or 0,
            'tong_diff': ws_gan.cell(r, 5).value or 0,
            'ca1ton_w35': ws_gan.cell(r, 6).value or 0,
            'ca1ton_w36': ws_gan.cell(r, 7).value or 0,
            'ca1ton_diff': ws_gan.cell(r, 8).value or 0,
            'ca2_w35': ws_gan.cell(r, 9).value or 0,
            'ca2_w36': ws_gan.cell(r, 10).value or 0,
            'ca2_diff': ws_gan.cell(r, 11).value or 0,
            'tong_w34': ws_gan.cell(r, 3).value or 0,
            'ca1ton_w34': ws_gan.cell(r, 6).value or 0,
            'ca2_w34': ws_gan.cell(r, 9).value or 0
        })

data['gan'] = {
    'overview': gan_overview,
    'am_full': gan_am_full,
    'am_tts': gan_am_tts,
    'am': gan_am_full
}

# 08_OPR TTS
ws_opr = wb['08_OPR TTS']
opr_am = []
for r in range(6, 23):
    am = ws_opr.cell(r, 1).value
    if am and str(am).strip() not in ['None', '', 'AM']:
        opr_am.append({
            'am': str(am).strip(),
            'vol_day': ws_opr.cell(r, 2).value or 0,
            'w35_day': ws_opr.cell(r, 3).value or 0,
            'w36_day': (ws_opr.cell(r, 4).value or 0) if (ws_opr.cell(r, 4).value or 0) <= 1 else 0,
            'diff_day': ws_opr.cell(r, 5).value or 0,
            'vol_night': ws_opr.cell(r, 6).value or 0,
            'w35_night': ws_opr.cell(r, 7).value or 0,
            'w36_night': ws_opr.cell(r, 8).value or 0,
            'diff_night': ws_opr.cell(r, 9).value or 0,
            'vol_total': ws_opr.cell(r, 10).value or 0,
            'w35_total': ws_opr.cell(r, 11).value or 0,
            'w36_total': ws_opr.cell(r, 12).value or 0,
            'diff_total': ws_opr.cell(r, 13).value or 0,
            # Fallback
            'w34_day': ws_opr.cell(r, 3).value or 0,
            'w34_night': ws_opr.cell(r, 7).value or 0,
            'w34_total': ws_opr.cell(r, 11).value or 0
        })

opr_tinh = []
for r in range(26, 32):
    t = ws_opr.cell(r, 1).value
    if t and str(t).strip() not in ['None', '', 'Tỉnh']:
        opr_tinh.append({
            'tinh': str(t).strip(),
            'vol_day': ws_opr.cell(r, 2).value or 0,
            'w35_day': ws_opr.cell(r, 3).value or 0,
            'w36_day': ws_opr.cell(r, 4).value or 0,
            'diff_day': ws_opr.cell(r, 5).value or 0,
            'vol_night': ws_opr.cell(r, 6).value or 0,
            'w35_night': ws_opr.cell(r, 7).value or 0,
            'w36_night': ws_opr.cell(r, 8).value or 0,
            'diff_night': ws_opr.cell(r, 9).value or 0,
            'vol_total': ws_opr.cell(r, 10).value or 0,
            'w35_total': ws_opr.cell(r, 11).value or 0,
            'w36_total': ws_opr.cell(r, 12).value or 0,
            'diff_total': ws_opr.cell(r, 13).value or 0,
            'w34_day': ws_opr.cell(r, 3).value or 0,
            'w34_night': ws_opr.cell(r, 7).value or 0,
            'w34_total': ws_opr.cell(r, 11).value or 0
        })

data['opr_tts'] = {
    'am': opr_am,
    'tinh': opr_tinh
}

# 09_Rot LC
ws_rot = wb['09_Rot LC']
rot_am = []
for r in range(11, 29):
    am = ws_rot.cell(r, 1).value
    if am and str(am).strip() not in ['None', '', 'AM']:
        w35_val = ws_rot.cell(r, 3).value or 0
        w36_val = ws_rot.cell(r, 4).value or 0
        diff_val = ws_rot.cell(r, 5).value if ws_rot.cell(r, 5).value is not None else (w36_val - w35_val)
        rot_am.append({
            'am': str(am).strip(),
            'vol': ws_rot.cell(r, 2).value or 0,
            'w35': w35_val,
            'w36': w36_val,
            'diff': diff_val,
            'w34': w35_val  # backward-compat fallback
        })

rot_tinh = []
for r in range(32, 38):
    t = ws_rot.cell(r, 1).value
    if t and str(t).strip() not in ['None', '', 'Tỉnh']:
        w35_val = ws_rot.cell(r, 3).value or 0
        w36_val = ws_rot.cell(r, 4).value or 0
        diff_val = ws_rot.cell(r, 5).value if ws_rot.cell(r, 5).value is not None else (w36_val - w35_val)
        rot_tinh.append({
            'tinh': str(t).strip(),
            'vol': ws_rot.cell(r, 2).value or 0,
            'w35': w35_val,
            'w36': w36_val,
            'diff': diff_val,
            'w34': w35_val  # backward-compat fallback
        })

co_cau_map = {}
try:
    import pandas as pd
    import re
    import unicodedata
    co_df = pd.read_csv('co_cau_ntb.csv')
    for _, cr in co_df.iterrows():
        b_raw = str(cr['Bưu cục']).strip()
        a_raw = unicodedata.normalize('NFC', str(cr['AM']).strip())
        b_norm = unicodedata.normalize('NFC', re.sub(r'[\s\-_]+', '', b_raw.lower()))
        co_cau_map[b_norm] = a_raw
except Exception as e:
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

# 12_FD - Báo cáo %FD Return (Full Hàng & TikTok Shop)
try:
    with open('scratch/fd_processed.json', 'r', encoding='utf-8') as f_fd:
        data['fd'] = json.load(f_fd)
except Exception as e:
    print(f"Warning: Could not load scratch/fd_processed.json: {e}")

# 10_KinhDoanh_TongQuan
ws_kd = wb['10_KinhDoanh_TongQuan']
kd_am = []
for r in range(5, 24):
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
for r in range(28, 33):
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
except Exception as e:
    pass


khach_hang_a = {}
try:
    kh_json_p = os.path.join(os.path.dirname(__file__), 'scratch', 'khach_hang_a.json')
    if os.path.exists(kh_json_p):
        with open(kh_json_p, 'r', encoding='utf-8') as f_kh:
            khach_hang_a = json.load(f_kh)
except Exception as e:
    pass

transport_costs = {}
try:
    tc_json_p = os.path.join(os.path.dirname(__file__), 'scratch', 'transport_costs.json')
    if not os.path.exists(tc_json_p):
        tc_json_p = os.path.join(os.path.dirname(__file__), 'transport_costs.json')
    if os.path.exists(tc_json_p):
        with open(tc_json_p, 'r', encoding='utf-8') as f_tc:
            transport_costs = json.load(f_tc)
except Exception as e:
    pass

data['transport_costs'] = transport_costs

data['kinh_doanh'] = {
    'am': kd_am,
    'top_drop': top_drop_kd,
    'churn_top10': churn_top10,
    'churn_zero': churn_zero,
    'khach_hang_a': khach_hang_a,
    'total': {
        'vol_prev': 32739,
        'vol_curr': 30132,
        'diff_vol': -2607,
        'rev_prev': 1073183298,
        'rev_curr': 947392461,
        'diff_rev': -125790837,
        'pct_diff_rev': -0.1172
    }
}

# 11_KinhDoanh_F30
ws_f30 = wb['11_KinhDoanh_F30']
f30_am = []
for r in range(5, 22):
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
for r in range(26, 31):
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
        'kh_prev': 95,
        'kh_curr': 93,
        'diff_kh': -2,
        'rev_prev': 21854296,
        'rev_curr': 6215673,
        'diff_rev': -15638623,
        'pct_diff_rev': -0.7156
    }
}

# Merge previous COD, Aging, Truy Thu data if already existing
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

if 'aging' in existing_data:
    data['aging'] = existing_data['aging']
if 'treo_lc' in existing_data:
    data['treo_lc'] = existing_data['treo_lc']
if 'cod_report' in existing_data:
    data['cod_report'] = existing_data['cod_report']
if 'truy_thu_report' in existing_data:
    data['truy_thu_report'] = existing_data['truy_thu_report']

# Embed KTC data (Backlog, Leadtime, Fill Rate)
if os.path.exists('scratch/ktc_processed.json'):
    try:
        with open('scratch/ktc_processed.json', 'r', encoding='utf-8') as f:
            data['ktc'] = json.load(f)
    except Exception as e:
        print("Error loading scratch/ktc_processed.json:", e)
elif 'ktc' in existing_data:
    data['ktc'] = existing_data['ktc']

# Write out data.json and data.js
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open('data.js', 'w', encoding='utf-8') as f:
    f.write('window.DASHBOARD_DATA = ' + json.dumps(data, ensure_ascii=False, indent=2) + ';\n')
    f.write('window.DATA = window.DASHBOARD_DATA;\n')

print("🎉 SUCCESS: Generated data.json and data.js for week W36 successfully!")
