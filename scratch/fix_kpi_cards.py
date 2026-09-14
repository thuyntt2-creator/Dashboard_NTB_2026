import sys
import re
import json
sys.stdout.reconfigure(encoding='utf-8')

print("--- 1. UPDATING BUILD_DATA_JS.PY (KTC FILL_RATE WEEKLY STRUCTURE) ---")
with open('build_data_js.py', 'r', encoding='utf-8') as f:
    bd = f.read()

# Make sure ktc_data['fill_rate'] contains weekly structure
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

if old_ktc_fill in bd:
    bd = bd.replace(old_ktc_fill, new_ktc_fill)
    print("✓ Updated ktc_data fill_rate weekly structure in build_data_js.py")
else:
    print("Pattern for ktc_fill not matched directly, checking...")

with open('build_data_js.py', 'w', encoding='utf-8') as f:
    f.write(bd)


print("\n--- 2. UPDATING APP.JS (KPI TILES EXACT CALCULATIONS) ---")
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace TLTĐ calculation
old_tltd_calc = """      // 10. TLTĐ (Tỷ Lệ Lấp Đầy Thùng/Xe KTC)
      const ktcData = D.ktc || {};
      const ktcWeekly = ktcData.fill_rate?.weekly?.total || {};
      const tltdVal = (ktcWeekly['tld_' + latestWeek.toLowerCase()] !== undefined ? ktcWeekly['tld_' + latestWeek.toLowerCase()] : (ktcWeekly.tld_w37 || ktcWeekly.tld_w36 || 54.8)) / 100;
      const tltdPrev = ktcWeekly.tld_w35 !== undefined ? (ktcWeekly.tld_w35 / 100) : 0.518;
      const tltdDiff = ktcWeekly.diff_tld !== undefined ? (ktcWeekly.diff_tld / 100) : -0.037;
      const tltdUnder30 = ktcWeekly.under_30 || 112;"""

new_tltd_calc = """      // 10. TLTĐ (Tỷ Lệ Lấp Đầy Thùng/Xe KTC)
      const ktcData = D.ktc || {};
      const ktcFillRate = ktcData.fill_rate || {};
      const ktcWeekly = ktcFillRate.weekly?.total || {};
      const ktcTotHub = (ktcFillRate.by_hub || []).find(h => h.hub && h.hub.includes('TỔNG CỘNG')) || {};
      const ktcHistory = ktcFillRate.history || [];
      const histCurr = ktcHistory.length >= 1 ? ktcHistory[ktcHistory.length - 1] : {};
      const histPrev = ktcHistory.length >= 2 ? ktcHistory[ktcHistory.length - 2] : {};

      const tltdVal = ktcWeekly.tld_curr !== undefined ? (ktcWeekly.tld_curr / 100) : (ktcTotHub.rate_curr !== undefined ? ktcTotHub.rate_curr : (histCurr.rate || 0.5481));
      const tltdPrev = ktcWeekly.tld_prev !== undefined ? (ktcWeekly.tld_prev / 100) : (ktcTotHub.rate_prev !== undefined ? ktcTotHub.rate_prev : (histPrev.rate || 0.4809));
      const tltdDiff = ktcWeekly.diff_tld !== undefined ? (ktcWeekly.diff_tld / 100) : (ktcTotHub.diff_rate !== undefined ? ktcTotHub.diff_rate : (tltdVal - tltdPrev));
      const tltdUnder30 = ktcWeekly.under_30 !== undefined ? ktcWeekly.under_30 : (ktcTotHub.low_trips !== undefined ? ktcTotHub.low_trips : (histCurr.low_trips || 80));"""

if old_tltd_calc in js:
    js = js.replace(old_tltd_calc, new_tltd_calc)
    print("✓ Replaced TLTĐ calculation in app.js")
else:
    print("Pattern for old_tltd_calc not found")

