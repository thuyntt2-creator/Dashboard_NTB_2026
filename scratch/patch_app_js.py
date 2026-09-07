import sys

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Patch Volume Tab (tblBodyFull)
old_vol_full = '''      let list = [...D.san_luong.am_full].map(r => ({
        ...r,
        diff_val: r.diff !== undefined ? r.diff : ((r.w35 || 0) - (r.w34 || 0))
      }));'''

new_vol_full = '''      let list = [...D.san_luong.am_full].map(r => {
        const curr = r.w36 !== undefined ? r.w36 : (r.w35 || 0);
        const prev = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);
        return {
          ...r,
          curr_val: curr,
          prev_val: prev,
          diff_val: r.diff !== undefined ? r.diff : (curr - prev)
        };
      });'''

if old_vol_full in js:
    js = js.replace(old_vol_full, new_vol_full)
    print("Patched old_vol_full")

old_vol_full_row = '''            <td class="num">${fNum(row.w34)}</td>
            <td class="num bold" style="background: var(--color-blue-bg); font-weight:800;">${fNum(row.w35)}</td>'''

new_vol_full_row = '''            <td class="num">${fNum(row.prev_val)}</td>
            <td class="num bold" style="background: var(--color-blue-bg); font-weight:800;">${fNum(row.curr_val)}</td>'''

if old_vol_full_row in js:
    js = js.replace(old_vol_full_row, new_vol_full_row)
    print("Patched old_vol_full_row")

# 2. Patch Volume Tab (tblBodyTTS)
old_vol_tts = '''      const fullMap = {};
      (D.san_luong.am_full || []).forEach(f => fullMap[f.am] = (f.w35 || 0));

      let listTTS = [...D.san_luong.am_tts].map(r => {
        const fullVol = fullMap[r.am] || 0;
        const rate = fullVol > 0 ? ((r.w35 || 0) / fullVol) : 0;
        return {
          ...r,
          rate_tts: rate,
          diff_val: r.diff !== undefined ? r.diff : ((r.w35 || 0) - (r.w34 || 0))
        };
      });'''

new_vol_tts = '''      const fullMap = {};
      (D.san_luong.am_full || []).forEach(f => fullMap[f.am] = (f.w36 !== undefined ? f.w36 : (f.w35 || 0)));

      let listTTS = [...D.san_luong.am_tts].map(r => {
        const fullVol = fullMap[r.am] || 0;
        const curTTS = r.w36 !== undefined ? r.w36 : (r.w35 || 0);
        const prevTTS = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);
        const rate = fullVol > 0 ? (curTTS / fullVol) : 0;
        return {
          ...r,
          curr_val: curTTS,
          prev_val: prevTTS,
          rate_tts: rate,
          diff_val: r.diff !== undefined ? r.diff : (curTTS - prevTTS)
        };
      });'''

if old_vol_tts in js:
    js = js.replace(old_vol_tts, new_vol_tts)
    print("Patched old_vol_tts")

old_vol_tts_row = '''            <td class="num">${fNum(row.w34)}</td>
            <td class="num bold" style="background: var(--color-amber-bg); color:#ea580c; font-weight:800;">${fNum(row.w35)}</td>'''

new_vol_tts_row = '''            <td class="num">${fNum(row.prev_val)}</td>
            <td class="num bold" style="background: var(--color-amber-bg); color:#ea580c; font-weight:800;">${fNum(row.curr_val)}</td>'''

if old_vol_tts_row in js:
    js = js.replace(old_vol_tts_row, new_vol_tts_row)
    print("Patched old_vol_tts_row")

# 3. Patch GTC Tổng Tab (tblBodyFull)
old_gtc_full = '''      let listFull = [...rawFull].map(r => ({
        ...r,
        diff_val: r.diff !== undefined ? r.diff : ((r.w35 || 0) - (r.w34 || 0))
      }));'''

new_gtc_full = '''      let listFull = [...rawFull].map(r => {
        const curr = r.w36 !== undefined ? r.w36 : (r.w35 || 0);
        const prev = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);
        return {
          ...r,
          curr_val: curr,
          prev_val: prev,
          diff_val: r.diff !== undefined ? r.diff : (curr - prev)
        };
      });'''

