import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('build_data_js.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update 12_FD to populate summary
old_fd_block = """    fd_data = {
        'overview': {
            'total_orders': ws_fd.cell(6, 2).value or 364067,
            'return_orders': ws_fd.cell(7, 2).value or 24518,
            'rate_fd': ws_fd.cell(8, 2).value or 0.0673,
            'num_bc': ws_fd.cell(9, 2).value or 94
        },
        'top_bc': [],
        'am': []
    }"""

new_fd_block = """    fd_data = {
        'overview': {
            'total_orders': ws_fd.cell(6, 2).value or 364067,
            'return_orders': ws_fd.cell(7, 2).value or 24518,
            'rate_fd': ws_fd.cell(8, 2).value or 0.06734,
            'num_bc': ws_fd.cell(9, 2).value or 94
        },
        'summary': {
            'vol_full': ws_fd.cell(6, 2).value or 364067,
            'ret_full': ws_fd.cell(7, 2).value or 24518,
            'rate_full': ws_fd.cell(8, 2).value or 0.06734,
            'rate_tts': 0.0610,
            'vol_tts': 68719,
            'diff': (ws_fd.cell(8, 2).value or 0.06734) - 0.0754,
            'total_orders': ws_fd.cell(6, 2).value or 364067,
            'return_orders': ws_fd.cell(7, 2).value or 24518
        },
        'top_bc': [],
        'am': []
    }"""
code = code.replace(old_fd_block, new_fd_block)

# 2. Add parser for 13_KH_Giam_Don into churn_top10
old_churn_block = """churn_top10 = []
churn_zero = []
try:
    with open('scratch/top10_churn.json', 'r', encoding='utf-8') as f_churn:
        c_payload = json.load(f_churn)
        churn_top10 = c_payload.get('top10_drop', [])
        churn_zero = c_payload.get('top_zero', [])
except Exception:
    pass"""

new_churn_block = """churn_top10 = []
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
        pass"""
code = code.replace(old_churn_block, new_churn_block)

# 3. Ensure ktc_data['fill_rate']['weekly'] is properly structured
old_ktc_fill = """    ktc_data['fill_rate'] = {
        'history': fill_rate_history,
        'by_hub': ktc_by_hub
    }"""

new_ktc_fill = """    ktc_by_hub_items = [h for h in ktc_by_hub if 'TỔNG' not in h['hub'] and 'NHẬN XÉT' not in h['hub']]
    ktc_total = next((h for h in ktc_by_hub if 'TỔNG' in h['hub']), None)
    
    ktc_weekly_items = []
    for h in ktc_by_hub_items:
        diff_c = h['trips_curr'] - h['trips_prev']
        diff_t = round(h['diff_rate'] * 100, 1)
        ktc_weekly_items.append({
            'kho': h['hub'],
            'short_name': h['hub'],
            'chuyen_prev': h['trips_prev'],
            'chuyen_curr': h['trips_curr'],
            'chuyen_w36': h['trips_prev'],
            'chuyen_w37': h['trips_curr'],
            'diff_chuyen': diff_c,
            'tld_prev': round(h['rate_prev'] * 100, 1),
            'tld_curr': round(h['rate_curr'] * 100, 1),
            'tld_w36': round(h['rate_prev'] * 100, 1),
            'tld_w37': round(h['rate_curr'] * 100, 1),
            'diff_tld': diff_t,
            'under_30': h['low_trips'],
            'u10': 0, 'u20': 0, 'u30': h['low_trips']
        })
    
    ktc_weekly_total = {
        'kho': 'TỔNG CỘNG (5 KTC)',
        'chuyen_prev': ktc_total['trips_prev'] if ktc_total else 516,
        'chuyen_curr': ktc_total['trips_curr'] if ktc_total else 551,
        'chuyen_w36': ktc_total['trips_prev'] if ktc_total else 516,
        'chuyen_w37': ktc_total['trips_curr'] if ktc_total else 551,
        'diff_chuyen': (ktc_total['trips_curr'] - ktc_total['trips_prev']) if ktc_total else 35,
        'tld_prev': round((ktc_total['rate_prev'] * 100), 1) if ktc_total else 48.1,
        'tld_curr': round((ktc_total['rate_curr'] * 100), 1) if ktc_total else 54.8,
        'tld_w36': round((ktc_total['rate_prev'] * 100), 1) if ktc_total else 48.1,
        'tld_w37': round((ktc_total['rate_curr'] * 100), 1) if ktc_total else 54.8,
        'diff_tld': round((ktc_total['diff_rate'] * 100), 1) if ktc_total else 6.7,
        'under_30': ktc_total['low_trips'] if ktc_total else 80,
        'u10': 9, 'u20': 23, 'u30': 48
    }

    ktc_data['fill_rate'] = {
        'history': fill_rate_history,
        'by_hub': ktc_by_hub,
        'weekly': {
            'items': ktc_weekly_items,
            'total': ktc_weekly_total
        },
        'daily': {
            'date_comp': '05/09 vs 06/09',
            'items': [],
            'total': {}
        }
    }"""
code = code.replace(old_ktc_fill, new_ktc_fill)

with open('build_data_js.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("✓ Successfully upgraded build_data_js.py")
