import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Fix renderGtcTtsCa1Tab: add tblBody.innerHTML = rowsHtml;
old_render_ca1 = """      tblBody.innerHTML = list.map((row, i) => {"""
# Wait, let's check how renderGtcTtsCa1Tab is structured around line 2760
# Let's inspect lines 2760 to 2785
pattern_ca1 = r'(function renderGtcTtsCa1Tab\(\) \{[\s\S]*?const rowsHtml = list\.map\([\s\S]*?\}\)\.join\(\'\'\);)(\s*\})'
replacement_ca1 = r'\1\n      tblBody.innerHTML = rowsHtml;\2'

if re.search(pattern_ca1, code):
    code = re.sub(pattern_ca1, replacement_ca1, code, count=1)
    print("SUCCESS: Fixed renderGtcTtsCa1Tab missing innerHTML assignment!")
else:
    print("FAILED: Could not match renderGtcTtsCa1Tab pattern!")

# 2. Fix getGtcCa1TtsData keys
old_get_ca1 = """  function getGtcCa1TtsData() {
    const prevKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2].toLowerCase() : 'w36';
    const currKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1].toLowerCase() : 'w37';
    const rawList = (D.gtc_ca1_thuan && D.gtc_ca1_thuan.am_tts) || (D.gtc_ca1_ton && D.gtc_ca1_ton.am_tts) || (D.gtc_tong && D.gtc_tong.am_tts) || [];
    return rawList.map(r => {
      const prev_val = r[currKey] !== undefined ? (r[prevKey] || 0) : (r.w36 !== undefined ? r.w36 : (r.w35 || 0));
      const curr_val = r[currKey] !== undefined ? (r[currKey] || 0) : (r.w37 !== undefined ? r.w37 : (r.w36 || 0));"""

new_get_ca1 = """  function getGtcCa1TtsData() {
    const prevKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2].toLowerCase() : 'w37';
    const currKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1].toLowerCase() : 'w38';
    const rawList = (D.gtc_ca1_thuan && D.gtc_ca1_thuan.am_tts) || (D.gtc_ca1_ton && D.gtc_ca1_ton.am_tts) || (D.gtc_tong && D.gtc_tong.am_tts) || [];
    return rawList.map(r => {
      const prev_val = r[currKey] !== undefined ? (r[prevKey] || 0) : (r.w37 !== undefined ? r.w37 : (r.w36 || 0));
      const curr_val = r[currKey] !== undefined ? (r[currKey] || 0) : (r.w38 !== undefined ? r.w38 : (r.w37 || 0));"""

if old_get_ca1 in code:
    code = code.replace(old_get_ca1, new_get_ca1, 1)
    print("SUCCESS: Fixed getGtcCa1TtsData keys to w37/w38!")
else:
    print("FAILED: Could not match getGtcCa1TtsData!")

# 3. Fix renderVolumeTab Bảng 3B (TTS 5 Tỉnh)
old_vol_tts_tinh = """    // 4. BẢNG 3B: SẢN LƯỢNG 5 TỈNH THÀNH (TIKTOK SHOP)
    const tblBodyTinhTTS = document.querySelector('#table-vol-tinh-tts tbody');
    if (tblBodyTinhTTS && D.san_luong) {
      const rawTinhTTS = D.san_luong.tinh_tts || [];
      const totalTtsVol = rawTinhTTS.reduce((sum, r) => sum + (r.w36 !== undefined ? r.w36 : (r.w35 || r.vol || 0)), 0);

      const listTinhTTS = [...rawTinhTTS].map(r => {
        const ttsVol = r.w36 !== undefined ? r.w36 : (r.w35 || r.vol || 0);
        const rate = totalTtsVol > 0 ? (ttsVol / totalTtsVol) : 0;
        return {
          ...r,
          rate_tts: rate,
          diff_val: r.diff !== undefined ? r.diff : (ttsVol - (r.w35 || r.w34 || 0))
        };
      }).sort((a, b) => b.diff_val - a.diff_val);"""

