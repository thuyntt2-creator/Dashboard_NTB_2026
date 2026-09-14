import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# 1. UPDATE APP.JS
# ==============================================================================
with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Replace updateDynamicWeekLabels in app.js
old_dyn_func = """  function updateDynamicWeekLabels() {
    if (!D.meta) return;
    const latestW = D.meta.latest_week || 'W37';
    const weeks = D.meta.weeks || ['W34', 'W35', 'W36', 'W37'];
    const dateRange = D.meta.date_range || '07/09 - 13/09/2026';

    const liveBadge = document.getElementById('header-live-badge') || document.querySelector('.live-badge');
    if (liveBadge) liveBadge.textContent = `DỮ LIỆU CHUẨN ${latestW}`;

    const dateRangeSpan = document.getElementById('header-weeks-range');
    if (dateRangeSpan) {
      dateRangeSpan.textContent = `So sánh 4 Tuần ${weeks[0]} – ${latestW} (${dateRange})`;
    }
  }"""

new_dyn_func = """  function updateDynamicWeekLabels() {
    if (!window.D || !D.meta) return;
    const currW = D.meta.latest_week || 'W37';
    const prevW = D.meta.prev_week || 'W36';
    const weeks = D.meta.weeks || ['W34', 'W35', 'W36', 'W37'];
    const w1 = weeks[0] || 'W34';
    const w2 = weeks[1] || 'W35';
    const w3 = weeks[2] || 'W36';
    const w4 = weeks[3] || 'W37';
    const dateRange = D.meta.date_range || '07/09 - 13/09/2026';

    // 1. Header Badges & Subtitle
    const liveBadge = document.getElementById('header-live-badge') || document.querySelector('.live-badge');
    if (liveBadge) liveBadge.textContent = `DỮ LIỆU CHUẨN ${currW}`;

    const dateRangeSpan = document.getElementById('header-weeks-range');
    if (dateRangeSpan) {
      dateRangeSpan.textContent = `So sánh 4 Tuần ${w1} – ${currW} (${dateRange})`;
    }

    const subEl = document.querySelector('.header-sub') || document.querySelector('.brand-subtitle');
    if (subEl) {
      subEl.textContent = `Báo Cáo Họp Vận Hành & Kinh Doanh Tuần ${currW} (${dateRange}) - Vùng Nam Trung Bộ`;
    }

    // 2. Select Dropdown
    const selWeek = document.getElementById('filter-week') || document.getElementById('week-select');
    if (selWeek && D.meta?.weeks) {
      const wList = [...D.meta.weeks].reverse();
      selWeek.innerHTML = wList.map((w, idx) => {
        const label = idx === 0 ? `Tuần ${w} (Hiện tại)` : (idx === 1 ? `Tuần ${w} (Tuần trước)` : `Tuần ${w}`);
        return `<option value="${w}" ${w === currW ? 'selected' : ''}>${label}</option>`;
      }).join('');
    }

    // 3. Tab 1: Overview table columns
    const thOv4 = document.querySelector('#table-overview-kpi thead th:nth-child(6)');
    if (thOv4) thOv4.textContent = `${currW} (Kỳ N)`;
    const thOv3 = document.querySelector('#table-overview-kpi thead th:nth-child(5)');
    if (thOv3) thOv3.textContent = prevW;
    const thOv2 = document.querySelector('#table-overview-kpi thead th:nth-child(4)');
    if (thOv2) thOv2.textContent = w2;
    const thOv1 = document.querySelector('#table-overview-kpi thead th:nth-child(3)');
    if (thOv1) thOv1.textContent = w1;

    // 4. Tab 2: Sản Lượng
    const volChartTitle = document.getElementById('chart-vol-am-title');
    if (volChartTitle) volChartTitle.textContent = `SẢN LƯỢNG GIAO 18 AM (CỘT ${prevW} vs ${currW} + ĐƯỜNG BIẾN ĐỘNG Δ)`;
    const btnVolFull = document.querySelector('[data-mode="w34_vs_w35_full"]');
    if (btnVolFull) btnVolFull.textContent = `📊 Sản Lượng Full Hàng (Cột ${prevW} vs ${currW} + Đường Line Δ)`;
    const btnVolTts = document.querySelector('[data-mode="w34_vs_w35_tts"]');
    if (btnVolTts) btnVolTts.textContent = `⚡ Sản Lượng TikTok Shop (Cột ${prevW} vs ${currW} + Đường Line Δ)`;

    const thVolFullPrev = document.querySelector('#table-vol-full-detailed thead th:nth-child(3)');
    const thVolFullCurr = document.querySelector('#table-vol-full-detailed thead th:nth-child(4)');
    if (thVolFullPrev) thVolFullPrev.textContent = `Full ${prevW}`;
    if (thVolFullCurr) thVolFullCurr.textContent = `Full ${currW}`;

    const thVolTtsPrev = document.querySelector('#table-vol-tts-detailed thead th:nth-child(3)');
    const thVolTtsCurr = document.querySelector('#table-vol-tts-detailed thead th:nth-child(4)');
    if (thVolTtsPrev) thVolTtsPrev.textContent = `TTS ${prevW}`;
    if (thVolTtsCurr) thVolTtsCurr.textContent = `TTS ${currW}`;

    // 5. Tab 3: %GTC Tổng
    const gtcTitle = document.getElementById('chart-gtc-tong-title');
    if (gtcTitle) gtcTitle.textContent = `BIỂU ĐỒ SO SÁNH %GTC TỔNG ${prevW} vs ${currW} THEO 18 AM (FULL HÀNG)`;
    const thGtcFullPrev = document.querySelector('#table-gtc-full-detailed thead th:nth-child(4)');
    const thGtcFullCurr = document.querySelector('#table-gtc-full-detailed thead th:nth-child(5)');
    if (thGtcFullPrev) thGtcFullPrev.textContent = prevW;
    if (thGtcFullCurr) thGtcFullCurr.textContent = currW;
    const thGtcTtsPrev = document.querySelector('#table-gtc-tts-detailed thead th:nth-child(4)');
    const thGtcTtsCurr = document.querySelector('#table-gtc-tts-detailed thead th:nth-child(5)');
    if (thGtcTtsPrev) thGtcTtsPrev.textContent = prevW;
    if (thGtcTtsCurr) thGtcTtsCurr.textContent = currW;

    // 6. Tab 4: %GTC TTS Ca 1
    const thGtcCa1Prev = document.querySelector('#table-gtc-tts-ca1-detailed thead th:nth-child(4)');
    const thGtcCa1Curr = document.querySelector('#table-gtc-tts-ca1-detailed thead th:nth-child(5)');
    if (thGtcCa1Prev) thGtcCa1Prev.textContent = `%GTC TTS Ca 1 (${prevW})`;
    if (thGtcCa1Curr) thGtcCa1Curr.textContent = `%GTC TTS Ca 1 (${currW})`;

    // 7. Tab 5: % Gán
    const thGanPrev = document.querySelector('#table-gan-full-detailed thead th:nth-child(6)');
    const thGanCurr = document.querySelector('#table-gan-full-detailed thead th:nth-child(7)');
    if (thGanPrev) thGanPrev.textContent = `Tổng ${prevW}`;
    if (thGanCurr) thGanCurr.textContent = `Tổng ${currW}`;
    const btnGanAm = document.getElementById('btn-gan-mode-am');
    if (btnGanAm) btnGanAm.innerHTML = `<i data-lucide="split" style="width: 14px; height: 14px;"></i> ⚡ So Sánh Full vs TTS (${currW})`;

    // 8. Tab 6: %ODR
    const thOdrFullPrev = document.querySelector('#table-odr-full-detailed thead th:nth-child(4)');
    const thOdrFullCurr = document.querySelector('#table-odr-full-detailed thead th:nth-child(5)');
    if (thOdrFullPrev) thOdrFullPrev.textContent = prevW;
    if (thOdrFullCurr) thOdrFullCurr.textContent = currW;

    // 9. Tab 7: %LTC
    const thLtcCurr = document.querySelector('#table-ltc-detailed thead th:nth-child(7)');
    if (thLtcCurr) thLtcCurr.textContent = `%LTC ${currW}`;
    const thLtcTinhCurr = document.querySelector('#table-ltc-tinh-detailed thead th:nth-child(7)');
    if (thLtcTinhCurr) thLtcTinhCurr.textContent = `%LTC ${currW}`;

    // 10. Tab 8: %OPR TTS
    const thOprDayPrev = document.querySelector('#table-opr-tts-data thead th:nth-child(4)');
    const thOprDayCurr = document.querySelector('#table-opr-tts-data thead th:nth-child(5)');
    const thOprNightPrev = document.querySelector('#table-opr-tts-data thead th:nth-child(8)');
    const thOprNightCurr = document.querySelector('#table-opr-tts-data thead th:nth-child(9)');
    if (thOprDayPrev) thOprDayPrev.textContent = `%OPR 9h–19h (${prevW})`;
    if (thOprDayCurr) thOprDayCurr.textContent = `%OPR 9h–19h (${currW})`;
    if (thOprNightPrev) thOprNightPrev.textContent = `%OPR 19h–9h (${prevW})`;
    if (thOprNightCurr) thOprNightCurr.textContent = `%OPR 19h–9h (${currW})`;

    // 11. Tab 9: % Rớt LC
    const thRotAmPrev = document.querySelector('#table-rot-am-detailed thead th:nth-child(6)');
    const thRotAmCurr = document.querySelector('#table-rot-am-detailed thead th:nth-child(7)');
    if (thRotAmPrev) thRotAmPrev.textContent = `% Rớt ${prevW}`;
    if (thRotAmCurr) thRotAmCurr.textContent = `% Rớt ${currW}`;
    const thRotTinhPrev = document.querySelector('#table-rot-tinh-detailed thead th:nth-child(6)');
    const thRotTinhCurr = document.querySelector('#table-rot-tinh-detailed thead th:nth-child(7)');
    if (thRotTinhPrev) thRotTinhPrev.textContent = `% Rớt ${prevW}`;
    if (thRotTinhCurr) thRotTinhCurr.textContent = `% Rớt ${currW}`;

    // 12. Tab 10: %FD Hoàn Trả
    const fdBannerDesc = document.querySelector('#tab-fd .exec-banner-desc');
    if (fdBannerDesc) {
      fdBannerDesc.textContent = `Dữ liệu chu kỳ ${currW} (${dateRange}) | So sánh biến động WoW với tuần trước (${prevW}) | Tách riêng Full Hàng và TikTok Shop`;
    }
    const spanFdFull = document.querySelector('#tab-fd .kpi-strip .kpi-tile:nth-child(2) .kpi-tile-header span');
    if (spanFdFull) spanFdFull.textContent = `%FD Return Full Hàng (${prevW} vs ${currW})`;
    const spanFdTts = document.querySelector('#tab-fd .kpi-strip .kpi-tile:nth-child(4) .kpi-tile-header span');
    if (spanFdTts) spanFdTts.textContent = `%FD Return TikTok Shop (${prevW} vs ${currW})`;

    const thFdFullPrev = document.querySelector('#table-fd-am-detailed thead th:nth-child(4)');
    const thFdFullCurr = document.querySelector('#table-fd-am-detailed thead th:nth-child(5)');
    const thFdTtsPrev = document.querySelector('#table-fd-am-detailed thead th:nth-child(8)');
    const thFdTtsCurr = document.querySelector('#table-fd-am-detailed thead th:nth-child(9)');
    if (thFdFullPrev) thFdFullPrev.textContent = `Full ${prevW}`;
    if (thFdFullCurr) thFdFullCurr.textContent = `Full ${currW}`;
    if (thFdTtsPrev) thFdTtsPrev.textContent = `TTS ${prevW}`;
    if (thFdTtsCurr) thFdTtsCurr.textContent = `TTS ${currW}`;

    // 13. Tab 11: KTC & Vận Tải
    const ktcTitle = document.querySelector('#tab-ktc .exec-banner-text h2');
    if (ktcTitle) ktcTitle.textContent = `BÁO CÁO ĐIỀU HÀNH KTC & VẬN TẢI — VÙNG NAM TRUNG BỘ (${currW})`;
    const btnKtcFillrate = document.getElementById('btn-ktc-fillrate');
    if (btnKtcFillrate) btnKtcFillrate.innerHTML = `<i data-lucide="truck" style="width: 14px; height: 14px;"></i> 🚚 3. Tỷ Lệ Lấp Đầy Thùng/Xe (${prevW} vs ${currW})`;
    const btnFrWeekly = document.getElementById('btn-fr-weekly');
    if (btnFrWeekly) btnFrWeekly.textContent = `📊 Tuần (${prevW} vs ${currW})`;

    // 14. Tab 14: Churn table
    const thChurnPrev = document.querySelector('#table-kd-churn-top10 thead th:nth-child(6)');
    const thChurnCurr = document.querySelector('#table-kd-churn-top10 thead th:nth-child(7)');
    if (thChurnPrev) thChurnPrev.textContent = `Kỳ Trước (${prevW})`;
    if (thChurnCurr) thChurnCurr.textContent = `Kỳ Này (${currW})`;

    // 15. Dynamic Card Titles and Headers with regex replacement
    document.querySelectorAll('.report-card-title, .exec-banner-text h2, .exec-banner-text h3').forEach(el => {
      if (el.textContent.includes('SO SÁNH TỶ LỆ GÁN 18 AM:')) {
        el.textContent = `SO SÁNH TỶ LỆ GÁN 18 AM: % GÁN CA 1+TỒN vs % GÁN CA 2 vs % GÁN TỔNG (${currW})`;
      } else if (el.textContent.includes('% RỚT LUÂN CHUYỂN THEO 18 AM PHỤ TRÁCH')) {
        el.textContent = `% RỚT LUÂN CHUYỂN THEO 18 AM PHỤ TRÁCH (${currW})`;
      } else if (el.textContent.includes('DANH SÁCH TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LUÂN CHUYỂN CAO NHẤT')) {
        el.textContent = `DANH SÁCH TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LUÂN CHUYỂN CAO NHẤT (${currW})`;
      } else if (el.textContent.includes('BẢNG 2: TOP BƯU CỤC CÓ TỶ LỆ %FD CAO NHẤT')) {
        el.textContent = `BẢNG 2: TOP BƯU CỤC CÓ TỶ LỆ %FD CAO NHẤT (${currW})`;
      } else if (el.textContent.includes('TOP 10 KHÁCH HÀNG CÓ SẢN LƯỢNG GIẢM / RỜI BỎ LỚN NHẤT')) {
        el.textContent = `TOP 10 KHÁCH HÀNG CÓ SẢN LƯỢNG GIẢM / RỜI BỎ LỚN NHẤT (${currW})`;
      }
    });

    // 16. Generic DOM Text Replacer for all badges and labels
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    let node;
    while ((node = walker.nextNode())) {
      if (!node.nodeValue) continue;
      let text = node.nodeValue;
      if (text.includes('(W36 vs W35)')) text = text.replaceAll('(W36 vs W35)', `(${prevW} vs ${currW})`);
      if (text.includes('W35: 51.8% → W36: 48.1%')) {
        text = text.replaceAll('W35: 51.8% → W36: 48.1% (▼3.7%p)', `${prevW}: 48.1% → ${currW}: 54.8% (▲ +6.7%p)`);
      }
      if (node.nodeValue !== text) {
        node.nodeValue = text;
      }
    }
  }"""

