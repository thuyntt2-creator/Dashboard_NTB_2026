import re
import time
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("--- 1. UPDATING INDEX.HTML ---")
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update table header in Overview (table-overview-kpi-data)
old_overview_th = """<th class="num">W33</th>
                  <th class="num">W34</th>
                  <th class="num">W35</th>
                  <th class="num" style="background: var(--color-blue-bg); color: var(--color-blue-dark); font-weight: 800;">W36 (Kỳ N)</th>"""
new_overview_th = """<th class="num">W34</th>
                  <th class="num">W35</th>
                  <th class="num">W36</th>
                  <th class="num" style="background: var(--color-blue-bg); color: var(--color-blue-dark); font-weight: 800;">W37 (Kỳ N)</th>"""
if old_overview_th in html:
    html = html.replace(old_overview_th, new_overview_th)
    print("✓ Overview table header updated")

# 2. Update Overview Region table (table-gan-overview-region)
old_reg_th = """<th class="num" style="color: #ffffff;">W33</th>
                    <th class="num" style="color: #ffffff;">W35</th>
                    <th class="num" style="color: #ffffff;">W36</th>
                    <th class="num" style="color: #ffffff; background: rgba(255,255,255,0.2); font-weight:800;">W36</th>
                    <th class="num" style="color: #ffffff;">Δ W36/W35</th>"""
new_reg_th = """<th class="num" style="color: #ffffff;">W34</th>
                    <th class="num" style="color: #ffffff;">W35</th>
                    <th class="num" style="color: #ffffff;">W36</th>
                    <th class="num" style="color: #ffffff; background: rgba(255,255,255,0.2); font-weight:800;">W37</th>
                    <th class="num" style="color: #ffffff;">Δ W37/W36</th>"""
if old_reg_th in html:
    html = html.replace(old_reg_th, new_reg_th)
    print("✓ Gan overview region header updated")

# 3. Tab 2 AM tables
html = html.replace("""<th class="num">Full W37</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">Full W37</th>""",
                    """<th class="num">Full W36</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">Full W37</th>""")

html = html.replace("""<th class="num">TTS W37</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">TTS W37</th>""",
                    """<th class="num">TTS W36</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">TTS W37</th>""")

# 4. Tab 2 5-tinh tables
old_tinh2_full = """<th class="num">W33</th>
                    <th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">W36</th>"""
new_tinh2_full = """<th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">W37</th>"""
html = html.replace(old_tinh2_full, new_tinh2_full)

old_tinh2_tts = """<th class="num">W33</th>
                    <th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">W36</th>"""
new_tinh2_tts = """<th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">W37</th>"""
html = html.replace(old_tinh2_tts, new_tinh2_tts)

# 5. Tab 3 GTC headers
html = html.replace("""<th class="num">W35</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">W36</th>""",
                    """<th class="num">W36</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">W37</th>""")

old_gtc_tinh = """<th class="num">W33</th>
                    <th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">%GTC W37</th>"""
new_gtc_tinh = """<th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">%GTC W37</th>"""
html = html.replace(old_gtc_tinh, new_gtc_tinh)

old_gtc_tinh_tts = """<th class="num">W33</th>
                    <th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">%GTC W37</th>"""
new_gtc_tinh_tts = """<th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight: 800; color: #ea580c;">%GTC W37</th>"""
html = html.replace(old_gtc_tinh_tts, new_gtc_tinh_tts)

# 6. Tab 4 Gan headers
html = html.replace("""<th class="num">Tổng W36</th>
                    <th class="num" style="background: var(--color-purple-bg); font-weight:800; color:#7e22ce;">Gán Tổng W36</th>""",
                    """<th class="num">Tổng W36</th>
                    <th class="num" style="background: var(--color-purple-bg); font-weight:800; color:#7e22ce;">Gán Tổng W37</th>""")

# 7. Tab 6 ODR headers
html = html.replace("""<th class="num">W35</th>
                    <th class="num" style="background: var(--color-green-bg); font-weight:800;">W36</th>""",
                    """<th class="num">W36</th>
                    <th class="num" style="background: var(--color-green-bg); font-weight:800;">W37</th>""")

old_odr_tinh = """<th class="num">W33</th>
                    <th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num" style="background: var(--color-green-bg); font-weight: 800;">%ODR W37</th>"""
new_odr_tinh = """<th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-green-bg); font-weight: 800;">%ODR W37</th>"""
html = html.replace(old_odr_tinh, new_odr_tinh)

# 8. Tab 7 LTC headers
old_ltc_tinh = """<th class="num">W33</th>
                    <th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%LTC W37</th>"""
new_ltc_tinh = """<th class="num">W34</th>
                    <th class="num">W35</th>
                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%LTC W37</th>"""
html = html.replace(old_ltc_tinh, new_ltc_tinh)

# 9. Tab 8 OPR TTS headers
html = html.replace("""<th class="num">Đơn Ngày</th>
                    <th class="num">W35</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%OPR W37</th>""",
                    """<th class="num">Đơn Ngày</th>
                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%OPR W37</th>""")

html = html.replace("""<th class="num">Đơn Đêm</th>
                    <th class="num">W35</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">%OPR W37</th>""",
                    """<th class="num">Đơn Đêm</th>
                    <th class="num">W36</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">%OPR W37</th>""")

html = html.replace("""<th class="num">%OPR 9h–19h (W37)</th>
                  <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%OPR 9h–19h (W37)</th>""",
                    """<th class="num">%OPR 9h–19h (W36)</th>
                  <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%OPR 9h–19h (W37)</th>""")

html = html.replace("""<th class="num">%OPR 19h–9h (W37)</th>
                  <th class="num" style="background: var(--color-amber-bg); font-weight:800;">%OPR 19h–9h (W37)</th>""",
                    """<th class="num">%OPR 19h–9h (W36)</th>
                  <th class="num" style="background: var(--color-amber-bg); font-weight:800;">%OPR 19h–9h (W37)</th>""")

# 10. Tab 9 Rot LC headers
html = html.replace("""<th class="num">% Rớt W37</th>
                    <th class="num" style="background: var(--color-red-bg); font-weight:800; color:#b91c1c;">% Rớt W37</th>""",
                    """<th class="num">% Rớt W36</th>
                    <th class="num" style="background: var(--color-red-bg); font-weight:800; color:#b91c1c;">% Rớt W37</th>""")