new_vol_tts_tinh = """    // 4. BẢNG 3B: SẢN LƯỢNG 5 TỈNH THÀNH (TIKTOK SHOP)
    const tblBodyTinhTTS = document.querySelector('#table-vol-tinh-tts tbody');
    if (tblBodyTinhTTS && D.san_luong) {
      const wKeys = (D.meta?.weeks || ['W35', 'W36', 'W37', 'W38']).map(w => w.toLowerCase());
      const rawTinhTTS = D.san_luong.tinh_tts || [];
      const totalTtsVol = rawTinhTTS.reduce((sum, r) => {
        const v = r[wKeys[3]] !== undefined ? r[wKeys[3]] : (r.w38 !== undefined ? r.w38 : (r.vol || 0));
        return sum + v;
      }, 0);

      const listTinhTTS = [...rawTinhTTS].map(r => {
        const ttsVol = r[wKeys[3]] !== undefined ? r[wKeys[3]] : (r.w38 !== undefined ? r.w38 : (r.vol || 0));
        const prevTtsVol = r[wKeys[2]] !== undefined ? r[wKeys[2]] : (r.w37 !== undefined ? r.w37 : 0);
        const rate = totalTtsVol > 0 ? (ttsVol / totalTtsVol) : 0;
        return {
          ...r,
          rate_tts: rate,
          diff_val: r.diff !== undefined ? r.diff : (ttsVol - prevTtsVol)
        };
      }).sort((a, b) => b.diff_val - a.diff_val);"""

if old_vol_tts_tinh in code:
    code = code.replace(old_vol_tts_tinh, new_vol_tts_tinh, 1)
    print("SUCCESS: Fixed table-vol-tinh-tts rendering logic!")
else:
    print("FAILED: Could not match table-vol-tinh-tts logic!")

# 4. Fix Tab 5 (Gán)
old_gan_ca1_logic = """      let listCa1 = [...D.gan.am].map(r => {
        const curr = r.ca1ton_w37 !== undefined ? r.ca1ton_w37 : (r.ca1ton_curr !== undefined ? r.ca1ton_curr : r.ca1ton_w36);
        const prev = r.ca1ton_w36 !== undefined ? r.ca1ton_w36 : (r.ca1ton_prev !== undefined ? r.ca1ton_prev : r.ca1ton_w35);"""

new_gan_ca1_logic = """      let listCa1 = [...D.gan.am].map(r => {
        const curr = r.ca1ton_w38 !== undefined ? r.ca1ton_w38 : (r.ca1ton_curr !== undefined ? r.ca1ton_curr : (r.ca1ton_w37 || 0));
        const prev = r.ca1ton_w37 !== undefined ? r.ca1ton_w37 : (r.ca1ton_prev !== undefined ? r.ca1ton_prev : (r.ca1ton_w36 || 0));"""

if old_gan_ca1_logic in code:
    code = code.replace(old_gan_ca1_logic, new_gan_ca1_logic, 1)
    print("SUCCESS: Fixed listCa1 in Tab 5!")
else:
    print("FAILED: Could not match listCa1 logic!")

old_gan_ca2_logic = """      let listCa2 = [...D.gan.am].map(r => {
        const curr = r.tong_w37 !== undefined ? r.tong_w37 : (r.tong_curr !== undefined ? r.tong_curr : r.tong_w36);
        const prev = r.tong_w36 !== undefined ? r.tong_w36 : (r.tong_prev !== undefined ? r.tong_prev : r.tong_w35);"""

new_gan_ca2_logic = """      let listCa2 = [...D.gan.am].map(r => {
        const curr = r.tong_w38 !== undefined ? r.tong_w38 : (r.tong_curr !== undefined ? r.tong_curr : (r.tong_w37 || 0));
        const prev = r.tong_w37 !== undefined ? r.tong_w37 : (r.tong_prev !== undefined ? r.tong_prev : (r.tong_w36 || 0));"""

if old_gan_ca2_logic in code:
    code = code.replace(old_gan_ca2_logic, new_gan_ca2_logic, 1)
    print("SUCCESS: Fixed listCa2 in Tab 5!")