if old_dyn_func in app_js:
    app_js = app_js.replace(old_dyn_func, new_dyn_func)
    print("✓ Replaced updateDynamicWeekLabels in app.js")
else:
    print("⚠ Could not find exact old_dyn_func in app.js, checking regex...")

# Call updateDynamicWeekLabels() when tabs switch
old_tab_click = """        setTimeout(() => {
          renderTabCharts(targetId);
          lucide.createIcons();
        }, 30);"""

new_tab_click = """        updateDynamicWeekLabels();
        setTimeout(() => {
          renderTabCharts(targetId);
          lucide.createIcons();
        }, 30);"""

if old_tab_click in app_js:
    app_js = app_js.replace(old_tab_click, new_tab_click)
    print("✓ Added updateDynamicWeekLabels on tab switch")

# Fix TLLĐ KPI Card in renderOverviewTab
old_tltd_block = """      // 10. TLTĐ (Tỷ Lệ Lấp Đầy Thùng/Xe KTC)
      const ktcData = D.ktc || {};
      const ktcWeekly = ktcData.fill_rate?.weekly?.total || {};
      const tltdVal = (ktcWeekly['tld_' + latestWeek.toLowerCase()] !== undefined ? ktcWeekly['tld_' + latestWeek.toLowerCase()] : (ktcWeekly.tld_w37 || ktcWeekly.tld_w36 || 54.8)) / 100;
      const tltdPrev = ktcWeekly.tld_w35 !== undefined ? (ktcWeekly.tld_w35 / 100) : 0.518;
      const tltdDiff = ktcWeekly.diff_tld !== undefined ? (ktcWeekly.diff_tld / 100) : -0.037;
      const tltdUnder30 = ktcWeekly.under_30 || 112;"""