if old_gtc_full in js:
    js = js.replace(old_gtc_full, new_gtc_full, 1)
    print("Patched old_gtc_full")

old_gtc_full_body = '''        const heatW35 = getHeatmapClass(row.w35, 'gtc');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = getGtcEvalBadge(row.w35);

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.w34)}</td>
            <td class="num bold ${heatW35}">${fPct(row.w35)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;'''

new_gtc_full_body = '''        const heatCurr = getHeatmapClass(row.curr_val, 'gtc');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = getGtcEvalBadge(row.curr_val);

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.prev_val)}</td>
            <td class="num bold ${heatCurr}">${fPct(row.curr_val)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;'''

if old_gtc_full_body in js:
    js = js.replace(old_gtc_full_body, new_gtc_full_body, 1)
    print("Patched old_gtc_full_body")

# 4. Patch GTC Tổng Tab (tblBodyTTS)
old_gtc_tts = '''      let listTTS = [...rawTTS].map(r => ({
        ...r,
        diff_val: r.diff !== undefined ? r.diff : ((r.w35 || 0) - (r.w34 || 0))
      }));'''

new_gtc_tts = '''      let listTTS = [...rawTTS].map(r => {
        const curr = r.w36 !== undefined ? r.w36 : (r.w35 || 0);
        const prev = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);
        return {
          ...r,
          curr_val: curr,
          prev_val: prev,
          diff_val: r.diff !== undefined ? r.diff : (curr - prev)
        };
      });'''

if old_gtc_tts in js:
    js = js.replace(old_gtc_tts, new_gtc_tts, 1)
    print("Patched old_gtc_tts")

old_gtc_tts_body = '''        const heatW35 = getHeatmapClass(row.w35, 'gtc');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = getGtcEvalBadge(row.w35);

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.w34)}</td>
            <td class="num bold ${heatW35}">${fPct(row.w35)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;'''

new_gtc_tts_body = '''        const heatCurr = getHeatmapClass(row.curr_val, 'gtc');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = getGtcEvalBadge(row.curr_val);

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.prev_val)}</td>
            <td class="num bold ${heatCurr}">${fPct(row.curr_val)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;'''

if old_gtc_tts_body in js:
    js = js.replace(old_gtc_tts_body, new_gtc_tts_body, 1)
    print("Patched old_gtc_tts_body")

# 5. Patch Gan Tab (Gán Tổng row template)
old_gan_ca2_row = '''            <td class="num">${fPct(row.tong_w34)}</td>
            <td class="num bold ${heatTong}" style="font-weight:800;">${fPct(row.tong_w35)}</td>'''

new_gan_ca2_row = '''            <td class="num">${fPct(row.prev_val)}</td>
            <td class="num bold ${heatTong}" style="font-weight:800;">${fPct(row.curr_val)}</td>'''

if old_gan_ca2_row in js:
    js = js.replace(old_gan_ca2_row, new_gan_ca2_row)
    print("Patched old_gan_ca2_row")

# 6. Patch ODR Tab (tblBodyFull and tblBodyTTS)
old_odr_full = '''      const rawFull = D.odr.am_full || D.odr.am || [];
      let listFull = [...rawFull].map(r => ({
        ...r,
        diff_val: r.diff !== undefined ? r.diff : ((r.w35 || 0) - (r.w34 || 0))
      }));'''

new_odr_full = '''      const rawFull = D.odr.am_full || D.odr.am || [];
      let listFull = [...rawFull].map(r => {
        const curr = r.w36 !== undefined ? r.w36 : (r.w35 || 0);
        const prev = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);
        return {
          ...r,
          curr_val: curr,
          prev_val: prev,
          diff_val: r.diff !== undefined ? r.diff : (curr - prev)
        };
      });'''

if old_odr_full in js:
    js = js.replace(old_odr_full, new_odr_full, 1)
    print("Patched old_odr_full")

old_odr_full_body = '''        const heatW35 = getHeatmapClass(row.w35, 'odr');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = getOdrEvalBadge(row.w35);

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.w34)}</td>
            <td class="num bold ${heatW35}">${fPct(row.w35)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;'''

new_odr_full_body = '''        const heatCurr = getHeatmapClass(row.curr_val, 'odr');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = getOdrEvalBadge(row.curr_val);

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.prev_val)}</td>
            <td class="num bold ${heatCurr}">${fPct(row.curr_val)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;'''