else:
    print("FAILED: Could not match listCa2 logic!")

# 5. Fix renderTransportTab (Tab 9: Rớt Luân Chuyển)
old_rot_tab = """  function renderTransportTab() {
    if (!D.rot_lc) return;

    // 1. BẢNG 1: 18 AM
    const tblBodyAM = document.querySelector('#table-rot-am-detailed tbody');
    if (tblBodyAM && D.rot_lc.am) {
      const totalRotAM = D.rot_lc.am.reduce((s, r) => {
        const wCurr = r.w37 !== undefined ? (r.w37 || 0) : (r.w36 || 0);
        return s + Math.round((r.vol || 0) * wCurr);
      }, 0);

      let listAM = [...D.rot_lc.am].map(r => {
        const wPrev = r.w36 !== undefined ? (r.w36 || 0) : (r.w35 || 0);
        const wCurr = r.w37 !== undefined ? (r.w37 || 0) : (r.w36 || 0);
        const diff_val = r.diff !== undefined ? r.diff : (wCurr - wPrev);
        const vol_rot = Math.round((r.vol || 0) * wCurr);
        const rate_rot = totalRotAM > 0 ? (vol_rot / totalRotAM) : 0;
        return {
          ...r,
          wPrev,
          wCurr,
          diff_val,
          vol_rot,
          rate_rot
        };
      }).sort((a, b) => (b.vol_rot || 0) - (a.vol_rot || 0) || (b.wCurr || 0) - (a.wCurr || 0));"""

new_rot_tab = """  function renderTransportTab() {
    if (!D.rot_lc) return;

    const prevKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2].toLowerCase() : 'w37';
    const currKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1].toLowerCase() : 'w38';

    // 1. BẢNG 1: 18 AM
    const tblBodyAM = document.querySelector('#table-rot-am-detailed tbody');
    if (tblBodyAM && D.rot_lc.am) {
      const totalRotAM = D.rot_lc.am.reduce((s, r) => {
        const wCurr = r[currKey] !== undefined ? (r[currKey] || 0) : (r.w38 !== undefined ? r.w38 : (r.w37 || 0));
        return s + Math.round((r.vol || 0) * wCurr);
      }, 0);

      let listAM = [...D.rot_lc.am].map(r => {
        const wPrev = r[prevKey] !== undefined ? (r[prevKey] || 0) : (r.w37 !== undefined ? r.w37 : (r.w36 || 0));
        const wCurr = r[currKey] !== undefined ? (r[currKey] || 0) : (r.w38 !== undefined ? r.w38 : (r.w37 || 0));
        const diff_val = r.diff !== undefined ? r.diff : (wCurr - wPrev);
        const vol_rot = Math.round((r.vol || 0) * wCurr);
        const rate_rot = totalRotAM > 0 ? (vol_rot / totalRotAM) : 0;
        return {
          ...r,
          wPrev,
          wCurr,
          diff_val,
          vol_rot,
          rate_rot
        };
      }).sort((a, b) => (b.vol_rot || 0) - (a.vol_rot || 0) || (b.wCurr || 0) - (a.wCurr || 0));"""

if old_rot_tab in code:
    code = code.replace(old_rot_tab, new_rot_tab, 1)
    print("SUCCESS: Fixed renderTransportTab AM table!")
else:
    print("FAILED: Could not match renderTransportTab AM table!")

old_rot_tinh_block = """    // 2. BẢNG 2: 5 TỈNH THÀNH
    const tblBodyTinh = document.querySelector('#table-rot-tinh-detailed tbody');
    if (tblBodyTinh && D.rot_lc.tinh) {
      const totalRotTinh = D.rot_lc.tinh.reduce((s, r) => {
        const wCurr = r.w37 !== undefined ? (r.w37 || 0) : (r.w36 || 0);
        return s + Math.round((r.vol || 0) * wCurr);
      }, 0);

      let listTinh = [...D.rot_lc.tinh].map(r => {
        const wPrev = r.w36 !== undefined ? (r.w36 || 0) : (r.w35 || 0);
        const wCurr = r.w37 !== undefined ? (r.w37 || 0) : (r.w36 || 0);
        const diff_val = r.diff !== undefined ? r.diff : (wCurr - wPrev);
        const vol_rot = Math.round((r.vol || 0) * wCurr);
        const rate_rot = totalRotTinh > 0 ? (vol_rot / totalRotTinh) : 0;
        return {
          ...r,
          wPrev,
          wCurr,
          diff_val,
          vol_rot,
          rate_rot
        };
      }).sort((a, b) => (b.vol_rot || 0) - (a.vol_rot || 0) || (b.wCurr || 0) - (a.wCurr || 0));"""