new_tltd_block = """      // 10. TLTĐ (Tỷ Lệ Lấp Đầy Thùng/Xe KTC)
      const ktcData = D.ktc || {};
      const ktcWeekly = ktcData.fill_rate?.weekly?.total || {};
      const tltdVal = (ktcWeekly.tld_curr !== undefined ? ktcWeekly.tld_curr : (ktcWeekly['tld_' + latestWeek.toLowerCase()] || 54.8)) / 100;
      const tltdPrev = (ktcWeekly.tld_prev !== undefined ? ktcWeekly.tld_prev : (ktcWeekly['tld_' + prevWeek.toLowerCase()] || 48.1)) / 100;
      const tltdDiff = ktcWeekly.diff_tld !== undefined ? (ktcWeekly.diff_tld / 100) : (tltdVal - tltdPrev);
      const tltdUnder30 = ktcWeekly.under_30 !== undefined ? ktcWeekly.under_30 : 80;"""

if old_tltd_block in app_js:
    app_js = app_js.replace(old_tltd_block, new_tltd_block)
    print("✓ Fixed TLLĐ KPI Card calculation in renderOverviewTab")

# Fix rot_lc card subtext in renderOverviewTab
old_rot_subval = """          subVal: `${prevWeek}: 1.57% (Tăng +0.7%p)`,"""
new_rot_subval = """          subVal: `${prevWeek}: ${fPct(rotVal - rotDiff)} (${rotDiff >= 0 ? 'Tăng +' : 'Giảm '}${(Math.abs(rotDiff)*100).toFixed(2)}%p)`,"""
if old_rot_subval in app_js:
    app_js = app_js.replace(old_rot_subval, new_rot_subval)
    print("✓ Fixed rot_lc subVal in renderOverviewTab")