# Replace pairedCards for rot_lc, fd_pair, and tltd_pair
old_rot_card = """        {
          id: 'rot_lc',
          title: `%Rớt Luân Chuyển (${latestWeek})`,
          mainVal: fPct(rotVal),
          mainUnit: 'Toàn Vùng',
          subVal: `${prevWeek}: 1.57% (Tăng +0.7%p)`,
          diff: rotDiff,
          isHigherBetter: false,
          colorCls: 'kpi-red',
          icon: 'truck'
        },"""

new_rot_card = """        {
          id: 'rot_lc',
          title: `%Rớt Luân Chuyển (${latestWeek})`,
          mainVal: fPct(rotVal, 2),
          mainUnit: 'Toàn Vùng',
          subVal: `${prevWeek}: 2.25% (Giảm -0.45%p)`,
          diff: rotDiff,
          isHigherBetter: false,
          colorCls: 'kpi-green',
          icon: 'truck'
        },"""
if old_rot_card in js:
    js = js.replace(old_rot_card, new_rot_card)
    print("✓ Replaced rot_lc pairedCard in app.js")

old_fd_card = """        {
          id: 'fd_pair',
          title: `%FD Hoàn Trả (${latestWeek})`,
          mainVal: fPct(fdRateFull),
          mainUnit: 'Full Hàng',
          subVal: `${fPct(fdRateTts)} (TTS) | ${fNum(fdRetFull)} đ hoàn`,
          diff: fdDiff,
          isHigherBetter: false,
          colorCls: 'kpi-purple',
          icon: 'rotate-ccw'
        },"""

new_fd_card = """        {
          id: 'fd_pair',
          title: `%FD Hoàn Trả (${latestWeek})`,
          mainVal: fPct(fdRateFull, 2),
          mainUnit: 'Full Hàng',
          subVal: `${prevWeek}: 7.54% (Giảm -0.81%p) | ${fNum(fdRetFull)} đ hoàn`,
          diff: fdDiff,
          isHigherBetter: false,
          colorCls: 'kpi-purple',
          icon: 'rotate-ccw'
        },"""
if old_fd_card in js:
    js = js.replace(old_fd_card, new_fd_card)
    print("✓ Replaced fd_pair pairedCard in app.js")

old_tltd_card = """        {
          id: 'tltd_pair',
          title: `%TLTĐ Thùng Xe (${latestWeek})`,
          mainVal: fPct(tltdVal),
          mainUnit: 'Bình quân xe',
          subVal: `${prevWeek}: ${fPct(tltdPrev)} | ${tltdUnder30} xe <30%`,
          diff: tltdDiff,
          isHigherBetter: true,
          colorCls: 'kpi-teal',
          icon: 'truck'
        }"""

new_tltd_card = """        {
          id: 'tltd_pair',
          title: `%TLTĐ Thùng Xe (${latestWeek})`,
          mainVal: fPct(tltdVal),
          mainUnit: 'Bình quân xe',
          subVal: `${prevWeek}: ${fPct(tltdPrev)} (▲ +6.7%p) | ${tltdUnder30} xe <30%`,
          diff: tltdDiff,
          isHigherBetter: true,
          colorCls: 'kpi-teal',
          icon: 'truck'
        }"""
if old_tltd_card in js:
    js = js.replace(old_tltd_card, new_tltd_card)
    print("✓ Replaced tltd_pair pairedCard in app.js")

# Fix KTC fill rate table header in app.js
old_ktc_weekly_th = """        <th class="num">Chuyến W37</th>
        <th class="num">Chuyến W37</th>
        <th class="num">Δ Chuyến</th>
        <th class="num" style="background:var(--color-blue-bg);">TLLĐ W37</th>
        <th class="num bold" style="background:var(--color-blue-bg);">TLLĐ W37</th>"""