new_rot_tinh_block = """    // 2. BẢNG 2: 5 TỈNH THÀNH
    const tblBodyTinh = document.querySelector('#table-rot-tinh-detailed tbody');
    if (tblBodyTinh && D.rot_lc.tinh) {
      const totalRotTinh = D.rot_lc.tinh.reduce((s, r) => {
        const wCurr = r[currKey] !== undefined ? (r[currKey] || 0) : (r.w38 !== undefined ? r.w38 : (r.w37 || 0));
        return s + Math.round((r.vol || 0) * wCurr);
      }, 0);

      let listTinh = [...D.rot_lc.tinh].map(r => {
        const wPrev = r[prevKey] !== undefined ? (r[prevKey] || 0) : (r.w37 !== undefined ? r.w37 : (r.w36 || 0));
        const wCurr = r[currKey] !== undefined ? (r[currKey] || 0) : (r.w38 !== undefined ? r.w38 : (r.w37 || 0));
        const diff_val = r.diff !== undefined ? r.diff : (wCurr - wPrev);
        const vol_rot = Math.round((r.vol || 0) * wCurr);
        const rate_rot = totalRotTinh > 0 ? (vol_rot / totalRotTinh) : 0;
        return {
          ...r,
          wPrev,
          wCurr,
          diff_val,
          vol_rot,
          rate_rot
        };
      }).sort((a, b) => (b.vol_rot || 0) - (a.vol_rot || 0) || (b.wCurr || 0) - (a.wCurr || 0));"""

if old_rot_tinh_block in code:
    code = code.replace(old_rot_tinh_block, new_rot_tinh_block, 1)
    print("SUCCESS: Fixed renderTransportTab Tỉnh table!")
else:
    print("FAILED: Could not match renderTransportTab Tỉnh table!")

# 6. Fix renderRotLcChart
old_rot_chart = """    const prevKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2].toLowerCase() : 'w35';
    const currKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1].toLowerCase() : 'w36';
    const prevLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2] : 'W35';
    const currLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1] : 'W36';

    const selectedAM = state.selectedAM;
    const sorted = [...D.rot_lc.am].map(r => {
      const prev_val = r[currKey] !== undefined ? (r[prevKey] || 0) : (r.w34 || 0);
      const curr_val = r[currKey] !== undefined ? (r[currKey] || 0) : (r.w35 || 0);
      const diff_val = r.diff !== undefined ? r.diff : (curr_val - prev_val);
      return {
        ...r,
        w34_pct: Number((prev_val * 100).toFixed(2)),
        w35_pct: Number((curr_val * 100).toFixed(2)),
        diff_pct: Number((diff_val * 100).toFixed(2))
      };
    }).sort((a, b) => a.diff_pct - b.diff_pct); // Sort từ cải thiện giảm rớt tốt nhất đến tăng rớt"""

new_rot_chart = """    const prevKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2].toLowerCase() : 'w37';
    const currKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1].toLowerCase() : 'w38';
    const prevLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2] : 'W37';
    const currLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1] : 'W38';

    const selectedAM = state.selectedAM;
    const sorted = [...D.rot_lc.am].map(r => {
      const prev_val = r[currKey] !== undefined ? (r[prevKey] || 0) : (r.w37 || 0);
      const curr_val = r[currKey] !== undefined ? (r[currKey] || 0) : (r.w38 || 0);
      const diff_val = r.diff !== undefined ? r.diff : (curr_val - prev_val);
      return {
        ...r,
        w34_pct: Number((prev_val * 100).toFixed(2)),
        w35_pct: Number((curr_val * 100).toFixed(2)),
        diff_pct: Number((diff_val * 100).toFixed(2))
      };
    }).sort((a, b) => a.diff_pct - b.diff_pct);"""