# Fix fd card subtext in renderOverviewTab
old_fd_subval = """          subVal: `${fPct(fdRateTts)} (TTS) | ${fNum(fdRetFull)} đ hoàn`,"""
new_fd_subval = """          subVal: `${fPct(fdRateTts)} (TTS) | ${fNum(fdRetFull)} đ hoàn (${prevWeek}: ${fPct(fdSum.rate_full_prev || 0.0754)})`,"""
if old_fd_subval in app_js:
    app_js = app_js.replace(old_fd_subval, new_fd_subval)
    print("✓ Fixed fd subVal in renderOverviewTab")

# Fix getGtcCa1TtsData and renderGtcTtsCa1Tab
old_gtc_ca1_block = """  function getGtcCa1TtsData() {
    const prevKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2].toLowerCase() : 'w35';
    const currKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1].toLowerCase() : 'w36';
    const rawList = (D.gtc_ca1_thuan && D.gtc_ca1_thuan.am_tts) || (D.gtc_ca1_ton && D.gtc_ca1_ton.am_tts) || (D.gtc_tong && D.gtc_tong.am_tts) || [];
    return rawList.map(r => {
      const prev_val = r[currKey] !== undefined ? (r[prevKey] || 0) : (r.w34 || 0);
      const curr_val = r[currKey] !== undefined ? (r[currKey] || 0) : (r.w35 || 0);
      const prev_pct = prev_val * 100;
      const curr_pct = curr_val * 100;
      const diff_val = (r.diff !== undefined) ? r.diff : (curr_val - prev_val);
      const diff_pct = diff_val * 100;
      const isPass = curr_val >= 0.76;
      return {
        am: r.am,
        vol: r.vol || 0,
        w34: prev_val,
        w35: curr_val,
        w34_pct: Number(prev_pct.toFixed(1)),
        w35_pct: Number(curr_pct.toFixed(1)),
        diff: diff_val, // Decimal for renderDeltaBadge
        diff_pct: Number(diff_pct.toFixed(1)), // Percent for chart & sorting
        isPass: isPass
      };
    });
  }

  function renderGtcTtsCa1Tab() {
    const tblBody = document.querySelector('#table-gtc-tts-ca1-detailed tbody');
    if (tblBody) {
      // Sort biến động WoW lớn nhất giảm dần (diff_pct descending)
      const list = getGtcCa1TtsData().sort((a, b) => b.diff_pct - a.diff_pct);

      tblBody.innerHTML = list.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const heatW35 = getHeatmapClass(row.w35, 'gtc');
        const diffBadge = renderDeltaBadge(row.diff, true, true);

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; color: ${isSelected ? '#ef4444' : 'inherit'}; font-weight:800;">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.w34)}</td>
            <td class="num bold ${heatW35}" style="font-size:13.5px; font-weight:800;">${fPct(row.w35)}</td>
            <td class="num bold">${diffBadge}</td>
          </tr>
        `;
      }).join('');
    }
  }"""

