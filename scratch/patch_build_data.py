import re

with open('build_data_js.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update parse_san_luong_sheet compatibility block
old_sl_block = """                # Compatibility fallbacks
                item['w32'] = w_vals[0]
                item['w33'] = w_vals[0]
                item['w34'] = w_vals[0] if weeks[0] == 'W34' else (w_vals[1] if weeks[1] == 'W34' else w_vals[0])
                item['w35'] = w_vals[1] if weeks[1] == 'W35' else (w_vals[2] if weeks[2] == 'W35' else w_vals[1])
                item['w36'] = w_vals[2] if weeks[2] == 'W36' else (w_vals[3] if len(weeks) > 3 and weeks[3] == 'W36' else w_vals[2])
                item['w37'] = w_vals[3] if len(weeks) > 3 and weeks[3] == 'W37' else w_vals[-1]
                items.append(item)"""

new_sl_block = """                for idx, w in enumerate(weeks):
                    item[w.lower()] = w_vals[idx] if idx < len(w_vals) else 0
                item['w35'] = item.get('w35', w_vals[0] if len(w_vals) > 0 else 0)
                item['w36'] = item.get('w36', w_vals[1] if len(w_vals) > 1 else 0)
                item['w37'] = item.get('w37', w_vals[2] if len(w_vals) > 2 else 0)
                item['w38'] = item.get('w38', w_vals[3] if len(w_vals) > 3 else 0)
                item['w34'] = item.get('w34', w_vals[0] if len(w_vals) > 0 else 0)
                items.append(item)"""

assert old_sl_block in content, "old_sl_block not found in build_data_js.py"
content = content.replace(old_sl_block, new_sl_block, 1)

# 2. Update parse_standard_sheet overview & extract_rows
old_std_ov = """            for idx, k in enumerate(w_keys):
                ov[k] = w_vals[idx]
            ov['w32'] = w_vals[0]
            ov['w33'] = w_vals[0]
            ov['w34'] = w_vals[0] if weeks[0] == 'W34' else w_vals[1]
            ov['w35'] = w_vals[1] if weeks[1] == 'W35' else w_vals[2]
            ov['w36'] = w_vals[2] if weeks[2] == 'W36' else w_vals[3]
            ov['w37'] = w_vals[3] if len(weeks) > 3 else w_vals[-1]
            overview.append(ov)"""

new_std_ov = """            for idx, w in enumerate(weeks):
                ov[w.lower()] = w_vals[idx] if idx < len(w_vals) else 0
            ov['w35'] = ov.get('w35', w_vals[0] if len(w_vals) > 0 else 0)
            ov['w36'] = ov.get('w36', w_vals[1] if len(w_vals) > 1 else 0)
            ov['w37'] = ov.get('w37', w_vals[2] if len(w_vals) > 2 else 0)
            ov['w38'] = ov.get('w38', w_vals[3] if len(w_vals) > 3 else 0)
            ov['w34'] = ov.get('w34', w_vals[0] if len(w_vals) > 0 else 0)
            overview.append(ov)"""

assert old_std_ov in content, "old_std_ov not found in build_data_js.py"
content = content.replace(old_std_ov, new_std_ov, 1)

old_std_rows = """                for idx, k in enumerate(w_keys):
                    item[k] = w_vals[idx]
                item['w32'] = w_vals[0]
                item['w33'] = w_vals[0]
                item['w34'] = w_vals[0] if weeks[0] == 'W34' else w_vals[1]
                item['w35'] = w_vals[1] if weeks[1] == 'W35' else w_vals[2]
                item['w36'] = w_vals[2] if weeks[2] == 'W36' else w_vals[3]
                item['w37'] = w_vals[3] if len(weeks) > 3 else w_vals[-1]
                items.append(item)"""

new_std_rows = """                for idx, w in enumerate(weeks):
                    item[w.lower()] = w_vals[idx] if idx < len(w_vals) else 0
                item['w35'] = item.get('w35', w_vals[0] if len(w_vals) > 0 else 0)
                item['w36'] = item.get('w36', w_vals[1] if len(w_vals) > 1 else 0)
                item['w37'] = item.get('w37', w_vals[2] if len(w_vals) > 2 else 0)
                item['w38'] = item.get('w38', w_vals[3] if len(w_vals) > 3 else 0)
                item['w34'] = item.get('w34', w_vals[0] if len(w_vals) > 0 else 0)
                items.append(item)"""

assert old_std_rows in content, "old_std_rows not found in build_data_js.py"
content = content.replace(old_std_rows, new_std_rows, 1)

# 3. Update tq_rows
old_tq = """        for idx, k in enumerate(w_keys):
            row_dict[k] = w_vals[idx]
        row_dict['w32'] = w_vals[0]
        row_dict['w33'] = w_vals[0]
        row_dict['w34'] = w_vals[0] if weeks[0] == 'W34' else w_vals[1]
        row_dict['w35'] = w_vals[1] if weeks[1] == 'W35' else w_vals[2]
        row_dict['w36'] = w_vals[2] if weeks[2] == 'W36' else w_vals[3]
        row_dict['w37'] = w_vals[3] if len(weeks) > 3 else w_vals[-1]
        tq_rows[clean_ind] = row_dict"""

new_tq = """        for idx, w in enumerate(weeks):
            row_dict[w.lower()] = w_vals[idx] if idx < len(w_vals) else None
        row_dict['w35'] = row_dict.get('w35', w_vals[0] if len(w_vals) > 0 else None)
        row_dict['w36'] = row_dict.get('w36', w_vals[1] if len(w_vals) > 1 else None)
        row_dict['w37'] = row_dict.get('w37', w_vals[2] if len(w_vals) > 2 else None)
        row_dict['w38'] = row_dict.get('w38', w_vals[3] if len(w_vals) > 3 else None)
        row_dict['w34'] = row_dict.get('w34', w_vals[0] if len(w_vals) > 0 else None)
        tq_rows[clean_ind] = row_dict"""

assert old_tq in content, "old_tq not found in build_data_js.py"
content = content.replace(old_tq, new_tq, 1)

# 4. Update 07_Gan
old_gan_ov = """# 07_Gan
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
        gan_overview.append(ov)"""

new_gan_ov = """# 07_Gan
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
        gan_overview.append(ov)"""

assert old_gan_ov in content, "old_gan_ov not found in build_data_js.py"
content = content.replace(old_gan_ov, new_gan_ov, 1)

old_gan_am = """def extract_gan_am(r_start, r_end):
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
    return items"""

new_gan_am = """def extract_gan_am(r_start, r_end):
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
    return items"""

assert old_gan_am in content, "old_gan_am not found in build_data_js.py"
content = content.replace(old_gan_am, new_gan_am, 1)

# 5. Update 08_OPR TTS
old_opr_am = """        opr_am.append({
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
        })"""

new_opr_am = """        opr_am.append({
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
            'w37_day': w_prev_day,
            'w38_day': w_curr_day,
            'w37_night': w_prev_night,
            'w38_night': w_curr_night,
            'w37_total': w_prev_total,
            'w38_total': w_curr_total,
            'w36_day': w_prev_day,
            'w36_night': w_prev_night,
            'w36_total': w_prev_total
        })"""

assert old_opr_am in content, "old_opr_am not found in build_data_js.py"
content = content.replace(old_opr_am, new_opr_am, 1)

old_opr_tinh = """        opr_tinh.append({
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
        })"""

new_opr_tinh = """        opr_tinh.append({
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
            'w37_day': w_prev_day,
            'w38_day': w_curr_day,
            'w37_night': w_prev_night,
            'w38_night': w_curr_night,
            'w37_total': w_prev_total,
            'w38_total': w_curr_total,
            'w36_day': w_prev_day,
            'w36_night': w_prev_night,
            'w36_total': w_prev_total
        })"""

assert old_opr_tinh in content, "old_opr_tinh not found in build_data_js.py"
content = content.replace(old_opr_tinh, new_opr_tinh, 1)

# 6. Update 09_Rot LC
old_rot_am = """# 09_Rot LC
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
        })"""

new_rot_am = """# 09_Rot LC
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
        })"""

assert old_rot_am in content, "old_rot_am not found in build_data_js.py"
content = content.replace(old_rot_am, new_rot_am, 1)

old_rot_data = """data['rot_lc'] = {
    'am': rot_am,
    'tinh': rot_tinh,
    'top_bc': rot_top_bc,
    'bc': rot_top_bc
}"""

new_rot_data = """tot_can_lc = sum(r['vol'] for r in rot_am)
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
}"""

assert old_rot_data in content, "old_rot_data not found in build_data_js.py"
content = content.replace(old_rot_data, new_rot_data, 1)

with open('build_data_js.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Patched build_data_js.py")