if old_rot_chart in code:
    code = code.replace(old_rot_chart, new_rot_chart, 1)
    print("SUCCESS: Fixed renderRotLcChart logic!")
else:
    print("FAILED: Could not match renderRotLcChart logic!")

# 7. Extend updateDynamicWeekLabels to dynamically keep all table headers synced
old_update_dyn = """    // 15. Dynamic Card Titles and Headers with regex replacement"""

new_update_dyn = """    // Additional Table Headers Dynamic Sync
    const thVolTinhFull = document.querySelectorAll('#table-vol-tinh-full thead th');
    if (thVolTinhFull.length >= 7) {
      thVolTinhFull[2].textContent = w1;
      thVolTinhFull[3].textContent = w2;
      thVolTinhFull[4].textContent = w3;
      thVolTinhFull[5].textContent = currW;
    }
    const thVolTinhTts = document.querySelectorAll('#table-vol-tinh-tts thead th');
    if (thVolTinhTts.length >= 7) {
      thVolTinhTts[2].textContent = w1;
      thVolTinhTts[3].textContent = w2;
      thVolTinhTts[4].textContent = w3;
      thVolTinhTts[5].textContent = currW;
    }

    const thGtcTinhFull = document.querySelectorAll('#table-gtc-tinh-full thead th');
    if (thGtcTinhFull.length >= 7) {
      thGtcTinhFull[3].textContent = w1;
      thGtcTinhFull[4].textContent = w2;
      thGtcTinhFull[5].textContent = w3;
      thGtcTinhFull[6].textContent = `%GTC ${currW}`;
    }
    const thGtcTinhTts = document.querySelectorAll('#table-gtc-tinh-tts thead th');
    if (thGtcTinhTts.length >= 7) {
      thGtcTinhTts[3].textContent = w1;
      thGtcTinhTts[4].textContent = w2;
      thGtcTinhTts[5].textContent = w3;
      thGtcTinhTts[6].textContent = `%GTC ${currW}`;
    }

    const thOdrTinhFull = document.querySelectorAll('#table-odr-tinh-full thead th');
    if (thOdrTinhFull.length >= 7) {
      thOdrTinhFull[3].textContent = w1;
      thOdrTinhFull[4].textContent = w2;
      thOdrTinhFull[5].textContent = w3;
      thOdrTinhFull[6].textContent = `%ODR ${currW}`;
    }
    const thOdrTinhTts = document.querySelectorAll('#table-odr-tinh-tts thead th');
    if (thOdrTinhTts.length >= 7) {
      thOdrTinhTts[3].textContent = w1;
      thOdrTinhTts[4].textContent = w2;
      thOdrTinhTts[5].textContent = w3;
      thOdrTinhTts[6].textContent = `%ODR ${currW}`;
    }

    const thGanOv = document.querySelectorAll('#table-gan-overview-region thead th');
    if (thGanOv.length >= 6) {
      thGanOv[1].textContent = w1;
      thGanOv[2].textContent = w2;
      thGanOv[3].textContent = w3;
      thGanOv[4].textContent = currW;
      thGanOv[5].textContent = `Δ ${currW}/${prevW}`;
    }

    const thRotBc = document.querySelector('#table-rot-lc-top-bc thead th:nth-child(6)');
    if (thRotBc) thRotBc.textContent = `% Rớt LC (${currW})`;

    // 15. Dynamic Card Titles and Headers with regex replacement"""

if old_update_dyn in code:
    code = code.replace(old_update_dyn, new_update_dyn, 1)
    print("SUCCESS: Enhanced updateDynamicWeekLabels!")
else:
    print("FAILED: Could not match old_update_dyn!")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("ALL APP.JS PATCHES APPLIED SUCCESSFULLY!")