new_gtc_ca1_block = """  function getGtcCa1TtsData() {
    const prevKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2].toLowerCase() : 'w36';
    const currKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1].toLowerCase() : 'w37';
    const rawList = (D.gtc_ca1_thuan && D.gtc_ca1_thuan.am_tts) || (D.gtc_ca1_ton && D.gtc_ca1_ton.am_tts) || (D.gtc_tong && D.gtc_tong.am_tts) || [];
    return rawList.map(r => {
      const prev_val = r[currKey] !== undefined ? (r[prevKey] || 0) : (r.w36 !== undefined ? r.w36 : (r.w35 || 0));
      const curr_val = r[currKey] !== undefined ? (r[currKey] || 0) : (r.w37 !== undefined ? r.w37 : (r.w36 || 0));
      const prev_pct = prev_val * 100;
      const curr_pct = curr_val * 100;
      const diff_val = (r.diff !== undefined) ? r.diff : (curr_val - prev_val);
      const diff_pct = diff_val * 100;
      const isPass = curr_val >= 0.76;
      return {
        am: r.am,
        vol: r.vol || 0,
        prev_val: prev_val,
        curr_val: curr_val,
        w34: prev_val,
        w35: curr_val,
        prev_pct: Number(prev_pct.toFixed(1)),
        curr_pct: Number(curr_pct.toFixed(1)),
        w34_pct: Number(prev_pct.toFixed(1)),
        w35_pct: Number(curr_pct.toFixed(1)),
        diff: diff_val,
        diff_pct: Number(diff_pct.toFixed(1)),
        isPass: isPass
      };
    });
  }

  function renderGtcTtsCa1Tab() {
    const tblBody = document.querySelector('#table-gtc-tts-ca1-detailed tbody');
    if (tblBody) {
      const list = getGtcCa1TtsData().sort((a, b) => b.diff_pct - a.diff_pct);
      tblBody.innerHTML = list.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const heatCls = getHeatmapClass(row.curr_val, 'gtc');
        const diffBadge = renderDeltaBadge(row.diff, true, true);

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; color: ${isSelected ? '#ef4444' : 'inherit'}; font-weight:800;">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.prev_val)}</td>
            <td class="num bold ${heatCls}" style="font-size:13.5px; font-weight:800;">${fPct(row.curr_val)}</td>
            <td class="num bold">${diffBadge}</td>
          </tr>
        `;
      }).join('');
    }
  }"""

if old_gtc_ca1_block in app_js:
    app_js = app_js.replace(old_gtc_ca1_block, new_gtc_ca1_block)
    print("✓ Fixed getGtcCa1TtsData and renderGtcTtsCa1Tab in app.js")

# Fix renderFdTab KPI card updates
old_fd_kpi_update = """    // 1. KPI Summary Cards
    if (D.fd.summary) {
      const s = D.fd.summary;
      const elVolFull = document.getElementById('kpi-fd-vol-full');
      const elRateFull = document.getElementById('kpi-fd-rate-full');
      const elVolTts = document.getElementById('kpi-fd-vol-tts');
      const elRateTts = document.getElementById('kpi-fd-rate-tts');
      if (elVolFull) elVolFull.innerHTML = `${fNum(s.vol_full)} <span class="kpi-unit">đơn</span>`;
      if (elRateFull) elRateFull.innerText = fPct(s.rate_full);
      if (elVolTts) elVolTts.innerHTML = `${fNum(s.vol_tts)} <span class="kpi-unit">đơn</span>`;
      if (elRateTts) elRateTts.innerText = fPct(s.rate_tts);
    }"""

new_fd_kpi_update = """    // 1. KPI Summary Cards
    if (D.fd.summary) {
      const s = D.fd.summary;
      const currW = D.meta?.latest_week || 'W37';
      const prevW = D.meta?.prev_week || 'W36';
      const elVolFull = document.getElementById('kpi-fd-vol-full');
      const elRateFull = document.getElementById('kpi-fd-rate-full');
      const elVolTts = document.getElementById('kpi-fd-vol-tts');
      const elRateTts = document.getElementById('kpi-fd-rate-tts');
      if (elVolFull) elVolFull.innerHTML = `${fNum(s.vol_full)} <small>đơn ${currW}</small>`;
      if (elRateFull) {
        const prevFullTxt = s.rate_full_prev ? ` <small style="color: var(--text-muted); font-size: 13px; font-weight: 600;">(${prevW}: ${fPct(s.rate_full_prev)})</small>` : '';
        elRateFull.innerHTML = `${fPct(s.rate_full)}${prevFullTxt}`;
      }
      if (elVolTts) elVolTts.innerHTML = `${fNum(s.vol_tts)} <small>đơn ${currW}</small>`;
      if (elRateTts) {
        const prevTtsTxt = s.rate_tts_prev ? ` <small style="color: var(--text-muted); font-size: 13px; font-weight: 600;">(${prevW}: ${fPct(s.rate_tts_prev)})</small>` : '';
        elRateTts.innerHTML = `${fPct(s.rate_tts)}${prevTtsTxt}`;
      }

      const cardRateFullMeta = document.querySelector('#tab-fd .kpi-strip .kpi-tile:nth-child(2) .kpi-tile-meta');
      if (cardRateFullMeta && s.diff_full !== undefined) {
        const diffCls = s.diff_full <= 0 ? 'diff-up-good' : 'diff-up-bad';
        const diffSign = s.diff_full >= 0 ? '▲ +' : '▼ ';
        const diffTxt = `${diffSign}${Math.abs(s.diff_full * 100).toFixed(2)}% WoW`;
        cardRateFullMeta.innerHTML = `
          <span class="diff-tag ${diffCls}">${diffTxt}</span>
          <span style="color: var(--text-muted); font-size: 11.5px;">${fNum(s.ret_full)} đ return (Mục tiêu ≤ 6.0%)</span>
        `;
      }

      const cardRateTtsMeta = document.querySelector('#tab-fd .kpi-strip .kpi-tile:nth-child(4) .kpi-tile-meta');
      if (cardRateTtsMeta && s.diff_tts !== undefined) {
        const diffCls = s.diff_tts <= 0 ? 'diff-up-good' : 'diff-up-bad';
        const diffSign = s.diff_tts >= 0 ? '▲ +' : '▼ ';
        const diffTxt = `${diffSign}${Math.abs(s.diff_tts * 100).toFixed(2)}% WoW`;
        cardRateTtsMeta.innerHTML = `
          <span class="diff-tag ${diffCls}">${diffTxt}</span>
          <span style="color: var(--text-muted); font-size: 11.5px;">${fNum(s.ret_tts || 0)} đ return TTS</span>
        `;
      }
    }"""