if old_odr_full_body in js:
    js = js.replace(old_odr_full_body, new_odr_full_body, 1)
    print("Patched old_odr_full_body")

old_odr_tts = '''      const rawTTS = D.odr.am_tts || [];
      let listTTS = [...rawTTS].map(r => ({
        ...r,
        diff_val: r.diff !== undefined ? r.diff : ((r.w35 || 0) - (r.w34 || 0))
      }));'''

new_odr_tts = '''      const rawTTS = D.odr.am_tts || [];
      let listTTS = [...rawTTS].map(r => {
        const curr = r.w36 !== undefined ? r.w36 : (r.w35 || 0);
        const prev = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);
        return {
          ...r,
          curr_val: curr,
          prev_val: prev,
          diff_val: r.diff !== undefined ? r.diff : (curr - prev)
        };
      });'''

if old_odr_tts in js:
    js = js.replace(old_odr_tts, new_odr_tts, 1)
    print("Patched old_odr_tts")

old_odr_tts_body = '''        const heatW35 = getHeatmapClass(row.w35, 'odr');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = getOdrEvalBadge(row.w35);

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.w34)}</td>
            <td class="num bold ${heatW35}">${fPct(row.w35)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;'''

new_odr_tts_body = '''        const heatCurr = getHeatmapClass(row.curr_val, 'odr');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = getOdrEvalBadge(row.curr_val);

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.prev_val)}</td>
            <td class="num bold ${heatCurr}">${fPct(row.curr_val)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;'''

if old_odr_tts_body in js:
    js = js.replace(old_odr_tts_body, new_odr_tts_body, 1)
    print("Patched old_odr_tts_body")

# 7. Add renderKdChurnTable and call it in renderCommercialTab
churn_func = '''  function renderKdChurnTable() {
    const tbody = document.querySelector('#table-kd-churn-top10 tbody');
    if (!tbody || !D.kinh_doanh || !D.kinh_doanh.churn_top10) return;

    tbody.innerHTML = D.kinh_doanh.churn_top10.map((row, i) => {
      const isSelected = state.selectedAM === row.am;
      const rowClass = isSelected ? 'presenter-laser-box' : '';
      const isZero = row.vol_curr === 0;
      const statusBadge = isZero
        ? '<span class="badge-tag badge-tag-red" style="font-weight:800;">🔴 Rời Bỏ (0 đơn)</span>'
        : `<span class="badge-tag badge-tag-amber">🟡 Giảm Mạnh (${row.pct_diff}%)</span>`;

      return `
        <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
          <td class="center bold">${row.stt || (i + 1)}</td>
          <td class="bold" style="color: var(--ghn-orange); font-size: 12.5px;">${row.makh}</td>
          <td class="bold" style="font-size: 13px;">${row.tenkh}</td>
          <td class="bold" style="color:${isSelected ? '#ef4444' : 'inherit'}; font-size: 13px;">${row.am}</td>
          <td style="font-size: 12px; color: var(--text-muted);">${row.bc}</td>
          <td class="num bold">${fNum(row.vol_prev)}</td>
          <td class="num bold" style="background: rgba(239, 68, 68, 0.1); color: #dc2626;">${fNum(row.vol_curr)}</td>
          <td class="num bold" style="color: #ef4444;">${fNum(row.diff)}</td>
          <td class="num bold" style="color: #ef4444;">${row.pct_diff}%</td>
          <td class="center">${statusBadge}</td>
        </tr>
      `;
    }).join('');
  }
'''

if 'function renderKdChurnTable' not in js:
    # insert before renderCommercialTab
    pos = js.find('function renderCommercialTab() {')
    assert pos != -1, "renderCommercialTab not found!"
    js = js[:pos] + churn_func + '\n  ' + js[pos:]
    
    # inside renderCommercialTab, call renderKdChurnTable()
    call_target = 'renderCommercialTab() {'
    call_repl = 'renderCommercialTab() {\n    renderKdChurnTable();'
    js = js.replace(call_target, call_repl, 1)
    print("Added renderKdChurnTable to renderCommercialTab")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("app.js updated successfully!")