# Cache buster
ts = str(int(time.time()))
html = re.sub(r'data\.js\?v=\d+', f'data.js?v={ts}', html)
html = re.sub(r'app\.js\?v=\d+', f'app.js?v={ts}', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("✓ index.html saved successfully!")


print("\n--- 2. UPDATING APP.JS ---")
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Overview Tab KPI tiles & values
js = js.replace("const latestWeek = D.meta?.latest_week || 'W36';", "const latestWeek = D.meta?.latest_week || 'W37';")
js = js.replace("const prevWeek = D.meta?.prev_week || 'W35';", "const prevWeek = D.meta?.prev_week || 'W36';")

js = js.replace("const gtcCa1Val = gtcCa1Trend[latestWeek.toLowerCase()] !== undefined ? gtcCa1Trend[latestWeek.toLowerCase()] : (latestWeek === 'W36' ? 0.7478 : 0.758);",
                "const gtcCa1Val = gtcCa1Trend[latestWeek.toLowerCase()] !== undefined ? gtcCa1Trend[latestWeek.toLowerCase()] : 0.758;")
js = js.replace("const gtcCa1Diff = gtcCa1Trend.diff !== undefined ? gtcCa1Trend.diff : (latestWeek === 'W36' ? -0.0104 : 0.0181);",
                "const gtcCa1Diff = gtcCa1Trend.diff !== undefined ? gtcCa1Trend.diff : 0.0181;")

js = js.replace("const ganVal = ganFullRow.w36 !== undefined ? ganFullRow.w36 : 0.8355;",
                "const ganVal = ganFullRow[latestWeek.toLowerCase()] !== undefined ? ganFullRow[latestWeek.toLowerCase()] : (ganFullRow.w37 || ganFullRow.w36 || 0.8355);")
js = js.replace("const ganTtsVal = ganTtsRow.w36 !== undefined ? ganTtsRow.w36 : 0.8343;",
                "const ganTtsVal = ganTtsRow[latestWeek.toLowerCase()] !== undefined ? ganTtsRow[latestWeek.toLowerCase()] : (ganTtsRow.w37 || ganTtsRow.w36 || 0.8343);")

js = js.replace("const tltdVal = ktcWeekly.tld_w36 !== undefined ? (ktcWeekly.tld_w36 / 100) : 0.481;",
                "const tltdVal = (ktcWeekly['tld_' + latestWeek.toLowerCase()] !== undefined ? ktcWeekly['tld_' + latestWeek.toLowerCase()] : (ktcWeekly.tld_w37 || ktcWeekly.tld_w36 || 54.8)) / 100;")

# 2. Overview Tab Table (table-overview-kpi-data)
old_ov_table_code = """          const isPct = row.type === 'percent';
          const val1 = row.w36 !== undefined ? row.w33 : row.w32;
          const val2 = row.w36 !== undefined ? row.w34 : row.w33;
          const val3 = row.w36 !== undefined ? row.w35 : row.w34;
          const val4 = row.w36 !== undefined ? row.w36 : row.w35;"""

new_ov_table_code = """          const isPct = row.type === 'percent';
          const wKeys = (D.meta?.weeks || ['W34', 'W35', 'W36', 'W37']).map(w => w.toLowerCase());
          const val1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
          const val2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
          const val3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
          const val4 = row[wKeys[3]] !== undefined ? row[wKeys[3]] : (row.w37 !== undefined ? row.w37 : (row.vol || 0));"""
if old_ov_table_code in js:
    js = js.replace(old_ov_table_code, new_ov_table_code)
    print("✓ Overview table row values updated")
else:
    print("Overview table code replace missed")

# 3. Tab 2 AM tables: Full and TTS
old_t2_full = """    const tblBodyFull = document.querySelector('#table-vol-full-detailed tbody');
    if (tblBodyFull && D.san_luong.am_full) {
      let list = [...D.san_luong.am_full].map(r => {
        const curr = r.w36 !== undefined ? r.w36 : (r.w35 || 0);
        const prev = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);"""

new_t2_full = """    const tblBodyFull = document.querySelector('#table-vol-full-detailed tbody');
    if (tblBodyFull && D.san_luong.am_full) {
      const latestKey = D.meta?.latest_week ? D.meta.latest_week.toLowerCase() : 'w37';
      const prevKey = D.meta?.prev_week ? D.meta.prev_week.toLowerCase() : 'w36';
      let list = [...D.san_luong.am_full].map(r => {
        const curr = r[latestKey] !== undefined ? r[latestKey] : (r.w37 !== undefined ? r.w37 : (r.w36 || 0));
        const prev = r[prevKey] !== undefined ? r[prevKey] : (r.w36 !== undefined ? r.w36 : (r.w35 || 0));"""
js = js.replace(old_t2_full, new_t2_full)

old_t2_tts = """    const tblBodyTTS = document.querySelector('#table-vol-tts-detailed tbody');
    if (tblBodyTTS && D.san_luong.am_tts) {
      const fullMap = {};
      (D.san_luong.am_full || []).forEach(f => fullMap[f.am] = (f.w36 !== undefined ? f.w36 : (f.w35 || 0)));

      let listTTS = [...D.san_luong.am_tts].map(r => {
        const fullVol = fullMap[r.am] || 0;
        const curTTS = r.w36 !== undefined ? r.w36 : (r.w35 || 0);
        const prevTTS = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);"""

new_t2_tts = """    const tblBodyTTS = document.querySelector('#table-vol-tts-detailed tbody');
    if (tblBodyTTS && D.san_luong.am_tts) {
      const latestKey = D.meta?.latest_week ? D.meta.latest_week.toLowerCase() : 'w37';
      const prevKey = D.meta?.prev_week ? D.meta.prev_week.toLowerCase() : 'w36';
      const fullMap = {};
      (D.san_luong.am_full || []).forEach(f => fullMap[f.am] = (f[latestKey] !== undefined ? f[latestKey] : (f.w37 !== undefined ? f.w37 : (f.w36 || 0))));

      let listTTS = [...D.san_luong.am_tts].map(r => {
        const fullVol = fullMap[r.am] || 0;
        const curTTS = r[latestKey] !== undefined ? r[latestKey] : (r.w37 !== undefined ? r.w37 : (r.w36 || 0));
        const prevTTS = r[prevKey] !== undefined ? r[prevKey] : (r.w36 !== undefined ? r.w36 : (r.w35 || 0));"""
js = js.replace(old_t2_tts, new_t2_tts)

# 4. Tab 2 5-tinh tables
old_t2_tinh_full = """    // 3. BẢNG 3A: SẢN LƯỢNG 5 TỈNH THÀNH (FULL HÀNG)
    const tblBodyTinhFull = document.querySelector('#table-vol-tinh-full tbody');
    if (tblBodyTinhFull && D.san_luong) {
      const rawTinhFull = D.san_luong.tinh_full || D.san_luong.tinh || [];
      const listTinhFull = [...rawTinhFull].map(r => ({
        ...r,
        diff_val: r.diff !== undefined ? r.diff : ((r.w36 || r.vol || 0) - (r.w35 || 0))
      })).sort((a, b) => (b.w36 || b.vol || 0) - (a.w36 || a.vol || 0));

      tblBodyTinhFull.innerHTML = listTinhFull.map((row, i) => {
        const diffBadge = renderDeltaBadge(row.diff_val, true, false);
        const evalBadge = row.diff_val > 0
          ? '<span class="badge-tag badge-tag-green">🟢 Tăng Trưởng</span>'
          : '<span class="badge-tag badge-tag-blue">Giảm Nhẹ</span>';

        const v1 = row.w36 !== undefined ? row.w33 : row.w32;
        const v2 = row.w36 !== undefined ? row.w34 : row.w33;
        const v3 = row.w36 !== undefined ? row.w35 : row.w34;
        const v4 = row.w36 !== undefined ? (row.w36 || row.vol) : (row.w35 || row.vol);"""

new_t2_tinh_full = """    // 3. BẢNG 3A: SẢN LƯỢNG 5 TỈNH THÀNH (FULL HÀNG)
    const tblBodyTinhFull = document.querySelector('#table-vol-tinh-full tbody');
    if (tblBodyTinhFull && D.san_luong) {
      const wKeys = (D.meta?.weeks || ['W34', 'W35', 'W36', 'W37']).map(w => w.toLowerCase());
      const rawTinhFull = D.san_luong.tinh_full || D.san_luong.tinh || [];
      const listTinhFull = [...rawTinhFull].map(r => {
        const curr = r[wKeys[3]] !== undefined ? r[wKeys[3]] : (r.w37 || r.vol || 0);
        const prev = r[wKeys[2]] !== undefined ? r[wKeys[2]] : (r.w36 || 0);
        return {
          ...r,
          diff_val: r.diff !== undefined ? r.diff : (curr - prev)
        };
      }).sort((a, b) => (b[wKeys[3]] || b.vol || 0) - (a[wKeys[3]] || a.vol || 0));

      tblBodyTinhFull.innerHTML = listTinhFull.map((row, i) => {
        const diffBadge = renderDeltaBadge(row.diff_val, true, false);
        const evalBadge = row.diff_val > 0
          ? '<span class="badge-tag badge-tag-green">🟢 Tăng Trưởng</span>'
          : '<span class="badge-tag badge-tag-blue">Giảm Nhẹ</span>';

        const v1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
        const v2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
        const v3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
        const v4 = row[wKeys[3]] !== undefined ? row[wKeys[3]] : (row.w37 || row.vol || 0);"""
js = js.replace(old_t2_tinh_full, new_t2_tinh_full)

old_t2_tinh_tts = """      const totalTtsVol = rawTinhTTS.reduce((sum, r) => sum + (r.w36 !== undefined ? r.w36 : (r.w35 || r.vol || 0)), 0);
      const listTinhTTS = [...rawTinhTTS].map(r => {
        const ttsVol = r.w36 !== undefined ? r.w36 : (r.w35 || r.vol || 0);
        return {
          ...r,
          vol_tts: ttsVol,
          rate_tts: totalTtsVol > 0 ? (ttsVol / totalTtsVol) : 0,
          diff_val: r.diff !== undefined ? r.diff : (ttsVol - (r.w35 || 0))
        };
      }).sort((a, b) => (b.vol_tts || 0) - (a.vol_tts || 0));

      tblBodyTinhTTS.innerHTML = listTinhTTS.map((row, i) => {
        const diffBadge = renderDeltaBadge(row.diff_val, true, false);
        const evalBadge = row.diff_val > 0
          ? '<span class="badge-tag badge-tag-green">🟢 Tăng Trưởng</span>'
          : '<span class="badge-tag badge-tag-amber">Ổn Định</span>';

        const v1 = row.w36 !== undefined ? row.w33 : row.w32;
        const v2 = row.w36 !== undefined ? row.w34 : row.w33;
        const v3 = row.w36 !== undefined ? row.w35 : row.w34;
        const v4 = row.w36 !== undefined ? (row.w36 || row.vol) : (row.w35 || row.vol);"""

new_t2_tinh_tts = """      const wKeys = (D.meta?.weeks || ['W34', 'W35', 'W36', 'W37']).map(w => w.toLowerCase());
      const totalTtsVol = rawTinhTTS.reduce((sum, r) => sum + (r[wKeys[3]] !== undefined ? r[wKeys[3]] : (r.w37 || r.vol || 0)), 0);
      const listTinhTTS = [...rawTinhTTS].map(r => {
        const ttsVol = r[wKeys[3]] !== undefined ? r[wKeys[3]] : (r.w37 || r.vol || 0);
        const prevTts = r[wKeys[2]] !== undefined ? r[wKeys[2]] : (r.w36 || 0);
        return {
          ...r,
          vol_tts: ttsVol,
          rate_tts: totalTtsVol > 0 ? (ttsVol / totalTtsVol) : 0,
          diff_val: r.diff !== undefined ? r.diff : (ttsVol - prevTts)
        };
      }).sort((a, b) => (b.vol_tts || 0) - (a.vol_tts || 0));

      tblBodyTinhTTS.innerHTML = listTinhTTS.map((row, i) => {
        const diffBadge = renderDeltaBadge(row.diff_val, true, false);
        const evalBadge = row.diff_val > 0
          ? '<span class="badge-tag badge-tag-green">🟢 Tăng Trưởng</span>'
          : '<span class="badge-tag badge-tag-amber">Ổn Định</span>';

        const v1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
        const v2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
        const v3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
        const v4 = row[wKeys[3]] !== undefined ? row[wKeys[3]] : (row.w37 || row.vol || 0);"""
js = js.replace(old_t2_tinh_tts, new_t2_tinh_tts)

# 5. Tab 3 %GTC
old_t3_full = """    // 1. BẢNG 1A: %GTC FULL HÀNG (18 AM)
    const tblBodyFull = document.querySelector('#table-gtc-full-detailed tbody');
    if (tblBodyFull) {
      const rawFull = D.gtc_tong.am_full || D.gtc_tong.am || [];
      let listFull = [...rawFull].map(r => {
        const curr = r.w36 !== undefined ? r.w36 : (r.w35 || 0);
        const prev = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);"""

new_t3_full = """    // 1. BẢNG 1A: %GTC FULL HÀNG (18 AM)
    const tblBodyFull = document.querySelector('#table-gtc-full-detailed tbody');
    if (tblBodyFull) {
      const latestKey = D.meta?.latest_week ? D.meta.latest_week.toLowerCase() : 'w37';
      const prevKey = D.meta?.prev_week ? D.meta.prev_week.toLowerCase() : 'w36';
      const rawFull = D.gtc_tong.am_full || D.gtc_tong.am || [];
      let listFull = [...rawFull].map(r => {
        const curr = r[latestKey] !== undefined ? r[latestKey] : (r.w37 !== undefined ? r.w37 : (r.w36 || 0));
        const prev = r[prevKey] !== undefined ? r[prevKey] : (r.w36 !== undefined ? r.w36 : (r.w35 || 0));"""
js = js.replace(old_t3_full, new_t3_full)

old_t3_tts = """    // 2. BẢNG 1B: %GTC TIKTOK SHOP (18 AM)
    const tblBodyTTS = document.querySelector('#table-gtc-tts-detailed tbody');
    if (tblBodyTTS) {
      const rawTTS = D.gtc_tong.am_tts || [];
      let listTTS = [...rawTTS].map(r => {
        const curr = r.w36 !== undefined ? r.w36 : (r.w35 || 0);
        const prev = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);"""

new_t3_tts = """    // 2. BẢNG 1B: %GTC TIKTOK SHOP (18 AM)
    const tblBodyTTS = document.querySelector('#table-gtc-tts-detailed tbody');
    if (tblBodyTTS) {
      const latestKey = D.meta?.latest_week ? D.meta.latest_week.toLowerCase() : 'w37';
      const prevKey = D.meta?.prev_week ? D.meta.prev_week.toLowerCase() : 'w36';
      const rawTTS = D.gtc_tong.am_tts || [];
      let listTTS = [...rawTTS].map(r => {
        const curr = r[latestKey] !== undefined ? r[latestKey] : (r.w37 !== undefined ? r.w37 : (r.w36 || 0));
        const prev = r[prevKey] !== undefined ? r[prevKey] : (r.w36 !== undefined ? r.w36 : (r.w35 || 0));"""
js = js.replace(old_t3_tts, new_t3_tts)

old_t3_tinh_full = """    // 3. BẢNG 2A: %GTC 5 TỈNH THÀNH (FULL HÀNG)
    const tblBodyTinhFull = document.querySelector('#table-gtc-tinh-full tbody');
    if (tblBodyTinhFull) {
      const rawTinhFull = D.gtc_tong.tinh_full || D.gtc_tong.tinh || [];
      let listTinhFull = [...rawTinhFull].map(r => {
        const v4 = r.w36 !== undefined ? r.w36 : r.w35;
        const v3 = r.w36 !== undefined ? r.w35 : r.w34;
        return {
          ...r,
          curr_val: v4,
          diff_val: r.diff !== undefined ? r.diff : ((v4 || 0) - (v3 || 0))
        };
      }).sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

      tblBodyTinhFull.innerHTML = listTinhFull.map((row, i) => {
        const v1 = row.w36 !== undefined ? row.w33 : row.w32;
        const v2 = row.w36 !== undefined ? row.w34 : row.w33;
        const v3 = row.w36 !== undefined ? row.w35 : row.w34;
        const v4 = row.curr_val;"""

new_t3_tinh_full = """    // 3. BẢNG 2A: %GTC 5 TỈNH THÀNH (FULL HÀNG)
    const tblBodyTinhFull = document.querySelector('#table-gtc-tinh-full tbody');
    if (tblBodyTinhFull) {
      const wKeys = (D.meta?.weeks || ['W34', 'W35', 'W36', 'W37']).map(w => w.toLowerCase());
      const rawTinhFull = D.gtc_tong.tinh_full || D.gtc_tong.tinh || [];
      let listTinhFull = [...rawTinhFull].map(r => {
        const v4 = r[wKeys[3]] !== undefined ? r[wKeys[3]] : (r.w37 || r.vol || 0);
        const v3 = r[wKeys[2]] !== undefined ? r[wKeys[2]] : (r.w36 || 0);
        return {
          ...r,
          curr_val: v4,
          diff_val: r.diff !== undefined ? r.diff : ((v4 || 0) - (v3 || 0))
        };
      }).sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

      tblBodyTinhFull.innerHTML = listTinhFull.map((row, i) => {
        const v1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
        const v2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
        const v3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
        const v4 = row.curr_val;"""
js = js.replace(old_t3_tinh_full, new_t3_tinh_full)

old_t3_tinh_tts = """    // 4. BẢNG 2B: %GTC 5 TỈNH THÀNH (TIKTOK SHOP)
    const tblBodyTinhTTS = document.querySelector('#table-gtc-tinh-tts tbody');
    if (tblBodyTinhTTS) {
      const rawTinhTTS = D.gtc_tong.tinh_tts || [];
      let listTinhTTS = [...rawTinhTTS].map(r => {
        const v4 = r.w36 !== undefined ? r.w36 : r.w35;
        const v3 = r.w36 !== undefined ? r.w35 : r.w34;
        return {
          ...r,
          curr_val: v4,
          diff_val: r.diff !== undefined ? r.diff : ((v4 || 0) - (v3 || 0))
        };
      }).sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

      tblBodyTinhTTS.innerHTML = listTinhTTS.map((row, i) => {
        const v1 = row.w36 !== undefined ? row.w33 : row.w32;
        const v2 = row.w36 !== undefined ? row.w34 : row.w33;
        const v3 = row.w36 !== undefined ? row.w35 : row.w34;
        const v4 = row.curr_val;"""

new_t3_tinh_tts = """    // 4. BẢNG 2B: %GTC 5 TỈNH THÀNH (TIKTOK SHOP)
    const tblBodyTinhTTS = document.querySelector('#table-gtc-tinh-tts tbody');
    if (tblBodyTinhTTS) {
      const wKeys = (D.meta?.weeks || ['W34', 'W35', 'W36', 'W37']).map(w => w.toLowerCase());
      const rawTinhTTS = D.gtc_tong.tinh_tts || [];
      let listTinhTTS = [...rawTinhTTS].map(r => {
        const v4 = r[wKeys[3]] !== undefined ? r[wKeys[3]] : (r.w37 || r.vol || 0);
        const v3 = r[wKeys[2]] !== undefined ? r[wKeys[2]] : (r.w36 || 0);
        return {
          ...r,
          curr_val: v4,
          diff_val: r.diff !== undefined ? r.diff : ((v4 || 0) - (v3 || 0))
        };
      }).sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

      tblBodyTinhTTS.innerHTML = listTinhTTS.map((row, i) => {
        const v1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
        const v2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
        const v3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
        const v4 = row.curr_val;"""
js = js.replace(old_t3_tinh_tts, new_t3_tinh_tts)

# 6. Tab 4 Gan (Gán vận hành)
old_t4_overview = """        const v1 = row.w36 !== undefined ? row.w33 : row.w32;
        const v2 = row.w36 !== undefined ? row.w34 : row.w33;
        const v3 = row.w36 !== undefined ? row.w35 : row.w34;
        const v4 = row.w36 !== undefined ? row.w36 : row.w35;"""

new_t4_overview = """        const wKeys = (D.meta?.weeks || ['W34', 'W35', 'W36', 'W37']).map(w => w.toLowerCase());
        const v1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
        const v2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
        const v3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
        const v4 = row[wKeys[3]] !== undefined ? row[wKeys[3]] : (row.w37 || row.w36 || 0);"""
js = js.replace(old_t4_overview, new_t4_overview)

old_t4_ca1 = """    const tblBodyCa1 = document.querySelector('#table-gan-ca1-detailed tbody');
    if (tblBodyCa1) {
      let listCa1 = [...D.gan.am].map(r => {
        const curr = r.ca1ton_w36 !== undefined ? r.ca1ton_w36 : r.ca1ton_w35;
        const prev = r.ca1ton_w36 !== undefined ? r.ca1ton_w35 : r.ca1ton_w34;"""

new_t4_ca1 = """    const tblBodyCa1 = document.querySelector('#table-gan-ca1-detailed tbody');
    if (tblBodyCa1) {
      let listCa1 = [...D.gan.am].map(r => {
        const curr = r.ca1ton_w37 !== undefined ? r.ca1ton_w37 : (r.ca1ton_curr !== undefined ? r.ca1ton_curr : r.ca1ton_w36);
        const prev = r.ca1ton_w36 !== undefined ? r.ca1ton_w36 : (r.ca1ton_prev !== undefined ? r.ca1ton_prev : r.ca1ton_w35);"""
js = js.replace(old_t4_ca1, new_t4_ca1)

old_t4_ca2 = """    const tblBodyCa2 = document.querySelector('#table-gan-ca2-detailed tbody');
    if (tblBodyCa2) {
      let listCa2 = [...D.gan.am].map(r => {
        const curr = r.tong_w36 !== undefined ? r.tong_w36 : r.tong_w35;
        const prev = r.tong_w36 !== undefined ? r.tong_w35 : r.tong_w34;"""

new_t4_ca2 = """    const tblBodyCa2 = document.querySelector('#table-gan-ca2-detailed tbody');
    if (tblBodyCa2) {
      let listCa2 = [...D.gan.am].map(r => {
        const curr = r.tong_w37 !== undefined ? r.tong_w37 : (r.tong_curr !== undefined ? r.tong_curr : r.tong_w36);
        const prev = r.tong_w36 !== undefined ? r.tong_w36 : (r.tong_prev !== undefined ? r.tong_prev : r.tong_w35);"""
js = js.replace(old_t4_ca2, new_t4_ca2)

old_t4_chart = """    const sorted = [...D.gan.am].map(r => {
      const prev_val = r.tong_w36 !== undefined ? (r.tong_w35 || 0) : (r.tong_w34 || 0);
      const curr_val = r.tong_w36 !== undefined ? (r.tong_w36 || 0) : (r.tong_w35 || 0);
      const diff_val = r.tong_diff !== undefined ? r.tong_diff : (r.diff !== undefined ? r.diff : (curr_val - prev_val));
      const ca1 = r.ca1ton_w36 !== undefined ? r.ca1ton_w36 : (r.ca1ton_w35 || 0);
      const ca2 = r.ca2_w36 !== undefined ? r.ca2_w36 : (r.ca2_w35 || 0);"""

new_t4_chart = """    const sorted = [...D.gan.am].map(r => {
      const prev_val = r.tong_w36 !== undefined ? r.tong_w36 : (r.tong_prev !== undefined ? r.tong_prev : (r.tong_w35 || 0));
      const curr_val = r.tong_w37 !== undefined ? r.tong_w37 : (r.tong_curr !== undefined ? r.tong_curr : (r.tong_w36 || 0));
      const diff_val = r.tong_diff !== undefined ? r.tong_diff : (curr_val - prev_val);
      const ca1 = r.ca1ton_w37 !== undefined ? r.ca1ton_w37 : (r.ca1ton_curr !== undefined ? r.ca1ton_curr : (r.ca1ton_w36 || 0));
      const ca2 = r.ca2_w37 !== undefined ? r.ca2_w37 : (r.ca2_curr !== undefined ? r.ca2_curr : (r.ca2_w36 || 0));"""
js = js.replace(old_t4_chart, new_t4_chart)

# 7. Tab 6 %ODR
old_t6_full = """    // 1. BẢNG 1A: %ODR FULL HÀNG (18 AM)
    const tblBodyFull = document.querySelector('#table-odr-full-detailed tbody');
    if (tblBodyFull) {
      const rawFull = D.odr.am_full || D.odr.am || [];
      let listFull = [...rawFull].map(r => {
        const curr = r.w36 !== undefined ? r.w36 : (r.w35 || 0);
        const prev = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);"""

new_t6_full = """    // 1. BẢNG 1A: %ODR FULL HÀNG (18 AM)
    const tblBodyFull = document.querySelector('#table-odr-full-detailed tbody');
    if (tblBodyFull) {
      const latestKey = D.meta?.latest_week ? D.meta.latest_week.toLowerCase() : 'w37';
      const prevKey = D.meta?.prev_week ? D.meta.prev_week.toLowerCase() : 'w36';
      const rawFull = D.odr.am_full || D.odr.am || [];
      let listFull = [...rawFull].map(r => {
        const curr = r[latestKey] !== undefined ? r[latestKey] : (r.w37 !== undefined ? r.w37 : (r.w36 || 0));
        const prev = r[prevKey] !== undefined ? r[prevKey] : (r.w36 !== undefined ? r.w36 : (r.w35 || 0));"""
js = js.replace(old_t6_full, new_t6_full)

old_t6_tts = """    // 2. BẢNG 1B: %ODR TIKTOK SHOP (18 AM)
    const tblBodyTTS = document.querySelector('#table-odr-tts-detailed tbody');
    if (tblBodyTTS) {
      const rawTTS = D.odr.am_tts || [];
      let listTTS = [...rawTTS].map(r => {
        const curr = r.w36 !== undefined ? r.w36 : (r.w35 || 0);
        const prev = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);"""

new_t6_tts = """    // 2. BẢNG 1B: %ODR TIKTOK SHOP (18 AM)
    const tblBodyTTS = document.querySelector('#table-odr-tts-detailed tbody');
    if (tblBodyTTS) {
      const latestKey = D.meta?.latest_week ? D.meta.latest_week.toLowerCase() : 'w37';
      const prevKey = D.meta?.prev_week ? D.meta.prev_week.toLowerCase() : 'w36';
      const rawTTS = D.odr.am_tts || [];
      let listTTS = [...rawTTS].map(r => {
        const curr = r[latestKey] !== undefined ? r[latestKey] : (r.w37 !== undefined ? r.w37 : (r.w36 || 0));
        const prev = r[prevKey] !== undefined ? r[prevKey] : (r.w36 !== undefined ? r.w36 : (r.w35 || 0));"""
js = js.replace(old_t6_tts, new_t6_tts)

old_t6_tinh_full = """    // 3. BẢNG 2A: %ODR 5 TỈNH THÀNH (FULL HÀNG)
    const tblBodyTinhFull = document.querySelector('#table-odr-tinh-full tbody');
    if (tblBodyTinhFull) {
      const rawTinhFull = D.odr.tinh_full || D.odr.tinh || [];
      let listTinhFull = [...rawTinhFull].map(r => {
        const v4 = r.w36 !== undefined ? r.w36 : r.w35;
        const v3 = r.w36 !== undefined ? r.w35 : r.w34;
        return {
          ...r,
          curr_val: v4,
          diff_val: r.diff !== undefined ? r.diff : ((v4 || 0) - (v3 || 0))
        };
      }).sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

      tblBodyTinhFull.innerHTML = listTinhFull.map((row, i) => {
        const v1 = row.w36 !== undefined ? row.w33 : row.w32;
        const v2 = row.w36 !== undefined ? row.w34 : row.w33;
        const v3 = row.w36 !== undefined ? row.w35 : row.w34;
        const v4 = row.curr_val;"""

new_t6_tinh_full = """    // 3. BẢNG 2A: %ODR 5 TỈNH THÀNH (FULL HÀNG)
    const tblBodyTinhFull = document.querySelector('#table-odr-tinh-full tbody');
    if (tblBodyTinhFull) {
      const wKeys = (D.meta?.weeks || ['W34', 'W35', 'W36', 'W37']).map(w => w.toLowerCase());
      const rawTinhFull = D.odr.tinh_full || D.odr.tinh || [];
      let listTinhFull = [...rawTinhFull].map(r => {
        const v4 = r[wKeys[3]] !== undefined ? r[wKeys[3]] : (r.w37 || r.vol || 0);
        const v3 = r[wKeys[2]] !== undefined ? r[wKeys[2]] : (r.w36 || 0);
        return {
          ...r,
          curr_val: v4,
          diff_val: r.diff !== undefined ? r.diff : ((v4 || 0) - (v3 || 0))
        };
      }).sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

      tblBodyTinhFull.innerHTML = listTinhFull.map((row, i) => {
        const v1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
        const v2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
        const v3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
        const v4 = row.curr_val;"""
js = js.replace(old_t6_tinh_full, new_t6_tinh_full)

old_t6_tinh_tts = """    // 4. BẢNG 2B: %ODR 5 TỈNH THÀNH (TIKTOK SHOP)
    const tblBodyTinhTTS = document.querySelector('#table-odr-tinh-tts tbody');
    if (tblBodyTinhTTS) {
      const rawTinhTTS = D.odr.tinh_tts || [];
      let listTinhTTS = [...rawTinhTTS].map(r => {
        const v4 = r.w36 !== undefined ? r.w36 : r.w35;
        const v3 = r.w36 !== undefined ? r.w35 : r.w34;
        return {
          ...r,
          curr_val: v4,
          diff_val: r.diff !== undefined ? r.diff : ((v4 || 0) - (v3 || 0))
        };
      }).sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

      tblBodyTinhTTS.innerHTML = listTinhTTS.map((row, i) => {
        const v1 = row.w36 !== undefined ? row.w33 : row.w32;
        const v2 = row.w36 !== undefined ? row.w34 : row.w33;
        const v3 = row.w36 !== undefined ? row.w35 : row.w34;
        const v4 = row.curr_val;"""

new_t6_tinh_tts = """    // 4. BẢNG 2B: %ODR 5 TỈNH THÀNH (TIKTOK SHOP)
    const tblBodyTinhTTS = document.querySelector('#table-odr-tinh-tts tbody');
    if (tblBodyTinhTTS) {
      const wKeys = (D.meta?.weeks || ['W34', 'W35', 'W36', 'W37']).map(w => w.toLowerCase());
      const rawTinhTTS = D.odr.tinh_tts || [];
      let listTinhTTS = [...rawTinhTTS].map(r => {
        const v4 = r[wKeys[3]] !== undefined ? r[wKeys[3]] : (r.w37 || r.vol || 0);
        const v3 = r[wKeys[2]] !== undefined ? r[wKeys[2]] : (r.w36 || 0);
        return {
          ...r,
          curr_val: v4,
          diff_val: r.diff !== undefined ? r.diff : ((v4 || 0) - (v3 || 0))
        };
      }).sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

      tblBodyTinhTTS.innerHTML = listTinhTTS.map((row, i) => {
        const v1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
        const v2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
        const v3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
        const v4 = row.curr_val;"""
js = js.replace(old_t6_tinh_tts, new_t6_tinh_tts)

# 8. Tab 7 %LTC
old_t7_am = """    // 1. BẢNG 1: 18 AM
    const tblBodyAM = document.querySelector('#table-ltc-detailed tbody');
    if (tblBodyAM && D.ltc.am) {
      let list = [...D.ltc.am].map(r => {
        const v4 = r.w36 !== undefined ? r.w36 : r.w35;
        const v3 = r.w36 !== undefined ? r.w35 : r.w34;
        return {
          ...r,
          curr_val: v4,
          diff_val: r.diff !== undefined ? r.diff : ((v4 || 0) - (v3 || 0))
        };
      }).sort((a, b) => b.diff_val - a.diff_val);

      tblBodyAM.innerHTML = list.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const v1 = row.w36 !== undefined ? row.w33 : row.w32;
        const v2 = row.w36 !== undefined ? row.w34 : row.w33;
        const v3 = row.w36 !== undefined ? row.w35 : row.w34;
        const v4 = row.curr_val;"""

new_t7_am = """    // 1. BẢNG 1: 18 AM
    const tblBodyAM = document.querySelector('#table-ltc-detailed tbody');
    if (tblBodyAM && D.ltc.am) {
      const wKeys = (D.meta?.weeks || ['W34', 'W35', 'W36', 'W37']).map(w => w.toLowerCase());
      let list = [...D.ltc.am].map(r => {
        const v4 = r[wKeys[3]] !== undefined ? r[wKeys[3]] : (r.w37 || r.w36 || 0);
        const v3 = r[wKeys[2]] !== undefined ? r[wKeys[2]] : (r.w36 || r.w35 || 0);
        return {
          ...r,
          curr_val: v4,
          diff_val: r.diff !== undefined ? r.diff : ((v4 || 0) - (v3 || 0))
        };
      }).sort((a, b) => b.diff_val - a.diff_val);

      tblBodyAM.innerHTML = list.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const v1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
        const v2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
        const v3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
        const v4 = row.curr_val;"""
js = js.replace(old_t7_am, new_t7_am)

old_t7_tinh = """    // 2. BẢNG 2: 5 TỈNH THÀNH (FULL HÀNG HOẶC TIKTOK SHOP)
    const tblBodyTinh = document.querySelector('#table-ltc-tinh-detailed tbody');
    if (tblBodyTinh && D.ltc) {
      const seg = state.ltcTinhSegment || 'full';
      const rawList = seg === 'tts' ? (D.ltc.tinh_tts || []) : (D.ltc.tinh_full || D.ltc.tinh || []);

      let listTinh = [...rawList].map(r => {
        const v4 = r.w36 !== undefined ? r.w36 : r.w35;
        const v3 = r.w36 !== undefined ? r.w35 : r.w34;
        return {
          ...r,
          curr_val: v4,
          diff_val: r.diff !== undefined ? r.diff : ((v4 || 0) - (v3 || 0))
        };
      }).sort((a, b) => b.diff_val - a.diff_val);

      tblBodyTinh.innerHTML = listTinh.map((row, i) => {
        const v1 = row.w36 !== undefined ? row.w33 : row.w32;
        const v2 = row.w36 !== undefined ? row.w34 : row.w33;
        const v3 = row.w36 !== undefined ? row.w35 : row.w34;
        const v4 = row.curr_val;"""

new_t7_tinh = """    // 2. BẢNG 2: 5 TỈNH THÀNH (FULL HÀNG HOẶC TIKTOK SHOP)
    const tblBodyTinh = document.querySelector('#table-ltc-tinh-detailed tbody');
    if (tblBodyTinh && D.ltc) {
      const wKeys = (D.meta?.weeks || ['W34', 'W35', 'W36', 'W37']).map(w => w.toLowerCase());
      const seg = state.ltcTinhSegment || 'full';
      const rawList = seg === 'tts' ? (D.ltc.tinh_tts || []) : (D.ltc.tinh_full || D.ltc.tinh || []);

      let listTinh = [...rawList].map(r => {
        const v4 = r[wKeys[3]] !== undefined ? r[wKeys[3]] : (r.w37 || r.w36 || 0);
        const v3 = r[wKeys[2]] !== undefined ? r[wKeys[2]] : (r.w36 || r.w35 || 0);
        return {
          ...r,
          curr_val: v4,
          diff_val: r.diff !== undefined ? r.diff : ((v4 || 0) - (v3 || 0))
        };
      }).sort((a, b) => b.diff_val - a.diff_val);

      tblBodyTinh.innerHTML = listTinh.map((row, i) => {
        const v1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
        const v2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
        const v3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
        const v4 = row.curr_val;"""
js = js.replace(old_t7_tinh, new_t7_tinh)

# 9. Tab 8 %OPR TTS
js = js.replace("OPR TTS Toàn Vùng W36 (Tổng Ngày + Đêm)", "OPR TTS Toàn Vùng W37 (Tổng Ngày + Đêm)")
js = js.replace("(W35: ${(_vung35*100).toFixed(1)}%)", "(W36: ${(_vung35*100).toFixed(1)}%)")

old_opr_agg = """    const _vung36Day = _volDay > 0 ? _ams.reduce((s, r) => s + (r.vol_day || 0) * (r.w36_day || 0), 0) / _volDay : 0;
    const _vung36Night = _volNight > 0 ? _ams.reduce((s, r) => s + (r.vol_night || 0) * (r.w36_night || 0), 0) / _volNight : 0;
    const _wtd36 = _ams.reduce((s, r) => {
      const vol = (r.vol_day||0) + (r.vol_night||0);
      const o36 = vol > 0 ? ((r.vol_day||0)*(r.w36_day||0) + (r.vol_night||0)*(r.w36_night||0)) / vol : 0;
      return s + vol * o36;
    }, 0);
    const _wtd35 = _ams.reduce((s, r) => {
      const vol = (r.vol_day||0) + (r.vol_night||0);
      const o35 = vol > 0 ? ((r.vol_day||0)*(r.w35_day||0) + (r.vol_night||0)*(r.w35_night||0)) / vol : 0;
      return s + vol * o35;
    }, 0);"""

new_opr_agg = """    const _vung36Day = _volDay > 0 ? _ams.reduce((s, r) => s + (r.vol_day || 0) * (r.w37_day !== undefined ? r.w37_day : (r.w36_day || 0)), 0) / _volDay : 0;
    const _vung36Night = _volNight > 0 ? _ams.reduce((s, r) => s + (r.vol_night || 0) * (r.w37_night !== undefined ? r.w37_night : (r.w36_night || 0)), 0) / _volNight : 0;
    const _wtd36 = _ams.reduce((s, r) => {
      const vol = (r.vol_day||0) + (r.vol_night||0);
      const curD = r.w37_day !== undefined ? r.w37_day : (r.w36_day || 0);
      const curN = r.w37_night !== undefined ? r.w37_night : (r.w36_night || 0);
      const o36 = vol > 0 ? ((r.vol_day||0)*curD + (r.vol_night||0)*curN) / vol : 0;
      return s + vol * o36;
    }, 0);
    const _wtd35 = _ams.reduce((s, r) => {
      const vol = (r.vol_day||0) + (r.vol_night||0);
      const prvD = r.w36_day !== undefined ? r.w36_day : (r.w35_day || 0);
      const prvN = r.w36_night !== undefined ? r.w36_night : (r.w35_night || 0);
      const o35 = vol > 0 ? ((r.vol_day||0)*prvD + (r.vol_night||0)*prvN) / vol : 0;
      return s + vol * o35;
    }, 0);"""
js = js.replace(old_opr_agg, new_opr_agg)

old_opr_tbl1 = """      let listDay = [...D.opr_tts.am].map(r => {
        const curr = r.w36_day !== undefined ? r.w36_day : r.w35_day;
        const prev = r.w36_day !== undefined ? r.w35_day : r.w34_day;"""

new_opr_tbl1 = """      let listDay = [...D.opr_tts.am].map(r => {
        const curr = r.w37_day !== undefined ? r.w37_day : (r.w36_day || 0);
        const prev = r.w36_day !== undefined ? r.w36_day : (r.w35_day || 0);"""
js = js.replace(old_opr_tbl1, new_opr_tbl1)

old_opr_tbl2 = """      let listNight = [...D.opr_tts.am].map(r => {
        const curr = r.w36_night !== undefined ? r.w36_night : r.w35_night;
        const prev = r.w36_night !== undefined ? r.w35_night : r.w34_night;"""

new_opr_tbl2 = """      let listNight = [...D.opr_tts.am].map(r => {
        const curr = r.w37_night !== undefined ? r.w37_night : (r.w36_night || 0);
        const prev = r.w36_night !== undefined ? r.w36_night : (r.w35_night || 0);"""
js = js.replace(old_opr_tbl2, new_opr_tbl2)

old_opr_detail = """        const rawDay = (row.vol_day === 0 || (row.w36_day || 0) > 1) ? 0 : (row.w36_day !== undefined ? row.w36_day : 0);
        const prevDay = row.w36_day !== undefined ? row.w35_day : row.w34_day;
        const rawNight = (row.vol_night === 0 || (row.w36_night || 0) > 1) ? 0 : (row.w36_night !== undefined ? row.w36_night : 0);
        const prevNight = row.w36_night !== undefined ? row.w35_night : row.w34_night;"""

new_opr_detail = """        const rawDay = (row.vol_day === 0) ? 0 : (row.w37_day !== undefined ? row.w37_day : (row.w36_day || 0));
        const prevDay = row.w36_day !== undefined ? row.w36_day : (row.w35_day || 0);
        const rawNight = (row.vol_night === 0) ? 0 : (row.w37_night !== undefined ? row.w37_night : (row.w36_night || 0));
        const prevNight = row.w36_night !== undefined ? row.w36_night : (row.w35_night || 0);"""
js = js.replace(old_opr_detail, new_opr_detail)

# 10. Tab 9 % Rớt LC
old_t9_am = """      const totalRotAM = D.rot_lc.am.reduce((s, r) => {
        const wCurr = r.w36 !== undefined ? (r.w36 || 0) : (r.w35 || 0);
        return s + Math.round((r.vol || 0) * wCurr);
      }, 0);

      let listAM = [...D.rot_lc.am].map(r => {
        const wPrev = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);
        const wCurr = r.w36 !== undefined ? (r.w36 || 0) : (r.w35 || 0);"""

new_t9_am = """      const totalRotAM = D.rot_lc.am.reduce((s, r) => {
        const wCurr = r.w37 !== undefined ? (r.w37 || 0) : (r.w36 || 0);
        return s + Math.round((r.vol || 0) * wCurr);
      }, 0);

      let listAM = [...D.rot_lc.am].map(r => {
        const wPrev = r.w36 !== undefined ? (r.w36 || 0) : (r.w35 || 0);
        const wCurr = r.w37 !== undefined ? (r.w37 || 0) : (r.w36 || 0);"""
js = js.replace(old_t9_am, new_t9_am)

old_t9_tinh = """      const totalRotTinh = D.rot_lc.tinh.reduce((s, r) => {
        const wCurr = r.w36 !== undefined ? (r.w36 || 0) : (r.w35 || 0);
        return s + Math.round((r.vol || 0) * wCurr);
      }, 0);

      let listTinh = [...D.rot_lc.tinh].map(r => {
        const wPrev = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);
        const wCurr = r.w36 !== undefined ? (r.w36 || 0) : (r.w35 || 0);"""

new_t9_tinh = """      const totalRotTinh = D.rot_lc.tinh.reduce((s, r) => {
        const wCurr = r.w37 !== undefined ? (r.w37 || 0) : (r.w36 || 0);
        return s + Math.round((r.vol || 0) * wCurr);
      }, 0);

      let listTinh = [...D.rot_lc.tinh].map(r => {
        const wPrev = r.w36 !== undefined ? (r.w36 || 0) : (r.w35 || 0);
        const wCurr = r.w37 !== undefined ? (r.w37 || 0) : (r.w36 || 0);"""
js = js.replace(old_t9_tinh, new_t9_tinh)

# 11. Tab 10 %FD Chart label
js = js.replace("label: mode === 'tts' ? '%FD TTS W35 (Tuần Trước)' : '%FD Full W35 (Tuần Trước)',",
                "label: mode === 'tts' ? '%FD TTS W36 (Tuần Trước)' : '%FD Full W36 (Tuần Trước)',")
js = js.replace("label: mode === 'tts' ? '%FD TTS W36 (Hiện Tại)' : '%FD Full W36 (Hiện Tại)',",
                "label: mode === 'tts' ? '%FD TTS W37 (Hiện Tại)' : '%FD Full W37 (Hiện Tại)',")

# 12. Tab 12 Kinh Doanh (Truy thu)
js = js.replace("label: 'Kỳ 23–29/8 (W35) (Triệu VNĐ)',", "label: 'Kỳ 30/8–5/9 (W36) (Triệu VNĐ)',")
js = js.replace("label: 'Kỳ 30/8–5/9 (W36) (Triệu VNĐ)',", "label: 'Kỳ 6–12/9 (W37) (Triệu VNĐ)',")

# 13. Tab 13 KTC Xe tải
js = js.replace("Chuyến W35", "Chuyến W36")
js = js.replace("Chuyến W36", "Chuyến W37")
js = js.replace("TLLĐ W35", "TLLĐ W36")
js = js.replace("TLLĐ W36", "TLLĐ W37")
js = js.replace("r.chuyen_w35", "r.chuyen_w36")
js = js.replace("r.chuyen_w36", "r.chuyen_w37")
js = js.replace("r.tld_w35", "r.tld_w36")
js = js.replace("r.tld_w36", "r.tld_w37")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("✓ app.js saved successfully!")