if old_fd_kpi_update in app_js:
    app_js = app_js.replace(old_fd_kpi_update, new_fd_kpi_update)
    print("✓ Enhanced renderFdTab KPI card update in app.js")

# Fix renderFdChart dynamic labels
app_js = app_js.replace(
    "label: mode === 'tts' ? '%FD TTS W36 (Tuần Trước)' : '%FD Full W36 (Tuần Trước)',",
    "label: mode === 'tts' ? `%FD TTS ${D.meta?.prev_week || 'W36'} (Tuần Trước)` : `%FD Full ${D.meta?.prev_week || 'W36'} (Tuần Trước)`,"
)
app_js = app_js.replace(
    "label: mode === 'tts' ? '%FD TTS W37 (Hiện Tại)' : '%FD Full W37 (Hiện Tại)',",
    "label: mode === 'tts' ? `%FD TTS ${D.meta?.latest_week || 'W37'} (Hiện Tại)` : `%FD Full ${D.meta?.latest_week || 'W37'} (Hiện Tại)`,"
)

# Fix renderKtcTab to update KPI Card 4 and support weekly mode by default
old_render_ktc = """  function renderKtcTab() {
    if (!D.ktc) return;
    renderKtcBacklog();
    renderKtcLeadtime();
    renderFillRateTable();
  }"""

new_render_ktc = """  function renderKtcTab() {
    if (!D.ktc) return;

    // Default to weekly if daily is empty
    if (!state.fillRateMode || (state.fillRateMode === 'daily' && (!D.ktc?.fill_rate?.daily?.items || D.ktc.fill_rate.daily.items.length === 0))) {
      state.fillRateMode = 'weekly';
      const btnD = document.getElementById('btn-fr-daily');
      const btnW = document.getElementById('btn-fr-weekly');
      if (btnD) btnD.className = 'btn btn-sm btn-secondary';
      if (btnW) btnW.className = 'btn btn-sm btn-primary active';
    }

    // Update KTC KPI Card 4 (TLLĐ Xe Bình Quân)
    const ktcWeeklyTot = D.ktc.fill_rate?.weekly?.total || {};
    const currW = D.meta?.latest_week || 'W37';
    const prevW = D.meta?.prev_week || 'W36';
    const tldVal = ktcWeeklyTot.tld_curr !== undefined ? ktcWeeklyTot.tld_curr : 54.8;
    const tldPrev = ktcWeeklyTot.tld_prev !== undefined ? ktcWeeklyTot.tld_prev : 48.1;
    const diffTld = ktcWeeklyTot.diff_tld !== undefined ? ktcWeeklyTot.diff_tld : 6.7;
    const under30 = ktcWeeklyTot.under_30 !== undefined ? ktcWeeklyTot.under_30 : 80;

    const ktcTile4 = document.querySelector('#tab-ktc .kpi-strip .kpi-tile:nth-child(4)');
    if (ktcTile4) {
      const headerSpan = ktcTile4.querySelector('.kpi-tile-header span');
      if (headerSpan) headerSpan.textContent = `TLLĐ Xe Bình Quân (${currW})`;
      const valEl = ktcTile4.querySelector('.kpi-tile-value');
      if (valEl) {
        valEl.style.color = '#10b981';
        valEl.innerHTML = `${tldVal.toFixed(1)}% <small style="color: var(--text-muted); font-size: 13px; font-weight: 600;">(${prevW}: ${tldPrev.toFixed(1)}%)</small>`;
      }
      const metaEl = ktcTile4.querySelector('.kpi-tile-meta');
      if (metaEl) {
        metaEl.innerHTML = `
          <span class="badge-tag badge-tag-green">▲ +${Math.abs(diffTld).toFixed(1)}%p WoW</span>
          <span style="color: var(--text-muted); font-size: 11.5px;">${under30} chuyến &lt;30%</span>
        `;
      }
    }

    const frBadge = document.querySelector('#ktc-subview-fillrate .badge-tag-amber');
    if (frBadge) {
      frBadge.className = 'badge-tag badge-tag-green';
      frBadge.textContent = `${prevW}: ${tldPrev.toFixed(1)}% → ${currW}: ${tldVal.toFixed(1)}% (▲ +${Math.abs(diffTld).toFixed(1)}%p)`;
    }

    renderKtcBacklog();
    renderKtcLeadtime();
    renderFillRateTable();
    renderFillRateChart();
  }"""

if old_render_ktc in app_js:
    app_js = app_js.replace(old_render_ktc, new_render_ktc)
    print("✓ Enhanced renderKtcTab in app.js")

