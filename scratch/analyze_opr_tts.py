# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

opr = d.get('opr_tts', {})

print("=== PROVINCE OPR TTS ===")
for t in opr.get('tinh', []):
    v_d = t.get('vol_day', 0)
    v_n = t.get('vol_night', 0)
    v_t = t.get('vol_total', 0)
    r_d = t.get('w40_day', 0) * 100
    r_n = t.get('w40_night', 0) * 100
    r_t = t.get('w40_total', 0) * 100
    p_d = t.get('w39_day', 0) * 100
    p_n = t.get('w39_night', 0) * 100
    p_t = t.get('w39_total', 0) * 100
    print(f"{t.get('tinh')}:")
    print(f"  Total: {r_t:.2f}% (W39: {p_t:.2f}%) | Vol: {v_t}")
    print(f"  Ngày (9h-19h): {r_d:.2f}% (W39: {p_d:.2f}%) | Vol: {v_d}")
    print(f"  Đêm (19h-9h): {r_n:.2f}% (W39: {p_n:.2f}%) | Vol: {v_n}")

print("\n=== AM OPR TTS & ERROR ANALYSIS ===")
# Target KPI >= 80%
am_list = opr.get('am', [])

# Calculate errors for each AM
# Error = total orders failed SLA
# Failed day = vol_day * (1 - w40_day)
# Failed night = vol_night * (1 - w40_night)
# Failed total = vol_total * (1 - w40_total)

total_day_vol = sum(a.get('vol_day', 0) for a in am_list)
total_night_vol = sum(a.get('vol_night', 0) for a in am_list)
total_vol = sum(a.get('vol_total', 0) for a in am_list)

passed_day_vol = sum(a.get('vol_day', 0) * a.get('w40_day', 0) for a in am_list)
passed_night_vol = sum(a.get('vol_night', 0) * a.get('w40_night', 0) for a in am_list)
passed_total_vol = sum(a.get('vol_total', 0) * a.get('w40_total', 0) for a in am_list)

failed_total_vol = total_vol - passed_total_vol
failed_night_vol = total_night_vol - passed_night_vol
failed_day_vol = total_day_vol - passed_day_vol

print(f"REGION TOTALS:")
print(f"  Total Vol: {total_vol} | Total Passed: {passed_total_vol:.0f} | Total Failed: {failed_total_vol:.0f}")
print(f"  Region %OPR Total: {passed_total_vol / total_vol * 100:.2f}%")
print(f"  Region %OPR Ngày (9h-19h): {passed_day_vol / total_day_vol * 100:.2f}% (Failed: {failed_day_vol:.0f} / {total_day_vol})")
print(f"  Region %OPR Đêm (19h-9h): {passed_night_vol / total_night_vol * 100:.2f}% (Failed: {failed_night_vol:.0f} / {total_night_vol})")

analysis = []
for a in am_list:
    am_name = a['am']
    v_tot = a.get('vol_total', 0)
    r_tot = a.get('w40_total', 0)
    v_day = a.get('vol_day', 0)
    r_day = a.get('w40_day', 0)
    v_ngt = a.get('vol_night', 0)
    r_ngt = a.get('w40_night', 0)
    
    fail_tot = round(v_tot * (1 - r_tot))
    fail_day = round(v_day * (1 - r_day))
    fail_ngt = round(v_ngt * (1 - r_ngt))
    
    share_fail_tot = (fail_tot / failed_total_vol * 100) if failed_total_vol > 0 else 0
    share_fail_ngt = (fail_ngt / failed_night_vol * 100) if failed_night_vol > 0 else 0
    
    analysis.append({
        'am': am_name,
        'vol_tot': v_tot,
        'rate_tot': r_tot,
        'fail_tot': fail_tot,
        'share_fail_tot': share_fail_tot,
        'vol_day': v_day,
        'rate_day': r_day,
        'fail_day': fail_day,
        'vol_ngt': v_ngt,
        'rate_ngt': r_ngt,
        'fail_ngt': fail_ngt,
        'share_fail_ngt': share_fail_ngt,
        'pass_kpi': r_tot >= 0.80
    })

print("\n--- TOP AMs (LÀM TỐT NHẤT OPR TTS >= 90%) ---")
for x in sorted([a for a in analysis if a['vol_tot'] > 50], key=lambda k: k['rate_tot'], reverse=True):
    if x['rate_tot'] >= 0.80:
        print(f"  ✓ {x['am']}: OPR Tổng {x['rate_tot']*100:.1f}% (Vol {x['vol_tot']}) | Ngày {x['rate_day']*100:.1f}% | Đêm {x['rate_ngt']*100:.1f}% (Lỗi: {x['fail_tot']} đơn)")

print("\n--- AMs KHÔNG ĐẠT KPI (< 80%) & KÉO TỶ TRỌNG LỖI NHIỀU NHẤT ---")
for x in sorted(analysis, key=lambda k: k['fail_tot'], reverse=True):
    status = "ĐẠT" if x['pass_kpi'] else "KHÔNG ĐẠT ❌"
    print(f"  {status} | {x['am']}: OPR Tổng {x['rate_tot']*100:.1f}% | Lỗi {x['fail_tot']} đơn ({x['share_fail_tot']:.1f}% tổng lỗi vùng) | Lỗi Đêm: {x['fail_ngt']} đơn (Vol đêm {x['vol_ngt']}, OPR đêm {x['rate_ngt']*100:.1f}%) | Lỗi Ngày: {x['fail_day']} đơn")
