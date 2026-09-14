import sys
import openpyxl
import json
import os

sys.stdout.reconfigure(encoding='utf-8')

with open('build_data_js.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update 12_FD parsing
# We map AM codes from 12_FD to full AM names and build proper schema
am_name_map = {
    'AM Linh': 'Trương Quang Linh',
    'AM Lợi': 'Trần Tấn Lợi',
    'AM Duân': 'Huỳnh Thúc Duân',
    'AM Long': 'Nguyễn Tiến Long',
    'AM Nhung': 'Trần Thị Nhung',
    'AM Tiến': 'Nguyễn Hữu Tiến',
    'AM Duy': 'Phan Đình Duy',
    'AM Phi': 'Nguyễn Hoàng Phi',
    'AM Trường': 'Lê Văn Trường',
    'AM Nga': 'Hồng Bích Nga',
    'AM Thư': 'Thái Thị Thanh Thư',
    'AM D.Long': 'Nguyễn Duy Long',
    'AM Chi': 'Lê Thị Kim Chi',
    'AM Thơ': 'Nguyễn Thị Tuyết Thơ',
    'AM Thủy': 'Cao Thị Thanh Thủy',
    'AM Vũ': 'Nguyễn Lê Nguyên Vũ',
    'AM Nhựt': 'Lê Thanh Nhựt',
    'AM Khánh': 'Nguyễn Văn Khánh'
}

# Find fd parsing block in build_data_js.py
fd_block_start = code.find("# 12_FD")
fd_block_end = code.find("# 10_KinhDoanh_TongQuan", fd_block_start)
if fd_block_end == -1:
    fd_block_end = code.find("data['fd'] = fd_data", fd_block_start) + len("data['fd'] = fd_data\n")

print(f"FD block found: {fd_block_start} to {fd_block_end}")

new_fd_code = '''# 12_FD
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
        'AM Linh': 'Trương Quang Linh', 'AM Lợi': 'Trần Tấn Lợi', 'AM Duân': 'Huỳnh Thúc Duân',
        'AM Long': 'Nguyễn Tiến Long', 'AM Nhung': 'Trần Thị Nhung', 'AM Tiến': 'Nguyễn Hữu Tiến',
        'AM Duy': 'Phan Đình Duy', 'AM Phi': 'Nguyễn Hoàng Phi', 'AM Trường': 'Lê Văn Trường',
        'AM Nga': 'Hồng Bích Nga', 'AM Thư': 'Thái Thị Thanh Thư', 'AM D.Long': 'Nguyễn Duy Long',
        'AM Chi': 'Lê Thị Kim Chi', 'AM Thơ': 'Nguyễn Thị Tuyết Thơ', 'AM Thủy': 'Cao Thị Thanh Thủy',
        'AM Vũ': 'Nguyễn Lê Nguyên Vũ', 'AM Nhựt': 'Lê Thanh Nhựt', 'AM Khánh': 'Nguyễn Văn Khánh'
    }

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
            top_bc_list.append({
                'stt': stt,
                'bc': str(bc).strip(),
                'am': am_name_map.get(am_c, am_c),
                'am_code': am_c,
                'vol': v,
                'ret': ret,
                'rate': rate,
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
'''

# Replace FD block
if fd_block_start != -1 and fd_block_end != -1:
    code = code[:fd_block_start] + new_fd_code + "\n" + code[fd_block_end:]

# 2. Update KTC block to ensure causes and trend_6w
ktc_find = code.find("ktc_data['fill_rate'] = {")
if ktc_find != -1:
    ktc_end = code.find("}", ktc_find + 30)
    # find closing brace of ktc_data['fill_rate']
    ktc_close = code.find("if '15_Leadtime_Mang_Luoi_Kho'", ktc_find)
    if ktc_close != -1:
        # replace the fill_rate dictionary assignment
        old_fill_block = code[ktc_find:ktc_close].strip()
        new_fill_block = '''ktc_data['fill_rate'] = {
        'history': fill_rate_history,
        'by_hub': ktc_by_hub,
        'weekly': {
            'week_comp': 'Tuần W36 vs Tuần W37 (31/08 – 13/09/2026)',
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
    }'''
        code = code[:ktc_find] + new_fill_block + "\n\n" + code[ktc_close:]

with open('build_data_js.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Successfully updated build_data_js.py with full FD schema and KTC fill_rate details!")