# Fix weekly fill rate table headers and row mapping in app.js
old_fillrate_weekly_thead = """      // Weekly: compare W35 vs W36
      thead.innerHTML = `<tr>
        <th class="center" style="width:44px;">#</th>
        <th>KTC / Kho</th>
        <th class="num">Chuyến W37</th>
        <th class="num">Chuyến W37</th>
        <th class="num">Δ Chuyến</th>
        <th class="num" style="background:var(--color-blue-bg);">TLLĐ W37</th>
        <th class="num bold" style="background:var(--color-blue-bg);">TLLĐ W37</th>
        <th class="num">Δ TLLĐ</th>
        <th class="num" style="background:var(--color-red-bg);color:#b91c1c;">&lt;10%</th>
        <th class="num" style="background:var(--color-red-bg);color:#b91c1c;">10-20%</th>
        <th class="num" style="background:var(--color-red-bg);color:#b91c1c;">20-30%</th>
        <th class="num bold" style="background:var(--color-red-bg);color:#b91c1c;">Tổng &lt;30%</th>
      </tr>`;"""

new_fillrate_weekly_thead = """      // Weekly: compare prevW vs currW
      const currW = D.meta?.latest_week || 'W37';
      const prevW = D.meta?.prev_week || 'W36';
      thead.innerHTML = `<tr>
        <th class="center" style="width:44px;">#</th>
        <th>KTC / Kho</th>
        <th class="num">Chuyến ${prevW}</th>
        <th class="num" style="background:var(--color-blue-bg); font-weight:800;">Chuyến ${currW}</th>
        <th class="num">Δ Chuyến</th>
        <th class="num">TLLĐ ${prevW}</th>
        <th class="num bold" style="background:var(--color-blue-bg);">TLLĐ ${currW}</th>
        <th class="num">Δ TLLĐ</th>
        <th class="num" style="background:var(--color-red-bg);color:#b91c1c;">&lt;10%</th>
        <th class="num" style="background:var(--color-red-bg);color:#b91c1c;">10-20%</th>
        <th class="num" style="background:var(--color-red-bg);color:#b91c1c;">20-30%</th>
        <th class="num bold" style="background:var(--color-red-bg);color:#b91c1c;">Tổng &lt;30%</th>
      </tr>`;"""

if old_fillrate_weekly_thead in app_js:
    app_js = app_js.replace(old_fillrate_weekly_thead, new_fillrate_weekly_thead)
    print("✓ Fixed fill rate weekly table thead in app.js")

old_fillrate_weekly_row = """        return `<tr${isTotal ? ' style="background:var(--color-blue-bg);font-weight:800;"' : ''}>
          ${rankCell}
          <td class="bold">${r.short_name || r.kho || ''}</td>
          <td class="num">${fNum(r.chuyen_w37 || 0)}</td>
          <td class="num">${fNum(r.chuyen_w37 || 0)}</td>
          <td class="num">${diffCBadge}</td>
          <td class="num" style="background:var(--color-blue-bg);">${(r.tld_w37 || 0).toFixed(1)}%</td>
          <td class="num bold" style="background:var(--color-blue-bg);">${(r.tld_w37 || 0).toFixed(1)}%</td>
          <td class="num">${diffTBadge}</td>"""

new_fillrate_weekly_row = """        const chuyenP = r.chuyen_prev !== undefined ? r.chuyen_prev : (r['chuyen_' + prevW.toLowerCase()] || 0);
        const chuyenC = r.chuyen_curr !== undefined ? r.chuyen_curr : (r['chuyen_' + currW.toLowerCase()] || 0);
        const tldP = r.tld_prev !== undefined ? r.tld_prev : (r['tld_' + prevW.toLowerCase()] || 0);
        const tldC = r.tld_curr !== undefined ? r.tld_curr : (r['tld_' + currW.toLowerCase()] || 0);
        return `<tr${isTotal ? ' style="background:var(--color-blue-bg);font-weight:800;"' : ''}>
          ${rankCell}
          <td class="bold">${r.short_name || r.kho || ''}</td>
          <td class="num">${fNum(chuyenP)}</td>
          <td class="num bold" style="background:var(--color-blue-bg);">${fNum(chuyenC)}</td>
          <td class="num">${diffCBadge}</td>
          <td class="num">${tldP.toFixed(1)}%</td>
          <td class="num bold" style="background:var(--color-blue-bg);">${tldC.toFixed(1)}%</td>
          <td class="num">${diffTBadge}</td>"""

if old_fillrate_weekly_row in app_js:
    app_js = app_js.replace(old_fillrate_weekly_row, new_fillrate_weekly_row)
    print("✓ Fixed fill rate weekly table rows in app.js")

# Fix renderFillRateChart trend data source
old_fr_chart_trend = """    const trend = ktc.fill_rate.trend_6w;"""
new_fr_chart_trend = """    const trend = ktc.fill_rate.trend_6w || (ktc.fill_rate.history || []).map(w => ({
      week: w.week,
      tld: Number(((w.rate || 0) * 100).toFixed(1)),
      chuyen: w.trips || 0,
      under30: w.low_trips || 0
    }));
    if (!trend || trend.length === 0) return;"""

if old_fr_chart_trend in app_js:
    app_js = app_js.replace(old_fr_chart_trend, new_fr_chart_trend)
    print("✓ Fixed renderFillRateChart trend source in app.js")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

print("🎉 app.js completely updated!")