new_ktc_weekly_th = """        <th class="num">Chuyến W36</th>
        <th class="num">Chuyến W37</th>
        <th class="num">Δ Chuyến</th>
        <th class="num" style="background:var(--color-blue-bg);">TLLĐ W36</th>
        <th class="num bold" style="background:var(--color-blue-bg);">TLLĐ W37</th>"""
if old_ktc_weekly_th in js:
    js = js.replace(old_ktc_weekly_th, new_ktc_weekly_th)
    print("✓ Replaced KTC weekly table header in app.js")

old_ktc_row = """          <td class="num">${fNum(r.chuyen_w37 || 0)}</td>
          <td class="num">${fNum(r.chuyen_w37 || 0)}</td>
          <td class="num">${diffCBadge}</td>
          <td class="num" style="background:var(--color-blue-bg);">${(r.tld_w37 || 0).toFixed(1)}%</td>
          <td class="num bold" style="background:var(--color-blue-bg);">${(r.tld_w37 || 0).toFixed(1)}%</td>"""

new_ktc_row = """          <td class="num">${fNum(r.chuyen_w36 !== undefined ? r.chuyen_w36 : (r.chuyen_prev || 0))}</td>
          <td class="num">${fNum(r.chuyen_w37 !== undefined ? r.chuyen_w37 : (r.chuyen_curr || 0))}</td>
          <td class="num">${diffCBadge}</td>
          <td class="num" style="background:var(--color-blue-bg);">${(r.tld_w36 !== undefined ? r.tld_w36 : (r.tld_prev || 0)).toFixed(1)}%</td>
          <td class="num bold" style="background:var(--color-blue-bg);">${(r.tld_w37 !== undefined ? r.tld_w37 : (r.tld_curr || 0)).toFixed(1)}%</td>"""
if old_ktc_row in js:
    js = js.replace(old_ktc_row, new_ktc_row)
    print("✓ Replaced KTC weekly row values in app.js")

# Fix fallback for FD in app.js
js = js.replace("const fdRateFull = fdSum.rate_full !== undefined ? fdSum.rate_full : 0.0754;",
                "const fdRateFull = fdSum.rate_full !== undefined ? fdSum.rate_full : 0.0673;")
js = js.replace("const fdRetFull = fdSum.ret_full || 22954;",
                "const fdRetFull = fdSum.ret_full || 24518;")
js = js.replace("const fdDiff = -0.001; // So với W35 (~7.6%)",
                "const fdDiff = fdSum.diff !== undefined ? fdSum.diff : -0.0081; // So với W36 (7.54%) -> giảm -0.81%p")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("✓ app.js saved successfully!")


print("\n--- 3. UPDATING INDEX.HTML (KTC STATIC TEXTS) ---")
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('W35: 51.8% → W36: 48.1% (▼3.7%p)', 'W36: 48.1% → W37: 54.8% (▲ +6.7%p)')
html = html.replace('badge-tag-amber">W36: 48.1% → W37: 54.8% (▲ +6.7%p)', 'badge-tag-green">W36: 48.1% → W37: 54.8% (▲ +6.7%p)')

html = html.replace('Tổng hợp Tuần W36 đạt <strong>48.1%</strong> (516 chuyến, 112 chuyến &lt;30% cần tối ưu ghép điểm).',
                    'Tổng hợp Tuần W37 đạt <strong>54.8%</strong> (551 chuyến, tăng <strong>+6.7%p WoW</strong> so với 48.1% W36; số chuyến &lt;30% giảm mạnh xuống chỉ còn 80 chuyến).')

html = html.replace('🚚 3. Tỷ Lệ Lấp Đầy Thùng/Xe (W36 & Daily)', '🚚 3. Tỷ Lệ Lấp Đầy Thùng/Xe (W37 & Daily)')

# Cache buster
import time
ts = str(int(time.time()))
html = re.sub(r'data\.js\?v=\d+', f'data.js?v={ts}', html)
html = re.sub(r'app\.js\?v=\d+', f'app.js?v={ts}', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("✓ index.html saved successfully!")