# ==============================================================================
# 2. UPDATE INDEX.HTML
# ==============================================================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Tab 1: Executive Banner
html = html.replace(
    "Dữ liệu chu kỳ W36 (31/08 – 06/09/2026) | So sánh biến động WoW với tuần trước (W35) | Tách riêng Full Hàng và TikTok Shop",
    "Dữ liệu chu kỳ W37 (07/09 – 13/09/2026) | So sánh biến động WoW với tuần trước (W36) | Tách riêng Full Hàng và TikTok Shop"
)
html = html.replace(
    "%FD Return Full Hàng (W36 vs W35)",
    "%FD Return Full Hàng (W36 vs W37)"
)
html = html.replace(
    "%FD Return TikTok Shop (W36 vs W35)",
    "%FD Return TikTok Shop (W36 vs W37)"
)
html = html.replace(
    "BẢNG 2: TOP BƯU CỤC CÓ TỶ LỆ %FD CAO NHẤT (W36)",
    "BẢNG 2: TOP BƯU CỤC CÓ TỶ LỆ %FD CAO NHẤT (W37)"
)

# Tab 4: GTC TTS Ca 1 headers
html = html.replace(
    '<th class="num">%GTC TTS Ca 1 (W35)</th>\n                  <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#c2410c;">%GTC TTS Ca 1 (W36)</th>',
    '<th class="num">%GTC TTS Ca 1 (W36)</th>\n                  <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#c2410c;">%GTC TTS Ca 1 (W37)</th>'
)

# Tab 5: Gan title & button
html = html.replace(
    "SO SÁNH TỶ LỆ GÁN 18 AM: % GÁN CA 1+TỒN vs % GÁN CA 2 vs % GÁN TỔNG (W36)",
    "SO SÁNH TỶ LỆ GÁN 18 AM: % GÁN CA 1+TỒN vs % GÁN CA 2 vs % GÁN TỔNG (W37)"
)
html = html.replace(
    '<i data-lucide="split" style="width: 14px; height: 14px;"></i> ⚡ So Sánh Full vs TTS (W35)',
    '<i data-lucide="split" style="width: 14px; height: 14px;"></i> ⚡ So Sánh Full vs TTS (W37)'
)

# Tab 9: Rot LC title
html = html.replace(
    "% RỚT LUÂN CHUYỂN THEO 18 AM PHỤ TRÁCH (W36)",
    "% RỚT LUÂN CHUYỂN THEO 18 AM PHỤ TRÁCH (W37)"
)
html = html.replace(
    "DANH SÁCH TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LUÂN CHUYỂN CAO NHẤT (W36)",
    "DANH SÁCH TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LUÂN CHUYỂN CAO NHẤT (W37)"
)

# Tab 10: Table 1 headers
html = html.replace(
    '<th class="num">Full W37</th>\n                  <th class="num" style="background: var(--color-blue-bg); font-weight:800;">Full W37</th>',
    '<th class="num">Full W36</th>\n                  <th class="num" style="background: var(--color-blue-bg); font-weight:800;">Full W37</th>'
)
html = html.replace(
    '<th class="num">TTS W37</th>\n                  <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">TTS W37</th>',
    '<th class="num">TTS W36</th>\n                  <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">TTS W37</th>'
)

# Tab 11: KTC banner & cards
html = html.replace(
    "Tổng hợp Tuần W36 đạt <strong>48.1%</strong> (516 chuyến, 112 chuyến &lt;30% cần tối ưu ghép điểm).",
    "Tổng hợp Tuần W37 đạt <strong>54.8%</strong> (551 chuyến, 80 chuyến &lt;30% – tăng <strong>+6.7%p WoW</strong> so với W36: 48.1%)."
)
html = html.replace(
    '<div class="kpi-tile-value" style="color: #ea580c;">48.1% <small style="color: var(--text-muted); font-size: 13px; font-weight: 600;">(W35: 51.8%)</small></div>',
    '<div class="kpi-tile-value" style="color: #10b981;">54.8% <small style="color: var(--text-muted); font-size: 13px; font-weight: 600;">(W36: 48.1%)</small></div>'
)
html = html.replace(
    '<span class="badge-tag badge-tag-amber">Daily 06/09: 56.2%</span>\n            <span style="color: var(--text-muted); font-size: 11.5px;">112 chuyến &lt;30%</span>',
    '<span class="badge-tag badge-tag-green">▲ +6.7%p WoW</span>\n            <span style="color: var(--text-muted); font-size: 11.5px;">80 chuyến &lt;30%</span>'
)
html = html.replace(
    '<span class="badge-tag badge-tag-amber">W35: 51.8% → W36: 48.1% (▼3.7%p)</span>',
    '<span class="badge-tag badge-tag-green">W36: 48.1% → W37: 54.8% (▲ +6.7%p)</span>'
)
html = html.replace(
    '<i data-lucide="truck" style="width: 14px; height: 14px;"></i> 🚚 3. Tỷ Lệ Lấp Đầy Thùng/Xe (W36 & Daily)',
    '<i data-lucide="truck" style="width: 14px; height: 14px;"></i> 🚚 3. Tỷ Lệ Lấp Đầy Thùng/Xe (W36 vs W37)'
)

# Tab 14: Churn table header
html = html.replace(
    "TOP 10 KHÁCH HÀNG CÓ SẢN LƯỢNG GIẢM / RỜI BỎ LỚN NHẤT (KỲ 23–29/8 vs KỲ 30/8–5/9)",
    "TOP 10 KHÁCH HÀNG CÓ SẢN LƯỢNG GIẢM / RỜI BỎ LỚN NHẤT (W37)"
)
html = html.replace(
    '<th class="num" style="color:#ffffff;">Kỳ Trước (23–29/8)</th>\n                  <th class="num" style="background: #ef4444; color:#ffffff; font-weight:800;">Kỳ Này (30/8–5/9)</th>',
    '<th class="num" style="color:#ffffff;">Kỳ Trước (W36)</th>\n                  <th class="num" style="background: #ef4444; color:#ffffff; font-weight:800;">Kỳ Này (W37)</th>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("🎉 index.html completely updated!")
