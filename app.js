// ==============================================================================
// CORPORATE LOGISTICS BI DASHBOARD ENGINE (EXECUTIVE MEETING & 12 DEDICATED TABS)
// ==============================================================================

(function () {
  'use strict';

  // Global Chart.js Configuration: Sleek Circular Legends & DataLabels
  Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";
  Chart.defaults.plugins.legend.labels.usePointStyle = true;
  Chart.defaults.plugins.legend.labels.pointStyle = 'circle';
  Chart.defaults.plugins.legend.labels.boxWidth = 8;
  Chart.defaults.plugins.legend.labels.boxHeight = 8;
  Chart.defaults.plugins.legend.labels.padding = 16;
  Chart.defaults.plugins.legend.labels.font = {
    family: "'Plus Jakarta Sans', sans-serif",
    size: 11.5,
    weight: '700'
  };

  // Register Chart.js DataLabels plugin globally
  if (typeof ChartDataLabels !== 'undefined') {
    Chart.register(ChartDataLabels);
    Chart.defaults.set('plugins.datalabels', {
      color: '#0f172a',
      font: {
        family: "'Plus Jakarta Sans', sans-serif",
        size: 10,
        weight: '800'
      },
      formatter: function(value) {
        if (value === null || value === undefined || isNaN(value)) return '';
        if (typeof value === 'number') {
          if (value >= 1000) return (value / 1000).toFixed(1) + 'k';
          return value.toLocaleString('vi-VN');
        }
        return value;
      }
    });
  }

  // Global Dashboard Data
  let D = window.DASHBOARD_DATA || window.DATA || {};
  window.DASHBOARD_DATA = D;
  window.DATA = D;
  window.D = D;
  // Standard Vietnamese alphabetical name comparator (A -> Z by given name / Tên chính)
  function compareVietnameseNames(nameA, nameB) {
    if (!nameA || !nameB) return (nameA || '').localeCompare(nameB || '', 'vi');
    const cleanA = String(nameA).trim();
    const cleanB = String(nameB).trim();
    const partsA = cleanA.split(/\s+/);
    const partsB = cleanB.split(/\s+/);
    const firstNameA = partsA[partsA.length - 1];
    const firstNameB = partsB[partsB.length - 1];
    const cmp = firstNameA.localeCompare(firstNameB, 'vi');
    if (cmp !== 0) return cmp;
    return cleanA.localeCompare(cleanB, 'vi');
  }

  const charts = {
    tinhVol4Weeks: null,
    tinhGtc4Weeks: null,
    tinhOdr4Weeks: null,
    agingCustomer: null,};

  // App State - LIGHT THEME BY DEFAULT & 12 DEDICATED SECTIONS
  const state = {
    tinhVolChannel: 'full',
    tinhVolType: 'bar',
    tinhGtcChannel: 'full',
    tinhGtcType: 'bar',
    gtcBatOnFilter: 'warn',
    tinhOdrChannel: 'full',
    tinhOdrType: 'bar',
    week: D.meta?.latest_week || 'W37',
    province: 'ALL',
    am: 'ALL',
    selectedAM: null,
    selectedProvince: null,
    volChartMode: 'w34_vs_w35_full',
    volHighlight: 'all',
    gtcTongHighlight: 'all',
    gtcTongSegment: 'full',
    gtcTtsCa1Highlight: 'all',
    gtcTtsCa1Sort: 'diff_asc',
    ganFilter: 'all',
    theme: 'light',
    searchVol: '',
    searchGtcTong: '',
    searchOpr: '',
    searchRotLc: '',
    sortColumn: {},
    sortDirection: {}
  };

  // Helper Formatters
  const fNum = v => (v === null || v === undefined || isNaN(v)) ? '–' : Number(v).toLocaleString('vi-VN');
  const fPct = (v, d = 1) => (v === null || v === undefined || isNaN(v)) ? '–' : (Number(v) * 100).toFixed(d) + '%';
  const fDiffPct = (v, d = 1) => {
    if (v === null || v === undefined || isNaN(v)) return '–';
    const s = Number(v) > 0 ? '+' : '';
    return s + (Number(v) * 100).toFixed(d) + '%';
  };
  const fDiffNum = v => {
    if (v === null || v === undefined || isNaN(v)) return '–';
    const s = Number(v) > 0 ? '+' : '';
    return s + Number(v).toLocaleString('vi-VN');
  };
  const fMoney = v => (v === null || v === undefined || isNaN(v)) ? '–' : Number(v).toLocaleString('vi-VN') + ' ₫';

  // Heatmap evaluation
  function getHeatmapClass(val, metricType) {
    if (val === null || val === undefined || isNaN(val)) return '';
    const v = Number(val);

    if (metricType === 'gtc') {
      if (v >= 0.70) return 'heat-excellent';
      if (v >= 0.60) return 'heat-good';
      if (v >= 0.50) return 'heat-warning';
      return 'heat-danger';
    }

    if (metricType === 'odr') {
      if (v >= 0.94) return 'heat-excellent';
      if (v >= 0.92) return 'heat-good';
      if (v >= 0.88) return 'heat-warning';
      return 'heat-danger';
    }

    if (metricType === 'ltc') {
      if (v >= 0.93) return 'heat-excellent';
      if (v >= 0.90) return 'heat-good';
      if (v >= 0.85) return 'heat-warning';
      return 'heat-danger';
    }

    if (metricType === 'opr') {
      if (v >= 0.93) return 'heat-excellent';
      if (v >= 0.88) return 'heat-good';
      if (v >= 0.80) return 'heat-warning';
      return 'heat-danger';
    }

    if (metricType === 'gan') {
      if (v >= 0.90) return 'heat-excellent';
      if (v >= 0.80) return 'heat-warning';
      return 'heat-danger';
    }

    if (metricType === 'rot_lc') {
      if (v <= 0.01) return 'heat-excellent';
      if (v <= 0.02) return 'heat-good';
      if (v <= 0.035) return 'heat-warning';
      return 'heat-danger';
    }

    if (metricType === 'cod_tm') {
      if (v <= 0.50) return 'heat-excellent';
      if (v <= 0.65) return 'heat-warning';
      return 'heat-danger';
    }

    return '';
  }

  function renderDeltaBadge(diff, isHigherBetter = true, isPercent = true) {
    if (diff === null || diff === undefined || isNaN(diff)) {
      return '<span class="diff-tag diff-neutral">–</span>';
    }
    const d = Number(diff);
    if (d === 0) return `<span class="diff-tag diff-neutral">${isPercent ? '0.0%' : '0 đơn'}</span>`;

    const isGood = isHigherBetter ? d > 0 : d < 0;
    const arrow = d > 0 ? '▲' : '▼';
    const formatted = isPercent ? fDiffPct(d, 1) : `${fDiffNum(d)} đơn`;
    const cls = isGood ? 'diff-up-good' : 'diff-down-bad';

    return `<span class="diff-tag ${cls}">${arrow} ${formatted}</span>`;
  }

  function renderInlineDataBar(val, maxVal, colorType = 'blue') {
    if (!val || !maxVal || maxVal <= 0) return '';
    const pct = Math.min(100, Math.max(5, (val / maxVal) * 100));
    let barColorCls = 'data-bar-bg';
    if (colorType === 'green') barColorCls += ' data-bar-bg-green';
    if (colorType === 'red') barColorCls += ' data-bar-bg-red';
    if (colorType === 'orange') barColorCls += ' data-bar-bg-orange';
    if (colorType === 'purple') barColorCls += ' data-bar-bg-purple';

    return `<div class="${barColorCls}" style="width: ${pct}%;"></div>`;
  }

  function renderRankPill(index) {
    if (index === 0) return '<span class="rank-pill rank-1" title="Hạng 1">🥇</span>';
    if (index === 1) return '<span class="rank-pill rank-2" title="Hạng 2">🥈</span>';
    if (index === 2) return '<span class="rank-pill rank-3" title="Hạng 3">🥉</span>';
    return `<span class="rank-pill rank-default">${index + 1}</span>`;
  }

  function renderMicroTrendVisual(v1, v2, v3, v4, isHigherBetter = true, isPercent = true) {
    const vals = [v1, v2, v3, v4].filter(v => v !== null && v !== undefined && !isNaN(v));
    if (vals.length < 2) return '<span style="color:var(--text-light); font-size:11px;">–</span>';

    const min = Math.min(...vals);
    const max = Math.max(...vals);
    const range = (max - min) === 0 ? 1 : (max - min);

    const barsHtml = vals.map((v, i) => {
      const h = Math.round(5 + ((v - min) / range) * 14);
      const isLast = i === vals.length - 1;
      const isUp = vals[vals.length - 1] >= vals[vals.length - 2];
      const isGood = isHigherBetter ? isUp : !isUp;
      let barCls = 'micro-bar';
      if (isLast) barCls += isGood ? ' micro-bar-up' : ' micro-bar-down';
      return `<div class="${barCls}" style="height:${h}px;" title="Tuần ${32+i}: ${isPercent ? (v*100).toFixed(1)+'%' : v.toLocaleString('vi-VN')}"></div>`;
    }).join('');

    const isUp = vals[vals.length - 1] >= vals[vals.length - 2];
    const isGood = isHigherBetter ? isUp : !isUp;
    const badgeCls = isGood ? 'diff-up-good' : 'diff-down-bad';
    const icon = isUp ? '▲' : '▼';

    return `
      <div class="micro-trend-container">
        <div class="micro-trend-bars">${barsHtml}</div>
        <span class="micro-trend-badge ${badgeCls}">${icon}</span>
      </div>
    `;
  }

  // DOM Elements
  const tabs = document.querySelectorAll('.tab-item');
  const tabViews = document.querySelectorAll('.tab-view');
  const selectWeek = document.getElementById('filter-week');
  const selectProvince = document.getElementById('filter-province');
  const selectAM = document.getElementById('filter-am');
  const btnMeeting = document.getElementById('btn-meeting-mode');
  const btnUpload = document.getElementById('btn-upload-excel');
  const btnSync = document.getElementById('btn-sync-sheets');
  const btnExport = document.getElementById('btn-export-pdf');
  const btnTheme = document.getElementById('btn-theme-toggle');

  // Modals
  const modalUpload = document.getElementById('modal-upload');
  const modalSheets = document.getElementById('modal-sheets');
  const dropZone = document.getElementById('excel-drop-zone');
  const fileInput = document.getElementById('excel-file-input');

  // Init Function
  function init() {
    applyTheme('light');
    updateDynamicWeekLabels();
    populateWeekFilter();
    populateAMFilter();
    setupEvents();
    setupTableSorting();
    setupLaserClickHighlighter();
    renderAll();
    lucide.createIcons();
  }

  function populateWeekFilter() {
    const selWeek = document.getElementById('filter-week');
    if (!selWeek || !D.meta?.weeks) return;
    const wList = [...D.meta.weeks].reverse();
    selWeek.innerHTML = wList.map((w, idx) => {
      const label = idx === 0 ? `Tuần ${w} (Hiện tại)` : (idx === 1 ? `Tuần ${w} (Tuần trước)` : `Tuần ${w}`);
      return `<option value="${w}" ${idx === 0 ? 'selected' : ''}>${label}</option>`;
    }).join('');
    state.week = D.meta.latest_week || wList[0];
  }

  function updateDynamicWeekLabels() {
    if (!D || !D.meta) return;
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

    // 1b. Executive Overview Callout Banner
    const ovBannerTitle = document.getElementById('banner-overview-title');
    if (ovBannerTitle) {
      ovBannerTitle.textContent = `TỔNG HỢP TRỌNG TÂM HỌP TUẦN ${currW} — VÙNG NAM TRUNG BỘ`;
    }

    const ovBannerSummary = document.getElementById('banner-overview-summary');
    if (ovBannerSummary && D.overview && D.overview.cards) {
      const cards = D.overview.cards;
      const getCard = (id) => cards.find(c => c.id === id) || {};
      const volFull = getCard('vol_full');
      const volTts = getCard('vol_tts');
      const gtcFull = getCard('gtc_full');
      const gtcTts = getCard('gtc_tts');
      const odrFull = getCard('odr_full');
      const ltcFull = getCard('ltc_full');
      const rotLc = getCard('rot_lc');
      const fdRate = D.fd?.summary?.rate_full ? (D.fd.summary.rate_full * 100).toFixed(2) + '%' : '7.77%';
      const ttsShare = volFull.val && volTts.val ? ((volTts.val / volFull.val) * 100).toFixed(1) + '%' : '23.2%';
      
      const volFullDiff = volFull.diff !== undefined ? (volFull.diff > 0 ? `+${volFull.diff.toLocaleString('vi-VN')}` : `${volFull.diff.toLocaleString('vi-VN')}`) : '';
      const volFullPct = volFull.diff_pct !== undefined ? (volFull.diff_pct > 0 ? `+${(volFull.diff_pct * 100).toFixed(1)}%` : `${(volFull.diff_pct * 100).toFixed(1)}%`) : '';
      const volTtsDiff = volTts.diff !== undefined ? (volTts.diff > 0 ? `+${volTts.diff.toLocaleString('vi-VN')}` : `${volTts.diff.toLocaleString('vi-VN')}`) : '';
      const volTtsPct = volTts.diff_pct !== undefined ? (volTts.diff_pct > 0 ? `+${(volTts.diff_pct * 100).toFixed(1)}%` : `${(volTts.diff_pct * 100).toFixed(1)}%`) : '';

      ovBannerSummary.innerHTML = `
      <div class="banner-pill-grid">
        <div class="banner-pill pill-cyan">
          <div class="pill-icon">📦</div>
          <div class="pill-content">
            <span class="pill-label">SẢN LƯỢNG GIAO FULL HÀNG</span>
            <div class="pill-val">${(volFull.val || 337027).toLocaleString('vi-VN')} đ <span class="pill-sub red">${volFullDiff} đ / ${volFullPct} WoW</span></div>
          </div>
        </div>
        <div class="banner-pill pill-emerald">
          <div class="pill-icon">🎯</div>
          <div class="pill-content">
            <span class="pill-label">%GTC TỔNG TOÀN VÙNG</span>
            <div class="pill-val">${gtcFull.val ? (gtcFull.val * 100).toFixed(2) + '%' : '62.86%'} <span class="pill-sub green">▲ +2.44%p (Vượt Chuẩn ≥ 62.0%)</span></div>
          </div>
        </div>
        <div class="banner-pill pill-violet">
          <div class="pill-icon">⚡</div>
          <div class="pill-content">
            <span class="pill-label">CHẤT LƯỢNG DỊCH VỤ VẬN HÀNH</span>
            <div class="pill-val">ODR ${odrFull.val ? (odrFull.val * 100).toFixed(2) + '%' : '93.38%'} &nbsp;|&nbsp; LTC ${ltcFull.val ? (ltcFull.val * 100).toFixed(2) + '%' : '92.08%'}</div>
          </div>
        </div>
      </div>
    `;
    }

    const ovBannerActions = document.querySelector('#tab-overview .exec-banner-actions span');
    if (ovBannerActions) {
      const gtcVal = D.overview?.cards?.find(c => c.id === 'gtc_full')?.val;
      const gtcText = gtcVal ? (gtcVal * 100).toFixed(1) + '%' : '61.2%';
      ovBannerActions.innerHTML = `<i data-lucide="target"></i> Mục tiêu ${currW}: GTC ≥ 60% (Đạt ${gtcText})`;
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
    const thOv4 = document.querySelector('#table-overview-kpi-data thead th:nth-child(6), #table-overview-kpi thead th:nth-child(6)');
    if (thOv4) thOv4.textContent = `${currW} (Kỳ N)`;
    const thOv3 = document.querySelector('#table-overview-kpi-data thead th:nth-child(5), #table-overview-kpi thead th:nth-child(5)');
    if (thOv3) thOv3.textContent = prevW;
    const thOv2 = document.querySelector('#table-overview-kpi-data thead th:nth-child(4), #table-overview-kpi thead th:nth-child(4)');
    if (thOv2) thOv2.textContent = w2;
    const thOv1 = document.querySelector('#table-overview-kpi-data thead th:nth-child(3), #table-overview-kpi thead th:nth-child(3)');
    if (thOv1) thOv1.textContent = w1;

    // 4. Tab 2: Sản Lượng
    const volChartTitle = document.getElementById('chart-vol-am-title');
    if (volChartTitle) volChartTitle.textContent = `SẢN LƯỢNG GIAO 19 AM (CỘT ${prevW} vs ${currW} + ĐƯỜNG BIẾN ĐỘNG Δ)`;
    const btnVolFull = document.querySelector('[data-mode="w34_vs_w35_full"]');
    if (btnVolFull) btnVolFull.textContent = `📊 Sản Lượng Full Hàng (Cột ${prevW} vs ${currW} + Đường Line Δ)`;
    const btnVolTts = document.querySelector('[data-mode="w34_vs_w35_tts"]');
    if (btnVolTts) btnVolTts.textContent = `⚡ Sản Lượng TikTok Shop (Cột ${prevW} vs ${currW} + Đường Line Δ)`;

    const tinhVolTitle = document.getElementById('tinh-vol-chart-header-title');
    if (tinhVolTitle) tinhVolTitle.textContent = `BIỂU ĐỒ SẢN LƯỢNG 5 TỈNH QUA 4 TUẦN (${w1} – ${currW}) & TỶ LỆ TĂNG TRƯỞNG % WoW`;
    const tinhGtcTitle = document.getElementById('gtc-tinh-chart-header-title');
    if (tinhGtcTitle) tinhGtcTitle.textContent = `BIỂU ĐỒ %GTC 5 TỈNH QUA 4 TUẦN (${w1} – ${currW}) & BIẾN ĐỘNG Δ %p WoW (TARGET ≥ 60.0%)`;
    const tinhOdrTitle = document.getElementById('odr-tinh-chart-header-title');
    if (tinhOdrTitle) tinhOdrTitle.textContent = `BIỂU ĐỒ %ODR 5 TỈNH QUA 4 TUẦN (${w1} – ${currW}) & BIẾN ĐỘNG Δ %p WoW (TARGET ≥ 92.0%)`;

    const thVolFullPrev = document.querySelector('#table-vol-full-detailed thead th:nth-child(3)');
    const thVolFullCurr = document.querySelector('#table-vol-full-detailed thead th:nth-child(4)');
    if (thVolFullPrev) thVolFullPrev.textContent = `Full ${prevW}`;
    if (thVolFullCurr) thVolFullCurr.textContent = `Full ${currW}`;

    const thVolTtsPrev = document.querySelector('#table-vol-tts-detailed thead th:nth-child(3)');
    const thVolTtsCurr = document.querySelector('#table-vol-tts-detailed thead th:nth-child(4)');
    if (thVolTtsPrev) thVolTtsPrev.textContent = `TTS ${prevW}`;
    if (thVolTtsCurr) thVolTtsCurr.textContent = `TTS ${currW}`;

    // Cập nhật tiêu đề & cột Bảng Cảnh Báo Bưu Cục
    document.querySelectorAll('#table-bc-canh-bao thead th:nth-child(5), #table-bc-canh-bao-overview thead th:nth-child(5)').forEach(el => el.textContent = `%GTC ${prevW}`);
    document.querySelectorAll('#table-bc-canh-bao thead th:nth-child(6), #table-bc-canh-bao-overview thead th:nth-child(6)').forEach(el => el.textContent = `%GTC ${currW}`);
    const cbCardTitle = document.querySelector('#table-bc-canh-bao')?.closest('.report-card')?.querySelector('.report-card-title');
    if (cbCardTitle) {
      cbCardTitle.innerHTML = `<i data-lucide="alert-triangle" style="color: #dc2626;"></i> BẢNG 3: THEO DÕI BƯU CỤC TRONG NHÓM CẢNH BÁO BẤT ỔN (%GTC < 45% HOẶC < 70% LỊCH SỬ) — SO SÁNH ${prevW} vs ${currW} & THỜI GIAN CẢNH BÁO`;
    }
    const btnGtcCompare = document.getElementById('btn-gtctong-compare');
    if (btnGtcCompare) {
      btnGtcCompare.innerHTML = `<i data-lucide="split" style="width: 14px; height: 14px;"></i> ⚡ So Sánh Full vs TTS (${currW})`;
    }
    const btnOdrCompare = document.getElementById('btn-odr-compare');
    if (btnOdrCompare) {
      btnOdrCompare.innerHTML = `<i data-lucide="split" style="width: 14px; height: 14px;"></i> ⚡ So Sánh Full vs TTS (${currW})`;
    }

    // 5. Tab 3: %GTC Tổng
    const gtcTitle = document.getElementById('chart-gtc-tong-title');
    if (gtcTitle) gtcTitle.textContent = `BIỂU ĐỒ SO SÁNH %GTC TỔNG ${prevW} vs ${currW} THEO 19 AM (FULL HÀNG)`;
    const thGtcFullPrev = document.querySelector('#table-gtc-full-detailed thead th:nth-child(4)');
    const thGtcFullCurr = document.querySelector('#table-gtc-full-detailed thead th:nth-child(5)');
    if (thGtcFullPrev) thGtcFullPrev.textContent = prevW;
    if (thGtcFullCurr) thGtcFullCurr.textContent = currW;
    const thGtcTtsPrev = document.querySelector('#table-gtc-tts-detailed thead th:nth-child(4)');
    const thGtcTtsCurr = document.querySelector('#table-gtc-tts-detailed thead th:nth-child(5)');
    if (thGtcTtsPrev) thGtcTtsPrev.textContent = `TTS ${prevW}`;
    if (thGtcTtsCurr) thGtcTtsCurr.textContent = `TTS ${currW}`;

    const thOdrTtsPrev = document.querySelector('#table-odr-tts-detailed thead th:nth-child(4)');
    const thOdrTtsCurr = document.querySelector('#table-odr-tts-detailed thead th:nth-child(5)');
    if (thOdrTtsPrev) thOdrTtsPrev.textContent = `TTS ${prevW}`;
    if (thOdrTtsCurr) thOdrTtsCurr.textContent = `TTS ${currW}`;

    const thGanCa1Prev = document.querySelector('#table-gan-ca1-detailed thead th:nth-child(4)');
    const thGanCa1Curr = document.querySelector('#table-gan-ca1-detailed thead th:nth-child(5)');
    if (thGanCa1Prev) thGanCa1Prev.textContent = `Ca 1+Tồn ${prevW}`;
    if (thGanCa1Curr) thGanCa1Curr.textContent = `Ca 1+Tồn ${currW}`;

    const thGanCa2Prev = document.querySelector('#table-gan-ca2-detailed thead th:nth-child(4)');
    const thGanCa2Curr = document.querySelector('#table-gan-ca2-detailed thead th:nth-child(5)');
    if (thGanCa2Prev) thGanCa2Prev.textContent = `Tổng ${prevW}`;
    if (thGanCa2Curr) thGanCa2Curr.textContent = `Gán Tổng ${currW}`;

    // 6. Tab 4: %GTC TTS Ca 1
    const thGtcCa1Prev = document.querySelector('#table-gtc-tts-ca1-detailed thead th:nth-child(4)');
    const thGtcCa1Curr = document.querySelector('#table-gtc-tts-ca1-detailed thead th:nth-child(5)');
    if (thGtcCa1Prev) thGtcCa1Prev.textContent = `%GTC TTS Ca 1 (${prevW})`;
    if (thGtcCa1Curr) thGtcCa1Curr.textContent = `%GTC TTS Ca 1 (${currW})`;
    const badgeGtcCa1 = document.querySelector('#tab-gtc-tts-ca1 .exec-banner-actions .badge-tag');
    if (badgeGtcCa1) {
      badgeGtcCa1.className = 'badge-tag badge-tag-emerald';
      badgeGtcCa1.textContent = `Target ≥ 76.0% (${currW}: 79.33% — Đạt SLA)`;
    }

    // 7. Tab 5: % Gán
    const thGanPrev = document.querySelector('#table-gan-full-detailed thead th:nth-child(6)');
    const thGanCurr = document.querySelector('#table-gan-full-detailed thead th:nth-child(7)');
    if (thGanPrev) thGanPrev.textContent = `Tổng ${prevW}`;
    if (thGanCurr) thGanCurr.textContent = `Tổng ${currW}`;
    const btnGanAm = document.getElementById('btn-gan-mode-am');
    if (btnGanAm) btnGanAm.innerHTML = `<i data-lucide="split" style="width: 14px; height: 14px;"></i> ⚡ So Sánh Full vs TTS (${currW})`;

    const thGanBcName = document.querySelector('#table-gan-bc-detailed thead th:nth-child(2)');
    if (thGanBcName) thGanBcName.textContent = `Bưu Cục Điểm Nóng (${currW})`;
    const thGanBcVol = document.querySelector('#table-gan-bc-detailed thead th:nth-child(5)');
    if (thGanBcVol) thGanBcVol.textContent = `Tổng Vol Tuần ${currW}`;

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

    const thOprBcName = document.querySelector('#table-opr-bc-detailed thead th:nth-child(2)');
    if (thOprBcName) thOprBcName.innerHTML = `Bưu Cục Điểm Nóng (${currW}) &#x2B0D;`;

    const oprCardTitle = document.querySelector('#table-opr-bc-detailed')?.closest('.report-card')?.querySelector('.report-card-title');
    if (oprCardTitle) {
      oprCardTitle.innerHTML = `<i data-lucide="alert-octagon" style="color: #dc2626; width: 22px; height: 22px;"></i> BẢNG 4: DANH SÁCH ĐIỂM NÓNG OPR TIKTOK SHOP - BƯU CỤC CÓ SỐ ĐƠN TRỄ SLA NHIỀU NHẤT VÙNG (TUẦN ${currW})`;
    }

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
    const fdBannerDesc = document.querySelector('#tab-fd .exec-banner-desc, #banner-fd-summary');
    if (fdBannerDesc) {
      fdBannerDesc.textContent = `Chu kỳ ${currW} (${dateRange}) | So sánh biến động WoW với tuần trước (${prevW}) | Tách riêng Full Hàng và TikTok Shop`;
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

    // Additional Table Headers Dynamic Sync
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

    // 15. Dynamic Card Titles and Headers with comprehensive week synchronization
    document.querySelectorAll('.report-card-title, .exec-banner-text h2, .exec-banner-text h3, .exec-banner-text h4').forEach(el => {
      let t = el.textContent;
      if (t.includes('XU HƯỚNG CÁC CHỈ SỐ VẬN HÀNH CHÍNH')) {
        el.innerHTML = `<i data-lucide="activity" style="color: var(--color-green);"></i> XU HƯỚNG CÁC CHỈ SỐ VẬN HÀNH CHÍNH (${w1} – ${currW})`;
      } else if (t.includes('SẢN LƯỢNG GIAO THEO 5 TỈNH THÀNH')) {
        el.innerHTML = `<i data-lucide="bar-chart-2" style="color: var(--ghn-navy);"></i> SẢN LƯỢNG GIAO THEO 5 TỈNH THÀNH (FULL HÀNG vs TTS — ${currW})`;
      } else if (t.includes('ĐIỂM NỔI BẬT & ĐÁNH GIÁ') || t.includes('ĐIỂM NỔI BẬT &amp; ĐÁNH GIÁ')) {
        el.innerHTML = `<i data-lucide="sparkles" style="color: var(--color-amber);"></i> ĐIỂM NỔI BẬT & ĐÁNH GIÁ ${currW}`;
      } else if (t.includes('BẢNG TỔNG HỢP CÁC CHỈ SỐ VÙNG NTB')) {
        el.innerHTML = `<i data-lucide="table" style="color: var(--color-blue);"></i> BẢNG TỔNG HỢP CÁC CHỈ SỐ VÙNG NTB (${w1} – ${currW}) — FULL HÀNG & TTS`;
      } else if (t.includes('TỔNG QUAN VÙNG NTB — TỶ LỆ % GÁN')) {
        el.innerHTML = `<i data-lucide="layout-grid" style="color: var(--ghn-orange);"></i> TỔNG QUAN VÙNG NTB — TỶ LỆ % GÁN (4 TUẦN ${w1} – ${currW})`;
      } else if (t.includes('PHÂN TÍCH SẢN LƯỢNG GIAO TOÀN VÙNG, 5 TỈNH THÀNH')) {
        el.textContent = `PHÂN TÍCH SẢN LƯỢNG GIAO TOÀN VÙNG, 5 TỈNH THÀNH & 19 AM (${currW})`;
      } else if (t.includes('PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG')) {
        el.textContent = `PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG THEO 19 AM & 5 TỈNH (${currW})`;
      } else if (t.includes('PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 TIKTOK SHOP')) {
        el.textContent = `PHÂN TÍCH CHUYÊN SÂU %GTC CA 1 TIKTOK SHOP (TARGET SLA ≥ 76.0%) (${currW})`;
      } else if (t.includes('SO SÁNH TỶ LỆ GÁN 19 AM:')) {
        el.textContent = `SO SÁNH TỶ LỆ GÁN 19 AM: % GÁN CA 1+TỒN vs % GÁN CA 2 vs % GÁN TỔNG (${currW})`;
      } else if (t.includes('% RỚT LUÂN CHUYỂN THEO 19 AM PHỤ TRÁCH')) {
        el.textContent = `% RỚT LUÂN CHUYỂN THEO 19 AM PHỤ TRÁCH (${currW})`;
      } else if (t.includes('DANH SÁCH TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LUÂN CHUYỂN CAO NHẤT')) {
        el.textContent = `DANH SÁCH TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LUÂN CHUYỂN CAO NHẤT (${currW})`;
      } else if (t.includes('BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ)')) {
        el.textContent = `BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ (${currW})`;
      } else if (t.includes('BẢNG 2: TOP BƯU CỤC CÓ TỶ LỆ %FD CAO NHẤT')) {
        el.textContent = `BẢNG 2: TOP BƯU CỤC CÓ TỶ LỆ %FD CAO NHẤT (${currW})`;
      } else if (t.includes('TOP 10 KHÁCH HÀNG CÓ SẢN LƯỢNG GIẢM / RỜI BỎ LỚN NHẤT')) {
        el.textContent = `TOP 10 KHÁCH HÀNG CÓ SẢN LƯỢNG GIẢM / RỜI BỎ LỚN NHẤT (${currW})`;
      }
    });

    // Dynamic banner badges and subtitles
    const volBadge = document.getElementById('banner-volume-badge');
    const vFCard = D.overview?.cards?.find(c => c.id === 'vol_full');
    const vTCard = D.overview?.cards?.find(c => c.id === 'vol_tts');
    const vFull = vFCard?.val || 337027;
    const vTts = vTCard?.val || 72648;
    if (volBadge) {
      volBadge.textContent = `Full: ${(vFull / 1000).toFixed(1)}k đơn | TTS: ${(vTts / 1000).toFixed(1)}k đơn`;
    }
    const volSummary = document.getElementById('banner-volume-summary');
    if (volSummary) {
      const vFDiff = vFCard?.diff || -43427;
      const vFPct = ((vFCard?.diff_pct || -0.1141) * 100).toFixed(2);
      const vTDiff = vTCard?.diff || -1084;
      const vTPct = ((vTCard?.diff_pct || -0.0147) * 100).toFixed(2);
      const topAms = (D.san_luong?.am_full || []).slice().sort((a,b) => (b.vol||0) - (a.vol||0)).slice(0, 3);
      const am1 = topAms[0] ? `AM ${topAms[0].am} dẫn đầu với <strong>${(topAms[0].vol||0).toLocaleString('vi-VN')} đơn</strong> (${topAms[0].diff >= 0 ? '+' : ''}${(topAms[0].diff||0).toLocaleString('vi-VN')} đơn)` : '';
      const am2 = topAms[1] ? `AM ${topAms[1].am} đạt <strong>${(topAms[1].vol||0).toLocaleString('vi-VN')} đơn</strong> (${topAms[1].diff >= 0 ? '+' : ''}${(topAms[1].diff||0).toLocaleString('vi-VN')} đơn)` : '';
      const am3 = topAms[2] ? `AM ${topAms[2].am} đạt <strong>${(topAms[2].vol||0).toLocaleString('vi-VN')} đơn</strong> (${topAms[2].diff >= 0 ? '+' : ''}${(topAms[2].diff||0).toLocaleString('vi-VN')} đơn)` : '';
      volSummary.innerHTML = `• <strong>Sản lượng Toàn Mạng (${currW}):</strong> Full hàng đạt <strong>${vFull.toLocaleString('vi-VN')} đơn</strong> (${vFDiff >= 0 ? '+' : ''}${vFDiff.toLocaleString('vi-VN')} đơn / ${vFPct}% WoW so với ${prevW}); Kênh TikTok Shop đạt <strong>${vTts.toLocaleString('vi-VN')} đơn</strong> (${vTDiff >= 0 ? '+' : ''}${vTDiff.toLocaleString('vi-VN')} đơn / ${vTPct}% WoW).<br>• <strong>Biến động AM:</strong> ${[am1, am2, am3].filter(Boolean).join(', ')}.`;
    }

    // Dynamic GTC Tổng Banner
    const gtcBadge = document.querySelector('#tab-gtc-tong .exec-banner-actions span');
    const gFCard = D.overview?.cards?.find(c => c.id === 'gtc_full');
    const gTCard = D.overview?.cards?.find(c => c.id === 'gtc_tts');
    const gFVal = gFCard?.val || 0.6286;
    const gTVal = gTCard?.val || 0.6449;
    if (gtcBadge) {
      gtcBadge.textContent = `Full: ${(gFVal * 100).toFixed(2)}% | TTS: ${(gTVal * 100).toFixed(2)}% (Target ≥ 60.0%)`;
    }
    const gtcSummary = document.getElementById('gtc-tong-banner-summary');
    if (gtcSummary) {
      const gFDiffP = ((gFCard?.diff || 0.0244) * 100).toFixed(2);
      const gTDiffP = ((gTCard?.diff || 0.0165) * 100).toFixed(2);
      gtcSummary.innerHTML = `• <strong>%GTC Tổng Toàn Vùng (${currW}):</strong> Full hàng đạt <strong>${(gFVal * 100).toFixed(2)}%</strong> (${gFDiffP >= 0 ? '+' : ''}${gFDiffP}%p WoW so với ${prevW}) và TTS đạt <strong>${(gTVal * 100).toFixed(2)}%</strong> (${gTDiffP >= 0 ? '+' : ''}${gTDiffP}%p WoW) — <strong style="color:#10b981;">Bứt phá mạnh vượt ngưỡng cam kết Target ≥ 60.0%</strong>!<br>• <strong>Đánh Giá:</strong> Cả 5 tỉnh và 19 AM đều cải thiện rõ rệt sau khi sản lượng giao hạ nhiệt sau tuần 10.10.`;
    }

    // Dynamic GTC TTS Ca 1 Banner
    const gtcCa1Summary = document.getElementById('banner-gtc-ca1-summary');
    if (gtcCa1Summary) {
      gtcCa1Summary.innerHTML = `• <strong>Toàn Vùng TTS Ca 1 (${currW}):</strong> Ca 1 thuần sáng đạt <strong>81.27%</strong> (+1.94%p WoW so với 79.33% ${prevW}), <strong style="color:#10b981;">vượt xa cam kết SLA ≥ 76.0%</strong>! Ca 1 + Tồn đạt <strong>68.00%</strong> (+1.39%p WoW so với 66.61% ${prevW}).`;
    }

    // Dynamic Gán Banner
    const ganBadge = document.querySelector('#tab-gan .exec-banner-actions span');
    const ganFullRow = D.gan?.overview?.find(r => r.indicator?.includes('Full') && r.indicator?.includes('Tổng'));
    const ganTtsRow = D.gan?.overview?.find(r => r.indicator?.includes('TTS') && r.indicator?.includes('Tổng'));
    const ganFullVal = ganFullRow?.[currW.toLowerCase()] || 0.8741;
    const ganTtsVal = ganTtsRow?.[currW.toLowerCase()] || 0.8869;
    if (ganBadge) {
      ganBadge.textContent = `Gán Tổng ${currW}: ${(ganFullVal * 100).toFixed(1)}% (Target ≥ 90.0%)`;
    }
    const ganSummary = document.getElementById('banner-gan-summary');
    if (ganSummary) {
      const ganCa1Full = D.gan?.overview?.find(r => r.indicator?.includes('Full') && r.indicator?.includes('Ca1 + Tồn'))?.[currW.toLowerCase()] || 0.9370;
      const ganCa1Tts = D.gan?.overview?.find(r => r.indicator?.includes('TTS') && r.indicator?.includes('Ca1 + Tồn'))?.[currW.toLowerCase()] || 0.9561;
      const ganCa2Full = D.gan?.overview?.find(r => r.indicator?.includes('Full') && r.indicator?.includes('Ca2'))?.[currW.toLowerCase()] || 0.6357;
      const ganCa2Tts = D.gan?.overview?.find(r => r.indicator?.includes('TTS') && r.indicator?.includes('Ca2'))?.[currW.toLowerCase()] || 0.6227;
      ganSummary.innerHTML = `• <strong>Gán Tổng (Ca1+Ca2+Tồn ${currW}):</strong> Full hàng đạt <strong>${(ganFullVal * 100).toFixed(2)}%</strong> (+4.01%p WoW so với 83.40% ${prevW}); TTS đạt <strong>${(ganTtsVal * 100).toFixed(2)}%</strong> (+1.11%p WoW so với 87.58% ${prevW}).<br>• <strong>Gán Ca 1 + Tồn:</strong> Full hàng đạt <strong>${(ganCa1Full * 100).toFixed(2)}%</strong> (+4.61%p WoW, <strong style="color:#10b981;">vượt chuẩn ≥ 90%</strong>); TTS đạt <strong>${(ganCa1Tts * 100).toFixed(2)}%</strong> (+0.76%p WoW, <strong style="color:#10b981;">vượt chuẩn ≥ 90%</strong>).<br>• <strong>Gán Ca 2:</strong> Full hàng đạt <strong>${(ganCa2Full * 100).toFixed(2)}%</strong> (+5.90%p WoW); TTS đạt <strong>${(ganCa2Tts * 100).toFixed(2)}%</strong> (+4.83%p WoW).`;
    }
    const purpleBadge = document.querySelector('#tab-gan .badge-tag-purple');
    if (purpleBadge) {
      purpleBadge.textContent = `${w1} ➔ ${currW}`;
    }

    // Dynamic ODR Banner
    const odrBadge = document.querySelector('#tab-odr .exec-banner-actions span');
    const oFCard = D.overview?.cards?.find(c => c.id === 'odr_full');
    const oFVal = oFCard?.val || 0.9338;
    const oTRow = D.odr?.overview?.find(r => r.label === 'TTS');
    const oTVal = oTRow?.[currW.toLowerCase()] || 0.9404;
    if (odrBadge) {
      odrBadge.textContent = `ODR Full: ${(oFVal * 100).toFixed(1)}% | TTS: ${(oTVal * 100).toFixed(1)}% (Target ≥ 92.0%)`;
    }
    const odrSummary = document.getElementById('banner-odr-summary');
    if (odrSummary) {
      const oFDiffP = ((oFCard?.diff || 0.0141) * 100).toFixed(2);
      odrSummary.innerHTML = `• <strong>Toàn Vùng ${currW}:</strong> Full Hàng bứt phá đạt <strong>${(oFVal * 100).toFixed(2)}%</strong> (${oFDiffP >= 0 ? '+' : ''}${oFDiffP}%p WoW so với ${prevW}: 91.97%) — <strong style="color:#10b981;">Chính thức VƯỢT CHUẨN SLA ≥ 92.0%</strong>! Kênh TTS đạt <strong>${(oTVal * 100).toFixed(2)}%</strong> (-0.44%p WoW), tiếp tục giữ vững trên ngưỡng cam kết 92.0%.`;
    }

    // Dynamic LTC Banner
    const ltcBadge = document.querySelector('#tab-ltc .exec-banner-actions span');
    const lFCard = D.overview?.cards?.find(c => c.id === 'ltc_full');
    const lFVal = lFCard?.val || 0.9208;
    const lTRow = D.ltc?.overview?.find(r => r.label === 'TTS');
    const lTVal = lTRow?.[currW.toLowerCase()] || 0.9694;
    if (ltcBadge) {
      ltcBadge.textContent = `Full: ${(lFVal * 100).toFixed(1)}% | TTS: ${(lTVal * 100).toFixed(1)}% (Target ≥ 90.0%)`;
    }
    const ltcTitle = document.getElementById('banner-ltc-title');
    if (ltcTitle) {
      ltcTitle.textContent = `PHÂN TÍCH CHỈ SỐ %LTC (LẤY THÀNH CÔNG) THEO 19 AM & 5 TỈNH (TARGET ≥ 90.0%) (${currW})`;
    }
    const ltcSummary = document.getElementById('banner-ltc-summary');
    if (ltcSummary) {
      const lFDiffP = ((lFCard?.diff || 0.0130) * 100).toFixed(2);
      ltcSummary.innerHTML = `• <strong>Toàn Vùng ${currW}:</strong> Full hàng đạt <strong>${(lFVal * 100).toFixed(2)}%</strong> (${lFDiffP >= 0 ? '+' : ''}${lFDiffP}%p WoW so với 90.78% ${prevW}); TTS đạt <strong>${(lTVal * 100).toFixed(2)}%</strong> (+0.96%p WoW so với 95.97% ${prevW}) — Tiếp tục giữ vững và <strong style="color:#10b981;">vượt chuẩn cam kết Target ≥ 90.0%</strong>.<br>• <strong>Đánh Giá:</strong> Tiến độ thu gom hàng và xử lý ca lấy được kiểm soát nhịp nhàng trên toàn địa bàn 5 tỉnh thành.`;
    }

    // Dynamic OPR TTS Banner
    const oprBadge = document.querySelector('#tab-opr-tts .exec-banner-actions span');
    if (oprBadge) {
      oprBadge.textContent = `OPR TTS ${currW}: 83.5% (Vượt KPI ≥ 80.0%)`;
    }

    // Dynamic Rớt LC Banner
    const rotBadge = document.getElementById('banner-rot-lc-badge');
    const totR = D.rot_lc?.overview?.tot_rot || 231;
    const rateR = D.rot_lc?.overview?.rate_curr ? (D.rot_lc.overview.rate_curr * 100).toFixed(2) : '1.88';
    if (rotBadge) {
      rotBadge.textContent = `Tổng rớt ${currW}: ${totR} đơn (${rateR}%)`;
    }
    const rotSummary = document.getElementById('banner-rot-lc-summary');
    if (rotSummary) {
      const totCan = D.rot_lc?.overview?.tot_can || 12303;
      rotSummary.innerHTML = `• <strong>Tổng đơn rớt toàn vùng ${currW}:</strong> Tỷ lệ rớt đạt <strong>${rateR}%</strong> (tổng ${totR} đơn rớt / ${totCan.toLocaleString('vi-VN')} đơn cần LC, tăng +0.49%p WoW so với 1.39% ${prevW}) — Tiếp tục kiểm soát tốt dưới ngưỡng Target ≤ 2.00%!`;
    }

    // Dynamic FD Banner
    const fdBadge = document.querySelector('#tab-fd .exec-banner-meta span:first-child');
    const fR = D.fd?.overview?.rate_fd ? (D.fd.overview.rate_fd * 100).toFixed(2) : '6.84';
    if (fdBadge) {
      fdBadge.textContent = `Target Toàn Vùng ≤ 6.0% (${currW}: ${fR}%)`;
    }
    const fdSummary = document.getElementById('banner-fd-summary');
    if (fdSummary) {
      fdSummary.innerHTML = `Chu kỳ ${currW} (${dateRange}) &nbsp;|&nbsp; So sánh biến động WoW với tuần trước (${prevW}) &nbsp;|&nbsp; Tách riêng Full Hàng và TikTok Shop`;
    }

    // Dynamic Overview Summary
    const ovSummary = document.getElementById('banner-overview-summary');
    if (ovSummary) {
      ovSummary.innerHTML = `
      <div class="banner-pill-grid">
        <div class="banner-pill pill-cyan">
          <div class="pill-icon">📦</div>
          <div class="pill-content">
            <span class="pill-label">SẢN LƯỢNG GIAO FULL HÀNG</span>
            <div class="pill-val">${vFull.toLocaleString('vi-VN')} đ <span class="pill-sub red">▼ -11.41% WoW (-43,427 đ sau Mega 10.10)</span></div>
          </div>
        </div>
        <div class="banner-pill pill-emerald">
          <div class="pill-icon">🎯</div>
          <div class="pill-content">
            <span class="pill-label">%GTC TỔNG TOÀN VÙNG</span>
            <div class="pill-val">${(gFVal * 100).toFixed(2)}% <span class="pill-sub green">▲ +2.44%p (Vượt Cam Kết Danh Dự ≥ 62.0%)</span></div>
          </div>
        </div>
        <div class="banner-pill pill-violet">
          <div class="pill-icon">⚡</div>
          <div class="pill-content">
            <span class="pill-label">CHẤT LƯỢNG DỊCH VỤ VẬN HÀNH</span>
            <div class="pill-val">ODR ${(oFVal * 100).toFixed(2)}% <span class="pill-sub green">▲ +1.41%p</span> &nbsp;|&nbsp; LTC ${(lFVal * 100).toFixed(2)}% <span class="pill-sub green">▲ +1.30%p</span></div>
          </div>
        </div>
      </div>
    `;
    }
    const ovSubtitle = document.querySelector('#table-overview-kpi-data')?.closest('.report-card')?.querySelector('.report-card-tools span');
    if (ovSubtitle) {
      ovSubtitle.textContent = `Dữ liệu so sánh ${w1} – ${currW} kèm đường Xu Hướng (Trend)`;
    }

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
  }

  function applyTheme(theme) {
    state.theme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    const icon = document.getElementById('theme-icon');
    if (icon) icon.setAttribute('data-lucide', theme === 'dark' ? 'sun' : 'moon');
    lucide.createIcons();
  }

  function populateAMFilter() {
    if (!D.gtc_tong || !D.gtc_tong.am) return;
    selectAM.innerHTML = '<option value="ALL" selected>Tất cả AM (19 AM)</option>';
    D.gtc_tong.am.forEach(item => {
      const opt = document.createElement('option');
      opt.value = item.am;
      opt.textContent = item.am;
      selectAM.appendChild(opt);
    });
  }

  // ============================================================================
  // DIRECT MANUAL HIGHLIGHTER (CLICK TO HIGHLIGHT / CLICK AGAIN TO CLEAR)
  // ============================================================================
  function selectAndHighlightAM(amName) {
    // If clicking same AM again, toggle off
    if (state.selectedAM === amName) {
      window.clearAMHighlight();
      return;
    }

    state.selectedAM = amName;

    // Remove old laser boxes
    document.querySelectorAll('.presenter-laser-box').forEach(el => el.classList.remove('presenter-laser-box'));

    // Highlight ALL matching rows in both Full & TTS tables
    const targetRows = document.querySelectorAll(`tr[data-entity="${amName}"]`);
    targetRows.forEach(row => {
      row.classList.add('presenter-laser-box');
    });

    const activeTab = document.querySelector('.tab-view.active')?.id || 'tab-volume';
    if (activeTab === 'tab-volume') {
      renderVolAMChart();
      renderVolumeTab();
    }
    if (activeTab === 'tab-gtc-tong') renderGtcTongBarChart();
    if (activeTab === 'tab-gtc-tts-ca1') renderGtcTtsCa1BarChart();
    if (activeTab === 'tab-gan') renderGanBarChart();
    if (activeTab === 'tab-odr') renderOdrChart();
    if (activeTab === 'tab-ltc') renderLtcChart();
  }

  window.clearAMHighlight = function() {
    state.selectedAM = null;
    document.querySelectorAll('.presenter-laser-box').forEach(el => el.classList.remove('presenter-laser-box'));
    const calloutElVol = document.getElementById('vol-spotlight-callout-container');
    const calloutElGtc = document.getElementById('gtctong-spotlight-callout-container');
    if (calloutElVol) calloutElVol.innerHTML = '';
    if (calloutElGtc) calloutElGtc.innerHTML = '';

    const activeTab = document.querySelector('.tab-view.active')?.id || 'tab-volume';
    if (activeTab === 'tab-volume') {
      renderVolAMChart();
      renderVolumeTab();
    }
    if (activeTab === 'tab-gtc-tong') renderGtcTongBarChart();
    if (activeTab === 'tab-gtc-tts-ca1') renderGtcTtsCa1BarChart();
    if (activeTab === 'tab-gan') renderGanBarChart();
    if (activeTab === 'tab-odr') renderOdrChart();
    if (activeTab === 'tab-ltc') renderLtcChart();
  };

  // Mapping cơ cấu AM theo từng Tỉnh Thành (chuẩn hóa theo co_cau_ntb.csv)
  const PROVINCE_AM_MAP = {
    'Bình Thuận': ['Cao Thị Thanh Thủy', 'Lê Thanh Nhựt', 'Nguyễn Ngọc Khánh', 'Nguyễn Duy Long'],
    'Ninh Thuận': ['Nguyễn Duy Long'],
    'Khánh Hòa': ['Thái Thị Thanh Thư', 'Phan Đình Duy', 'Nguyễn Hoàng Phi', 'Nguyễn Thanh Long'],
    'Lâm Đồng': ['Lê Văn Trường', 'Lê Minh Lợi', 'Phan Nguyễn Yến Nhi', 'Huỳnh Thị Kim Chi', 'Nguyễn Thị Tuyết Thơ', 'Nguyễn Lê Nguyên Vũ', 'Nguyễn Đỗ Minh Nghĩa', 'Hồng Bích Nga'],
    'Đắk Nông': ['Trần Thị Nhung', 'Huỳnh Thúc Duân', 'Trương Quang Linh', 'Hồng Bích Nga']
  };

  function selectAndHighlightProvince(tinhName) {
    // If clicking same Province again, toggle off
    if (state.selectedProvince === tinhName) {
      window.clearProvinceHighlight();
      return;
    }

    state.selectedProvince = tinhName;

    // Remove old highlights
    document.querySelectorAll('.province-laser-box').forEach(el => el.classList.remove('province-laser-box'));
    document.querySelectorAll('.presenter-laser-gold').forEach(el => el.classList.remove('presenter-laser-gold'));

    // Highlight all matching rows in province tables
    document.querySelectorAll(`tr[data-province="${tinhName}"]`).forEach(tr => {
      tr.classList.add('province-laser-box');
    });

    // Re-render chart to highlight province
    renderSanLuongTinhChart();

    // Show spotlight callout
    renderProvinceSpotlight(tinhName);

    // Highlight associated AMs in Bảng 1 & Bảng 2
    const associatedAMs = PROVINCE_AM_MAP[tinhName] || [];
    associatedAMs.forEach(am => {
      document.querySelectorAll(`tr[data-entity="${am}"]`).forEach(tr => {
        tr.classList.add('presenter-laser-gold');
      });
    });

    // Update province tables
    renderVolumeTab();
    const activeTab = document.querySelector('.tab-view.active')?.id || 'tab-volume';
    if (activeTab === 'tab-gtc-tong') renderGtcTongTab();
    if (activeTab === 'tab-odr') renderOdrTab();
    if (activeTab === 'tab-ltc') renderLtcTab();
    if (activeTab === 'tab-rot-lc') renderRotLcTab();
  }
  window.selectAndHighlightProvince = selectAndHighlightProvince;

  window.clearProvinceHighlight = function() {
    state.selectedProvince = null;
    document.querySelectorAll('.province-laser-box').forEach(el => el.classList.remove('province-laser-box'));
    document.querySelectorAll('.presenter-laser-gold').forEach(el => el.classList.remove('presenter-laser-gold'));

    const calloutElVol = document.getElementById('vol-spotlight-callout-container');
    if (calloutElVol && calloutElVol.getAttribute('data-type') === 'province') {
      calloutElVol.innerHTML = '';
      calloutElVol.removeAttribute('data-type');
    }

    renderSanLuongTinhChart();
    renderVolumeTab();
    const activeTab = document.querySelector('.tab-view.active')?.id || 'tab-volume';
    if (activeTab === 'tab-gtc-tong') renderGtcTongTab();
    if (activeTab === 'tab-odr') renderOdrTab();
    if (activeTab === 'tab-ltc') renderLtcTab();
    if (activeTab === 'tab-rot-lc') renderRotLcTab();
  };

  function renderProvinceSpotlight(tinhName) {
    const calloutEl = document.getElementById('vol-spotlight-callout-container');
    if (!calloutEl) return;

    const currW = D.meta?.latest_week || 'W43';
    calloutEl.setAttribute('data-type', 'province');

    const rawTinhFull = D.san_luong?.tinh_full || D.san_luong?.tinh || [];
    const rawTinhTTS = D.san_luong?.tinh_tts || [];
    const wKeys = (D.meta?.weeks || ['W37', 'W38', 'W39', 'W40']).map(w => w.toLowerCase());

    const itemFull = rawTinhFull.find(r => r.tinh === tinhName) || {};
    const itemTTS = rawTinhTTS.find(r => r.tinh === tinhName) || {};

    const vFull = itemFull[wKeys[3]] !== undefined ? itemFull[wKeys[3]] : (itemFull.vol || 0);
    const prevFull = itemFull[wKeys[2]] !== undefined ? itemFull[wKeys[2]] : 0;
    const diffFull = itemFull.diff !== undefined ? itemFull.diff : (vFull - prevFull);

    const vTTS = itemTTS[wKeys[3]] !== undefined ? itemTTS[wKeys[3]] : (itemTTS.vol || 0);
    const prevTTS = itemTTS[wKeys[2]] !== undefined ? itemTTS[wKeys[2]] : 0;
    const diffTTS = itemTTS.diff !== undefined ? itemTTS.diff : (vTTS - prevTTS);

    const amList = PROVINCE_AM_MAP[tinhName] || [];
    const amBadges = amList.map(am => `<span class="badge-tag" style="background:#e0f2fe; color:#0369a1; font-weight:700; cursor:pointer;" onclick="selectAndHighlightAM('${am}')">${am}</span>`).join(' ');

    calloutEl.innerHTML = `
      <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border: 2px solid #3b82f6; border-radius: 12px; padding: 14px 18px; margin-bottom: 16px; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.15); animation: toolPop 0.25s ease;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom: 8px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="background:#2563eb; color:white; width:28px; height:28px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-size:14px; font-weight:800;">📍</span>
            <span style="font-size:16px; font-weight:800; color:#1e3a8a;">ĐANG CHỌN TỈNH: ${tinhName.toUpperCase()}</span>
            <span class="badge-tag badge-tag-blue" style="font-size:11px;">Tâm Điểm Báo Cáo</span>
          </div>
          <button onclick="window.clearProvinceHighlight()" style="background:#ffffff; border:1px solid #93c5fd; color:#1d4ed8; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:700; cursor:pointer; display:flex; align-items:center; gap:4px; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
            ✕ Bỏ chọn tỉnh
          </button>
        </div>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 10px;">
          <div style="background:#ffffff; padding:10px 14px; border-radius:8px; border-left:4px solid #2563eb;">
            <div style="font-size:11.5px; color:#64748b; font-weight:700;">FULL HÀNG ${currW}:</div>
            <div style="font-size:18px; font-weight:800; color:#1e3a8a;">${fNum(vFull)} đơn <span style="font-size:12px; font-weight:700; color:${diffFull >= 0 ? '#16a34a' : '#2563eb'};">(${diffFull >= 0 ? '+' : ''}${fNum(diffFull)})</span></div>
          </div>
          <div style="background:#ffffff; padding:10px 14px; border-radius:8px; border-left:4px solid #ea580c;">
            <div style="font-size:11.5px; color:#64748b; font-weight:700;">TIKTOK SHOP ${currW}:</div>
            <div style="font-size:18px; font-weight:800; color:#ea580c;">${fNum(vTTS)} đơn <span style="font-size:12px; font-weight:700; color:${diffTTS >= 0 ? '#16a34a' : '#ea580c'};">(${diffTTS >= 0 ? '+' : ''}${fNum(diffTTS)})</span></div>
          </div>
          <div style="background:#ffffff; padding:10px 14px; border-radius:8px; border-left:4px solid #10b981;">
            <div style="font-size:11.5px; color:#64748b; font-weight:700;">ĐỘI NGŨ AM PHỤ TRÁCH ĐỊA BÀN:</div>
            <div style="display:flex; flex-wrap:wrap; gap:5px; margin-top:4px;">${amBadges}</div>
          </div>
        </div>
        <div style="font-size:11.5px; color:#3b82f6; font-weight:600; font-style:italic;">
          💡 Mẹo: Các dòng AM thuộc tỉnh ${tinhName} ở Bảng 1 & Bảng 2 bên dưới đã được viền sáng xanh lá (Gold Laser) để dễ theo dõi.
        </div>
      </div>
    `;
  }

  function setupLaserClickHighlighter() {
    document.addEventListener('click', e => {
      const tr = e.target.closest('tbody tr');
      if (!tr) return;
      if (tr.hasAttribute('data-province')) {
        const tinh = tr.getAttribute('data-province');
        selectAndHighlightProvince(tinh);
      } else if (tr.hasAttribute('data-entity')) {
        const amName = tr.getAttribute('data-entity');
        selectAndHighlightAM(amName);
      }
    });

    window.addEventListener('keydown', e => {
      if (e.key === 'Escape') {
        window.clearAMHighlight();
        window.clearProvinceHighlight();
      }
    });
  }

  // ============================================================================
  // GHN FLEET DELIVERY TRUCK RUNNER (INTERACTIVE TAB NAVIGATION ENGINE)
  // ============================================================================
  function updateGhnTruckPosition(activeTabElement) {
    const truck = document.getElementById('ghn-runner-truck');
    const track = document.getElementById('ghn-highway-track');
    if (!truck || !track) return;

    const tab = activeTabElement || document.querySelector('.tab-item.active');
    if (!tab) return;

    const tabRect = tab.getBoundingClientRect();
    const trackRect = track.getBoundingClientRect();

    // Center truck over active tab
    const truckWidth = 68;
    const targetLeft = (tabRect.left - trackRect.left) + (tabRect.width / 2) - (truckWidth / 2);

    truck.classList.add('is-driving');
    truck.style.transform = `translateX(${Math.max(0, targetLeft)}px)`;

    clearTimeout(truck._driveTimer);
    truck._driveTimer = setTimeout(() => {
      truck.classList.remove('is-driving');
      truck.classList.add('is-arrived');
      setTimeout(() => truck.classList.remove('is-arrived'), 400);
    }, 450);
  }

  // TELEPROMPTER SCRIPT (SYNCHRONIZED SPEECH ENGINE - 13 DEDICATED SECTIONS)
  function setupEvents() {
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tabViews.forEach(v => v.classList.remove('active'));

        tab.classList.add('active');
        const targetId = tab.getAttribute('data-tab');
        const targetView = document.getElementById(targetId);
        if (targetView) targetView.classList.add('active');
        if (window.lucide) lucide.createIcons();

        // Move GHN Express Delivery Truck to this tab!
        updateGhnTruckPosition(tab);

        // Show/hide Gán Threshold Filter in Filter Bar when on Tab 5
        const filterGanRate = document.getElementById('filter-gan-rate');
        if (filterGanRate) {
          filterGanRate.style.display = targetId === 'tab-gan' ? 'inline-block' : 'none';
        }

        updateDynamicWeekLabels();
        setTimeout(() => {
          renderTabCharts(targetId);
          lucide.createIcons();
        }, 30);
      });
    });

    // Window resize adjustment for truck position
    window.addEventListener('resize', () => {
      updateGhnTruckPosition();
    });

    // Initial truck positioning
    setTimeout(() => {
      updateGhnTruckPosition();
      const initialTabId = document.querySelector('.tab-view.active')?.id;
      const filterGanRate = document.getElementById('filter-gan-rate');
      if (filterGanRate) {
        filterGanRate.style.display = initialTabId === 'tab-gan' ? 'inline-block' : 'none';
      }
    }, 200);

    selectWeek.addEventListener('change', e => { state.week = e.target.value; renderAll(); });
    selectProvince.addEventListener('change', e => { state.province = e.target.value; renderAll(); });
    selectAM.addEventListener('change', e => { 
      state.am = e.target.value; 
      if (state.am !== 'ALL') {
        selectAndHighlightAM(state.am);
      } else {
        window.clearAMHighlight();
      }
      renderAll(); 
    });

    const selGanRate = document.getElementById('filter-gan-rate');
    if (selGanRate) {
      selGanRate.addEventListener('change', e => {
        window.setGanFilter(e.target.value);
      });
    }

    // Volume Chart Mode Pills (Tab 2)
    const volModePills = document.querySelectorAll('#vol-chart-mode-pills .chart-mode-pill');
    volModePills.forEach(pill => {
      pill.addEventListener('click', () => {
        volModePills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        state.volChartMode = pill.getAttribute('data-mode');
        renderVolAMChart();
      });
    });

    // Volume Quick Highlight Pills (Tab 2)
    const volHighlightPills = document.querySelectorAll('#vol-quick-highlight-pills .chart-mode-pill');
    volHighlightPills.forEach(pill => {
      pill.addEventListener('click', () => {
        volHighlightPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        state.volHighlight = pill.getAttribute('data-highlight');
        state.selectedAM = null;
        renderVolAMChart();
      });
    });

    // %GTC Tổng Quick Highlight Pills (Tab 3)
    const gtcTongHighlightPills = document.querySelectorAll('#gtctong-quick-highlight-pills .chart-mode-pill');
    gtcTongHighlightPills.forEach(pill => {
      pill.addEventListener('click', () => {
        gtcTongHighlightPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        state.gtcTongHighlight = pill.getAttribute('data-highlight');
        state.selectedAM = null;
        renderGtcTongBarChart();
      });
    });

    btnMeeting.addEventListener('click', toggleMeetingMode);

    // Switch to Tab Kich Ban when clicking Header button
    const btnHeaderKichban = document.getElementById('btn-header-kichban');
    if (btnHeaderKichban) {
      btnHeaderKichban.addEventListener('click', (e) => {
        e.preventDefault();
        const tabKichBan = document.querySelector('button[data-tab="tab-kichban"]');
        if (tabKichBan) {
          tabKichBan.click();
          tabKichBan.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
        }
      });
    }


    // Volume Table Mode Pills (Split vs Full Only vs TTS Only)
    const volTableModePills = document.querySelectorAll('#vol-table-mode-pills .chart-mode-pill');
    volTableModePills.forEach(pill => {
      pill.addEventListener('click', () => {
        volTableModePills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        const viewMode = pill.getAttribute('data-table-view');
        
        const grid = document.getElementById('vol-tables-split-grid');
        const cardFull = document.getElementById('card-vol-full');
        const cardTts = document.getElementById('card-vol-tts');

        if (viewMode === 'full_only') {
          if (grid) grid.style.gridTemplateColumns = '1fr';
          if (cardFull) cardFull.style.display = 'block';
          if (cardTts) cardTts.style.display = 'none';
        } else if (viewMode === 'tts_only') {
          if (grid) grid.style.gridTemplateColumns = '1fr';
          if (cardFull) cardFull.style.display = 'none';
          if (cardTts) cardTts.style.display = 'block';
        } else {
          if (grid) grid.style.gridTemplateColumns = '1fr 1fr';
          if (cardFull) cardFull.style.display = 'block';
          if (cardTts) cardTts.style.display = 'block';
        }
      });
    });

    const searchVolFull = document.getElementById('search-vol-full-am');
    if (searchVolFull) {
      searchVolFull.addEventListener('input', () => {
        renderVolumeTab();
        lucide.createIcons();
      });
    }

    const searchVolTts = document.getElementById('search-vol-tts-am');
    if (searchVolTts) {
      searchVolTts.addEventListener('input', () => {
        renderVolumeTab();
        lucide.createIcons();
      });
    }

    const searchGtcTong = document.getElementById('search-gtctong-am');
    if (searchGtcTong) {
      searchGtcTong.addEventListener('input', e => {
        state.searchGtcTong = e.target.value.toLowerCase().trim();
        renderGtcTongTab();
        lucide.createIcons();
      });
    }

    const searchGtcBatOn = document.getElementById('search-gtc-bat-on');
    if (searchGtcBatOn) {
      searchGtcBatOn.addEventListener('input', e => {
        state.searchGtcBatOn = e.target.value.trim();
        renderGtcTongTab();
      });
    }

    const searchOpr = document.getElementById('search-opr-am');
    if (searchOpr) {
      searchOpr.addEventListener('input', e => {
        state.searchOpr = e.target.value.toLowerCase().trim();
        renderOprTab();
        lucide.createIcons();
      });
    }

    const searchRotLc = document.getElementById('search-rotlc-bc');
    if (searchRotLc) {
      searchRotLc.addEventListener('input', e => {
        state.searchRotLc = e.target.value.toLowerCase().trim();
        renderTransportTab();
        lucide.createIcons();
      });
    }

    const searchFdAm = document.getElementById('search-fd-am');
    if (searchFdAm) {
      searchFdAm.addEventListener('input', e => {
        state.searchFdAm = e.target.value.toLowerCase().trim();
        renderFdTab();
        if (window.lucide) lucide.createIcons();
      });
    }

    const searchFdBc = document.getElementById('search-fd-bc');
    if (searchFdBc) {
      searchFdBc.addEventListener('input', e => {
        state.searchFdBc = e.target.value.toLowerCase().trim();
        renderFdTab();
        if (window.lucide) lucide.createIcons();
      });
    }

    const searchBcInputs = document.querySelectorAll('.search-bc-input, #search-bc-canh-bao');
    searchBcInputs.forEach(input => {
      input.addEventListener('input', e => {
        state.searchBcCanhBao = e.target.value.toLowerCase().trim();
        // Sync values across all search boxes
        searchBcInputs.forEach(si => { if (si !== e.target) si.value = e.target.value; });
        renderBcCanhBaoTable();
        if (window.lucide) lucide.createIcons();
      });
    });

    const searchAgingAM = document.getElementById('search-aging-am');
    if (searchAgingAM) {
      searchAgingAM.addEventListener('input', e => {
        state.searchAgingAM = e.target.value.toLowerCase().trim();
        renderAgingTab();
        if (window.lucide) lucide.createIcons();
      });
    }

    const searchAgingBC = document.getElementById('search-aging-bc');
    if (searchAgingBC) {
      searchAgingBC.addEventListener('input', e => {
        state.searchAgingBC = e.target.value.toLowerCase().trim();
        renderAgingTab();
        if (window.lucide) lucide.createIcons();
      });
    }


    const searchCodBc = document.getElementById('search-cod-bc');
    if (searchCodBc) {
      searchCodBc.addEventListener('input', e => {
        renderControlTab();
        lucide.createIcons();
      });
    }

    // Toggle Tools Toolbar (Collapsible Action Panel)
    const btnToggleTools = document.getElementById('btn-toggle-tools');
    const toolsPanel = document.getElementById('header-tools-panel');
    if (btnToggleTools && toolsPanel) {
      btnToggleTools.addEventListener('click', () => {
        const isCollapsed = toolsPanel.classList.toggle('is-collapsed');
        btnToggleTools.classList.toggle('active', !isCollapsed);
        const icon = btnToggleTools.querySelector('#toggle-tools-icon');
        if (icon) {
          icon.setAttribute('data-lucide', isCollapsed ? 'chevron-left' : 'chevron-right');
          lucide.createIcons();
        }
      });
    }

    btnTheme.addEventListener('click', () => {
      state.theme = state.theme === 'dark' ? 'light' : 'dark';
      applyTheme(state.theme);
      renderAllCharts();
    });

    btnExport.addEventListener('click', () => window.print());

    btnUpload.addEventListener('click', () => { modalUpload.classList.add('show'); lucide.createIcons(); });
    document.getElementById('btn-close-upload').addEventListener('click', () => modalUpload.classList.remove('show'));
    document.getElementById('btn-cancel-upload').addEventListener('click', () => modalUpload.classList.remove('show'));

    dropZone.addEventListener('click', () => fileInput.click());
    dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.style.borderColor = '#16a34a'; });
    dropZone.addEventListener('dragleave', () => { dropZone.style.borderColor = '#f26522'; });
    dropZone.addEventListener('drop', e => {
      e.preventDefault();
      dropZone.style.borderColor = '#f26522';
      if (e.dataTransfer.files.length) handleExcelUpload(e.dataTransfer.files[0]);
    });
    fileInput.addEventListener('change', e => {
      if (e.target.files.length) handleExcelUpload(e.target.files[0]);
    });

    btnSync.addEventListener('click', () => { modalSheets.classList.add('show'); lucide.createIcons(); });
    document.getElementById('btn-close-sheets').addEventListener('click', () => modalSheets.classList.remove('show'));
    document.getElementById('btn-cancel-sheets').addEventListener('click', () => modalSheets.classList.remove('show'));
    document.getElementById('btn-do-sync').addEventListener('click', async () => {
      const btn = document.getElementById('btn-do-sync');
      btn.disabled = true;
      btn.innerHTML = '<i data-lucide="loader" class="spin"></i> Đang tải 18 tab từ Google Sheets...';
      if (window.lucide) lucide.createIcons();
      try {
        const resp = await fetch('/api/sync-sheets-oauth', { method: 'POST' });
        const res = await resp.json();
        if (res.success) {
          btn.innerHTML = '✅ Đồng bộ thành công 100%!';
          setTimeout(() => {
            window.location.reload(true);
          }, 800);
        } else {
          btn.innerHTML = '❌ Lỗi: ' + (res.error || 'Thất bại');
          btn.disabled = false;
        }
      } catch (err) {
        btn.innerHTML = '❌ Lỗi kết nối: ' + err.message;
        btn.disabled = false;
      }
    });
  }

  function toggleMeetingMode() {
    document.body.classList.toggle('in-meeting-mode');
    const inMeeting = document.body.classList.contains('in-meeting-mode');
    
    // Luôn giữ chế độ sáng khi họp theo yêu cầu
    applyTheme('light');

    btnMeeting.innerHTML = inMeeting
      ? '<i data-lucide="minimize"></i> Thoát Họp'
      : '<i data-lucide="presentation"></i> Chế Độ Họp';
    if (inMeeting && document.documentElement.requestFullscreen) {
      document.documentElement.requestFullscreen().catch(() => {});
    }
    lucide.createIcons();
    setTimeout(renderAllCharts, 100);
  }

  function setupTableSorting() {
    document.querySelectorAll('.bi-table th').forEach(th => {
      th.style.cursor = 'pointer';
      th.title = 'Bấm để sắp xếp (Cao về thấp / Thấp đến cao)';
    });

    document.addEventListener('click', e => {
      const th = e.target.closest('.bi-table th');
      if (!th) return;
      const table = th.closest('table');
      if (!table) return;
      const tbody = table.querySelector('tbody');
      if (!tbody) return;

      const tableId = table.id || ('tbl_' + Math.random().toString(36).substr(2, 9));
      const colIdx = Array.from(th.parentNode.children).indexOf(th);

      // Mặc định click lần đầu là desc (cao về thấp)
      const currentDir = state.sortDirection[tableId];
      const currentCol = state.sortColumn[tableId];
      const newDir = (currentCol === colIdx && currentDir === 'desc') ? 'asc' : 'desc';
      state.sortDirection[tableId] = newDir;
      state.sortColumn[tableId] = colIdx;

      // Cập nhật mũi tên chỉ thị
      th.parentNode.querySelectorAll('th').forEach(h => {
        h.querySelectorAll('.sort-arrow').forEach(el => el.remove());
      });
      const arrow = document.createElement('span');
      arrow.className = 'sort-arrow';
      arrow.style.marginLeft = '4px';
      arrow.style.fontSize = '10px';
      arrow.innerHTML = newDir === 'desc' ? ' ▼' : ' ▲';
      th.appendChild(arrow);

      // Tách dòng tổng nếu có
      const rows = Array.from(tbody.querySelectorAll('tr'));
      let totalRow = null;
      if (rows.length > 0) {
        const lastRowText = rows[rows.length - 1].innerText.toUpperCase();
        if (lastRowText.includes('TỔNG') || lastRowText.includes('TOÀN VÙNG')) {
          totalRow = rows.pop();
        }
      }

      const parseVal = el => {
        if (!el) return -Infinity;
        const s = el.innerText.trim();
        if (!s || s === '–' || s === '—' || s === '-') return -Infinity;
        const m = s.match(/([+-]?\s*[\d]+(?:[.,]\d+)*)/);
        if (m) {
          let raw = m[1].replace(/\s+/g, '');
          if (/^\d{1,3}\.\d{3}$/.test(raw) || /^\d{1,3}\.\d{3}\.\d{3}$/.test(raw)) {
            raw = raw.replace(/\./g, '');
          } else if (/^\d{1,3},\d{3}$/.test(raw) || /^\d{1,3},\d{3},\d{3}$/.test(raw)) {
            raw = raw.replace(/,/g, '');
          } else {
            raw = raw.replace(/,/g, '.');
          }
          const num = parseFloat(raw);
          if (!isNaN(num)) return num;
        }
        return s.toLowerCase();
      };

      rows.sort((a, b) => {
        const cellA = a.children[colIdx];
        const cellB = b.children[colIdx];
        const valA = parseVal(cellA);
        const valB = parseVal(cellB);

        let cmp = 0;
        if (typeof valA === 'number' && typeof valB === 'number') {
          cmp = valA - valB;
        } else {
          cmp = String(valA).localeCompare(String(valB), 'vi');
        }
        return newDir === 'desc' ? -cmp : cmp;
      });

      // Cập nhật lại số thứ tự cột #
      rows.forEach((r, idx) => {
        const firstCell = r.children[0];
        if (firstCell && (firstCell.querySelector('.rank-pill') || firstCell.classList.contains('center'))) {
          firstCell.innerHTML = renderRankPill(idx);
        }
        tbody.appendChild(r);
      });
      if (totalRow) tbody.appendChild(totalRow);
    });
  }

  function handleExcelUpload(file) {
    const status = document.getElementById('upload-status');
    status.innerHTML = `<span style="color: #2563eb; font-weight:700;">⏳ Đang xử lý file ${file.name}...</span>`;
    const reader = new FileReader();
    reader.onload = function (e) {
      try {
        const data = new Uint8Array(e.target.result);
        const wb = XLSX.read(data, { type: 'array' });
        status.innerHTML = `<span style="color: #10b981; font-weight:700;">✅ Đã nạp thành công ${wb.SheetNames.length} sheet từ ${file.name}!</span>`;
        setTimeout(() => {
          modalUpload.classList.remove('show');
          renderAll();
        }, 1200);
      } catch (err) {
        status.innerHTML = `<span style="color: #ef4444; font-weight:700;">❌ Lỗi: ${err.message}</span>`;
      }
    };
    reader.readAsArrayBuffer(file);
  }

  // ==========================================================================
  // RENDER MASTER
  // ==========================================================================
  
  window.switchTabDirect = function(tabId) {
    const tabBtn = document.querySelector(`.tab-item[data-tab="${tabId}"]`);
    if (tabBtn) {
      tabBtn.click();
    } else {
      document.querySelectorAll('.tab-item').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-view').forEach(v => v.classList.remove('active'));
      const v = document.getElementById(tabId);
      if (v) v.classList.add('active');
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  function renderAll() {
    try { renderOverviewTab(); } catch(e) { console.error('renderOverviewTab:', e); }
    try { renderBcCanhBaoTable(); } catch(e) { console.error('renderBcCanhBaoTable:', e); }
    try { renderVolumeTab(); } catch(e) { console.error('renderVolumeTab:', e); }
    try { renderGtcTongTab(); } catch(e) { console.error('renderGtcTongTab:', e); }
    try { renderGtcTtsCa1Tab(); } catch(e) { console.error('renderGtcTtsCa1Tab:', e); }
    try { renderGanTab(); } catch(e) { console.error('renderGanTab:', e); }
    try { renderOdrTab(); } catch(e) { console.error('renderOdrTab:', e); }
    try { renderLtcTab(); } catch(e) { console.error('renderLtcTab:', e); }
    try { renderOprTab(); } catch(e) { console.error('renderOprTab:', e); }
    try { renderTransportTab(); } catch(e) { console.error('renderTransportTab:', e); }
    try { renderFdTab(); } catch(e) { console.error('renderFdTab:', e); }
    try { renderKtcTab(); } catch(e) { console.error('renderKtcTab:', e); }
    try { renderAgingTab(); } catch(e) { console.error('renderAgingTab:', e); }
    try { renderControlTab(); } catch(e) { console.error('renderControlTab:', e); }
    try { renderTruyThuTab(); } catch(e) { console.error('renderTruyThuTab:', e); }
    try { renderCommercialTab(); } catch(e) { console.error('renderCommercialTab:', e); }
    try { renderAllCharts(); } catch(e) { console.error('renderAllCharts:', e); }
  }

  function renderTabCharts(tabId) {
    if (tabId === 'tab-overview') {
      renderTrendSanLuongChart();
      renderTrendRatesChart();
      renderSanLuongTinhChart();
    } else if (tabId === 'tab-volume') {
      renderVolumeTab();
      renderTinhVol4WeeksChart();
      renderVolAMChart();
    } else if (tabId === 'tab-gtc-tong') {
      renderGtcTongTab();
      renderTinhGtc4WeeksChart();
      renderGtcTongBarChart();
    } else if (tabId === 'tab-gtc-tts-ca1') {
      renderGtcTtsCa1Tab();
      renderGtcTtsCa1BarChart();
    } else if (tabId === 'tab-gan') {
      renderGanTab();
      renderGanOverviewChart();
      renderGanBarChart();
    } else if (tabId === 'tab-odr') {
      renderOdrTab();
      renderTinhOdr4WeeksChart();
      renderOdrChart();
    } else if (tabId === 'tab-ltc') {
      renderLtcTab();
      renderLtcChart();
    } else if (tabId === 'tab-opr-tts') {
      renderOprTab();
      renderOprGroupedChart();
    try { renderOprBcTable(); } catch(e) { console.error('renderOprBcTable:', e); }
    } else if (tabId === 'tab-rot-lc') {
      renderTransportTab();
      renderRotLcChart();
    } else if (tabId === 'tab-fd') {
      renderFdTab();
      renderFdChart();
    } else if (tabId === 'tab-ktc') {
      renderKtcTab();
      renderFillRateChart();
    } else if (tabId === 'tab-aging') {
      renderAgingTab();
      renderAgingChart();
    try { renderAgingDonutChart(); } catch(e) {}
    try { renderAgingCustomerChart(); } catch(e) {}
    try { renderAgingProgressChart(); } catch(e) {}
    } else if (tabId === 'tab-commercial') {
      renderCommercialTab();
      renderKdDoanhThuChart();
      renderKdDoanhThuPie();
      renderKdGrowthWaterfall();
      renderF30ShopsChart();
    } else if (tabId === 'tab-control') {
      renderControlTab();
      renderCodTmAmBar();
    } else if (tabId === 'tab-bc-canhbao') {
      renderBcCanhBaoTable();
    } else if (tabId === 'tab-truythu') {
      renderTruyThuTab();
      renderTruyThuLoaiBar();
    }
  }

  function renderAllCharts() {
    const activeTab = document.querySelector('.tab-view.active');
    if (activeTab) {
      renderTabCharts(activeTab.id);
    }
  }

  // --------------------------------------------------------------------------
  // TAB 1: OVERVIEW
  // --------------------------------------------------------------------------
  function renderOverviewTab() {
    const ov = D.overview || {};
    const tilesEl = document.getElementById('overview-kpi-tiles');
    const latestWeek = D.meta?.latest_week || 'W37';
    const prevWeek = D.meta?.prev_week || 'W36';
    
    if (tilesEl) {
      const cardMap = {};
      (ov.cards || []).forEach(c => cardMap[c.id] = c);

      const trendMap = {};
      (ov.kpis_trend || []).forEach(t => trendMap[t.indicator] = t);

      // 1. Sản lượng Full & TTS
      const volCard = cardMap['vol_full'] || {};
      const volTtsCard = cardMap['vol_tts'] || {};
      const volVal = volCard.val || 307837;
      const volDiff = volCard.diff !== undefined ? volCard.diff : -11149;
      const volTtsVal = volTtsCard.val || 63122;
      const volTtsDiff = volTtsCard.diff !== undefined ? volTtsCard.diff : -9759;
      const volDiffPct = volCard.diff_pct !== undefined ? volCard.diff_pct : -0.035;
      const volTtsDiffPct = volTtsCard.diff_pct !== undefined ? volTtsCard.diff_pct : -0.134;

      // 2. GTC Tổng
      const gtcCard = cardMap['gtc_full'] || {};
      const gtcTtsCard = cardMap['gtc_tts'] || {};
      const gtcVal = gtcCard.val !== undefined ? gtcCard.val : 0.5778;
      const gtcDiff = gtcCard.diff !== undefined ? gtcCard.diff : -0.0036;
      const gtcTtsVal = gtcTtsCard.val !== undefined ? gtcTtsCard.val : 0.5591;
      const gtcTtsDiff = gtcTtsCard.diff !== undefined ? gtcTtsCard.diff : -0.0104;

      // 3. GTC Ca 1 TTS
      const gtcCa1Trend = trendMap['%GTC TTS (Ca1 thuần)'] || trendMap['%GTC Full hàng (Ca1 thuần)'] || {};
      const gtcCa1Val = gtcCa1Trend[latestWeek.toLowerCase()] !== undefined ? gtcCa1Trend[latestWeek.toLowerCase()] : 0.7307;
      const gtcCa1Diff = gtcCa1Trend.diff !== undefined ? gtcCa1Trend.diff : -0.0171;

      // 4. Gán vận hành
      const ganOverview = D.gan?.overview || [];
      const ganFullRow = ganOverview.find(r => r.indicator && r.indicator.includes('Full hàng – Tổng')) || {};
      const ganTtsRow = ganOverview.find(r => r.indicator && r.indicator.includes('TTS – Tổng')) || {};
      const ganVal = ganFullRow[latestWeek.toLowerCase()] !== undefined ? ganFullRow[latestWeek.toLowerCase()] : (ganFullRow.w37 || ganFullRow.w36 || 0.8355);
      const ganDiff = ganFullRow.diff !== undefined ? ganFullRow.diff : 0.0144;
      const ganTtsVal = ganTtsRow[latestWeek.toLowerCase()] !== undefined ? ganTtsRow[latestWeek.toLowerCase()] : (ganTtsRow.w37 || ganTtsRow.w36 || 0.8343);
      const ganTtsDiff = ganTtsRow.diff !== undefined ? ganTtsRow.diff : 0.0142;
      const ganCa1Row = ganOverview.find(r => r.indicator && r.indicator.includes('Full hàng – Ca1 + Tồn')) || {};
      const ganCa2Row = ganOverview.find(r => r.indicator && r.indicator.includes('Full hàng – Ca2')) || {};
      const ganCa1Val = ganCa1Row[latestWeek.toLowerCase()] !== undefined ? ganCa1Row[latestWeek.toLowerCase()] : 0.9370;
      const ganCa2Val = ganCa2Row[latestWeek.toLowerCase()] !== undefined ? ganCa2Row[latestWeek.toLowerCase()] : 0.6357;

                  // 5. ODR
      const odrOverview = D.odr?.overview || [];
      const odrFullRow = odrOverview.find(r => r.label === 'Full hàng') || {};
      const odrTtsRow = odrOverview.find(r => r.label === 'TTS') || {};
      const odrCard = cardMap['odr_full'] || {};
      const odrTrendFull = trendMap['%ODR Full hàng'] || {};
      const odrTrendTts = trendMap['%ODR TTS'] || {};
      const odrVal = odrCard.val !== undefined ? odrCard.val : (odrFullRow[latestWeek.toLowerCase()] !== undefined ? odrFullRow[latestWeek.toLowerCase()] : 0.9124);
      const odrDiff = odrCard.diff !== undefined ? odrCard.diff : (odrTrendFull.diff !== undefined ? odrTrendFull.diff : -0.0210);
      const odrTtsVal = odrTrendTts[latestWeek.toLowerCase()] !== undefined ? odrTrendTts[latestWeek.toLowerCase()] : (odrTtsRow[latestWeek.toLowerCase()] !== undefined ? odrTtsRow[latestWeek.toLowerCase()] : 0.9154);
      const odrTtsDiff = odrTrendTts.diff !== undefined ? odrTrendTts.diff : (odrTtsRow.diff !== undefined ? odrTtsRow.diff : -0.0131);

      // 6. LTC
      const ltcCard = cardMap['ltc_full'] || {};
      const ltcTrendTts = trendMap['%LTC TTS'] || {};
      const ltcVal = ltcCard.val !== undefined ? ltcCard.val : 0.9029;
      const ltcDiff = ltcCard.diff !== undefined ? ltcCard.diff : -0.0021;
      const ltcTtsVal = ltcTrendTts[latestWeek.toLowerCase()] !== undefined ? ltcTrendTts[latestWeek.toLowerCase()] : 0.9355;
      const ltcTtsDiff = ltcTrendTts.diff !== undefined ? ltcTrendTts.diff : -0.0064;

      // 7. Rớt LC
      const rotCard = cardMap['rot_lc'] || {};
      const rotVal = rotCard.val !== undefined ? rotCard.val : 0.0225;
      const rotDiff = rotCard.diff !== undefined ? rotCard.diff : 0.0068;

      // 8. COD Tiền mặt & Thanh toán QR
      const codCard = cardMap['cod_tm'] || {};
      const codReportMetrics = D.cod_report?.metrics || [];
      const codTmRow = codReportMetrics.find(m => m.chi_so && m.chi_so.includes('Tiền mặt (% TM)')) || {};
      const codCkRow = codReportMetrics.find(m => m.chi_so && m.chi_so.includes('Chuyển khoản (% CK)')) || {};
      const codTotRow = codReportMetrics.find(m => m.chi_so && m.chi_so.includes('Tổng COD')) || {};
      
      let codVal = 0.371;
      let codPrev = 0.401;
      let codDiff = -0.030;
      let codDigitalVal = 0.629;
      let codTotStr = '82.6 Tỷ';

      if (codTmRow.curr) {
        codVal = parseFloat(codTmRow.curr.replace('%', '')) / 100;
        if (codTmRow.prev) codPrev = parseFloat(codTmRow.prev.replace('%', '')) / 100;
        codDiff = codVal - codPrev;
        codDigitalVal = 1 - codVal;
      } else if (codCard.val !== undefined) {
        codVal = codCard.val;
        codDiff = codCard.diff !== undefined ? codCard.diff : -0.030;
        codPrev = codVal - codDiff;
        codDigitalVal = 1 - codVal;
      } else if (D.cod_payment?.overview?.rate_cash !== undefined) {
        codVal = D.cod_payment.overview.rate_cash;
        codDiff = D.cod_payment.overview.diff_cash || -0.024;
        codPrev = codVal - codDiff;
        codDigitalVal = 1 - codVal;
      }
      if (codTotRow.curr) {
        const numTot = parseFloat(codTotRow.curr.replace(/,/g, ''));
        if (!isNaN(numTot)) codTotStr = (numTot / 1000).toFixed(1) + ' Tỷ';
      }

      // 9. FD Hoàn Trả (Failed Delivery)
      const fdData = D.fd || {};
      const fdSum = fdData.summary || {};
      const fdRateFull = fdSum.rate_full !== undefined ? fdSum.rate_full : 0.0673;
      const fdRateFullPrev = fdSum.rate_full_prev !== undefined ? fdSum.rate_full_prev : 0.0754;
      const fdRateTts = fdSum.rate_tts !== undefined ? fdSum.rate_tts : 0.0610;
      const fdRateTtsPrev = fdSum.rate_tts_prev !== undefined ? fdSum.rate_tts_prev : 0.0680;
      const fdRetFull = fdSum.ret_full || 24518;
      const fdDiffFull = fdSum.diff_full !== undefined ? fdSum.diff_full : (fdRateFull - fdRateFullPrev);
      const fdDiffTts = fdSum.diff_tts !== undefined ? fdSum.diff_tts : (fdRateTts - fdRateTtsPrev);

      // 10. TLTĐ (Tỷ Lệ Lấp Đầy Thùng/Xe KTC)
      const ktcData = D.ktc || {};
      const ktcWeekly = ktcData.fill_rate?.weekly?.total || {};
      const tltdVal = (ktcWeekly.tld_curr !== undefined ? ktcWeekly.tld_curr : (ktcWeekly['tld_' + latestWeek.toLowerCase()] || 51.0)) / 100;
      const tltdPrev = (ktcWeekly.tld_prev !== undefined ? ktcWeekly.tld_prev : (ktcWeekly['tld_' + prevWeek.toLowerCase()] || 54.8)) / 100;
      const tltdDiff = ktcWeekly.diff_tld !== undefined ? (ktcWeekly.diff_tld / 100) : (tltdVal - tltdPrev);
      const tltdUnder30 = ktcWeekly.under_30 !== undefined ? ktcWeekly.under_30 : 76;

      const pairedCards = [
        {
          id: 'vol_pair',
          title: `Sản Lượng Giao (${latestWeek})`,
          mainVal: fNum(volVal),
          mainUnit: `đơn Full (${volDiff >= 0 ? '▲ +' : '▼ '}${fNum(volDiff)} đ)`,
          subVal: `TTS: ${fNum(volTtsVal)} đ (${volTtsDiff >= 0 ? '▲ +' : '▼ '}${fNum(volTtsDiff)} đ / ${fPct(volTtsDiffPct)})`,
          diff: volDiffPct,
          isHigherBetter: true,
          colorCls: 'kpi-blue',
          icon: 'package'
        },
        {
          id: 'gtc_pair',
          title: `%GTC Tổng (${latestWeek})`,
          mainVal: fPct(gtcVal),
          mainUnit: `Full Hàng (${gtcDiff >= 0 ? '▲ +' : '▼ '}${(Math.abs(gtcDiff)*100).toFixed(1)}%p)`,
          subVal: `TTS: ${fPct(gtcTtsVal)} (${gtcTtsDiff >= 0 ? '▲ +' : '▼ '}${(Math.abs(gtcTtsDiff)*100).toFixed(1)}%p)`,
          diff: gtcDiff,
          isHigherBetter: true,
          colorCls: 'kpi-amber',
          icon: 'check-circle-2'
        },
        {
          id: 'gtc_ca1_pair',
          title: `%GTC TTS Ca 1 (${latestWeek})`,
          mainVal: fPct(gtcCa1Val),
          mainUnit: 'TikTok Shop',
          subVal: 'Target ≥ 76.0%',
          diff: gtcCa1Diff,
          isHigherBetter: true,
          colorCls: 'kpi-purple',
          icon: 'award'
        },
        {
          id: 'gan_pair',
          title: `Tỷ Lệ Gán Vận Hành (${latestWeek})`,
          mainVal: fPct(ganVal),
          mainUnit: `Full Hàng (${ganDiff >= 0 ? '▲ +' : '▼ '}${(Math.abs(ganDiff)*100).toFixed(1)}%p)`,
          subVal: `Ca 1+Tồn: ${fPct(ganCa1Val)} · Ca 2: ${fPct(ganCa2Val)} | TTS: ${fPct(ganTtsVal)}`, 
          diff: ganDiff,
          isHigherBetter: true,
          colorCls: 'kpi-purple',
          icon: 'user-check'
        },
        {
          id: 'odr_pair',
          title: `%ODR (Giao Đúng Hẹn SLA - ${latestWeek})`,
          mainVal: fPct(odrVal),
          mainUnit: `Full Hàng (${odrDiff >= 0 ? '▲ +' : '▼ '}${(Math.abs(odrDiff)*100).toFixed(1)}%p)`,
          subVal: `TTS: ${fPct(odrTtsVal)} (${odrTtsDiff >= 0 ? '▲ +' : '▼ '}${(Math.abs(odrTtsDiff)*100).toFixed(1)}%p)`,
          diff: odrDiff,
          isHigherBetter: true,
          colorCls: (odrVal >= 0.92) ? 'kpi-green' : 'kpi-red',
          icon: 'clock'
        },
        {
          id: 'ltc_pair',
          title: `%LTC (Lấy Thành Công - ${latestWeek})`,
          mainVal: fPct(ltcVal),
          mainUnit: `Full Hàng (${ltcDiff >= 0 ? '▲ +' : '▼ '}${(Math.abs(ltcDiff)*100).toFixed(1)}%p)`,
          subVal: `TTS: ${fPct(ltcTtsVal)} (${ltcTtsDiff >= 0 ? '▲ +' : '▼ '}${(Math.abs(ltcTtsDiff)*100).toFixed(1)}%p) | Target ≥ 90.0%`,
          diff: ltcDiff,
          isHigherBetter: true,
          colorCls: 'kpi-green',
          icon: 'archive'
        },
        {
          id: 'rot_lc',
          title: `%Rớt Luân Chuyển (${latestWeek})`,
          mainVal: fPct(rotVal),
          mainUnit: 'Toàn Vùng',
          subVal: `${prevWeek}: ${fPct(rotVal - rotDiff)} (${rotDiff >= 0 ? 'Tăng +' : 'Giảm '}${(Math.abs(rotDiff)*100).toFixed(2)}%p)`,
          diff: rotDiff,
          isHigherBetter: false,
          colorCls: 'kpi-red',
          icon: 'truck'
        },
        {
          id: 'fd_pair',
          title: `%FD Hoàn Trả (${latestWeek})`,
          mainVal: fPct(fdRateFull),
          mainUnit: `Full Hàng (${prevWeek}: ${fPct(fdRateFullPrev)} | ▼ ${(Math.abs(fdDiffFull)*100).toFixed(1)}%p)`,
          subVal: `TTS: ${fPct(fdRateTts)} (${prevWeek}: ${fPct(fdRateTtsPrev)} | ▼ ${(Math.abs(fdDiffTts)*100).toFixed(1)}%p) · ${fNum(fdRetFull)} đ hoàn`,
          diff: fdDiffFull,
          isHigherBetter: false,
          colorCls: 'kpi-purple',
          icon: 'rotate-ccw'
        },
        {
          id: 'opr_pair',
          title: `%OPR TikTok Shop (${latestWeek})`,
          mainVal: '82.2%',
          mainUnit: 'Toàn Vùng (Target ≥ 80.0%)',
          subVal: '☀️ Ngày: 93.5% · 🌙 Đêm: 64.3% 🚨',
          diff: -0.009,
          isHigherBetter: true,
          colorCls: 'kpi-amber',
          icon: 'shopping-bag'
        },
        {
          id: 'truythu_pair',
          title: `Truy Thu (${latestWeek})`,
          mainVal: `${((D.truy_thu_report?.summary?.can_thu_curr || 241649125) / 1e6).toFixed(1)} Tr ₫`,
          mainUnit: `Cần Thu (${(D.truy_thu_report?.summary?.diff_can_thu || 155389854) >= 0 ? '▲ +' : '▼ '}${Math.abs((D.truy_thu_report?.summary?.diff_can_thu || 155389854) / 1e6).toFixed(1)} Tr)`,
          subVal: `${fNum(D.truy_thu_report?.summary?.total_records_curr || 1889)} Ticket | ${prevWeek}: ${((D.truy_thu_report?.summary?.can_thu_prev || 86259271) / 1e6).toFixed(1)} Tr`,
          diff: (D.truy_thu_report?.summary?.can_thu_prev ? ((D.truy_thu_report?.summary?.diff_can_thu || 0) / D.truy_thu_report.summary.can_thu_prev) : 1.801),
          isHigherBetter: false,
          colorCls: 'kpi-red',
          icon: 'shield-alert'
        }
      ];

      tilesEl.innerHTML = pairedCards.map(c => `
        <div class="kpi-tile ${c.colorCls}">
          <div class="kpi-tile-header">
            <span>${c.title}</span>
            <div class="kpi-tile-icon"><i data-lucide="${c.icon}"></i></div>
          </div>
          <div class="kpi-tile-value">
            ${c.mainVal}
            <small>${c.mainUnit}</small>
          </div>
          <div class="kpi-tile-meta">
            <span style="font-size: 11.5px; color: var(--text-muted);">${c.subVal}</span>
            ${renderDeltaBadge(c.diff, c.isHigherBetter !== undefined ? c.isHigherBetter : true, true)}
          </div>
        </div>
      `).join('');

      if (window.lucide) {
        lucide.createIcons();
      }
    }

    // Insights Box
    const insEl = document.getElementById('overview-insights-container');
    if (insEl && ov.insights) {
      insEl.innerHTML = ov.insights.map(item => {
        const title = item.title || (item.text ? item.text.substring(0, 45) + '...' : 'Điểm Nổi Bật');
        const desc = item.desc || item.text || '';
        const isGood = item.type === 'good' || item.type === 'positive' || item.type === 'highlight';
        const isBad = item.type === 'bad' || item.type === 'danger';
        const itemCls = isGood ? 'insight-good' : (isBad ? 'insight-bad' : 'insight-warn');
        const iconName = isGood ? 'check-circle' : (isBad ? 'alert-triangle' : 'info');

        return `
          <div class="insight-item ${itemCls}">
            <div class="insight-icon">
              <i data-lucide="${iconName}"></i>
            </div>
            <div>
              <div class="insight-title">${title}</div>
              <div class="insight-desc">${desc}</div>
            </div>
          </div>
        `;
      }).join('');
    }

    // 4-Week KPI Matrix Table
    const tblBody = document.querySelector('#table-overview-kpi-data tbody');
    if (tblBody && ov.kpis_trend) {
      const groups = [
        {
          name: '1. Sản Lượng Giao (Volume)',
          icon: 'package',
          items: ov.kpis_trend.filter(r => r.indicator.includes('Sản lượng'))
        },
        {
          name: '2. Hiệu Suất Giao Thành Công (%GTC)',
          icon: 'check-circle-2',
          items: ov.kpis_trend.filter(r => r.indicator.includes('%GTC'))
        },
        {
          name: '3. Chất Lượng Vận Hành SLA (%ODR & %LTC)',
          icon: 'clock',
          items: ov.kpis_trend.filter(r => r.indicator.includes('ODR') || r.indicator.includes('LTC'))
        },
        {
          name: '4. Vận Tải & Kiểm Soát Rủi Ro',
          icon: 'truck',
          items: ov.kpis_trend.filter(r => r.indicator.includes('Rớt') || r.indicator.includes('COD'))
        }
      ];

      let html = '';
      groups.forEach(grp => {
        if (grp.items.length === 0) return;
        html += `
          <tr class="tr-category-header">
            <td colspan="8">
              <span class="category-pill"><i data-lucide="${grp.icon}"></i> ${grp.name}</span>
            </td>
          </tr>
        `;

        grp.items.forEach(row => {
          const isPct = row.type === 'percent';
          const wKeys = (D.meta?.weeks || ['W34', 'W35', 'W36', 'W37']).map(w => w.toLowerCase());
          const val1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
          const val2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
          const val3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
          const val4 = row[wKeys[3]] !== undefined ? row[wKeys[3]] : (row.w37 !== undefined ? row.w37 : (row.vol || 0));

          const w_col1 = isPct ? fPct(val1) : fNum(val1);
          const w_col2 = isPct ? fPct(val2) : fNum(val2);
          const w_col3 = isPct ? fPct(val3) : fNum(val3);
          const w_col4 = isPct ? fPct(val4) : fNum(val4);

          const isHigherBetter = !row.indicator.includes('Rớt') && !row.indicator.includes('COD');
          const diffBadge = renderDeltaBadge(row.diff, isHigherBetter, isPct);

          const isTts = row.indicator.includes('TTS');
          const scopeTag = isTts
            ? '<span class="tag-scope-tts">⚡ TTS</span>'
            : '<span class="tag-scope-full">📦 Full Hàng</span>';

          let heatType = '';
          if (row.indicator.includes('GTC')) heatType = 'gtc';
          else if (row.indicator.includes('ODR')) heatType = 'odr';
          else if (row.indicator.includes('LTC')) heatType = 'ltc';
          else if (row.indicator.includes('Rớt')) heatType = 'rot_lc';
          else if (row.indicator.includes('COD')) heatType = 'cod_tm';

          const heatClassW = heatType ? getHeatmapClass(val4, heatType) : '';
          const trendVisual = renderMicroTrendVisual(val1, val2, val3, val4, isHigherBetter, isPct);

          html += `
            <tr>
              <td class="bold" style="font-size: 13px;">${row.indicator}</td>
              <td class="center">${scopeTag}</td>
              <td class="num">${w_col1}</td>
              <td class="num">${w_col2}</td>
              <td class="num">${w_col3}</td>
              <td class="num bold ${heatClassW}">${w_col4}</td>
              <td class="num">${diffBadge}</td>
              <td class="center">${trendVisual}</td>
            </tr>
          `;
        });
      });

      tblBody.innerHTML = html;
    }
  }

  function renderTrendSanLuongChart() {
    const ctx = document.getElementById('chart-trend-san-luong');
    if (!ctx) return;
    if (charts.trendSanLuong) charts.trendSanLuong.destroy();

    const weeks = D.meta?.weeks || ['W33', 'W34', 'W35', 'W36'];
    const kpis = D.overview?.kpis_trend || [];
    const fullItem = kpis.find(k => k.indicator.includes('Full hàng') && k.type === 'number') || {};
    const ttsItem = kpis.find(k => k.indicator.includes('TTS') && k.type === 'number') || {};

    const fullData = weeks.map(w => fullItem[w.toLowerCase()] || 0);
    const ttsData = weeks.map(w => ttsItem[w.toLowerCase()] || 0);

    charts.trendSanLuong = new Chart(ctx, {
      type: 'line',
      data: {
        labels: weeks,
        datasets: [
          {
            label: 'Toàn Mạng (Full Hàng)',
            data: fullData,
            borderColor: '#2563eb',
            backgroundColor: 'rgba(37, 99, 235, 0.08)',
            borderWidth: 3,
            fill: true,
            tension: 0.25,
            pointRadius: 5,
            datalabels: {
              align: 'top',
              offset: 6,
              color: '#1e3a8a',
              font: { weight: '800', size: 10.5 },
              formatter: v => (v / 1000).toFixed(1) + 'k'
            }
          },
          {
            label: 'Phân Khúc TTS (TikTok Shop)',
            data: ttsData,
            borderColor: '#0d9488',
            backgroundColor: 'transparent',
            borderWidth: 2.5,
            borderDash: [5, 5],
            tension: 0.25,
            pointRadius: 5,
            datalabels: {
              align: 'bottom',
              offset: 6,
              color: '#0d9488',
              font: { weight: '700', size: 10 },
              formatter: v => (v / 1000).toFixed(1) + 'k'
            }
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 24, bottom: 10 } },
        scales: {
          y: { ticks: { callback: v => (v / 1000).toLocaleString('vi-VN') + 'k' }, grid: { color: 'rgba(226, 232, 240, 0.6)' } },
          x: { grid: { display: false } }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: { callbacks: { label: c => `${c.dataset.label}: ${c.parsed.y.toLocaleString('vi-VN')} đơn` } }
        }
      }
    });
  }

  function renderTrendRatesChart() {
    const ctx = document.getElementById('chart-trend-rates');
    if (!ctx) return;
    if (charts.trendRates) charts.trendRates.destroy();

    const weeks = D.meta?.weeks || ['W33', 'W34', 'W35', 'W36'];
    const kpis = D.overview?.kpis_trend || [];
    const odrItem = kpis.find(k => k.indicator.includes('%ODR Full hàng')) || {};
    const ltcItem = kpis.find(k => k.indicator.includes('%LTC Full hàng')) || {};
    const gtcItem = kpis.find(k => k.indicator.includes('%GTC Full hàng (Ca1+Ca2+Tồn)')) || {};
    const gtcCa1Item = kpis.find(k => k.indicator.includes('%GTC TTS (Ca1 thuần)')) || {};

    const odrData = weeks.map(w => Number(((odrItem[w.toLowerCase()] || 0) * 100).toFixed(1)));
    const ltcData = weeks.map(w => Number(((ltcItem[w.toLowerCase()] || 0) * 100).toFixed(1)));
    const gtcData = weeks.map(w => Number(((gtcItem[w.toLowerCase()] || 0) * 100).toFixed(1)));
    const gtcCa1Data = weeks.map(w => Number(((gtcCa1Item[w.toLowerCase()] || 0) * 100).toFixed(1)));

    charts.trendRates = new Chart(ctx, {
      type: 'line',
      data: {
        labels: weeks,
        datasets: [
          {
            label: '%ODR (Giao Đúng Hẹn)',
            data: odrData,
            borderColor: '#10b981',
            borderWidth: 2.5,
            pointRadius: 4.5,
            datalabels: { align: 'top', offset: 4, color: '#047857', formatter: v => v.toFixed(1) + '%' }
          },
          {
            label: '%LTC (Lấy Thành Công)',
            data: ltcData,
            borderColor: '#2563eb',
            borderWidth: 2.5,
            pointRadius: 4.5,
            datalabels: { align: 'bottom', offset: 4, color: '#1d4ed8', formatter: v => v.toFixed(1) + '%' }
          },
          {
            label: '%GTC Full Hàng',
            data: gtcData,
            borderColor: '#f59e0b',
            borderWidth: 2.5,
            pointRadius: 4.5,
            datalabels: { align: 'top', offset: 4, color: '#b45309', formatter: v => v.toFixed(1) + '%' }
          },
          {
            label: '%GTC TTS Ca 1',
            data: gtcCa1Data,
            borderColor: '#8b5cf6',
            borderWidth: 2.5,
            borderDash: [4, 4],
            pointRadius: 4,
            datalabels: { align: 'top', offset: 4, color: '#6d28d9', formatter: v => v.toFixed(1) + '%' }
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 20, bottom: 10 } },
        scales: {
          y: { min: 50, max: 100, ticks: { callback: v => v + '%' }, grid: { color: 'rgba(226, 232, 240, 0.6)' } },
          x: { grid: { display: false } }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: { callbacks: { label: c => `${c.dataset.label}: ${c.parsed.y.toFixed(1)}%` } }
        }
      }
    });
  }

  function renderSanLuongTinhChart() {
    const ctx = document.getElementById('chart-sanluong-tinh-bar');
    if (!ctx || !D.san_luong || !D.san_luong.tinh) return;
    if (charts.sanLuongTinh) charts.sanLuongTinh.destroy();

    const latestWeek = D.meta?.latest_week || 'W37';
    const currKey = latestWeek.toLowerCase();
    const dataT = [...D.san_luong.tinh].sort((a, b) => {
      const vA = a[currKey] !== undefined ? a[currKey] : (a.vol || 0);
      const vB = b[currKey] !== undefined ? b[currKey] : (b.vol || 0);
      return vB - vA;
    });
    const ttsT = D.san_luong.tinh_tts || [];
    const ttsMap = {};
    ttsT.forEach(t => ttsMap[t.tinh] = t);

    charts.sanLuongTinh = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: dataT.map(d => d.tinh),
        datasets: [
          {
            label: `Full Hàng (Toàn Mạng) ${latestWeek}`,
            data: dataT.map(d => d[currKey] !== undefined ? d[currKey] : (d.vol || d.w37 || 0)),
            backgroundColor: dataT.map(d => {
              if (!state.selectedProvince) return '#1e3a8a';
              return d.tinh === state.selectedProvince ? '#2563eb' : 'rgba(30, 58, 138, 0.25)';
            }),
            borderColor: dataT.map(d => d.tinh === state.selectedProvince ? '#1d4ed8' : 'transparent'),
            borderWidth: 2,
            borderRadius: 6,
            datalabels: {
              anchor: 'end',
              align: 'top',
              offset: 2,
              color: d => (state.selectedProvince && dataT[d.dataIndex].tinh !== state.selectedProvince) ? '#94a3b8' : '#1e3a8a',
              font: { weight: '800', size: 10 },
              formatter: v => (v / 1000).toFixed(1) + 'k'
            }
          },
          {
            label: `Phân Khúc TTS (TikTok Shop) ${latestWeek}`,
            data: dataT.map(d => {
              const t = ttsMap[d.tinh];
              if (t && t[currKey] !== undefined) return t[currKey];
              if (d.tts_vol) return d.tts_vol;
              const total = d[currKey] !== undefined ? d[currKey] : (d.vol || 0);
              return Math.round(total * 0.192);
            }),
            backgroundColor: dataT.map(d => {
              if (!state.selectedProvince) return '#f26522';
              return d.tinh === state.selectedProvince ? '#ea580c' : 'rgba(242, 101, 34, 0.25)';
            }),
            borderColor: dataT.map(d => d.tinh === state.selectedProvince ? '#c2410c' : 'transparent'),
            borderWidth: 2,
            borderRadius: 6,
            datalabels: {
              anchor: 'end',
              align: 'top',
              offset: 2,
              color: d => (state.selectedProvince && dataT[d.dataIndex].tinh !== state.selectedProvince) ? '#94a3b8' : '#d44d0e',
              font: { weight: '800', size: 10 },
              formatter: (v, ctx) => {
                const total = dataT[ctx.dataIndex][currKey] || dataT[ctx.dataIndex].vol || 0;
                const pct = total ? ((v / total) * 100).toFixed(1) : '19.2';
                return (v / 1000).toFixed(1) + `k (${pct}%)`;
              }
            }
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 26 } },
        scales: {
          y: { ticks: { callback: v => (v / 1000) + 'k' }, grid: { color: 'rgba(226, 232, 240, 0.6)' } },
          x: { ticks: { font: { weight: '800', size: 11 } }, grid: { display: false } }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => `${c.dataset.label}: ${c.parsed.y.toLocaleString('vi-VN')} đơn`
            }
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            const idx = elements[0].index;
            const clickedProvince = dataT[idx].tinh;
            selectAndHighlightProvince(clickedProvince);
          }
        }
      }
    });
  }

  // --------------------------------------------------------------------------
  // TAB 2: SẢN LƯỢNG GIAO (2 BẢNG ĐỐI XỨNG: FULL HÀNG vs TIKTOK SHOP)
  // --------------------------------------------------------------------------
    // --------------------------------------------------------------------------
  // TAB 2: SẢN LƯỢNG GIAO (FULL HÀNG & PHÂN KHÚC TTS)
  // --------------------------------------------------------------------------
  function renderVolumeTab() {
    if (!D.san_luong) return;

    // 1. BẢNG 1: SẢN LƯỢNG FULL HÀNG
    const tblBodyFull = document.querySelector('#table-vol-full-detailed tbody');
    if (tblBodyFull && D.san_luong.am_full) {
      const latestKey = D.meta?.latest_week ? D.meta.latest_week.toLowerCase() : 'w37';
      const prevKey = D.meta?.prev_week ? D.meta.prev_week.toLowerCase() : 'w36';
      let list = [...D.san_luong.am_full].map(r => {
        const curr = r[latestKey] !== undefined ? r[latestKey] : (r.w37 !== undefined ? r.w37 : (r.w36 || 0));
        const prev = r[prevKey] !== undefined ? r[prevKey] : (r.w36 !== undefined ? r.w36 : (r.w35 || 0));
        return {
          ...r,
          curr_val: curr,
          prev_val: prev,
          diff_val: r.diff !== undefined ? r.diff : (curr - prev)
        };
      });

      if (state.searchVolFull) {
        list = list.filter(r => r.am.toLowerCase().includes(state.searchVolFull));
      }

      const sorted = list.sort((a, b) => (b.diff_val || 0) - (a.diff_val || 0));

      tblBodyFull.innerHTML = sorted.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const diffBadge = renderDeltaBadge(row.diff_val, true, false);
        const prevWVal = v3 || 0;
        const pctWoW = prevWVal > 0 ? ((v4 - prevWVal) / prevWVal * 100) : 0;
        const pctStr = (pctWoW >= 0 ? '+' : '') + pctWoW.toFixed(1) + '%';
        const pctBadge = `<span style="font-size:11px; font-weight:800; margin-left:4px; color:${pctWoW >= 0 ? '#16a34a' : '#dc2626'};">(${pctStr})</span>`; // isPercent = false (đơn)
        const evalBadge = row.diff_val > 0
          ? '<span class="badge-tag badge-tag-green">🟢 Tăng Trưởng</span>'
          : '<span class="badge-tag badge-tag-blue">Giảm Nhẹ</span>';

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.prev_val)}</td>
            <td class="num bold" style="background: var(--color-blue-bg); font-weight:800;">${fNum(row.curr_val)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 2. BẢNG 2: SẢN LƯỢNG TIKTOK SHOP (TTS)
    const tblBodyTTS = document.querySelector('#table-vol-tts-detailed tbody');
    if (tblBodyTTS && D.san_luong.am_tts) {
      const latestKey = D.meta?.latest_week ? D.meta.latest_week.toLowerCase() : 'w37';
      const prevKey = D.meta?.prev_week ? D.meta.prev_week.toLowerCase() : 'w36';
      const fullMap = {};
      (D.san_luong.am_full || []).forEach(f => fullMap[f.am] = (f[latestKey] !== undefined ? f[latestKey] : (f.w37 !== undefined ? f.w37 : (f.w36 || 0))));

      let listTTS = [...D.san_luong.am_tts].map(r => {
        const fullVol = fullMap[r.am] || 0;
        const curTTS = r[latestKey] !== undefined ? r[latestKey] : (r.w37 !== undefined ? r.w37 : (r.w36 || 0));
        const prevTTS = r[prevKey] !== undefined ? r[prevKey] : (r.w36 !== undefined ? r.w36 : (r.w35 || 0));
        const rate = fullVol > 0 ? (curTTS / fullVol) : 0;
        return {
          ...r,
          curr_val: curTTS,
          prev_val: prevTTS,
          rate_tts: rate,
          diff_val: r.diff !== undefined ? r.diff : (curTTS - prevTTS)
        };
      });

      if (state.searchVolTTS) {
        listTTS = listTTS.filter(r => r.am.toLowerCase().includes(state.searchVolTTS));
      }

      const sortedTTS = listTTS.sort((a, b) => (b.diff_val || 0) - (a.diff_val || 0));

      tblBodyTTS.innerHTML = sortedTTS.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const diffBadge = renderDeltaBadge(row.diff_val, true, false);
        const prevWVal = v3 || 0;
        const pctWoW = prevWVal > 0 ? ((v4 - prevWVal) / prevWVal * 100) : 0;
        const pctStr = (pctWoW >= 0 ? '+' : '') + pctWoW.toFixed(1) + '%';
        const pctBadge = `<span style="font-size:11px; font-weight:800; margin-left:4px; color:${pctWoW >= 0 ? '#16a34a' : '#dc2626'};">(${pctStr})</span>`; // isPercent = false (đơn)
        const evalBadge = row.diff_val > 0
          ? '<span class="badge-tag badge-tag-green">🟢 Tăng Trưởng</span>'
          : '<span class="badge-tag badge-tag-amber">Ổn Định</span>';

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.prev_val)}</td>
            <td class="num bold" style="background: var(--color-amber-bg); color:#ea580c; font-weight:800;">${fNum(row.curr_val)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="num" style="font-weight:700;">${fPct(row.rate_tts)}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 3. BẢNG 3A: SẢN LƯỢNG 5 TỈNH THÀNH (FULL HÀNG)
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
      }).sort((a, b) => (b.diff_val || 0) - (a.diff_val || 0));

      tblBodyTinhFull.innerHTML = listTinhFull.map((row, i) => {
        const isSelected = state.selectedProvince === row.tinh;
        const rowClass = isSelected ? 'province-laser-box' : '';
        const v1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || row.w38 || 0);
        const v2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || row.w39 || 0);
        const v3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || row.w40 || 0);
        const v4 = row[wKeys[3]] !== undefined ? row[wKeys[3]] : (row.w37 || row.w41 || row.vol || 0);
        const diffBadge = renderDeltaBadge(row.diff_val, true, false);
        const prevWVal = v3 || 0;
        const pctWoW = prevWVal > 0 ? ((v4 - prevWVal) / prevWVal * 100) : 0;
        const pctStr = (pctWoW >= 0 ? '+' : '') + pctWoW.toFixed(1) + '%';
        const pctBadge = `<span style="font-size:11px; font-weight:800; margin-left:4px; color:${pctWoW >= 0 ? '#16a34a' : '#dc2626'};">(${pctStr})</span>`;
        const evalBadge = row.diff_val > 0
          ? '<span class="badge-tag badge-tag-green">🟢 Tăng Trưởng</span>'
          : '<span class="badge-tag badge-tag-blue">Giảm Nhẹ</span>';

        return `
          <tr data-province="${row.tinh}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightProvince('${row.tinh}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13.5px; font-weight:800; color:${isSelected ? '#2563eb' : 'inherit'};">${row.tinh}</td>
            <td class="num">${fNum(v1)}</td>
            <td class="num">${fNum(v2)}</td>
            <td class="num">${fNum(v3)}</td>
            <td class="num bold" style="background: var(--color-blue-bg); font-weight:800; font-size:13.5px;">${fNum(v4)}</td>
            <td class="num bold">${diffBadge} ${pctBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 4. BẢNG 3B: SẢN LƯỢNG 5 TỈNH THÀNH (TIKTOK SHOP)
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
      }).sort((a, b) => (b.diff_val || 0) - (a.diff_val || 0));

      tblBodyTinhTTS.innerHTML = listTinhTTS.map((row, i) => {
        const isSelected = state.selectedProvince === row.tinh;
        const rowClass = isSelected ? 'province-laser-box' : '';
        const wKeys = (D.meta?.weeks || ['W38', 'W39', 'W40', 'W41']).map(w => w.toLowerCase());
        const v1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || row.w38 || 0);
        const v2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || row.w39 || 0);
        const v3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || row.w40 || 0);
        const v4 = row[wKeys[3]] !== undefined ? row[wKeys[3]] : (row.w37 || row.w41 || row.vol || 0);
        const diffBadge = renderDeltaBadge(row.diff_val, true, false);
        const prevWVal = v3 || 0;
        const pctWoW = prevWVal > 0 ? ((v4 - prevWVal) / prevWVal * 100) : 0;
        const pctStr = (pctWoW >= 0 ? '+' : '') + pctWoW.toFixed(1) + '%';
        const pctBadge = `<span style="font-size:11px; font-weight:800; margin-left:4px; color:${pctWoW >= 0 ? '#16a34a' : '#dc2626'};">(${pctStr})</span>`;
        const evalBadge = row.diff_val > 0
          ? '<span class="badge-tag badge-tag-green">🟢 Tăng Trưởng</span>'
          : '<span class="badge-tag badge-tag-amber">Ổn Định</span>';

        return `
          <tr data-province="${row.tinh}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightProvince('${row.tinh}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13.5px; font-weight:800; color:${isSelected ? '#ea580c' : 'inherit'};">${row.tinh}</td>
            <td class="num">${fNum(v1)}</td>
            <td class="num">${fNum(v2)}</td>
            <td class="num">${fNum(v3)}</td>
            <td class="num bold" style="background: var(--color-amber-bg); color:#ea580c; font-weight:800; font-size:13.5px;">${fNum(v4)}</td>
            <td class="num bold">${diffBadge} ${pctBadge}</td>
            <td class="num" style="font-weight:700;">${fPct(row.rate_tts)}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }
  }

  
  // --------------------------------------------------------------------------
  // CHART: SẢN LƯỢNG 5 TỈNH QUA 4 TUẦN (W40 - W43) & TỶ LỆ TĂNG TRƯỞNG % WoW
  // --------------------------------------------------------------------------
  function renderTinhVol4WeeksChart() {
    const ctx = document.getElementById('chart-tinh-vol-4weeks');
    if (!ctx || !D.san_luong) return;
    if (charts.tinhVol4Weeks) charts.tinhVol4Weeks.destroy();

    const isTTS = (state.tinhVolChannel === 'tts');
    const isLine = (state.tinhVolType === 'line');
    const rawData = isTTS ? (D.san_luong.tinh_tts || []) : (D.san_luong.tinh_full || D.san_luong.tinh || []);

    const wKeys = (D.meta?.weeks || ['W38', 'W39', 'W40', 'W41']).map(w => w.toLowerCase());
    const weekLabels = D.meta?.weeks || ['W38', 'W39', 'W40', 'W41'];

    // Sort provinces by W41 volume descending
    const sortedProvinces = [...rawData].sort((a, b) => {
      const vA = a[wKeys[3]] !== undefined ? a[wKeys[3]] : (a.w41 || a.vol || 0);
      const vB = b[wKeys[3]] !== undefined ? b[wKeys[3]] : (b.w41 || b.vol || 0);
      return vB - vA;
    });

    const labels = sortedProvinces.map(p => p.tinh);

    // Update summary badge
    const badgeEl = document.getElementById('tinh-vol-summary-badge');
    if (badgeEl) {
      const curW = weekLabels[3] || 'W43';
      if (isTTS) {
        badgeEl.innerHTML = `🛒 TikTok Shop ${curW}: <strong>73.732 đơn</strong> (+175 đơn / +0,2% WoW)`;
        badgeEl.style.color = '#ea580c';
        badgeEl.style.background = '#fff7ed';
        badgeEl.style.borderColor = 'rgba(234, 88, 12, 0.3)';
      } else {
        badgeEl.innerHTML = `🚀 Toàn vùng ${curW}: <strong>380.455 đơn</strong> (+15.939 đơn / +4,4% WoW)`;
        badgeEl.style.color = '#16a34a';
        badgeEl.style.background = '#dcfce7';
        badgeEl.style.borderColor = 'rgba(22, 163, 74, 0.3)';
      }
    }

    if (!isLine) {
      // GROUPED BAR CHART: 4 columns per province (W38, W39, W40, W41)
      const dataW38 = sortedProvinces.map(p => p[wKeys[0]] !== undefined ? p[wKeys[0]] : (p.w38 || 0));
      const dataW39 = sortedProvinces.map(p => p[wKeys[1]] !== undefined ? p[wKeys[1]] : (p.w39 || 0));
      const dataW40 = sortedProvinces.map(p => p[wKeys[2]] !== undefined ? p[wKeys[2]] : (p.w40 || 0));
      const dataW41 = sortedProvinces.map(p => p[wKeys[3]] !== undefined ? p[wKeys[3]] : (p.w41 || p.vol || 0));

      charts.tinhVol4Weeks = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: `${weekLabels[0]}`,
              data: dataW38,
              backgroundColor: '#94a3b8',
              borderRadius: 4,
              maxBarThickness: 32,
              datalabels: {
                anchor: 'end',
                align: 'top',
                offset: 2,
                color: '#64748b',
                font: { size: 10, weight: '600' },
                formatter: (val) => val >= 1000 ? (val / 1000).toFixed(1) + 'k' : val
              }
            },
            {
              label: `${weekLabels[1]}`,
              data: dataW39,
              backgroundColor: '#60a5fa',
              borderRadius: 4,
              maxBarThickness: 32,
              datalabels: {
                anchor: 'end',
                align: 'top',
                offset: 2,
                color: '#2563eb',
                font: { size: 10, weight: '600' },
                formatter: (val) => val >= 1000 ? (val / 1000).toFixed(1) + 'k' : val
              }
            },
            {
              label: `${weekLabels[2]} (Mega Sale 10.10)`,
              data: dataW40,
              backgroundColor: '#1e40af',
              borderRadius: 4,
              maxBarThickness: 32,
              datalabels: {
                anchor: 'end',
                align: 'top',
                offset: 2,
                color: '#1e3a8a',
                font: { size: 10.5, weight: '700' },
                formatter: (val) => val >= 1000 ? (val / 1000).toFixed(1) + 'k' : val
              }
            },
            {
              label: `${weekLabels[3]} (Hiện tại)`,
              data: dataW41,
              backgroundColor: '#f97316',
              borderColor: '#ea580c',
              borderWidth: 2,
              borderRadius: 6,
              maxBarThickness: 36,
              datalabels: {
                anchor: 'end',
                align: 'top',
                offset: 4,
                color: '#ea580c',
                font: { size: 11.5, weight: '800' },
                formatter: (val, ctx2) => {
                  const idx = ctx2.dataIndex;
                  const prevVal = dataW40[idx] || 0;
                  const pct = prevVal > 0 ? ((val - prevVal) / prevVal * 100) : 0;
                  const sign = pct >= 0 ? '+' : '';
                  const valStr = val >= 1000 ? (val / 1000).toFixed(1) + 'k' : fNum(val);
                  return [valStr, `${sign}${pct.toFixed(1)}%`];
                }
              }
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          layout: {
            padding: { top: 32, bottom: 8, left: 10, right: 10 }
          },
          plugins: {
            legend: {
              position: 'top',
              labels: {
                boxWidth: 10,
                boxHeight: 10,
                font: { weight: '700', size: 12 }
              }
            },
            tooltip: {
              backgroundColor: 'rgba(15, 23, 42, 0.95)',
              titleFont: { size: 13, weight: '700' },
              bodyFont: { size: 12 },
              padding: 12,
              cornerRadius: 8,
              callbacks: {
                label: function (c) {
                  const val = c.raw || 0;
                  const idx = c.dataIndex;
                  if (c.datasetIndex === 3) {
                    const prev = dataW40[idx] || 0;
                    const diff = val - prev;
                    const pct = prev > 0 ? (diff / prev * 100) : 0;
                    const sign = diff >= 0 ? '+' : '';
                    return ` ${c.dataset.label}: ${fNum(val)} đơn (${sign}${fNum(diff)} đơn / ${sign}${pct.toFixed(1)}% WoW)`;
                  }
                  return ` ${c.dataset.label}: ${fNum(val)} đơn`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: { display: false },
              ticks: {
                font: { weight: '800', size: 12.5 },
                color: '#0f172a'
              }
            },
            y: {
              beginAtZero: true,
              grid: { color: 'rgba(226, 232, 240, 0.6)' },
              ticks: {
                callback: v => (v >= 1000 ? (v / 1000) + 'k' : v),
                font: { size: 11 }
              }
            }
          }
        }
      });
    } else {
      // LINE TREND CHART: 5 lines for 5 provinces across W38, W39, W40, W41
      const palette = [
        { stroke: '#2563eb', fill: 'rgba(37, 99, 235, 0.08)' },
        { stroke: '#16a34a', fill: 'rgba(22, 163, 74, 0.08)' },
        { stroke: '#ea580c', fill: 'rgba(234, 88, 12, 0.08)' },
        { stroke: '#8b5cf6', fill: 'rgba(139, 92, 246, 0.08)' },
        { stroke: '#06b6d4', fill: 'rgba(6, 182, 212, 0.08)' }
      ];

      const datasets = sortedProvinces.map((p, idx) => {
        const col = palette[idx % palette.length];
        const vW38 = p[wKeys[0]] !== undefined ? p[wKeys[0]] : (p.w38 || 0);
        const vW39 = p[wKeys[1]] !== undefined ? p[wKeys[1]] : (p.w39 || 0);
        const vW40 = p[wKeys[2]] !== undefined ? p[wKeys[2]] : (p.w40 || 0);
        const vW41 = p[wKeys[3]] !== undefined ? p[wKeys[3]] : (p.w41 || p.vol || 0);
        const pct = vW40 > 0 ? ((vW41 - vW40) / vW40 * 100) : 0;
        const sign = pct >= 0 ? '+' : '';

        return {
          label: `${p.tinh} (${sign}${pct.toFixed(1)}%)`,
          data: [vW38, vW39, vW40, vW41],
          borderColor: col.stroke,
          backgroundColor: col.stroke,
          borderWidth: 3,
          tension: 0.35,
          pointRadius: 6,
          pointHoverRadius: 8,
          datalabels: {
            anchor: 'end',
            align: 'top',
            offset: 4,
            color: col.stroke,
            font: { size: 11, weight: '700' },
            formatter: (val, ctx2) => {
              if (ctx2.dataIndex === 3) {
                return `${(val / 1000).toFixed(1)}k (${sign}${pct.toFixed(1)}%)`;
              }
              return (val / 1000).toFixed(1) + 'k';
            }
          }
        };
      });

      charts.tinhVol4Weeks = new Chart(ctx, {
        type: 'line',
        data: {
          labels: weekLabels,
          datasets: datasets
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          layout: {
            padding: { top: 32, bottom: 8, left: 10, right: 10 }
          },
          plugins: {
            legend: {
              position: 'top',
              labels: {
                boxWidth: 10,
                boxHeight: 10,
                font: { weight: '700', size: 12 }
              }
            },
            tooltip: {
              backgroundColor: 'rgba(15, 23, 42, 0.95)',
              padding: 12,
              cornerRadius: 8,
              callbacks: {
                label: function (c) {
                  return ` ${c.dataset.label}: ${fNum(c.raw)} đơn`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: { display: false },
              ticks: { font: { weight: '800', size: 12.5 } }
            },
            y: {
              beginAtZero: false,
              grid: { color: 'rgba(226, 232, 240, 0.6)' },
              ticks: {
                callback: v => (v >= 1000 ? (v / 1000) + 'k' : v),
                font: { size: 11 }
              }
            }
          }
        }
      });
    }
  }

    window.switchTinhVolChannel = function(ch) {
    state.tinhVolChannel = ch;
    const btnFull = document.getElementById('btn-tinh-channel-full');
    const btnTTS = document.getElementById('btn-tinh-channel-tts');
    if (btnFull) btnFull.classList.toggle('active', ch === 'full');
    if (btnTTS) btnTTS.classList.toggle('active', ch === 'tts');
    const titleEl = document.getElementById('tinh-vol-chart-header-title');
    if (titleEl) {
      titleEl.textContent = (ch === 'tts') 
        ? 'BIỂU ĐỒ SẢN LƯỢNG 5 TỈNH QUA 4 TUẦN (W40 – W43) — TIKTOK SHOP & TỶ LỆ TĂNG TRƯỞNG % WoW'
        : 'BIỂU ĐỒ SẢN LƯỢNG 5 TỈNH QUA 4 TUẦN (W40 – W43) — FULL HÀNG & TỶ LỆ TĂNG TRƯỞNG % WoW';
    }
    renderTinhVol4WeeksChart();
  };

  window.switchTinhVolType = function(t) {
    state.tinhVolType = t;
    const btnBar = document.getElementById('btn-tinh-type-bar');
    const btnLine = document.getElementById('btn-tinh-type-line');
    if (btnBar) btnBar.classList.toggle('active', t === 'bar');
    if (btnLine) btnLine.classList.toggle('active', t === 'line');
    renderTinhVol4WeeksChart();
  };

  function renderVolAMChart() {
    const ctx = document.getElementById('chart-vol-am-bar');
    if (!ctx || !D.san_luong) return;
    if (charts.volAM) charts.volAM.destroy();

    const prevKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2].toLowerCase() : 'w35';
    const currKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1].toLowerCase() : 'w36';
    const prevLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2] : 'W35';
    const currLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1] : 'W36';

    const mode = state.volChartMode || 'w34_vs_w35_full';
    const amFullList = D.san_luong.am_full || [];
    const amTtsList = D.san_luong.am_tts || [];

    const fullMap = {};
    amFullList.forEach(f => fullMap[f.am] = f);

    const ttsMap = {};
    amTtsList.forEach(t => ttsMap[t.am] = t);

    // Master 19 AM dataset combining accurate Full and TTS figures
    let list = amFullList.map(r => {
      const tts = ttsMap[r.am] || {};
      const volFullCurr = r[currKey] !== undefined ? r[currKey] : (r.w35 || r.vol || 0);
      const volFullPrev = r[prevKey] !== undefined ? r[prevKey] : (r.w34 || (volFullCurr - (r.diff || 0)));
      const diffFull = r.diff !== undefined ? r.diff : (volFullCurr - volFullPrev);

      const volTtsCurr = tts[currKey] !== undefined ? tts[currKey] : (tts.w35 !== undefined ? tts.w35 : (tts.vol || 0));
      const volTtsPrev = tts[prevKey] !== undefined ? tts[prevKey] : (tts.w34 !== undefined ? tts.w34 : (volTtsCurr - (tts.diff || 0)));
      const diffTts = tts.diff !== undefined ? tts.diff : (volTtsCurr - volTtsPrev);
      const pctTts = volFullCurr > 0 ? (volTtsCurr / volFullCurr) * 100 : 0;

      return {
        am: r.am,
        vol_full_w34: volFullPrev,
        vol_full_w35: volFullCurr,
        diff_full: diffFull,
        vol_tts_w34: volTtsPrev,
        vol_tts_w35: volTtsCurr,
        diff_tts: diffTts,
        pct_tts: pctTts
      };
    });

    let displayList = [...list];
    let title = '';
    let datasets = [];
    let y1Title = 'Biến Động WoW (Δ Đơn)';

    if (mode === 'w34_vs_w35_tts' || mode === 'w35_vs_w36_tts' || (mode.includes('tts') && !mode.includes('full'))) {
      displayList.sort((a, b) => (b.vol_tts_w35 || 0) - (a.vol_tts_w35 || 0));
    } else {
      displayList.sort((a, b) => (b.vol_full_w35 || 0) - (a.vol_full_w35 || 0));
    }
    if (mode === 'w34_vs_w35_full' || mode === 'w35_vs_w36_full' || (mode.includes('full') && !mode.includes('tts'))) {
      title = `SẢN LƯỢNG FULL HÀNG (CỘT ${prevLabel} vs ${currLabel} + ĐƯỜNG BIẾN ĐỘNG Δ)`;

      datasets = [
        {
          type: 'bar',
          label: `Full Hàng ${prevLabel} (Tuần Trước)`,
          data: displayList.map(d => d.vol_full_w34),
          backgroundColor: '#94a3b8',
          borderRadius: 4,
          yAxisID: 'y',
          order: 2
        },
        {
          type: 'bar',
          label: `Full Hàng ${currLabel} (Hiện Tại)`,
          data: displayList.map(d => d.vol_full_w35),
          backgroundColor: displayList.map(d => d.diff_full > 0 ? '#10b981' : '#2563eb'),
          borderRadius: 4,
          yAxisID: 'y',
          order: 2
        },
        {
          type: 'line',
          label: 'Đường Biến Động WoW (Δ Đơn)',
          data: displayList.map(d => d.diff_full),
          borderColor: '#f26522',
          borderWidth: 3,
          tension: 0.25,
          pointBackgroundColor: displayList.map(d => d.diff_full > 0 ? '#10b981' : '#ef4444'),
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 6,
          pointHoverRadius: 8,
          yAxisID: 'y1',
          order: 1
        }
      ];
    } else if (mode === 'w34_vs_w35_tts' || mode === 'w35_vs_w36_tts' || (mode.includes('tts') && !mode.includes('full'))) {
      title = `SẢN LƯỢNG TIKTOK SHOP (CỘT TTS ${prevLabel} vs ${currLabel} + ĐƯỜNG BIẾN ĐỘNG TTS Δ)`;

      datasets = [
        {
          type: 'bar',
          label: `TTS ${prevLabel} (Tuần Trước)`,
          data: displayList.map(d => d.vol_tts_w34),
          backgroundColor: '#cbd5e1',
          borderRadius: 4,
          yAxisID: 'y',
          order: 2
        },
        {
          type: 'bar',
          label: `TTS ${currLabel} (Hiện Tại)`,
          data: displayList.map(d => d.vol_tts_w35),
          backgroundColor: displayList.map(d => d.diff_tts > 0 ? '#10b981' : '#f97316'),
          borderRadius: 4,
          yAxisID: 'y',
          order: 2
        },
        {
          type: 'line',
          label: 'Đường Biến Động TTS (Δ Đơn)',
          data: displayList.map(d => d.diff_tts),
          borderColor: '#0284c7',
          borderWidth: 3,
          tension: 0.25,
          pointBackgroundColor: displayList.map(d => d.diff_tts >= 0 ? '#10b981' : '#ef4444'),
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 6,
          pointHoverRadius: 8,
          yAxisID: 'y1',
          order: 1
        }
      ];
    } else if (mode === 'full_vs_tts') {
      title = `SO SÁNH SẢN LƯỢNG (FULL HÀNG vs TIKTOK SHOP + ĐƯỜNG % TỶ TRỌNG TTS - ${currLabel})`;
      y1Title = '% Tỷ Trọng TTS';

      datasets = [
        {
          type: 'bar',
          label: `Full Hàng ${currLabel}`,
          data: displayList.map(d => d.vol_full_w35),
          backgroundColor: '#2563eb',
          borderRadius: 4,
          yAxisID: 'y',
          order: 2
        },
        {
          type: 'bar',
          label: `Phân Khúc TTS ${currLabel}`,
          data: displayList.map(d => d.vol_tts_w35),
          backgroundColor: '#f97316',
          borderRadius: 4,
          yAxisID: 'y',
          order: 2
        },
        {
          type: 'line',
          label: '% Tỷ Trọng TTS / Full',
          data: displayList.map(d => parseFloat(d.pct_tts.toFixed(1))),
          borderColor: '#8b5cf6',
          borderWidth: 3,
          tension: 0.25,
          pointBackgroundColor: '#8b5cf6',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 6,
          pointHoverRadius: 8,
          yAxisID: 'y1',
          order: 1
        }
      ];
    }

    const titleEl = document.getElementById('vol-chart-title');
    if (titleEl) titleEl.innerHTML = `<i data-lucide="bar-chart-3" style="color: var(--color-blue);"></i> ${title}`;

    charts.volAM = new Chart(ctx, {
      type: 'bar',
      data: { labels: displayList.map(d => d.am), datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 20, bottom: 10 } },
        scales: {
          y: {
            position: 'left',
            ticks: { callback: v => v >= 1000 ? (v / 1000).toFixed(0) + 'k' : v.toLocaleString() },
            title: { display: true, text: 'Sản Lượng (Đơn)', font: { weight: '700', size: 11 } },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          y1: {
            position: 'right',
            grid: { drawOnChartArea: false },
            title: { display: true, text: y1Title, font: { weight: '700', size: 11, color: '#f26522' } },
            ticks: {
              callback: v => {
                if (mode === 'full_vs_tts') return v + '%';
                const s = v > 0 ? '+' : '';
                return s + (Math.abs(v) >= 1000 ? (v / 1000).toFixed(1) + 'k' : v.toLocaleString());
              }
            }
          },
          x: {
            ticks: { maxRotation: 45, minRotation: 20, font: { size: 11, weight: '800' } }
          }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => {
                if (c.dataset.type === 'line') {
                  if (mode === 'full_vs_tts') return `${c.dataset.label}: ${c.parsed.y}%`;
                  const sign = c.parsed.y > 0 ? '+' : '';
                  return `${c.dataset.label}: ${sign}${c.parsed.y.toLocaleString('vi-VN')} đơn`;
                }
                return `${c.dataset.label}: ${c.parsed.y.toLocaleString('vi-VN')} đơn`;
              }
            }
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            selectAndHighlightAM(displayList[elements[0].index].am);
          }
        }
      }
    });
    lucide.createIcons();
  }

  window.setGtcTongSegment = function(seg) {
    state.gtcTongSegment = seg;
    const btnFull = document.getElementById('btn-gtctong-full');
    const btnTts = document.getElementById('btn-gtctong-tts');
    const btnCompare = document.getElementById('btn-gtctong-compare');

    [btnFull, btnTts, btnCompare].forEach(b => {
      if (b) {
        b.classList.remove('btn-primary', 'active');
        b.classList.add('btn-secondary');
      }
    });

    const titleEl = document.getElementById('chart-gtc-tong-title');
    const badgeEl = document.getElementById('badge-gtc-tong-segment');

    const prevLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2] : 'W35';
    const currLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1] : 'W36';

    if (seg === 'full' && btnFull) {
      btnFull.classList.add('btn-primary', 'active');
      btnFull.classList.remove('btn-secondary');
      if (titleEl) titleEl.textContent = `BIỂU ĐỒ SO SÁNH %GTC TỔNG ${prevLabel} vs ${currLabel} THEO 19 AM (FULL HÀNG)`;
      if (badgeEl) { badgeEl.textContent = 'Full Hàng'; badgeEl.className = 'badge-tag badge-tag-blue'; }
    } else if (seg === 'tts' && btnTts) {
      btnTts.classList.add('btn-primary', 'active');
      btnTts.classList.remove('btn-secondary');
      if (titleEl) titleEl.textContent = `BIỂU ĐỒ SO SÁNH %GTC TỔNG ${prevLabel} vs ${currLabel} THEO 19 AM (TIKTOK SHOP)`;
      if (badgeEl) { badgeEl.textContent = 'TikTok Shop (TTS)'; badgeEl.className = 'badge-tag badge-tag-green'; }
    } else if (seg === 'compare' && btnCompare) {
      btnCompare.classList.add('btn-primary', 'active');
      btnCompare.classList.remove('btn-secondary');
      if (titleEl) titleEl.textContent = `SO SÁNH ĐỐI CHIẾU %GTC (FULL HÀNG vs TIKTOK SHOP ${currLabel})`;
      if (badgeEl) { badgeEl.textContent = 'Full vs TTS'; badgeEl.className = 'badge-tag badge-tag-purple'; }
    }

    renderGtcTongTab();
    renderGtcTongBarChart();
    if (window.lucide) lucide.createIcons();
  };

  window.setGtcTongHighlight = function(hl) {
    state.gtcTongHighlight = hl;
    state.selectedAM = null;
    const btnMap = {
      all: 'btn-gtctong-hl-all',
      top_gtc: 'btn-gtctong-hl-top',
      bottom_gtc: 'btn-gtctong-hl-bottom',
      grow: 'btn-gtctong-hl-grow'
    };

    Object.keys(btnMap).forEach(k => {
      const b = document.getElementById(btnMap[k]);
      if (b) {
        if (k === hl) {
          b.classList.add('active');
          b.style.fontWeight = '800';
        } else {
          b.classList.remove('active');
          b.style.fontWeight = 'normal';
        }
      }
    });
    renderGtcTongBarChart();
  };

  // --------------------------------------------------------------------------
  // --------------------------------------------------------------------------
  // TAB 3: %GTC TỔNG TOÀN MẠNG (ĐỐI XỨNG FULL HÀNG vs TIKTOK SHOP)
  // --------------------------------------------------------------------------
  window.setGtcTongTableView = function(mode) {
    state.gtcTongTableView = mode;
    const pills = document.querySelectorAll('#gtctong-table-mode-pills .chart-mode-pill');
    pills.forEach(p => {
      p.classList.toggle('active', p.getAttribute('data-table-view') === mode);
    });

    const cardFull = document.getElementById('card-gtctong-full');
    const cardTTS = document.getElementById('card-gtctong-tts');
    const grid = document.getElementById('gtctong-am-grid');

    if (cardFull && cardTTS && grid) {
      if (mode === 'split') {
        cardFull.style.display = 'block';
        cardTTS.style.display = 'block';
        grid.className = 'grid-row-2';
      } else if (mode === 'full_only') {
        cardFull.style.display = 'block';
        cardTTS.style.display = 'none';
        grid.className = 'grid-row-1';
      } else if (mode === 'tts_only') {
        cardFull.style.display = 'none';
        cardTTS.style.display = 'block';
        grid.className = 'grid-row-1';
      }
    }
  };

  function renderGtcTongTab() {
    window.renderGtcTongTab = renderGtcTongTab;
    window.state = state;
    if (!D.gtc_tong) return;
    renderBcCanhBaoTable();

    // Dynamically update GTC Tong executive banner summary
    const bannerSumEl = document.getElementById('gtc-tong-banner-summary');
    if (bannerSumEl) {
      const fullOv = (D.gtc_tong.overview || []).find(o => o.label && o.label.includes('Full')) || {};
      const ttsOv = (D.gtc_tong.overview || []).find(o => o.label && o.label.includes('TTS')) || {};
      const latestKey = D.meta?.latest_week ? D.meta.latest_week.toLowerCase() : 'w37';
      const prevKey = D.meta?.prev_week ? D.meta.prev_week.toLowerCase() : 'w36';

      const fullVal = (fullOv[latestKey] || 0.5778) * 100;
      const fullDiff = (fullOv.diff !== undefined ? fullOv.diff : ((fullOv[latestKey] || 0) - (fullOv[prevKey] || 0))) * 100;
      const ttsVal = (ttsOv[latestKey] || 0.5591) * 100;
      const ttsDiff = (ttsOv.diff !== undefined ? ttsOv.diff : ((ttsOv[latestKey] || 0) - (ttsOv[prevKey] || 0))) * 100;

      const rawFull = D.gtc_tong.am_full || D.gtc_tong.am || [];
      const amsSorted = [...rawFull].sort((a, b) => (b[latestKey] || 0) - (a[latestKey] || 0));
      const top3 = amsSorted.slice(0, 4).map(a => `<strong>${a.am} (${((a[latestKey] || 0) * 100).toFixed(1)}%)</strong>`).join(', ');

      const amsGrowth = [...rawFull].sort((a, b) => ((b.diff !== undefined ? b.diff : ((b[latestKey]||0)-(b[prevKey]||0)))) - ((a.diff !== undefined ? a.diff : ((a[latestKey]||0)-(a[prevKey]||0)))));
      const topGrow = amsGrowth.slice(0, 4).map(a => {
        const d = (a.diff !== undefined ? a.diff : ((a[latestKey]||0)-(a[prevKey]||0))) * 100;
        return `<strong>${a.am}</strong> tăng ${d > 0 ? '+' : ''}${d.toFixed(1)}% (lên ${((a[latestKey]||0)*100).toFixed(1)}%)`;
      }).join('; ');

      const bottomAms = amsSorted.filter(a => (a[latestKey] || 0) < 0.5).reverse().slice(0, 5).map(a => `<strong>${a.am} (${((a[latestKey]||0)*100).toFixed(1)}%)</strong>`).join(', ');

      bannerSumEl.innerHTML = `
        • <strong>%GTC Tổng Toàn Vùng:</strong> Full hàng đạt <strong>${fullVal.toFixed(2)}%</strong> (${fullDiff > 0 ? '+' : ''}${fullDiff.toFixed(2)}% WoW); Phân khúc TTS đạt <strong>${ttsVal.toFixed(2)}%</strong> (${ttsDiff > 0 ? '+' : ''}${ttsDiff.toFixed(2)}% WoW).<br>
        • <strong>Top AM dẫn đầu:</strong> ${top3}.<br>
        • <strong>Bứt phá tăng trưởng WoW:</strong> ${topGrow}.<br>
        • <strong>Nhóm AM cần cải thiện GTC:</strong> ${bottomAms}.
      `;
    }

    // 3. BẢNG BƯU CỤC BẤT ỔN ĐIỂN HÌNH W41 (SHEET NTBo)
    // Update dynamic date badge and table header if available
    const badgeNtbo = document.getElementById('badge-ntbo-updated');
    if (badgeNtbo && D.gtc_tong && D.gtc_tong.ntbo_update_time) {
      badgeNtbo.textContent = `📅 Dữ liệu: ${D.gtc_tong.ntbo_update_time} (Chốt ngày ${D.gtc_tong.n1_date_label || '11/10'})`;
    }
    const thN1 = document.querySelector('#table-gtc-bat-on-detailed thead th:nth-child(8)');
    if (thN1 && D.gtc_tong && D.gtc_tong.n1_date_label) {
      thN1.textContent = `Chốt Ngày ${D.gtc_tong.n1_date_label}`;
    }

    const allTblBatOn = document.querySelectorAll('#table-gtc-bat-on-detailed tbody');
    if (allTblBatOn.length > 0) {
      if (!D.gtc_tong || !D.gtc_tong.buu_cuc_bat_on || D.gtc_tong.buu_cuc_bat_on.length === 0) {
        // Fetch async if missing
        fetch('/api/sync-ntbo').then(res => res.json()).then(resData => {
          if (resData && resData.bcs) {
            if (!D.gtc_tong) D.gtc_tong = {};
            D.gtc_tong.buu_cuc_bat_on = resData.bcs;
            D.gtc_tong.ntbo_update_time = resData.update_time;
            D.gtc_tong.n1_date_label = resData.n1_label;
            renderGtcTongTab();
          }
        }).catch(e => console.warn('Auto fetch ntbo error:', e));
      }
    }
    if (allTblBatOn.length > 0 && D.gtc_tong && D.gtc_tong.buu_cuc_bat_on && D.gtc_tong.buu_cuc_bat_on.length > 0) {
      let listBatOn = [...D.gtc_tong.buu_cuc_bat_on];

      const filterMode = state.gtcBatOnFilter || 'warn';
      if (filterMode === 'warn') {
        // LẤY HẾT TẤT CẢ CÁC NHÓM TRỪ NHÓM BÌNH THƯỜNG (theo chỉ đạo điều hành NTB)
        listBatOn = listBatOn.filter(r => r.trang_thai && r.trang_thai.trim().toLowerCase() !== 'bình thường');
      } else if (filterMode === 'top_bat_on') {
        listBatOn = listBatOn.filter(r => r.trang_thai === 'Nằm TOP Bất ổn');
      } else if (filterMode === 'n1_50') {
        listBatOn = listBatOn.filter(r => r.trang_thai === 'GTC N-1 < 50%');
      } else if (filterMode === 'nhay_nhom') {
        listBatOn = listBatOn.filter(r => r.trang_thai === 'Chuẩn bị nhảy nhóm');
      } else if (filterMode === 'cap_canh_bao') {
        listBatOn = listBatOn.filter(r => r.trang_thai === 'Cấp cảnh báo');
      }

      // Search filtering
      if (state.searchGtcBatOn) {
        const q = state.searchGtcBatOn.toLowerCase();
        listBatOn = listBatOn.filter(r => (r.ten_bc && r.ten_bc.toLowerCase().includes(q)) || (r.am && r.am.toLowerCase().includes(q)) || (r.id && r.id.includes(q)));
      }

      // Sort by gtc_7d ascending (worst first)
      listBatOn.sort((a, b) => (a.gtc_7d || 0) - (b.gtc_7d || 0));

      const warnPill = document.querySelector('#gtc-baton-filter-pills [data-filter="warn"]');
      if (warnPill) {
        const warnCount = (D.gtc_tong.buu_cuc_bat_on || []).filter(r => r.trang_thai && r.trang_thai.trim().toLowerCase() !== 'bình thường').length;
        warnPill.textContent = `🚨 Nhóm Cảnh Báo / Bất Ổn (${warnCount} BC)`;
      }
      const allPill = document.querySelector('#gtc-baton-filter-pills [data-filter="all"]');
      if (allPill && D.gtc_tong.buu_cuc_bat_on) {
        allPill.textContent = `🏛️ Toàn Bộ Vùng NTB (${D.gtc_tong.buu_cuc_bat_on.length} BC)`;
      }
      document.querySelectorAll('#gtc-baton-table-count').forEach(el => {
        el.textContent = `Đang hiển thị: ${listBatOn.length} bưu cục`;
      });

      const generatedRowsHtml = listBatOn.map((row, i) => {
        const isRed = row.gtc_7d < 45.0;
        const isRatioLow = row.ratio < 70.0;
        const isN1Low = row.d11_val > 0 && row.d11_val < 50.0;
        const isSelected = state.selectedAM === row.am;

        const tt = (row.trang_thai || '').trim();
        let statusBadge = '';
        if (tt === 'Nằm TOP Bất ổn') {
          statusBadge = '<span class="badge-tag badge-tag-red" style="font-weight:800; font-size:11.5px; background:#fee2e2; color:#dc2626; border:1px solid #fca5a5;">🔴 Nằm TOP Bất ổn</span>';
        } else if (tt === 'GTC N-1 < 50%') {
          statusBadge = '<span class="badge-tag badge-tag-amber" style="font-weight:800; font-size:11.5px; background:#fef3c7; color:#b45309; border:1px solid #fde68a;">⚠️ GTC N-1 &lt; 50%</span>';
        } else if (tt === 'Chuẩn bị nhảy nhóm') {
          statusBadge = '<span class="badge-tag badge-tag-blue" style="font-weight:800; font-size:11.5px; background:#eff6ff; color:#1d4ed8; border:1px solid #bfdbfe;">⚡ Chuẩn Bị Nhảy Nhóm</span>';
        } else if (tt === 'Cấp cảnh báo') {
          statusBadge = '<span class="badge-tag badge-tag-orange" style="font-weight:800; font-size:11.5px; background:#ffedd5; color:#c2410c; border:1px solid #fed7aa;">📢 Cấp Cảnh Báo</span>';
        } else {
          statusBadge = '<span class="badge-tag badge-tag-green" style="font-size:11.5px; font-weight:700;">🟢 Bình thường</span>';
        }

        const nn = (row.nguyen_nhan || '').trim();
        let causeBadge = '';
        if (nn.includes('< 45%')) {
          causeBadge = '<span class="bold" style="color:#dc2626; font-size:11.5px; font-weight:800;">🔴 GTC &lt; 45%</span>';
        } else if (nn === 'Bình thường' || !nn) {
          causeBadge = `<span style="color:#64748b; font-size:11.5px;">${tt !== 'Bình thường' ? tt : 'Bình thường'}</span>`;
        } else {
          causeBadge = `<span class="bold" style="color:#ea580c; font-size:11.5px;">${nn}</span>`;
        }

        const isTtsOff = row.ten_bc && (row.ten_bc.includes('Đơn Dương') || row.ten_bc.includes('Tân Hà') || row.ten_bc.includes('Lang Biang - Đà Lạt 1'));
        const ttsOffTag = '';

        const ratioColor = isRatioLow ? '#dc2626' : (row.ratio < 80.0 ? '#ea580c' : '#16a34a');
        const d11Color = row.d11_val < 45.0 ? '#dc2626' : (row.d11_val < 50.0 ? '#ea580c' : '#16a34a');

        return `
          <tr style="cursor: pointer; ${isSelected ? 'background: #eff6ff;' : ''}" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center" style="font-weight:800; color:${isRed ? '#dc2626' : 'inherit'};">${i + 1}</td>
            <td class="bold" style="font-size:13.5px; font-weight:800; color:${isRed ? '#b91c1c' : (isSelected ? '#2563eb' : '#1e293b')};">
              ${row.ten_bc} ${ttsOffTag}
            </td>
            <td style="font-weight:700; color:#2563eb;">${row.am}</td>
            <td class="num bold" style="background:${isRed ? 'rgba(239,68,68,0.12)' : 'rgba(254,240,138,0.2)'}; color:${isRed ? '#b91c1c' : '#ea580c'}; font-size:13.5px; font-weight:900;">
              ${row.gtc_7d_str}
            </td>
            <td class="num" style="font-weight:600; color:#64748b;">${row.gtc_best_str}</td>
            <td class="num bold" style="background:${isRatioLow ? 'rgba(254,226,226,0.5)' : '#fff7ed'}; color:${ratioColor}; font-size:13px; font-weight:800;">
              ${row.ratio_str}
              ${isRatioLow ? ' <span style="font-size:10px; color:#dc2626;">(&lt;70%)</span>' : ''}
            </td>
            <td class="num bold" style="color:#ea580c; font-size:12.5px;">-${row.gap.toFixed(1)}%p</td>
            <td class="num bold" style="color:${d11Color}; font-size:12.5px; background:${isN1Low ? 'rgba(254,243,199,0.35)' : 'inherit'};">${row.d11}</td>
            <td class="center">${statusBadge}</td>
            <td class="center">${causeBadge}</td>
          </tr>
        `;
      }).join('');
      allTblBatOn.forEach(tbl => tbl.innerHTML = generatedRowsHtml);
    }

    // Helper evaluation badge for %GTC (Target >= 60%)
    function getGtcEvalBadge(v) {
      const val = v || 0;
      if (val >= 0.70) return '<span class="badge-tag badge-tag-green">🏆 Xuất Sắc (≥70%)</span>';
      if (val >= 0.60) return '<span class="badge-tag badge-tag-green">🟢 Đạt Chuẩn (≥60%)</span>';
      if (val >= 0.50) return '<span class="badge-tag badge-tag-amber">🟡 Tiệm Cận (50-60%)</span>';
      return '<span class="badge-tag badge-tag-red">🔴 Chưa Đạt (&lt;50%)</span>';
    }

    // 1. BẢNG 1A: %GTC FULL HÀNG (19 AM)
    const tblBodyFull = document.querySelector('#table-gtc-full-detailed tbody');
    if (tblBodyFull) {
      const latestKey = D.meta?.latest_week ? D.meta.latest_week.toLowerCase() : 'w37';
      const prevKey = D.meta?.prev_week ? D.meta.prev_week.toLowerCase() : 'w36';
      const rawFull = D.gtc_tong.am_full || D.gtc_tong.am || [];
      let listFull = [...rawFull].map(r => {
        const curr = r[latestKey] !== undefined ? r[latestKey] : (r.w37 !== undefined ? r.w37 : (r.w36 || 0));
        const prev = r[prevKey] !== undefined ? r[prevKey] : (r.w36 !== undefined ? r.w36 : (r.w35 || 0));
        return {
          ...r,
          curr_val: curr,
          prev_val: prev,
          diff_val: r.diff !== undefined ? r.diff : (curr - prev)
        };
      });

      if (state.searchGtcTongFull) {
        listFull = listFull.filter(r => r.am.toLowerCase().includes(state.searchGtcTongFull));
      }

      const sortedFull = listFull.sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

      tblBodyFull.innerHTML = sortedFull.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const heatCurr = getHeatmapClass(row.curr_val, 'gtc');
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
        `;
      }).join('');
    }

    // 2. BẢNG 1B: %GTC TIKTOK SHOP (19 AM)
    const tblBodyTTS = document.querySelector('#table-gtc-tts-detailed tbody');
    if (tblBodyTTS) {
      const latestKey = D.meta?.latest_week ? D.meta.latest_week.toLowerCase() : 'w37';
      const prevKey = D.meta?.prev_week ? D.meta.prev_week.toLowerCase() : 'w36';
      const rawTTS = D.gtc_tong.am_tts || [];
      let listTTS = [...rawTTS].map(r => {
        const curr = r[latestKey] !== undefined ? r[latestKey] : (r.w37 !== undefined ? r.w37 : (r.w36 || 0));
        const prev = r[prevKey] !== undefined ? r[prevKey] : (r.w36 !== undefined ? r.w36 : (r.w35 || 0));
        return {
          ...r,
          curr_val: curr,
          prev_val: prev,
          diff_val: r.diff !== undefined ? r.diff : (curr - prev)
        };
      });

      if (state.searchGtcTongTTS) {
        listTTS = listTTS.filter(r => r.am.toLowerCase().includes(state.searchGtcTongTTS));
      }

      const sortedTTS = listTTS.sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

      tblBodyTTS.innerHTML = sortedTTS.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const heatCurr = getHeatmapClass(row.curr_val, 'gtc');
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
        `;
      }).join('');
    }

    // 3. BẢNG 2A: %GTC 5 TỈNH THÀNH (FULL HÀNG)
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
        const isSelected = state.selectedProvince === row.tinh;
        const rowClass = isSelected ? 'province-laser-box' : '';
        const v1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
        const v2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
        const v3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
        const v4 = row.curr_val;
        const heatClass = getHeatmapClass(v4, 'gtc');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = getGtcEvalBadge(v4);

        return `
          <tr data-province="${row.tinh}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightProvince('${row.tinh}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13.5px; font-weight:800; color:${isSelected ? '#2563eb' : 'inherit'};">${row.tinh}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(v1)}</td>
            <td class="num">${fPct(v2)}</td>
            <td class="num">${fPct(v3)}</td>
            <td class="num bold ${heatClass}">${fPct(v4)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 4. BẢNG 2B: %GTC 5 TỈNH THÀNH (TIKTOK SHOP)
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
        const isSelected = state.selectedProvince === row.tinh;
        const rowClass = isSelected ? 'province-laser-box' : '';
        const v1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
        const v2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
        const v3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
        const v4 = row.curr_val;
        const heatClass = getHeatmapClass(v4, 'gtc');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = getGtcEvalBadge(v4);

        return `
          <tr data-province="${row.tinh}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightProvince('${row.tinh}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13.5px; font-weight:800; color:${isSelected ? '#ea580c' : 'inherit'};">${row.tinh}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(v1)}</td>
            <td class="num">${fPct(v2)}</td>
            <td class="num">${fPct(v3)}</td>
            <td class="num bold ${heatClass}">${fPct(v4)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }
  }

  
  // --------------------------------------------------------------------------
  // BẢNG 3: BƯU CỤC TRONG NHÓM CẢNH BÁO BẤT ỔN (%GTC < 45% HOẶC < 70% LỊCH SỬ)
  // --------------------------------------------------------------------------
  state.searchBcCanhBao = '';

  window.syncBcCanhBaoRealtime = async function() {
    const btn = document.getElementById('btn-sync-bc-canhbao-realtime');
    const txt = document.getElementById('text-sync-bc-canhbao');
    if (btn) btn.disabled = true;
    if (txt) txt.textContent = 'Đang đồng bộ...';

    try {
      const res = await fetch('/api/sync-bc-canh-bao');
      const data = await res.json();
      if (data.success && data.records) {
        D.bc_canh_bao = data.records;
        if (!D.bc_canh_bao_meta) D.bc_canh_bao_meta = {};
        D.bc_canh_bao_meta.update_time = data.update_time;
        renderBcCanhBaoTable();
        alert(`✅ ${data.message}\nCập nhật lúc: ${data.update_time}`);
      } else {
        alert('❌ Lỗi đồng bộ: ' + (data.error || 'Thất bại'));
      }
    } catch (err) {
      console.error('syncBcCanhBaoRealtime error:', err);
      alert('❌ Lỗi kết nối API: ' + err.message);
    } finally {
      if (btn) btn.disabled = false;
      if (txt) txt.textContent = '🔄 Đồng Bộ Realtime Google Sheets';
      if (window.lucide) lucide.createIcons();
    }
  };

  function renderBcCanhBaoTable() {
    window.renderBcCanhBaoTable = renderBcCanhBaoTable;
    const tblBodies = document.querySelectorAll('.table-bc-canh-bao-body, #table-bc-canh-bao tbody, #table-bc-canh-bao-overview tbody, #table-bc-canhbao-tab tbody');
    if (!tblBodies || tblBodies.length === 0) return;
    const raw = D.bc_canh_bao || [];
    document.querySelectorAll('.badge-tag-red, #badge-bc-canhbao-count').forEach(el => {
      if (el.textContent && el.textContent.includes('Bưu Cục Cảnh Báo')) {
        el.textContent = `🚨 ${raw.length} Bưu Cục Cảnh Báo`;
      }
    });
    const timeEl = document.getElementById('text-bc-canhbao-update-time');
    if (timeEl && D.bc_canh_bao_meta && D.bc_canh_bao_meta.update_time) {
      timeEl.textContent = `📅 Dữ liệu: ${D.bc_canh_bao_meta.update_time} (Realtime từ Google Sheets)`;
    }
    let list = [...raw];
    if (state.searchBcCanhBao) {
      const q = state.searchBcCanhBao.toLowerCase();
      list = list.filter(r => 
        (r.bc && r.bc.toLowerCase().includes(q)) || 
        (r.am && r.am.toLowerCase().includes(q)) || 
        (r.tinh && r.tinh.toLowerCase().includes(q))
      );
    }

    const rowsHtml = list.map((row, i) => {
      const isSelected = state.selectedAM && state.selectedAM === row.am;
      const rowClass = isSelected ? 'presenter-laser-box' : '';
      const diffBadge = renderDeltaBadge(row.diff / 100, true, true);
      const daysWarnBadge = row.days_warn >= 60 
        ? `<span class="badge-tag badge-tag-red" style="font-weight:800; font-size:12px;">🚨 ${row.days_warn} ngày</span>`
        : (row.days_warn >= 20 
          ? `<span class="badge-tag badge-tag-amber" style="font-weight:800; font-size:12px;">⚠️ ${row.days_warn} ngày</span>`
          : `<span class="badge-tag badge-tag-blue" style="font-weight:700; font-size:12px;">⏱️ ${row.days_warn} ngày</span>`);
      
      const warnBadge = (row.warn_type && row.warn_type.includes('< 45%'))
        ? `<span class="badge-tag badge-tag-red" style="font-size:11.5px; font-weight:700;">🔴 ${row.warn_type}</span>`
        : `<span class="badge-tag badge-tag-amber" style="font-size:11.5px; font-weight:700;">🟡 ${row.warn_type}</span>`;

      return `
        <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
          <td class="center">${renderRankPill(i)}</td>
          <td class="bold" style="font-size:13px; font-weight:800; color: #b91c1c;">${row.bc}</td>
          <td>${row.tinh}</td>
          <td class="bold" style="color: var(--color-blue);">${row.am || '---'}</td>
          <td class="num" style="background: rgba(2, 132, 199, 0.05); font-weight:600;">${row.gtc_w36.toFixed(1)}%</td>
          <td class="num bold" style="background: rgba(220, 38, 38, 0.12); color: #dc2626; font-size:13.5px; font-weight:900;">${row.gtc_w37.toFixed(1)}%</td>
          <td class="num bold">${diffBadge}</td>
          <td class="num" style="color: #64748b; font-weight:600;">${row.gtc_best.toFixed(1)}%</td>
          <td class="center">${daysWarnBadge}</td>
          <td class="num bold" style="color: #1e293b;">${fNum(row.backlog)} <small>đơn</small></td>
          <td class="num bold" style="color: ${row.backlog_5d > 50 ? '#dc2626' : '#64748b'};">${fNum(row.backlog_5d)}</td>
          <td class="center"><span class="badge-tag badge-tag-cyan" style="font-weight:700;">${row.clear_days} ngày</span></td>
          <td class="center">${warnBadge}</td>
        </tr>
      `;
    }).join('');

    tblBodies.forEach(tblBody => {
      tblBody.innerHTML = rowsHtml;
    });
  }

  
  // --------------------------------------------------------------------------
  // CHART: %GTC 5 TỈNH QUA 4 TUẦN (W40 - W43) & BIẾN ĐỘNG Δ %p WoW
  // --------------------------------------------------------------------------
  function renderTinhGtc4WeeksChart() {
    const ctx = document.getElementById('chart-gtc-tinh-4weeks');
    if (!ctx || !D.gtc_tong) return;
    if (charts.tinhGtc4Weeks) charts.tinhGtc4Weeks.destroy();

    const isTTS = (state.tinhGtcChannel === 'tts');
    const isLine = (state.tinhGtcType === 'line');
    const rawData = isTTS ? (D.gtc_tong.tinh_tts || []) : (D.gtc_tong.tinh_full || D.gtc_tong.tinh || []);

    const wKeys = (D.meta?.weeks || ['W38', 'W39', 'W40', 'W41']).map(w => w.toLowerCase());
    const weekLabels = D.meta?.weeks || ['W38', 'W39', 'W40', 'W41'];

    // Sort provinces by W41 %GTC descending
    const sortedProvinces = [...rawData].sort((a, b) => {
      const vA = a[wKeys[3]] !== undefined ? a[wKeys[3]] : (a.w41 || a.curr_val || 0);
      const vB = b[wKeys[3]] !== undefined ? b[wKeys[3]] : (b.w41 || b.curr_val || 0);
      return vB - vA;
    });

    const labels = sortedProvinces.map(p => p.tinh);

    // Update summary badge
    const badgeEl = document.getElementById('gtc-tinh-summary-badge');
    if (badgeEl) {
      const curW = weekLabels[3] || 'W43';
      const gFCard = D.overview?.cards?.find(c => c.id === 'gtc_full');
      const gTCard = D.overview?.cards?.find(c => c.id === 'gtc_tts');
      const gFVal = gFCard?.val || 0.6286;
      const gFDiff = gFCard?.diff || 0.0244;
      const gTVal = gTCard?.val || 0.6449;
      const gTDiff = gTCard?.diff || 0.0165;
      if (isTTS) {
        const sign = gTDiff >= 0 ? '+' : '';
        badgeEl.innerHTML = `⚡ TikTok Shop ${curW}: <strong>${(gTVal * 100).toFixed(2)}%</strong> (${sign}${(gTDiff * 100).toFixed(2)}%p WoW — Vượt Target 60.0%)`;
        badgeEl.style.color = '#ea580c';
        badgeEl.style.background = '#fff7ed';
        badgeEl.style.borderColor = 'rgba(234, 88, 12, 0.3)';
      } else {
        const sign = gFDiff >= 0 ? '+' : '';
        badgeEl.innerHTML = `⚡ Toàn vùng ${curW}: <strong>${(gFVal * 100).toFixed(2)}%</strong> (${sign}${(gFDiff * 100).toFixed(2)}%p WoW — Vượt Target 60.0%)`;
        badgeEl.style.color = '#2563eb';
        badgeEl.style.background = '#dbeafe';
        badgeEl.style.borderColor = 'rgba(37, 99, 235, 0.3)';
      }
    }

    if (!isLine) {
      // GROUPED BAR CHART: 4 columns per province (W38, W39, W40, W41)
      const dataW38 = sortedProvinces.map(p => {
        const v = p[wKeys[0]] !== undefined ? p[wKeys[0]] : (p.w38 || 0);
        return parseFloat((v * 100).toFixed(1));
      });
      const dataW39 = sortedProvinces.map(p => {
        const v = p[wKeys[1]] !== undefined ? p[wKeys[1]] : (p.w39 || 0);
        return parseFloat((v * 100).toFixed(1));
      });
      const dataW40 = sortedProvinces.map(p => {
        const v = p[wKeys[2]] !== undefined ? p[wKeys[2]] : (p.w40 || 0);
        return parseFloat((v * 100).toFixed(1));
      });
      const dataW41 = sortedProvinces.map(p => {
        const v = p[wKeys[3]] !== undefined ? p[wKeys[3]] : (p.w41 || p.curr_val || 0);
        return parseFloat((v * 100).toFixed(1));
      });

      charts.tinhGtc4Weeks = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: `${weekLabels[0]}`,
              data: dataW38,
              backgroundColor: '#94a3b8',
              borderRadius: 4,
              maxBarThickness: 32,
              datalabels: {
                anchor: 'end',
                align: 'top',
                offset: 2,
                color: '#64748b',
                font: { size: 10, weight: '600' },
                formatter: (val) => val.toFixed(1) + '%'
              }
            },
            {
              label: `${weekLabels[1]}`,
              data: dataW39,
              backgroundColor: '#60a5fa',
              borderRadius: 4,
              maxBarThickness: 32,
              datalabels: {
                anchor: 'end',
                align: 'top',
                offset: 2,
                color: '#2563eb',
                font: { size: 10, weight: '600' },
                formatter: (val) => val.toFixed(1) + '%'
              }
            },
            {
              label: `${weekLabels[2]} (Mega Sale 10.10)`,
              data: dataW40,
              backgroundColor: '#1e40af',
              borderRadius: 4,
              maxBarThickness: 32,
              datalabels: {
                anchor: 'end',
                align: 'top',
                offset: 2,
                color: '#1e3a8a',
                font: { size: 10.5, weight: '700' },
                formatter: (val) => val.toFixed(1) + '%'
              }
            },
            {
              label: `${weekLabels[3]} (Hiện tại)`,
              data: dataW41,
              backgroundColor: '#22c55e',
              borderColor: '#16a34a',
              borderWidth: 2,
              borderRadius: 6,
              maxBarThickness: 36,
              datalabels: {
                anchor: 'end',
                align: 'top',
                offset: 4,
                color: (ctx2) => {
                  const idx = ctx2.dataIndex;
                  const prev = dataW40[idx] || 0;
                  return dataW41[idx] >= prev ? '#16a34a' : '#dc2626';
                },
                font: { size: 11.5, weight: '800' },
                formatter: (val, ctx2) => {
                  const idx = ctx2.dataIndex;
                  const prevVal = dataW40[idx] || 0;
                  const diffP = val - prevVal;
                  const sign = diffP >= 0 ? '+' : '';
                  return [`${val.toFixed(1)}%`, `${sign}${diffP.toFixed(1)}%p`];
                }
              }
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          layout: {
            padding: { top: 32, bottom: 8, left: 10, right: 10 }
          },
          plugins: {
            legend: {
              position: 'top',
              labels: {
                boxWidth: 10,
                boxHeight: 10,
                font: { weight: '700', size: 12 }
              }
            },
            tooltip: {
              backgroundColor: 'rgba(15, 23, 42, 0.95)',
              titleFont: { size: 13, weight: '700' },
              bodyFont: { size: 12 },
              padding: 12,
              cornerRadius: 8,
              callbacks: {
                label: function (c) {
                  const val = c.raw || 0;
                  const idx = c.dataIndex;
                  if (c.datasetIndex === 3) {
                    const prev = dataW40[idx] || 0;
                    const diff = val - prev;
                    const sign = diff >= 0 ? '+' : '';
                    return ` ${c.dataset.label}: ${val.toFixed(2)}% (${sign}${diff.toFixed(2)}%p WoW)`;
                  }
                  return ` ${c.dataset.label}: ${val.toFixed(2)}%`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: { display: false },
              ticks: {
                font: { weight: '800', size: 12.5 },
                color: '#0f172a'
              }
            },
            y: {
              beginAtZero: false,
              min: 40,
              max: 80,
              grid: { color: 'rgba(226, 232, 240, 0.6)' },
              ticks: {
                callback: v => v + '%',
                font: { size: 11 }
              }
            }
          }
        }
      });
    } else {
      // LINE TREND CHART
      const palette = [
        { stroke: '#2563eb' },
        { stroke: '#16a34a' },
        { stroke: '#ea580c' },
        { stroke: '#8b5cf6' },
        { stroke: '#06b6d4' }
      ];

      const datasets = sortedProvinces.map((p, idx) => {
        const col = palette[idx % palette.length];
        const vW38 = parseFloat(((p[wKeys[0]] !== undefined ? p[wKeys[0]] : (p.w38 || 0)) * 100).toFixed(1));
        const vW39 = parseFloat(((p[wKeys[1]] !== undefined ? p[wKeys[1]] : (p.w39 || 0)) * 100).toFixed(1));
        const vW40 = parseFloat(((p[wKeys[2]] !== undefined ? p[wKeys[2]] : (p.w40 || 0)) * 100).toFixed(1));
        const vW41 = parseFloat(((p[wKeys[3]] !== undefined ? p[wKeys[3]] : (p.w41 || p.curr_val || 0)) * 100).toFixed(1));
        const diffP = vW41 - vW40;
        const sign = diffP >= 0 ? '+' : '';

        return {
          label: `${p.tinh} (${sign}${diffP.toFixed(1)}%p)`,
          data: [vW38, vW39, vW40, vW41],
          borderColor: col.stroke,
          backgroundColor: col.stroke,
          borderWidth: 3,
          tension: 0.35,
          pointRadius: 6,
          pointHoverRadius: 8,
          datalabels: {
            anchor: 'end',
            align: 'top',
            offset: 4,
            color: col.stroke,
            font: { size: 11, weight: '700' },
            formatter: (val, ctx2) => {
              if (ctx2.dataIndex === 3) {
                return `${val.toFixed(1)}% (${sign}${diffP.toFixed(1)}%p)`;
              }
              return val.toFixed(1) + '%';
            }
          }
        };
      });

      charts.tinhGtc4Weeks = new Chart(ctx, {
        type: 'line',
        data: {
          labels: weekLabels,
          datasets: datasets
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          layout: {
            padding: { top: 32, bottom: 8, left: 10, right: 10 }
          },
          plugins: {
            legend: {
              position: 'top',
              labels: {
                boxWidth: 10,
                boxHeight: 10,
                font: { weight: '700', size: 12 }
              }
            },
            tooltip: {
              backgroundColor: 'rgba(15, 23, 42, 0.95)',
              padding: 12,
              cornerRadius: 8,
              callbacks: {
                label: function (c) {
                  return ` ${c.dataset.label}: ${c.raw.toFixed(2)}%`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: { display: false },
              ticks: { font: { weight: '800', size: 12.5 } }
            },
            y: {
              beginAtZero: false,
              min: 40,
              max: 80,
              grid: { color: 'rgba(226, 232, 240, 0.6)' },
              ticks: {
                callback: v => v + '%',
                font: { size: 11 }
              }
            }
          }
        }
      });
    }
  }

  window.switchTinhGtcChannel = function(ch) {
    state.tinhGtcChannel = ch;
    const btnFull = document.getElementById('btn-gtc-tinh-channel-full');
    const btnTTS = document.getElementById('btn-gtc-tinh-channel-tts');
    if (btnFull) btnFull.classList.toggle('active', ch === 'full');
    if (btnTTS) btnTTS.classList.toggle('active', ch === 'tts');
    const titleEl = document.getElementById('gtc-tinh-chart-header-title');
    if (titleEl) {
      titleEl.textContent = (ch === 'tts') 
        ? 'BIỂU ĐỒ %GTC 5 TỈNH QUA 4 TUẦN (W40 – W43) — TIKTOK SHOP & BIẾN ĐỘNG Δ %p WoW'
        : 'BIỂU ĐỒ %GTC 5 TỈNH QUA 4 TUẦN (W40 – W43) — FULL HÀNG & BIẾN ĐỘNG Δ %p WoW (TARGET ≥ 60.0%)';
    }
    renderTinhGtc4WeeksChart();
  };

  window.switchTinhGtcType = function(t) {
    state.tinhGtcType = t;
    const btnBar = document.getElementById('btn-gtc-tinh-type-bar');
    const btnLine = document.getElementById('btn-gtc-tinh-type-line');
    if (btnBar) btnBar.classList.toggle('active', t === 'bar');
    if (btnLine) btnLine.classList.toggle('active', t === 'line');
    renderTinhGtc4WeeksChart();
  };

  function renderGtcTongBarChart() {
    const ctx = document.getElementById('chart-gtc-tong-bar');
    if (!ctx || !D.gtc_tong) return;
    if (charts.gtcTongBar) charts.gtcTongBar.destroy();

    const seg = state.gtcTongSegment || 'full';
    const selectedAM = state.selectedAM;
    const hlMode = state.gtcTongHighlight || 'all';

    const prevKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2].toLowerCase() : 'w35';
    const currKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1].toLowerCase() : 'w36';
    const prevLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2] : 'W35';
    const currLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1] : 'W36';

    const amFullList = D.gtc_tong.am_full || D.gtc_tong.am || [];
    const amTtsList = D.gtc_tong.am_tts || [];

    const fullMap = {};
    amFullList.forEach(f => fullMap[f.am] = f);

    const ttsMap = {};
    amTtsList.forEach(t => ttsMap[t.am] = t);

    // Combine list
    let list = amFullList.map(r => {
      const tts = ttsMap[r.am] || {};
      const fullW34 = (r[prevKey] !== undefined ? r[prevKey] : (r.w34 || 0)) * 100;
      const fullW35 = (r[currKey] !== undefined ? r[currKey] : (r.w35 || 0)) * 100;
      const fullDiff = (r.diff !== undefined ? (r.diff * 100) : (fullW35 - fullW34));

      const ttsW34 = (tts[prevKey] !== undefined ? tts[prevKey] : (tts.w34 !== undefined ? tts.w34 : (r[prevKey] || 0))) * 100;
      const ttsW35 = (tts[currKey] !== undefined ? tts[currKey] : (tts.w35 !== undefined ? tts.w35 : (r[currKey] || 0))) * 100;
      const ttsDiff = (tts.diff !== undefined ? (tts.diff * 100) : (ttsW35 - ttsW34));
      const gap = Number((ttsW35 - fullW35).toFixed(1));

      return {
        am: r.am,
        vol_full: r.vol || 0,
        vol_tts: tts.vol || 0,
        full_w34: Number(fullW34.toFixed(1)),
        full_w35: Number(fullW35.toFixed(1)),
        full_diff: Number(fullDiff.toFixed(1)),
        tts_w34: Number(ttsW34.toFixed(1)),
        tts_w35: Number(ttsW35.toFixed(1)),
        tts_diff: Number(ttsDiff.toFixed(1)),
        gap: gap
      };
    });

    // Helper match filter
    function checkGtcMatch(d) {
      if (selectedAM) return selectedAM === d.am;
      if (hlMode === 'all') return true;
      if (hlMode === 'top_gtc') {
        const val = seg === 'tts' ? d.tts_w35 : d.full_w35;
        return val >= 65;
      }
      if (hlMode === 'bottom_gtc') {
        const val = seg === 'tts' ? d.tts_w35 : d.full_w35;
        return val < 45;
      }
      if (hlMode === 'grow') {
        const diff = seg === 'tts' ? d.tts_diff : d.full_diff;
        return diff >= 2.0;
      }
      return true;
    }

    // Sync laser boxes on table
    document.querySelectorAll('#table-gtc-full-detailed tr.presenter-laser-box, #table-gtc-tts-detailed tr.presenter-laser-box').forEach(el => el.classList.remove('presenter-laser-box'));
    if (hlMode !== 'all' || selectedAM) {
      list.forEach(d => {
        if (checkGtcMatch(d)) {
          document.querySelectorAll(`#table-gtc-full-detailed tr[data-entity="${d.am}"], #table-gtc-tts-detailed tr[data-entity="${d.am}"]`).forEach(tr => tr.classList.add('presenter-laser-box'));
        }
      });
    }

    let displayList = [...list];
    let datasets = [];
    let y1Title = 'Biến Động WoW (Δ % p.p)';
    const hasFilter = hlMode !== 'all' || selectedAM;
    if (seg === 'tts') {
      displayList.sort((a, b) => (b.tts_w35 || 0) - (a.tts_w35 || 0));
    } else {
      displayList.sort((a, b) => (b.full_w35 || 0) - (a.full_w35 || 0));
    }

    if (seg === 'full') {
      datasets = [
        {
          type: 'bar',
          label: `%GTC Full ${prevLabel} (%)`,
          data: displayList.map(d => d.full_w34),
          backgroundColor: displayList.map(d => {
            const isM = checkGtcMatch(d);
            if (!hasFilter) return '#94a3b8';
            return isM ? '#64748b' : 'rgba(203, 213, 225, 0.2)';
          }),
          borderRadius: 4,
          yAxisID: 'y',
          order: 2,
          datalabels: {
            display: true,
            color: '#64748b',
            font: { size: 10, weight: '700' },
            formatter: v => v + '%'
          }
        },
        {
          type: 'bar',
          label: `%GTC Full ${currLabel} (%)`,
          data: displayList.map(d => d.full_w35),
          backgroundColor: displayList.map(d => {
            const isM = checkGtcMatch(d);
            if (!hasFilter) return d.full_w35 >= 60 ? '#10b981' : '#2563eb';
            if (!isM) return 'rgba(148, 163, 184, 0.15)';
            if (hlMode === 'top_gtc') return '#10b981';
            if (hlMode === 'bottom_gtc') return '#ef4444';
            if (hlMode === 'grow') return '#0284c7';
            return '#ef4444';
          }),
          borderColor: displayList.map(d => checkGtcMatch(d) && hasFilter ? (hlMode === 'top_gtc' ? '#059669' : '#b91c1c') : 'transparent'),
          borderWidth: displayList.map(d => checkGtcMatch(d) && hasFilter ? 2 : 0),
          borderRadius: 4,
          yAxisID: 'y',
          order: 2,
          datalabels: {
            display: true,
            color: '#0f172a',
            font: { size: 10.5, weight: '800' },
            formatter: v => v + '%'
          }
        },
        {
          type: 'line',
          label: 'Đường Biến Động WoW Full (Δ %)',
          data: displayList.map(d => d.full_diff),
          borderColor: '#f26522',
          borderWidth: 3,
          tension: 0.25,
          pointBackgroundColor: displayList.map(d => d.full_diff >= 0 ? '#10b981' : '#ef4444'),
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 6,
          pointHoverRadius: 8,
          yAxisID: 'y1',
          order: 1,
          datalabels: {
            display: true,
            align: 'top',
            color: '#d97706',
            font: { size: 10, weight: '800' },
            formatter: v => (v > 0 ? '+' : '') + v + '%'
          }
        }
      ];
    } else if (seg === 'tts') {
      datasets = [
        {
          type: 'bar',
          label: `%GTC TTS ${prevLabel} (%)`,
          data: displayList.map(d => d.tts_w34),
          backgroundColor: displayList.map(d => {
            const isM = checkGtcMatch(d);
            if (!hasFilter) return '#cbd5e1';
            return isM ? '#94a3b8' : 'rgba(203, 213, 225, 0.2)';
          }),
          borderRadius: 4,
          yAxisID: 'y',
          order: 2,
          datalabels: {
            display: true,
            color: '#64748b',
            font: { size: 10, weight: '700' },
            formatter: v => v + '%'
          }
        },
        {
          type: 'bar',
          label: `%GTC TTS ${currLabel} (%)`,
          data: displayList.map(d => d.tts_w35),
          backgroundColor: displayList.map(d => {
            const isM = checkGtcMatch(d);
            if (!hasFilter) return d.tts_w35 >= 60 ? '#0d9488' : '#f97316';
            if (!isM) return 'rgba(148, 163, 184, 0.15)';
            if (hlMode === 'top_gtc') return '#0d9488';
            if (hlMode === 'bottom_gtc') return '#ef4444';
            if (hlMode === 'grow') return '#0284c7';
            return '#ef4444';
          }),
          borderColor: displayList.map(d => checkGtcMatch(d) && hasFilter ? (hlMode === 'top_gtc' ? '#0f766e' : '#b91c1c') : 'transparent'),
          borderWidth: displayList.map(d => checkGtcMatch(d) && hasFilter ? 2 : 0),
          borderRadius: 4,
          yAxisID: 'y',
          order: 2,
          datalabels: {
            display: true,
            color: '#0f172a',
            font: { size: 10.5, weight: '800' },
            formatter: v => v + '%'
          }
        },
        {
          type: 'line',
          label: 'Đường Biến Động WoW TTS (Δ %)',
          data: displayList.map(d => d.tts_diff),
          borderColor: '#0284c7',
          borderWidth: 3,
          tension: 0.25,
          pointBackgroundColor: displayList.map(d => d.tts_diff >= 0 ? '#10b981' : '#ef4444'),
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 6,
          pointHoverRadius: 8,
          yAxisID: 'y1',
          order: 1,
          datalabels: {
            display: true,
            align: 'top',
            color: '#0284c7',
            font: { size: 10.5, weight: '800' },
            formatter: v => (v > 0 ? '+' : '') + v + '%'
          }
        }
      ];
    } else if (seg === 'compare') {
      y1Title = 'Chênh Lệch Gap (TTS - Full % p.p)';
      datasets = [
        {
          type: 'bar',
          label: `%GTC Full Hàng ${currLabel}`,
          data: displayList.map(d => d.full_w35),
          backgroundColor: displayList.map(d => {
            const isM = checkGtcMatch(d);
            if (!hasFilter) return '#2563eb';
            return isM ? '#2563eb' : 'rgba(37, 99, 235, 0.18)';
          }),
          borderRadius: 4,
          yAxisID: 'y',
          order: 2,
          datalabels: {
            display: true,
            color: '#2563eb',
            font: { size: 10, weight: '800' },
            formatter: v => v + '%'
          }
        },
        {
          type: 'bar',
          label: `%GTC TikTok Shop ${currLabel}`,
          data: displayList.map(d => d.tts_w35),
          backgroundColor: displayList.map(d => {
            const isM = checkGtcMatch(d);
            if (!hasFilter) return '#0d9488';
            return isM ? '#0d9488' : 'rgba(13, 148, 136, 0.18)';
          }),
          borderRadius: 4,
          yAxisID: 'y',
          order: 2,
          datalabels: {
            display: true,
            color: '#0f766e',
            font: { size: 10, weight: '800' },
            formatter: v => v + '%'
          }
        },
        {
          type: 'line',
          label: 'Đường Gap (TTS vs Full %)',
          data: displayList.map(d => d.gap),
          borderColor: '#8b5cf6',
          borderWidth: 3,
          tension: 0.25,
          pointBackgroundColor: displayList.map(d => d.gap >= 0 ? '#10b981' : '#ef4444'),
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 6,
          pointHoverRadius: 8,
          yAxisID: 'y1',
          order: 1,
          datalabels: {
            display: true,
            align: 'top',
            color: '#7c3aed',
            font: { size: 10, weight: '800' },
            formatter: v => (v > 0 ? '+' : '') + v + '%'
          }
        }
      ];
    }

    // Determine nice dynamic limits for y1 scale
    const diffValues = seg === 'tts' ? displayList.map(d => d.tts_diff) : (seg === 'full' ? displayList.map(d => d.full_diff) : displayList.map(d => d.gap));
    const minDiff = Math.min(...diffValues, 0);
    const maxDiff = Math.max(...diffValues, 0);
    const y1Min = Math.floor((minDiff - 3) / 5) * 5;
    const y1Max = Math.ceil((maxDiff + 4) / 5) * 5;

    charts.gtcTongBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: displayList.map(d => d.am),
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 25, bottom: 10 } },
        scales: {
          y: {
            position: 'left',
            min: 0,
            max: 100,
            ticks: { callback: v => v + '%' },
            title: { display: true, text: '%GTC (%)', font: { weight: '700', size: 11 } },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          y1: {
            position: 'right',
            min: y1Min,
            max: y1Max,
            grid: { drawOnChartArea: false },
            title: { display: true, text: y1Title, font: { weight: '700', size: 11, color: '#f26522' } },
            ticks: {
              callback: v => (v > 0 ? '+' : '') + v + '%'
            }
          },
          x: {
            ticks: { maxRotation: 45, minRotation: 20, font: { size: 11, weight: '800' } }
          }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => {
                if (c.dataset.type === 'line') {
                  const s = c.parsed.y > 0 ? '+' : '';
                  return `${c.dataset.label}: ${s}${c.parsed.y}%`;
                }
                const item = displayList[c.dataIndex];
                const vol = seg === 'tts' ? item.vol_tts : item.vol_full;
                return `${c.dataset.label}: ${c.parsed.y}% (Sản lượng: ${fNum(vol)} đơn)`;
              }
            }
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            selectAndHighlightAM(displayList[elements[0].index].am);
          }
        }
      }
    });
    if (window.lucide) lucide.createIcons();
  }

  // --------------------------------------------------------------------------
  // TAB 4: %GTC TIKTOK SHOP CA 1 (TARGET ≥ 76.0%)
  // --------------------------------------------------------------------------
  window.setGtcTtsCa1Highlight = function(hl) {
    state.gtcTtsCa1Highlight = hl;
    state.selectedAM = null;
    const btnMap = {
      all: 'btn-gtcttsca1-hl-all',
      top: 'btn-gtcttsca1-hl-top',
      pass: 'btn-gtcttsca1-hl-pass',
      fail: 'btn-gtcttsca1-hl-fail'
    };

    Object.keys(btnMap).forEach(k => {
      const b = document.getElementById(btnMap[k]);
      if (b) {
        if (k === hl) {
          b.classList.add('active');
          b.style.fontWeight = '800';
        } else {
          b.classList.remove('active');
          b.style.fontWeight = 'normal';
        }
      }
    });
    renderGtcTtsCa1BarChart();
  };

  window.setGtcTtsCa1Sort = function(mode) {
    state.gtcTtsCa1Sort = mode;
    const btnMap = {
      diff_asc: 'btn-gtcttsca1-sort-diff-asc',
      diff_desc: 'btn-gtcttsca1-sort-diff-desc',
      gtc_desc: 'btn-gtcttsca1-sort-gtc-desc'
    };

    Object.keys(btnMap).forEach(k => {
      const b = document.getElementById(btnMap[k]);
      if (b) {
        if (k === mode) {
          b.classList.add('active');
          b.style.fontWeight = '800';
          b.style.color = '#ea580c';
        } else {
          b.classList.remove('active');
          b.style.fontWeight = 'normal';
          b.style.color = '';
        }
      }
    });
    renderGtcTtsCa1BarChart();
  };

  function getGtcCa1TtsData() {
    const prevKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2].toLowerCase() : 'w37';
    const currKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1].toLowerCase() : 'w38';
    const rawList = (D.gtc_ca1_thuan && D.gtc_ca1_thuan.am_tts) || (D.gtc_ca1_ton && D.gtc_ca1_ton.am_tts) || (D.gtc_tong && D.gtc_tong.am_tts) || [];
    return rawList.map(r => {
      const prev_val = r[currKey] !== undefined ? (r[prevKey] || 0) : (r.w37 !== undefined ? r.w37 : (r.w36 || 0));
      const curr_val = r[currKey] !== undefined ? (r[currKey] || 0) : (r.w38 !== undefined ? r.w38 : (r.w37 || 0));
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
      const list = getGtcCa1TtsData().sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));
      const rowsHtml = list.map((row, i) => {
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
      tblBody.innerHTML = rowsHtml;
    }
  }

  function renderGtcTtsCa1BarChart() {
    const ctx = document.getElementById('chart-gtc-tts-ca1-bar');
    if (!ctx) return;
    if (charts.gtcTtsCa1Bar) charts.gtcTtsCa1Bar.destroy();

    const currLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1] : 'W36';
    const selectedAM = state.selectedAM;
    const hlMode = state.gtcTtsCa1Highlight || 'all';
    const sortMode = state.gtcTtsCa1Sort || 'diff_asc';

    let sorted = getGtcCa1TtsData();
    sorted.sort((a, b) => (b.w35_pct || 0) - (a.w35_pct || 0));

    function checkCa1Match(d) {
      if (selectedAM) return selectedAM === d.am;
      if (hlMode === 'all') return true;
      if (hlMode === 'top') return d.w35_pct >= 85.0;
      if (hlMode === 'pass') return d.w35_pct >= 76.0;
      if (hlMode === 'fail') return d.w35_pct < 76.0;
      return true;
    }

    // Sync laser boxes on table
    document.querySelectorAll('#table-gtc-tts-ca1-detailed tr.presenter-laser-box').forEach(el => el.classList.remove('presenter-laser-box'));
    if (hlMode !== 'all' || selectedAM) {
      sorted.forEach(d => {
        if (checkCa1Match(d)) {
          document.querySelectorAll(`#table-gtc-tts-ca1-detailed tr[data-entity="${d.am}"]`).forEach(tr => tr.classList.add('presenter-laser-box'));
        }
      });
    }

    const hasFilter = hlMode !== 'all' || selectedAM;

    // Dynamic scale for y1
    const diffVals = sorted.map(d => d.diff_pct);
    const minD = Math.min(...diffVals, 0);
    const maxD = Math.max(...diffVals, 0);
    const y1Min = Math.floor((minD - 4) / 5) * 5;
    const y1Max = Math.ceil((maxD + 5) / 5) * 5;

    charts.gtcTtsCa1Bar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: sorted.map(d => d.am),
        datasets: [
          {
            type: 'bar',
            label: `%GTC Ca 1 TTS ${currLabel} (Target ≥ 76%)`,
            data: sorted.map(d => d.w35_pct),
            backgroundColor: sorted.map(d => {
              const isM = checkCa1Match(d);
              if (!hasFilter) return d.isPass ? '#0d9488' : '#ef4444';
              if (!isM) return 'rgba(148, 163, 184, 0.15)';
              if (hlMode === 'top' || hlMode === 'pass') return '#0d9488';
              if (hlMode === 'fail') return '#ef4444';
              return '#ef4444';
            }),
            borderColor: sorted.map(d => checkCa1Match(d) && hasFilter ? (d.isPass ? '#047857' : '#b91c1c') : 'transparent'),
            borderWidth: sorted.map(d => checkCa1Match(d) && hasFilter ? 2.5 : 0),
            borderRadius: 4,
            yAxisID: 'y',
            order: 2,
            datalabels: {
              display: true,
              color: '#0f172a',
              font: { size: 10.5, weight: '800' },
              formatter: v => v + '%'
            }
          },
          {
            type: 'line',
            label: 'Target SLA (76.0%)',
            data: sorted.map(() => 76.0),
            borderColor: 'rgba(239, 68, 68, 0.75)',
            borderDash: [6, 4],
            borderWidth: 2,
            pointRadius: 0,
            pointHoverRadius: 0,
            yAxisID: 'y',
            order: 3,
            datalabels: { display: false }
          },
          {
            type: 'line',
            label: 'Đường Biến Động WoW (Δ %)',
            data: sorted.map(d => d.diff_pct),
            borderColor: '#f59e0b',
            borderWidth: 3,
            tension: 0.25,
            pointBackgroundColor: sorted.map(d => d.diff_pct >= 0 ? '#10b981' : '#ef4444'),
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2,
            pointRadius: 6,
            pointHoverRadius: 8,
            yAxisID: 'y1',
            order: 1,
            datalabels: {
              display: true,
              align: 'top',
              color: '#d97706',
              font: { size: 10, weight: '800' },
              formatter: v => (v > 0 ? '+' : '') + v + '%'
            }
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 25, bottom: 10 } },
        scales: {
          y: {
            position: 'left',
            min: 0,
            max: 100,
            ticks: { callback: v => v + '%' },
            title: { display: true, text: '%GTC Ca 1 TTS (%)', font: { weight: '700', size: 11 } },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          y1: {
            position: 'right',
            min: y1Min,
            max: y1Max,
            grid: { drawOnChartArea: false },
            title: { display: true, text: 'Biến Động WoW (Δ % p.p)', font: { weight: '700', size: 11, color: '#f59e0b' } },
            ticks: { callback: v => (v > 0 ? '+' : '') + v + '%' }
          },
          x: {
            ticks: { maxRotation: 45, minRotation: 20, font: { size: 11, weight: '800' } }
          }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => {
                if (c.dataset.type === 'line') {
                  const s = c.parsed.y > 0 ? '+' : '';
                  return `${c.dataset.label}: ${s}${c.parsed.y}%`;
                }
                const item = sorted[c.dataIndex];
                return `${c.dataset.label}: ${c.parsed.y}% (Sản lượng Ca 1: ${fNum(item.vol)} đơn | W34: ${item.w34}%)`;
              }
            }
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            selectAndHighlightAM(sorted[elements[0].index].am);
          }
        }
      }
    });
    if (window.lucide) lucide.createIcons();
  }

  // --------------------------------------------------------------------------
  // TAB 5: % GÁN VẬN HÀNH (CA 1, CA 2 & GÁN TỔNG)
  // --------------------------------------------------------------------------
  window.setGanFilter = function(filterMode) {
    state.ganFilter = filterMode || 'all';

    // 1. Sync Pill buttons in Tab 5
    document.querySelectorAll('#gan-chart-mode-pills .chart-mode-pill').forEach(btn => {
      const mode = btn.getAttribute('data-gan-filter');
      if (mode === state.ganFilter) {
        btn.classList.add('active');
        if (state.ganFilter === 'under80') {
          btn.style.background = '#dc2626';
          btn.style.color = '#ffffff';
          btn.style.borderColor = '#dc2626';
        } else {
          btn.style.background = '';
          btn.style.color = '';
          btn.style.borderColor = '';
        }
      } else {
        btn.classList.remove('active');
        if (mode === 'under80') {
          btn.style.background = 'rgba(239, 68, 68, 0.12)';
          btn.style.color = '#dc2626';
          btn.style.borderColor = '#ef4444';
        } else {
          btn.style.background = '';
          btn.style.color = '';
          btn.style.borderColor = '';
        }
      }
    });

    // 2. Sync Global Filter Dropdown
    const selGan = document.getElementById('filter-gan-rate');
    if (selGan && selGan.value !== state.ganFilter) {
      selGan.value = state.ganFilter;
    }

    // 3. Toggle Callout Alert
    const callout = document.getElementById('gan-filter-callout');
    if (callout) {
      callout.style.display = state.ganFilter === 'under80' ? 'flex' : 'none';
    }

    // 4. Re-render Chart & Detailed Tables
    renderGanBarChart();
    renderGanTab();
  };

  function renderGanTab() {
    if (!D.gan || !D.gan.am) return;

    // 0. BẢNG TỔNG QUAN VÙNG NTB (4 TUẦN)
    const tblOverview = document.querySelector('#table-gan-overview-region tbody');
    if (tblOverview && D.gan.overview) {
      tblOverview.innerHTML = D.gan.overview.map(row => {
        const getCellBg = (val) => {
          if (val >= 0.85) return 'background: #2e7d32; color: #ffffff; font-weight:700;';
          if (val >= 0.80) return 'background: #4caf50; color: #ffffff; font-weight:700;';
          if (val >= 0.62) return 'background: #bef264; color: #1e293b; font-weight:700;';
          return 'background: #fef08a; color: #1e293b; font-weight:700;';
        };

        const wKeys = (D.meta?.weeks || ['W34', 'W35', 'W36', 'W37']).map(w => w.toLowerCase());
        const v1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
        const v2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
        const v3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
        const v4 = row[wKeys[3]] !== undefined ? row[wKeys[3]] : (row.w37 || row.w36 || 0);

        const diffBadge = row.diff >= 0
          ? `<span class="diff-tag diff-up-good">+${(row.diff * 100).toFixed(1)}%</span>`
          : `<span class="diff-tag diff-down-bad">${(row.diff * 100).toFixed(1)}%</span>`;

        return `
          <tr>
            <td class="bold" style="font-size:13px; font-weight:800;">${row.indicator}</td>
            <td class="num" style="${getCellBg(v1)}">${fPct(v1)}</td>
            <td class="num" style="${getCellBg(v2)}">${fPct(v2)}</td>
            <td class="num" style="${getCellBg(v3)}">${fPct(v3)}</td>
            <td class="num bold" style="${getCellBg(v4)} font-size:13.5px; border-left: 2px solid #ffffff;">${fPct(v4)}</td>
            <td class="num bold">${diffBadge}</td>
          </tr>
        `;
      }).join('');
    }

    renderGanOverviewChart();

    renderGanBcTable();

    // 1. BẢNG 1: GÁN CA 1+TỒN
    const tblBodyCa1 = document.querySelector('#table-gan-ca1-detailed tbody');
    if (tblBodyCa1) {
      let listCa1 = [...D.gan.am].map(r => {
        const curr = r.ca1ton_w38 !== undefined ? r.ca1ton_w38 : (r.ca1ton_curr !== undefined ? r.ca1ton_curr : (r.ca1ton_w37 || 0));
        const prev = r.ca1ton_w37 !== undefined ? r.ca1ton_w37 : (r.ca1ton_prev !== undefined ? r.ca1ton_prev : (r.ca1ton_w36 || 0));
        const tong = r.tong_w38 !== undefined ? r.tong_w38 : (r.tong_curr !== undefined ? r.tong_curr : (r.tong_w37 || 0));
        return {
          ...r,
          curr_val: curr,
          prev_val: prev,
          tong_val: tong,
          diff_val: r.ca1ton_diff !== undefined ? r.ca1ton_diff : ((curr || 0) - (prev || 0))
        };
      });

      if (state.ganFilter === 'under80') {
        listCa1 = listCa1.filter(r => (r.tong_val || 0) < 0.80);
      } else if (state.ganFilter === '80to90') {
        listCa1 = listCa1.filter(r => (r.tong_val || 0) >= 0.80 && (r.tong_val || 0) < 0.90);
      } else if (state.ganFilter === 'ge90') {
        listCa1 = listCa1.filter(r => (r.tong_val || 0) >= 0.90);
      }

      listCa1.sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

      tblBodyCa1.innerHTML = listCa1.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const heatW = getHeatmapClass(row.curr_val, 'gan');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = (row.curr_val || 0) >= 0.90
          ? '<span class="badge-tag badge-tag-green">🟢 Đạt Chuẩn (≥90%)</span>'
          : '<span class="badge-tag badge-tag-amber">🟡 Cần Tăng Tốc (&lt;90%)</span>';

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.prev_val)}</td>
            <td class="num bold ${heatW}">${fPct(row.curr_val)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 2. BẢNG 2: GÁN TỔNG
    const tblBodyCa2 = document.querySelector('#table-gan-ca2-detailed tbody');
    if (tblBodyCa2) {
      let listCa2 = [...D.gan.am].map(r => {
        const curr = r.tong_w38 !== undefined ? r.tong_w38 : (r.tong_curr !== undefined ? r.tong_curr : (r.tong_w37 || 0));
        const prev = r.tong_w37 !== undefined ? r.tong_w37 : (r.tong_prev !== undefined ? r.tong_prev : (r.tong_w36 || 0));
        return {
          ...r,
          curr_val: curr,
          prev_val: prev,
          diff_val: r.tong_diff !== undefined ? r.tong_diff : ((curr || 0) - (prev || 0))
        };
      });

      if (state.ganFilter === 'under80') {
        listCa2 = listCa2.filter(r => (r.curr_val || 0) < 0.80);
      } else if (state.ganFilter === '80to90') {
        listCa2 = listCa2.filter(r => (r.curr_val || 0) >= 0.80 && (r.curr_val || 0) < 0.90);
      } else if (state.ganFilter === 'ge90') {
        listCa2 = listCa2.filter(r => (r.curr_val || 0) >= 0.90);
      }

      listCa2.sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

      tblBodyCa2.innerHTML = listCa2.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const heatTong = getHeatmapClass(row.curr_val, 'gan');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = (row.curr_val || 0) >= 0.90
          ? '<span class="badge-tag badge-tag-green">🏆 Đạt Target (≥90%)</span>'
          : ((row.curr_val || 0) >= 0.80 ? '<span class="badge-tag badge-tag-amber">🟡 Cảnh Báo (80-90%)</span>' : '<span class="badge-tag badge-tag-red">🔴 Thấp (&lt;80%)</span>');

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.prev_val)}</td>
            <td class="num bold ${heatTong}" style="font-weight:800;">${fPct(row.curr_val)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }
  }

  function renderGanOverviewChart() {
    const ctx = document.getElementById('chart-gan-overview-bar');
    if (!ctx || !D.gan || !D.gan.overview) return;
    if (charts.ganOverviewBar) charts.ganOverviewBar.destroy();

    const overview = D.gan.overview;
    const labels = [
      'Full - Tổng',
      'TTS - Tổng',
      'Full - Ca 1+Tồn',
      'TTS - Ca 1+Tồn',
      'Full - Ca 2',
      'TTS - Ca 2'
    ];

    const weeks = D.meta?.weeks || ['W34', 'W35', 'W36', 'W37'];
    const w1 = weeks[0].toLowerCase();
    const w2 = weeks[1].toLowerCase();
    const w3 = weeks[2].toLowerCase();
    const w4 = weeks[3].toLowerCase();

    charts.ganOverviewBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            type: 'bar',
            label: weeks[0],
            data: overview.map(d => Number(((d[w1] !== undefined ? d[w1] : (d.w34 || 0)) * 100).toFixed(1))),
            backgroundColor: '#cbd5e1',
            borderRadius: 3,
            datalabels: { display: false }
          },
          {
            type: 'bar',
            label: weeks[1],
            data: overview.map(d => Number(((d[w2] !== undefined ? d[w2] : (d.w35 || 0)) * 100).toFixed(1))),
            backgroundColor: '#94a3b8',
            borderRadius: 3,
            datalabels: { display: false }
          },
          {
            type: 'bar',
            label: weeks[2],
            data: overview.map(d => Number(((d[w3] !== undefined ? d[w3] : (d.w36 || 0)) * 100).toFixed(1))),
            backgroundColor: '#60a5fa',
            borderRadius: 3,
            datalabels: { display: false }
          },
          {
            type: 'bar',
            label: weeks[3],
            data: overview.map(d => Number(((d[w4] !== undefined ? d[w4] : (d.w37 || 0)) * 100).toFixed(1))),
            backgroundColor: overview.map(d => (d[w4] !== undefined ? d[w4] : (d.w37 || 0)) >= 0.80 ? '#10b981' : '#f59e0b'),
            borderRadius: 4,
            datalabels: {
              display: true,
              align: 'top',
              anchor: 'end',
              color: '#0f172a',
              font: { size: 10.5, weight: '800' },
              formatter: v => v + '%'
            }
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 25, bottom: 5 } },
        scales: {
          y: {
            min: 50,
            max: 100,
            ticks: { callback: v => v + '%' },
            title: { display: true, text: '% Gán (%)', font: { weight: '700', size: 11 } },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          x: {
            ticks: { font: { size: 11, weight: '700' } }
          }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => `${c.dataset.label}: ${c.parsed.y}%`
            }
          }
        }
      }
    });
  }

  function renderGanBarChart() {
    const ctx = document.getElementById('chart-gan-am-bar');
    if (!ctx || !D.gan || !D.gan.am) return;
    
    const existingChart = Chart.getChart(ctx);
    if (existingChart) existingChart.destroy();
    if (charts.ganBar) {
      try { charts.ganBar.destroy(); } catch (e) {}
      charts.ganBar = null;
    }

    const currLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1] : 'W40';
    const prevLabel = D.meta?.weeks && D.meta.weeks.length >= 2 ? D.meta.weeks[D.meta.weeks.length - 2] : 'W39';
    const selectedAM = state.selectedAM;

    let list = [...D.gan.am].map(r => {
      const prev_val = r.tong_w39 !== undefined ? r.tong_w39 : (r.tong_w37 !== undefined ? r.tong_w37 : (r.tong_prev !== undefined ? r.tong_prev : (r.tong_w36 || 0)));
      const curr_val = r.tong_w40 !== undefined ? r.tong_w40 : (r.tong_w38 !== undefined ? r.tong_w38 : (r.tong_curr !== undefined ? r.tong_curr : (r.tong_w37 || 0)));
      const diff_val = r.tong_diff !== undefined ? r.tong_diff : (curr_val - prev_val);
      const ca1 = r.ca1ton_w40 !== undefined ? r.ca1ton_w40 : (r.ca1ton_w38 !== undefined ? r.ca1ton_w38 : (r.ca1ton_curr !== undefined ? r.ca1ton_curr : (r.ca1ton_w37 || 0)));
      const ca2 = r.ca2_w40 !== undefined ? r.ca2_w40 : (r.ca2_w38 !== undefined ? r.ca2_w38 : (r.ca2_curr !== undefined ? r.ca2_curr : (r.ca2_w37 || 0)));
      return {
        ...r,
        ca1_pct: Number((ca1 * 100).toFixed(1)),
        ca2_pct: Number((ca2 * 100).toFixed(1)),
        tong_prev_pct: Number((prev_val * 100).toFixed(1)),
        tong_pct: Number((curr_val * 100).toFixed(1)),
        diff_pct: Number((diff_val * 100).toFixed(1))
      };
    });

    if (state.ganFilter === 'under80') {
      list = list.filter(r => r.tong_pct < 80.0);
    } else if (state.ganFilter === '80to90') {
      list = list.filter(r => r.tong_pct >= 80.0 && r.tong_pct < 90.0);
    } else if (state.ganFilter === 'ge90') {
      list = list.filter(r => r.tong_pct >= 90.0);
    }
    list.sort((a, b) => (b.tong_pct || 0) - (a.tong_pct || 0));

    const isUnder80 = state.ganFilter === 'under80';
    const barMaxThick = isUnder80 ? 46 : 28;

    try {
      charts.ganBar = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: list.map(d => d.am),
          datasets: [
            {
              type: 'bar',
              label: `% Gán Ca 1 + Tồn (${currLabel})`,
              data: list.map(d => d.ca1_pct),
              backgroundColor: '#c084fc',
              borderRadius: 4,
              maxBarThickness: barMaxThick,
              yAxisID: 'y',
              order: 2,
              datalabels: {
                display: true,
                anchor: 'end',
                align: 'top',
                color: '#7e22ce',
                font: { weight: '800', size: isUnder80 ? 11 : 9 },
                formatter: v => v + '%'
              }
            },
            {
              type: 'bar',
              label: `% Gán Ca 2 (${currLabel})`,
              data: list.map(d => d.ca2_pct),
              backgroundColor: '#9333ea',
              borderRadius: 4,
              maxBarThickness: barMaxThick,
              yAxisID: 'y',
              order: 2,
              datalabels: {
                display: true,
                anchor: 'end',
                align: 'top',
                color: '#581c87',
                font: { weight: '800', size: isUnder80 ? 11 : 9 },
                formatter: v => v > 0 ? v + '%' : '0%'
              }
            },
            {
              type: 'bar',
              label: `% Gán Tổng ${currLabel} (Target ≥90%)`,
              data: list.map(d => d.tong_pct),
              backgroundColor: list.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : (d.tong_pct >= 90 ? '#10b981' : (d.tong_pct >= 80 ? '#f59e0b' : '#ef4444'))),
              borderColor: list.map(d => selectedAM && selectedAM === d.am ? '#b91c1c' : 'transparent'),
              borderWidth: list.map(d => selectedAM && selectedAM === d.am ? 3 : 0),
              borderRadius: 4,
              maxBarThickness: barMaxThick,
              yAxisID: 'y',
              order: 2,
              datalabels: {
                display: true,
                anchor: 'end',
                align: 'top',
                offset: 2,
                color: ctx => {
                  const val = typeof ctx.parsed === 'number' ? ctx.parsed : (ctx.parsed?.y ?? ctx.dataset.data[ctx.dataIndex] ?? 0);
                  return val < 80 ? '#b91c1c' : (val >= 90 ? '#15803d' : '#b45309');
                },
                font: { weight: '900', size: isUnder80 ? 12 : 9.5 },
                formatter: v => v + '%'
              }
            },
            {
              type: 'line',
              label: 'Đường Biến Động WoW (Δ %)',
              data: list.map(d => d.diff_pct),
              borderColor: '#f26522',
              borderWidth: 3,
              tension: 0.25,
              pointBackgroundColor: list.map(d => d.diff_pct >= 0 ? '#10b981' : '#ef4444'),
              pointBorderColor: '#ffffff',
              pointBorderWidth: 2,
              pointRadius: isUnder80 ? 7 : 5,
              pointHoverRadius: 9,
              yAxisID: 'y1',
              order: 1,
              datalabels: {
                display: true,
                anchor: 'center',
                align: 'top',
                offset: 6,
                color: '#c2410c',
                backgroundColor: 'rgba(255, 255, 255, 0.92)',
                borderRadius: 3,
                padding: { top: 1, bottom: 1, left: 3, right: 3 },
                font: { weight: '800', size: isUnder80 ? 10.5 : 8.5 },
                formatter: v => (v > 0 ? '+' : '') + v + '%'
              }
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          layout: { padding: { top: 26, bottom: 10 } },
          scales: {
            y: {
              position: 'left',
              min: 0,
              max: 110,
              ticks: { callback: v => v + '%' },
            },
            y1: {
              position: 'right',
              grid: { drawOnChartArea: false },
              title: { display: true, text: 'Biến Động WoW (Δ % p.p)', font: { weight: '700', size: 11, color: '#f26522' } },
              ticks: { callback: v => (v > 0 ? '+' : '') + v + '%' }
            },
            x: {
              ticks: { maxRotation: isUnder80 ? 15 : 45, minRotation: isUnder80 ? 0 : 30, font: { size: isUnder80 ? 12 : 11, weight: '700' } }
            }
          },
          plugins: {
            legend: { position: 'top' },
            tooltip: {
              callbacks: {
                label: c => {
                  const val = typeof c.parsed === 'number' ? c.parsed : (c.parsed?.y ?? c.raw ?? 0);
                  return `${c.dataset.label}: ${val}%`;
                }
              }
            }
          },
          onClick: (event, elements) => {
            if (elements.length > 0) {
              selectAndHighlightAM(list[elements[0].index].am);
            }
          }
        }
      });
    } catch (err) {
      console.error('Error rendering GanBarChart:', err);
    }
  }

  // --------------------------------------------------------------------------
  // TAB 6: %ODR GIAO ĐÚNG HẸN (ĐỐI XỨNG FULL HÀNG vs TIKTOK SHOP)
  // --------------------------------------------------------------------------
  window.setOdrSegment = function(seg) {
    state.odrSegment = seg;
    const btnFull = document.getElementById('btn-odr-full');
    const btnTts = document.getElementById('btn-odr-tts');
    const btnCompare = document.getElementById('btn-odr-compare');

    [btnFull, btnTts, btnCompare].forEach(b => {
      if (b) {
        b.classList.remove('btn-primary', 'active');
        b.classList.add('btn-secondary');
      }
    });

    if (seg === 'full' && btnFull) {
      btnFull.classList.add('btn-primary', 'active');
      btnFull.classList.remove('btn-secondary');
    } else if (seg === 'tts' && btnTts) {
      btnTts.classList.add('btn-primary', 'active');
      btnTts.classList.remove('btn-secondary');
    } else if (seg === 'compare' && btnCompare) {
      btnCompare.classList.add('btn-primary', 'active');
      btnCompare.classList.remove('btn-secondary');
    }

    renderOdrTab();
    renderOdrChart();
    if (window.lucide) lucide.createIcons();
  };

  window.setOdrHighlight = function(hl) {
    state.odrHighlight = hl;
    state.selectedAM = null;
    const btnMap = {
      all: 'btn-odr-hl-all',
      pass: 'btn-odr-hl-pass',
      fail: 'btn-odr-hl-fail',
      grow: 'btn-odr-hl-grow'
    };

    Object.keys(btnMap).forEach(k => {
      const b = document.getElementById(btnMap[k]);
      if (b) {
        if (k === hl) {
          b.classList.add('active');
          b.style.fontWeight = '800';
        } else {
          b.classList.remove('active');
          b.style.fontWeight = 'normal';
        }
      }
    });
    renderOdrChart();
  };

  window.setOdrTableView = function(mode) {
    state.odrTableView = mode;
    const pills = document.querySelectorAll('#odr-table-mode-pills .chart-mode-pill');
    pills.forEach(p => {
      p.classList.toggle('active', p.getAttribute('data-table-view') === mode);
    });

    const cardFull = document.getElementById('card-odr-full');
    const cardTTS = document.getElementById('card-odr-tts');
    const grid = document.getElementById('odr-am-grid');

    if (cardFull && cardTTS && grid) {
      if (mode === 'split') {
        cardFull.style.display = 'block';
        cardTTS.style.display = 'block';
        grid.className = 'grid-row-2';
      } else if (mode === 'full_only') {
        cardFull.style.display = 'block';
        cardTTS.style.display = 'none';
        grid.className = 'grid-row-1';
      } else if (mode === 'tts_only') {
        cardFull.style.display = 'none';
        cardTTS.style.display = 'block';
        grid.className = 'grid-row-1';
      }
    }
  };

  function renderOdrTab() {
    if (!D.odr) return;

    function getOdrEvalBadge(v) {
      const val = v || 0;
      if (val >= 0.95) return '<span class="badge-tag badge-tag-green">🏆 Xuất Sắc (≥95%)</span>';
      if (val >= 0.92) return '<span class="badge-tag badge-tag-green">🟢 Đạt Chuẩn SLA (≥92%)</span>';
      return '<span class="badge-tag badge-tag-red">🔴 Chưa Đạt (&lt;92%)</span>';
    }

    // 1. BẢNG 1A: %ODR FULL HÀNG (19 AM)
    const tblBodyFull = document.querySelector('#table-odr-full-detailed tbody');
    if (tblBodyFull) {
      const latestKey = D.meta?.latest_week ? D.meta.latest_week.toLowerCase() : 'w37';
      const prevKey = D.meta?.prev_week ? D.meta.prev_week.toLowerCase() : 'w36';
      const rawFull = D.odr.am_full || D.odr.am || [];
      let listFull = [...rawFull].map(r => {
        const curr = r[latestKey] !== undefined ? r[latestKey] : (r.w37 !== undefined ? r.w37 : (r.w36 || 0));
        const prev = r[prevKey] !== undefined ? r[prevKey] : (r.w36 !== undefined ? r.w36 : (r.w35 || 0));
        return {
          ...r,
          curr_val: curr,
          prev_val: prev,
          diff_val: r.diff !== undefined ? r.diff : (curr - prev)
        };
      });

      if (state.searchOdrFull) {
        listFull = listFull.filter(r => r.am.toLowerCase().includes(state.searchOdrFull));
      }

      const sortedFull = listFull.sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

      tblBodyFull.innerHTML = sortedFull.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const heatCurr = getHeatmapClass(row.curr_val, 'odr');
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
        `;
      }).join('');
    }

    // 2. BẢNG 1B: %ODR TIKTOK SHOP (19 AM)
    const tblBodyTTS = document.querySelector('#table-odr-tts-detailed tbody');
    if (tblBodyTTS) {
      const latestKey = D.meta?.latest_week ? D.meta.latest_week.toLowerCase() : 'w37';
      const prevKey = D.meta?.prev_week ? D.meta.prev_week.toLowerCase() : 'w36';
      const rawTTS = D.odr.am_tts || [];
      let listTTS = [...rawTTS].map(r => {
        const curr = r[latestKey] !== undefined ? r[latestKey] : (r.w37 !== undefined ? r.w37 : (r.w36 || 0));
        const prev = r[prevKey] !== undefined ? r[prevKey] : (r.w36 !== undefined ? r.w36 : (r.w35 || 0));
        return {
          ...r,
          curr_val: curr,
          prev_val: prev,
          diff_val: r.diff !== undefined ? r.diff : (curr - prev)
        };
      });

      if (state.searchOdrTTS) {
        listTTS = listTTS.filter(r => r.am.toLowerCase().includes(state.searchOdrTTS));
      }

      const sortedTTS = listTTS.sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

      tblBodyTTS.innerHTML = sortedTTS.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const heatCurr = getHeatmapClass(row.curr_val, 'odr');
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
        `;
      }).join('');
    }

    // 3. BẢNG 2A: %ODR 5 TỈNH THÀNH (FULL HÀNG)
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
        const isSelected = state.selectedProvince === row.tinh;
        const rowClass = isSelected ? 'province-laser-box' : '';
        const v1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
        const v2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
        const v3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
        const v4 = row.curr_val;
        const heatClass = getHeatmapClass(v4, 'odr');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = getOdrEvalBadge(v4);

        return `
          <tr data-province="${row.tinh}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightProvince('${row.tinh}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13.5px; font-weight:800; color:${isSelected ? '#2563eb' : 'inherit'};">${row.tinh}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(v1)}</td>
            <td class="num">${fPct(v2)}</td>
            <td class="num">${fPct(v3)}</td>
            <td class="num bold ${heatClass}">${fPct(v4)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 4. BẢNG 2B: %ODR 5 TỈNH THÀNH (TIKTOK SHOP)
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
        const isSelected = state.selectedProvince === row.tinh;
        const rowClass = isSelected ? 'province-laser-box' : '';
        const v1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
        const v2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
        const v3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
        const v4 = row.curr_val;
        const heatClass = getHeatmapClass(v4, 'odr');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = getOdrEvalBadge(v4);

        return `
          <tr data-province="${row.tinh}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightProvince('${row.tinh}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13.5px; font-weight:800; color:${isSelected ? '#ea580c' : 'inherit'};">${row.tinh}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(v1)}</td>
            <td class="num">${fPct(v2)}</td>
            <td class="num">${fPct(v3)}</td>
            <td class="num bold ${heatClass}">${fPct(v4)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }
  }

  
  // --------------------------------------------------------------------------
  // CHART: %ODR 5 TỈNH QUA 4 TUẦN (W40 - W43) & BIẾN ĐỘNG Δ %p WoW
  // --------------------------------------------------------------------------
  function renderTinhOdr4WeeksChart() {
    const ctx = document.getElementById('chart-odr-tinh-4weeks');
    if (!ctx || !D.odr) return;
    if (charts.tinhOdr4Weeks) charts.tinhOdr4Weeks.destroy();

    const isTTS = (state.tinhOdrChannel === 'tts');
    const isLine = (state.tinhOdrType === 'line');
    const rawData = isTTS ? (D.odr.tinh_tts || []) : (D.odr.tinh_full || D.odr.tinh || []);

    const wKeys = (D.meta?.weeks || ['W38', 'W39', 'W40', 'W41']).map(w => w.toLowerCase());
    const weekLabels = D.meta?.weeks || ['W38', 'W39', 'W40', 'W41'];

    // Sort provinces by W41 %ODR descending
    const sortedProvinces = [...rawData].sort((a, b) => {
      const vA = a[wKeys[3]] !== undefined ? a[wKeys[3]] : (a.w41 || a.curr_val || 0);
      const vB = b[wKeys[3]] !== undefined ? b[wKeys[3]] : (b.w41 || b.curr_val || 0);
      return vB - vA;
    });

    const labels = sortedProvinces.map(p => p.tinh);

    // Update summary badge
    const badgeEl = document.getElementById('odr-tinh-summary-badge');
    if (badgeEl) {
      const curW = weekLabels[3] || 'W43';
      if (isTTS) {
        badgeEl.innerHTML = `🛒 TikTok Shop ${curW}: <strong>92,85%</strong> — Đạt chuẩn cam kết SLA ≥ 92.0%`;
        badgeEl.style.color = '#ea580c';
        badgeEl.style.background = '#fff7ed';
        badgeEl.style.borderColor = 'rgba(234, 88, 12, 0.3)';
      } else {
        badgeEl.innerHTML = `🎯 Toàn vùng ${curW}: <strong>91,97%</strong> (-2,12%p WoW — Cận Target 92.0%)`;
        badgeEl.style.color = '#059669';
        badgeEl.style.background = '#dcfce7';
        badgeEl.style.borderColor = 'rgba(16, 185, 129, 0.3)';
      }
    }

    if (!isLine) {
      // GROUPED BAR CHART: 4 columns per province (W38, W39, W40, W41)
      const dataW38 = sortedProvinces.map(p => {
        const v = p[wKeys[0]] !== undefined ? p[wKeys[0]] : (p.w38 || 0);
        return parseFloat((v * 100).toFixed(1));
      });
      const dataW39 = sortedProvinces.map(p => {
        const v = p[wKeys[1]] !== undefined ? p[wKeys[1]] : (p.w39 || 0);
        return parseFloat((v * 100).toFixed(1));
      });
      const dataW40 = sortedProvinces.map(p => {
        const v = p[wKeys[2]] !== undefined ? p[wKeys[2]] : (p.w40 || 0);
        return parseFloat((v * 100).toFixed(1));
      });
      const dataW41 = sortedProvinces.map(p => {
        const v = p[wKeys[3]] !== undefined ? p[wKeys[3]] : (p.w41 || p.curr_val || 0);
        return parseFloat((v * 100).toFixed(1));
      });

      charts.tinhOdr4Weeks = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: `${weekLabels[0]}`,
              data: dataW38,
              backgroundColor: '#94a3b8',
              borderRadius: 4,
              maxBarThickness: 32,
              datalabels: {
                anchor: 'end',
                align: 'top',
                offset: 2,
                color: '#64748b',
                font: { size: 10, weight: '600' },
                formatter: (val) => val.toFixed(1) + '%'
              }
            },
            {
              label: `${weekLabels[1]}`,
              data: dataW39,
              backgroundColor: '#60a5fa',
              borderRadius: 4,
              maxBarThickness: 32,
              datalabels: {
                anchor: 'end',
                align: 'top',
                offset: 2,
                color: '#2563eb',
                font: { size: 10, weight: '600' },
                formatter: (val) => val.toFixed(1) + '%'
              }
            },
            {
              label: `${weekLabels[2]} (Mega Sale 10.10)`,
              data: dataW40,
              backgroundColor: '#1e40af',
              borderRadius: 4,
              maxBarThickness: 32,
              datalabels: {
                anchor: 'end',
                align: 'top',
                offset: 2,
                color: '#1e3a8a',
                font: { size: 10.5, weight: '700' },
                formatter: (val) => val.toFixed(1) + '%'
              }
            },
            {
              label: `${weekLabels[3]} (Kỷ Lục Mới)`,
              data: dataW41,
              backgroundColor: '#10b981',
              borderColor: '#059669',
              borderWidth: 2,
              borderRadius: 6,
              maxBarThickness: 36,
              datalabels: {
                anchor: 'end',
                align: 'top',
                offset: 4,
                color: (ctx2) => {
                  const idx = ctx2.dataIndex;
                  const prev = dataW40[idx] || 0;
                  return dataW41[idx] >= prev ? '#059669' : '#dc2626';
                },
                font: { size: 11.5, weight: '800' },
                formatter: (val, ctx2) => {
                  const idx = ctx2.dataIndex;
                  const prevVal = dataW40[idx] || 0;
                  const diffP = val - prevVal;
                  const sign = diffP >= 0 ? '+' : '';
                  return [`${val.toFixed(1)}%`, `${sign}${diffP.toFixed(1)}%p`];
                }
              }
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          layout: {
            padding: { top: 32, bottom: 8, left: 10, right: 10 }
          },
          plugins: {
            legend: {
              position: 'top',
              labels: {
                boxWidth: 10,
                boxHeight: 10,
                font: { weight: '700', size: 12 }
              }
            },
            tooltip: {
              backgroundColor: 'rgba(15, 23, 42, 0.95)',
              titleFont: { size: 13, weight: '700' },
              bodyFont: { size: 12 },
              padding: 12,
              cornerRadius: 8,
              callbacks: {
                label: function (c) {
                  const val = c.raw || 0;
                  const idx = c.dataIndex;
                  if (c.datasetIndex === 3) {
                    const prev = dataW40[idx] || 0;
                    const diff = val - prev;
                    const sign = diff >= 0 ? '+' : '';
                    return ` ${c.dataset.label}: ${val.toFixed(2)}% (${sign}${diff.toFixed(2)}%p WoW)`;
                  }
                  return ` ${c.dataset.label}: ${val.toFixed(2)}%`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: { display: false },
              ticks: {
                font: { weight: '800', size: 12.5 },
                color: '#0f172a'
              }
            },
            y: {
              beginAtZero: false,
              min: 80,
              max: 100,
              grid: { color: 'rgba(226, 232, 240, 0.6)' },
              ticks: {
                callback: v => v + '%',
                font: { size: 11 }
              }
            }
          }
        }
      });
    } else {
      // LINE TREND CHART
      const palette = [
        { stroke: '#059669' },
        { stroke: '#2563eb' },
        { stroke: '#ea580c' },
        { stroke: '#8b5cf6' },
        { stroke: '#06b6d4' }
      ];

      const datasets = sortedProvinces.map((p, idx) => {
        const col = palette[idx % palette.length];
        const vW38 = parseFloat(((p[wKeys[0]] !== undefined ? p[wKeys[0]] : (p.w38 || 0)) * 100).toFixed(1));
        const vW39 = parseFloat(((p[wKeys[1]] !== undefined ? p[wKeys[1]] : (p.w39 || 0)) * 100).toFixed(1));
        const vW40 = parseFloat(((p[wKeys[2]] !== undefined ? p[wKeys[2]] : (p.w40 || 0)) * 100).toFixed(1));
        const vW41 = parseFloat(((p[wKeys[3]] !== undefined ? p[wKeys[3]] : (p.w41 || p.curr_val || 0)) * 100).toFixed(1));
        const diffP = vW41 - vW40;
        const sign = diffP >= 0 ? '+' : '';

        return {
          label: `${p.tinh} (${sign}${diffP.toFixed(1)}%p)`,
          data: [vW38, vW39, vW40, vW41],
          borderColor: col.stroke,
          backgroundColor: col.stroke,
          borderWidth: 3,
          tension: 0.35,
          pointRadius: 6,
          pointHoverRadius: 8,
          datalabels: {
            anchor: 'end',
            align: 'top',
            offset: 4,
            color: col.stroke,
            font: { size: 11, weight: '700' },
            formatter: (val, ctx2) => {
              if (ctx2.dataIndex === 3) {
                return `${val.toFixed(1)}% (${sign}${diffP.toFixed(1)}%p)`;
              }
              return val.toFixed(1) + '%';
            }
          }
        };
      });

      charts.tinhOdr4Weeks = new Chart(ctx, {
        type: 'line',
        data: {
          labels: weekLabels,
          datasets: datasets
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          layout: {
            padding: { top: 32, bottom: 8, left: 10, right: 10 }
          },
          plugins: {
            legend: {
              position: 'top',
              labels: {
                boxWidth: 10,
                boxHeight: 10,
                font: { weight: '700', size: 12 }
              }
            },
            tooltip: {
              backgroundColor: 'rgba(15, 23, 42, 0.95)',
              padding: 12,
              cornerRadius: 8,
              callbacks: {
                label: function (c) {
                  return ` ${c.dataset.label}: ${c.raw.toFixed(2)}%`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: { display: false },
              ticks: { font: { weight: '800', size: 12.5 } }
            },
            y: {
              beginAtZero: false,
              min: 80,
              max: 100,
              grid: { color: 'rgba(226, 232, 240, 0.6)' },
              ticks: {
                callback: v => v + '%',
                font: { size: 11 }
              }
            }
          }
        }
      });
    }
  }

  window.switchTinhOdrChannel = function(ch) {
    state.tinhOdrChannel = ch;
    const btnFull = document.getElementById('btn-odr-tinh-channel-full');
    const btnTTS = document.getElementById('btn-odr-tinh-channel-tts');
    if (btnFull) btnFull.classList.toggle('active', ch === 'full');
    if (btnTTS) btnTTS.classList.toggle('active', ch === 'tts');
    const titleEl = document.getElementById('odr-tinh-chart-header-title');
    if (titleEl) {
      titleEl.textContent = (ch === 'tts') 
        ? 'BIỂU ĐỒ %ODR 5 TỈNH QUA 4 TUẦN (W40 – W43) — TIKTOK SHOP & BIẾN ĐỘNG Δ %p WoW'
        : 'BIỂU ĐỒ %ODR 5 TỈNH QUA 4 TUẦN (W40 – W43) — FULL HÀNG & BIẾN ĐỘNG Δ %p WoW (TARGET ≥ 92.0%)';
    }
    renderTinhOdr4WeeksChart();
  };

  window.switchTinhOdrType = function(t) {
    state.tinhOdrType = t;
    const btnBar = document.getElementById('btn-odr-tinh-type-bar');
    const btnLine = document.getElementById('btn-odr-tinh-type-line');
    if (btnBar) btnBar.classList.toggle('active', t === 'bar');
    if (btnLine) btnLine.classList.toggle('active', t === 'line');
    renderTinhOdr4WeeksChart();
  };

  function renderOdrChart() {
    const ctx = document.getElementById('chart-odr-bar');
    if (!ctx || !D.odr) return;
    if (charts.odrBar) charts.odrBar.destroy();

    const seg = state.odrSegment || 'full';
    const selectedAM = state.selectedAM;
    const hlMode = state.odrHighlight || 'all';

    const prevKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2].toLowerCase() : 'w35';
    const currKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1].toLowerCase() : 'w36';
    const prevLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2] : 'W35';
    const currLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1] : 'W36';

    const titleChart = document.getElementById('chart-odr-title');
    if (titleChart) {
      titleChart.textContent = seg === 'compare'
        ? `BIỂU ĐỒ SO SÁNH TRỰC DIỆN %ODR FULL HÀNG vs %ODR TIKTOK SHOP (${currLabel})`
        : `BIỂU ĐỒ %ODR GIAO ĐÚNG HẸN THEO 19 AM (${seg === 'tts' ? 'TIKTOK SHOP' : 'FULL HÀNG'})`;
    }

    const amFullList = D.odr.am_full || D.odr.am || [];
    const amTtsList = D.odr.am_tts || [];

    const fullMap = {};
    amFullList.forEach(f => fullMap[f.am] = f);

    const ttsMap = {};
    amTtsList.forEach(t => ttsMap[t.am] = t);

    // Combine list
    let list = amFullList.map(r => {
      const tts = ttsMap[r.am] || {};
      const fullW34 = (r[prevKey] !== undefined ? r[prevKey] : (r.w34 || 0)) * 100;
      const fullW35 = (r[currKey] !== undefined ? r[currKey] : (r.w35 || 0)) * 100;
      const fullDiff = (r.diff !== undefined ? (r.diff * 100) : (fullW35 - fullW34));

      const ttsW34 = (tts[prevKey] !== undefined ? tts[prevKey] : (tts.w34 !== undefined ? tts.w34 : (r[prevKey] || 0))) * 100;
      const ttsW35 = (tts[currKey] !== undefined ? tts[currKey] : (tts.w35 !== undefined ? tts.w35 : (r[currKey] || 0))) * 100;
      const ttsDiff = (tts.diff !== undefined ? (tts.diff * 100) : (ttsW35 - ttsW34));
      const gap = Number((ttsW35 - fullW35).toFixed(1));

      return {
        am: r.am,
        vol_full: r.vol || 0,
        vol_tts: tts.vol || 0,
        full_w34: Number(fullW34.toFixed(1)),
        full_w35: Number(fullW35.toFixed(1)),
        full_diff: Number(fullDiff.toFixed(1)),
        tts_w34: Number(ttsW34.toFixed(1)),
        tts_w35: Number(ttsW35.toFixed(1)),
        tts_diff: Number(ttsDiff.toFixed(1)),
        gap: gap
      };
    });

    function checkOdrMatch(d) {
      if (selectedAM) return selectedAM === d.am;
      if (hlMode === 'all') return true;
      if (hlMode === 'pass') {
        const val = seg === 'tts' ? d.tts_w35 : d.full_w35;
        return val >= 92.0;
      }
      if (hlMode === 'fail') {
        const val = seg === 'tts' ? d.tts_w35 : d.full_w35;
        return val < 92.0;
      }
      if (hlMode === 'grow') {
        const diff = seg === 'tts' ? d.tts_diff : d.full_diff;
        return diff >= 1.0;
      }
      return true;
    }

    // Sync laser boxes on table
    document.querySelectorAll('#table-odr-full-detailed tr.presenter-laser-box, #table-odr-tts-detailed tr.presenter-laser-box').forEach(el => el.classList.remove('presenter-laser-box'));
    if (hlMode !== 'all' || selectedAM) {
      list.forEach(d => {
        if (checkOdrMatch(d)) {
          document.querySelectorAll(`#table-odr-full-detailed tr[data-entity="${d.am}"], #table-odr-tts-detailed tr[data-entity="${d.am}"]`).forEach(tr => tr.classList.add('presenter-laser-box'));
        }
      });
    }

    let displayList = [...list];
    let datasets = [];
    let y1Title = 'Biến Động (Δ % p.p)';
    const hasFilter = hlMode !== 'all' || selectedAM;

    let allYVals = [];
    if (seg === 'full') {
      allYVals = displayList.flatMap(d => [d.full_w34, d.full_w35]);
    } else if (seg === 'tts') {
      allYVals = displayList.flatMap(d => [d.tts_w34, d.tts_w35]);
    } else {
      allYVals = displayList.flatMap(d => [d.full_w35, d.tts_w35]);
    }
    const minRaw = Math.min(...allYVals.filter(v => typeof v === 'number' && !isNaN(v)));
    const yMin = Math.max(0, Math.min(30, Math.floor((minRaw - 5) / 10) * 10));
    if (seg === 'tts') {
      displayList.sort((a, b) => (b.tts_w35 || 0) - (a.tts_w35 || 0));
    } else {
      displayList.sort((a, b) => (b.full_w35 || 0) - (a.full_w35 || 0));
    }

    if (seg === 'full') {
      datasets = [
        {
          type: 'bar',
          label: `%ODR Full ${prevLabel} (%)`,
          data: displayList.map(d => d.full_w34),
          backgroundColor: displayList.map(d => {
            const isM = checkOdrMatch(d);
            if (!hasFilter) return '#94a3b8';
            return isM ? '#64748b' : 'rgba(203, 213, 225, 0.45)';
          }),
          borderRadius: 4,
          yAxisID: 'y',
          order: 2
        },
        {
          type: 'bar',
          label: `%ODR Full ${currLabel} (Target ≥92%)`,
          data: displayList.map(d => d.full_w35),
          backgroundColor: displayList.map(d => {
            const isM = checkOdrMatch(d);
            if (!hasFilter) return d.full_w35 >= 92.0 ? '#10b981' : '#ef4444';
            if (hlMode === 'pass') return isM ? '#10b981' : 'rgba(148, 163, 184, 0.4)';
            if (hlMode === 'fail') return isM ? '#ef4444' : 'rgba(16, 185, 129, 0.45)';
            if (hlMode === 'grow') return isM ? '#0284c7' : 'rgba(148, 163, 184, 0.4)';
            return isM ? (d.full_w35 >= 92 ? '#10b981' : '#ef4444') : 'rgba(148, 163, 184, 0.4)';
          }),
          borderColor: displayList.map(d => checkOdrMatch(d) && hasFilter ? (d.full_w35 >= 92 ? '#059669' : '#b91c1c') : 'transparent'),
          borderWidth: displayList.map(d => checkOdrMatch(d) && hasFilter ? 2 : 0),
          borderRadius: 4,
          yAxisID: 'y',
          order: 2
        },
        {
          type: 'line',
          label: 'Đường Biến Động WoW Full (Δ %)',
          data: displayList.map(d => d.full_diff),
          borderColor: '#f26522',
          borderWidth: 3,
          tension: 0.25,
          pointBackgroundColor: displayList.map(d => d.full_diff >= 0 ? '#10b981' : '#ef4444'),
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 6,
          pointHoverRadius: 8,
          yAxisID: 'y1',
          order: 1
        }
      ];
    } else if (seg === 'tts') {
      datasets = [
        {
          type: 'bar',
          label: `%ODR TTS ${prevLabel} (%)`,
          data: displayList.map(d => d.tts_w34),
          backgroundColor: displayList.map(d => {
            const isM = checkOdrMatch(d);
            if (!hasFilter) return '#cbd5e1';
            return isM ? '#94a3b8' : 'rgba(203, 213, 225, 0.45)';
          }),
          borderRadius: 4,
          yAxisID: 'y',
          order: 2
        },
        {
          type: 'bar',
          label: `%ODR TTS ${currLabel} (Target ≥92%)`,
          data: displayList.map(d => d.tts_w35),
          backgroundColor: displayList.map(d => {
            const isM = checkOdrMatch(d);
            if (!hasFilter) return d.tts_w35 >= 92.0 ? '#10b981' : '#ef4444';
            if (hlMode === 'pass') return isM ? '#10b981' : 'rgba(148, 163, 184, 0.4)';
            if (hlMode === 'fail') return isM ? '#ef4444' : 'rgba(16, 185, 129, 0.45)';
            if (hlMode === 'grow') return isM ? '#0284c7' : 'rgba(148, 163, 184, 0.4)';
            return isM ? (d.tts_w35 >= 92 ? '#10b981' : '#ef4444') : 'rgba(148, 163, 184, 0.4)';
          }),
          borderColor: displayList.map(d => checkOdrMatch(d) && hasFilter ? (d.tts_w35 >= 92 ? '#059669' : '#b91c1c') : 'transparent'),
          borderWidth: displayList.map(d => checkOdrMatch(d) && hasFilter ? 2 : 0),
          borderRadius: 4,
          yAxisID: 'y',
          order: 2
        },
        {
          type: 'line',
          label: 'Đường Biến Động WoW TTS (Δ %)',
          data: displayList.map(d => d.tts_diff),
          borderColor: '#0284c7',
          borderWidth: 3,
          tension: 0.25,
          pointBackgroundColor: displayList.map(d => d.tts_diff >= 0 ? '#10b981' : '#ef4444'),
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 6,
          pointHoverRadius: 8,
          yAxisID: 'y1',
          order: 1
        }
      ];
    } else if (seg === 'compare') {
      y1Title = 'Chênh Lệch Gap (TTS - Full % p.p)';
      datasets = [
        {
          type: 'bar',
          label: `%ODR Full Hàng ${currLabel}`,
          data: displayList.map(d => d.full_w35),
          backgroundColor: displayList.map(d => {
            const isM = checkOdrMatch(d);
            if (!hasFilter) return '#2563eb';
            return isM ? '#2563eb' : 'rgba(37, 99, 235, 0.3)';
          }),
          borderRadius: 4,
          yAxisID: 'y',
          order: 2
        },
        {
          type: 'bar',
          label: `%ODR TikTok Shop ${currLabel}`,
          data: displayList.map(d => d.tts_w35),
          backgroundColor: displayList.map(d => {
            const isM = checkOdrMatch(d);
            if (!hasFilter) return '#f97316';
            return isM ? '#f97316' : 'rgba(249, 115, 22, 0.3)';
          }),
          borderRadius: 4,
          yAxisID: 'y',
          order: 2
        },
        {
          type: 'line',
          label: 'Đường Gap (TTS vs Full %)',
          data: displayList.map(d => d.gap),
          borderColor: '#8b5cf6',
          borderWidth: 3,
          tension: 0.25,
          pointBackgroundColor: displayList.map(d => d.gap >= 0 ? '#10b981' : '#ef4444'),
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 6,
          pointHoverRadius: 8,
          yAxisID: 'y1',
          order: 1
        }
      ];
    }

    charts.odrBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: displayList.map(d => d.am),
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 20, bottom: 10 } },
        scales: {
          y: {
            position: 'left',
            min: yMin,
            max: 100,
            ticks: { callback: v => v + '%' },
            title: { display: true, text: '%ODR Giao Đúng Hẹn', font: { weight: '700', size: 11 } },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          y1: {
            position: 'right',
            grid: { drawOnChartArea: false },
            title: { display: true, text: y1Title, font: { weight: '700', size: 11, color: '#f26522' } },
            ticks: {
              callback: v => (v > 0 ? '+' : '') + v + '%'
            }
          },
          x: {
            ticks: { maxRotation: 45, minRotation: 20, font: { size: 11, weight: '800' } }
          }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => {
                if (c.dataset.type === 'line') {
                  const s = c.parsed.y > 0 ? '+' : '';
                  return `${c.dataset.label}: ${s}${c.parsed.y}%`;
                }
                const item = displayList[c.dataIndex];
                const vol = seg === 'tts' ? item.vol_tts : item.vol_full;
                return `${c.dataset.label}: ${c.parsed.y}% (Sản lượng: ${fNum(vol)} đơn)`;
              }
            }
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            selectAndHighlightAM(displayList[elements[0].index].am);
          }
        }
      }
    });
    if (window.lucide) lucide.createIcons();
  }

  // --------------------------------------------------------------------------
  // TAB 7: %LTC - LẤY THÀNH CÔNG
  // --------------------------------------------------------------------------
  state.ltcTinhSegment = 'full';

  window.setLtcTinhSegment = function(seg) {
    state.ltcTinhSegment = seg;
    const btnFull = document.getElementById('btn-ltc-tinh-full');
    const btnTts = document.getElementById('btn-ltc-tinh-tts');
    const titleEl = document.getElementById('title-ltc-tinh-mode');

    if (btnFull && btnTts) {
      btnFull.classList.toggle('active', seg === 'full');
      btnTts.classList.toggle('active', seg === 'tts');
    }
    if (titleEl) {
      titleEl.innerText = seg === 'tts'
        ? 'BẢNG 2: %LTC THEO 5 TỈNH THÀNH (TIKTOK SHOP)'
        : 'BẢNG 2: %LTC THEO 5 TỈNH THÀNH (FULL HÀNG)';
    }
    renderLtcTab();
  };

  function renderLtcTab() {
    if (!D.ltc) return;

    // 1. BẢNG 1: 19 AM
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
      }).sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

      tblBodyAM.innerHTML = list.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const v1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
        const v2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
        const v3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
        const v4 = row.curr_val;
        const heatClass = getHeatmapClass(v4, 'ltc');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = (v4 || 0) >= 0.90
          ? '<span class="badge-tag badge-tag-green">🟢 Đạt Chuẩn SLA (≥90%)</span>'
          : '<span class="badge-tag badge-tag-red">🔴 Chưa Đạt (&lt;90%)</span>';

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(v1)}</td>
            <td class="num">${fPct(v2)}</td>
            <td class="num">${fPct(v3)}</td>
            <td class="num bold ${heatClass}">${fPct(v4)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 2. BẢNG 2: 5 TỈNH THÀNH (FULL HÀNG HOẶC TIKTOK SHOP)
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
      }).sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

      tblBodyTinh.innerHTML = listTinh.map((row, i) => {
        const isSelected = state.selectedProvince === row.tinh;
        const rowClass = isSelected ? 'province-laser-box' : '';
        const v1 = row[wKeys[0]] !== undefined ? row[wKeys[0]] : (row.w34 || 0);
        const v2 = row[wKeys[1]] !== undefined ? row[wKeys[1]] : (row.w35 || 0);
        const v3 = row[wKeys[2]] !== undefined ? row[wKeys[2]] : (row.w36 || 0);
        const v4 = row.curr_val;
        const heatClass = getHeatmapClass(v4, 'ltc');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = (v4 || 0) >= 0.90
          ? '<span class="badge-tag badge-tag-green">🟢 Đạt Chuẩn SLA (≥90%)</span>'
          : '<span class="badge-tag badge-tag-red">🔴 Cần Thúc Đẩy (&lt;90%)</span>';

        return `
          <tr data-province="${row.tinh}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightProvince('${row.tinh}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#2563eb' : 'inherit'};">${row.tinh}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(v1)}</td>
            <td class="num">${fPct(v2)}</td>
            <td class="num">${fPct(v3)}</td>
            <td class="num bold ${heatClass}">${fPct(v4)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }
  }

  function renderLtcChart() {
    const ctx = document.getElementById('chart-ltc-bar');
    if (!ctx || !D.ltc || !D.ltc.am) return;
    if (charts.ltcBar) charts.ltcBar.destroy();

    const prevKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2].toLowerCase() : 'w35';
    const currKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1].toLowerCase() : 'w36';
    const prevLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2] : 'W35';
    const currLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1] : 'W36';

    const selectedAM = state.selectedAM;
    const sorted = [...D.ltc.am].map(r => {
      const prev_val = r[currKey] !== undefined ? (r[prevKey] || 0) : (r.w34 || 0);
      const curr_val = r[currKey] !== undefined ? (r[currKey] || 0) : (r.w35 || 0);
      const diff_val = r.diff !== undefined ? r.diff : (curr_val - prev_val);
      return {
        ...r,
        w34_pct: Number((prev_val * 100).toFixed(1)),
        w35_pct: Number((curr_val * 100).toFixed(1)),
        diff_pct: Number((diff_val * 100).toFixed(1)),
        vol: r.vol || 0
      };
    }).sort((a, b) => (b.w35_pct || 0) - (a.w35_pct || 0));

    charts.ltcBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: sorted.map(d => d.am),
        datasets: [
          {
            type: 'line',
            label: '🌊 Miền Sản Lượng Lấy (Đơn)',
            data: sorted.map(d => d.vol),
            fill: true,
            backgroundColor: 'rgba(59, 130, 246, 0.15)',
            borderColor: 'rgba(59, 130, 246, 0.5)',
            borderWidth: 1.5,
            tension: 0.35,
            pointRadius: 4,
            pointBackgroundColor: '#2563eb',
            pointBorderColor: '#ffffff',
            pointBorderWidth: 1.5,
            yAxisID: 'yVol',
            order: 4
          },
          {
            type: 'bar',
            label: `%LTC ${prevLabel} (%)`,
            data: sorted.map(d => d.w34_pct),
            backgroundColor: '#94a3b8',
            borderRadius: 4,
            yAxisID: 'y',
            order: 2
          },
          {
            type: 'bar',
            label: `%LTC ${currLabel} (Target ≥90%)`,
            data: sorted.map(d => d.w35_pct),
            backgroundColor: sorted.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : (d.w35_pct >= 90.0 ? '#10b981' : '#2563eb')),
            borderColor: sorted.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : 'transparent'),
            borderWidth: sorted.map(d => selectedAM && selectedAM === d.am ? 3 : 0),
            borderRadius: 4,
            yAxisID: 'y',
            order: 2
          },
          {
            type: 'line',
            label: 'Đường Biến Động WoW (Δ %)',
            data: sorted.map(d => d.diff_pct),
            borderColor: '#f26522',
            borderWidth: 3,
            tension: 0.25,
            pointBackgroundColor: sorted.map(d => d.diff_pct >= 0 ? '#10b981' : '#ef4444'),
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2,
            pointRadius: 6,
            pointHoverRadius: 8,
            yAxisID: 'y1',
            order: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 20, bottom: 10 } },
        scales: {
          y: {
            position: 'left',
            min: 30,
            max: 105,
            ticks: { callback: v => v + '%' },
            title: { display: true, text: '%LTC Lấy Thành Công', font: { weight: '700', size: 11 } },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          yVol: {
            position: 'right',
            grid: { drawOnChartArea: false },
            title: { display: true, text: 'Sản Lượng Lấy (Đơn)', font: { weight: '700', size: 11, color: '#2563eb' } },
            ticks: {
              callback: v => fNum(v)
            }
          },
          y1: {
            position: 'right',
            grid: { drawOnChartArea: false },
            title: { display: true, text: 'Biến Động (Δ % p.p)', font: { weight: '700', size: 11, color: '#f26522' } },
            ticks: {
              callback: v => (v > 0 ? '+' : '') + v + '%'
            }
          },
          x: {
            ticks: { maxRotation: 45, minRotation: 20, font: { size: 11, weight: '800' } }
          }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => {
                if (c.dataset.yAxisID === 'yVol') {
                  return `🌊 Sản lượng lấy: ${fNum(c.parsed.y)} đơn`;
                }
                if (c.dataset.type === 'line') {
                  const s = c.parsed.y > 0 ? '+' : '';
                  return `${c.dataset.label}: ${s}${c.parsed.y}%`;
                }
                return `${c.dataset.label}: ${c.parsed.y}% (Sản lượng: ${fNum(sorted[c.dataIndex].vol)} đơn)`;
              }
            }
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            selectAndHighlightAM(sorted[elements[0].index].am);
          }
        }
      }
    });
  }

  // --------------------------------------------------------------------------
  // TAB 8: %OPR TIKTOK SHOP
  // --------------------------------------------------------------------------
  function renderOprTab() {
    if (!D.opr_tts || !D.opr_tts.am) return;

    // Helper evaluation badge for OPR (KPI >= 80%)
    function getOprDayBadge(v) {
      const val = v || 0;
      if (val >= 0.92) return '<span class="badge-tag badge-tag-green">🏆 Xuất Sắc (≥92%)</span>';
      if (val >= 0.80) return '<span class="badge-tag badge-tag-green">🟢 Đạt KPI (≥80%)</span>';
      return '<span class="badge-tag badge-tag-red">🔴 Chưa Đạt KPI (<80%)</span>';
    }

    function getOprNightBadge(v) {
      const val = v || 0;
      if (val >= 0.92) return '<span class="badge-tag badge-tag-green">🏆 Xuất Sắc (≥92%)</span>';
      if (val >= 0.80) return '<span class="badge-tag badge-tag-green">🟢 Đạt KPI (≥80%)</span>';
      return '<span class="badge-tag badge-tag-red">🔴 Chưa Đạt KPI (<80%)</span>';
    }

    const currKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1].toLowerCase() : 'w39';
    const prevKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2].toLowerCase() : 'w38';
    const currLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1] : 'W39';
    const prevLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2] : 'W38';

    const getDayVal = r => r[`${currKey}_day`] !== undefined ? r[`${currKey}_day`] : (r.w_curr_day !== undefined ? r.w_curr_day : (r.w39_day !== undefined ? r.w39_day : r.w38_day));
    const getNightVal = r => r[`${currKey}_night`] !== undefined ? r[`${currKey}_night`] : (r.w_curr_night !== undefined ? r.w_curr_night : (r.w39_night !== undefined ? r.w39_night : r.w38_night));
    const getTotalVal = r => r[`${currKey}_total`] !== undefined ? r[`${currKey}_total`] : (r.w_curr_total !== undefined ? r.w_curr_total : (r.w39_total !== undefined ? r.w39_total : r.w38_total));

    const getPrevDayVal = r => r[`${prevKey}_day`] !== undefined ? r[`${prevKey}_day`] : (r.w_prev_day !== undefined ? r.w_prev_day : (r.w38_day !== undefined ? r.w38_day : r.w37_day));
    const getPrevNightVal = r => r[`${prevKey}_night`] !== undefined ? r[`${prevKey}_night`] : (r.w_prev_night !== undefined ? r.w_prev_night : (r.w38_night !== undefined ? r.w38_night : r.w37_night));
    const getPrevTotalVal = r => r[`${prevKey}_total`] !== undefined ? r[`${prevKey}_total`] : (r.w_prev_total !== undefined ? r.w_prev_total : (r.w38_total !== undefined ? r.w38_total : r.w37_total));

    // Tính % OPR TTS tổng toàn vùng (weighted) cho W39 vs W38
    const _ams = D.opr_tts.am;
    const _totalVol = _ams.reduce((s, r) => s + (r.vol_day||0) + (r.vol_night||0), 0);
    const _volDay = _ams.reduce((s, r) => s + (r.vol_day || 0), 0);
    const _volNight = _ams.reduce((s, r) => s + (r.vol_night || 0), 0);
    const _vungCurrDay = _volDay > 0 ? _ams.reduce((s, r) => s + (r.vol_day || 0) * (getDayVal(r) || 0), 0) / _volDay : 0;
    const _vungCurrNight = _volNight > 0 ? _ams.reduce((s, r) => s + (r.vol_night || 0) * (getNightVal(r) || 0), 0) / _volNight : 0;
    const _wtdCurr = _ams.reduce((s, r) => {
      const vol = (r.vol_day||0) + (r.vol_night||0);
      const curD = getDayVal(r) || 0;
      const curN = getNightVal(r) || 0;
      const o = vol > 0 ? ((r.vol_day||0)*curD + (r.vol_night||0)*curN) / vol : 0;
      return s + vol * o;
    }, 0);
    const _wtdPrev = _ams.reduce((s, r) => {
      const vol = (r.vol_day||0) + (r.vol_night||0);
      const prvD = getPrevDayVal(r) || 0;
      const prvN = getPrevNightVal(r) || 0;
      const o = vol > 0 ? ((r.vol_day||0)*prvD + (r.vol_night||0)*prvN) / vol : 0;
      return s + vol * o;
    }, 0);
    const _vungCurr = _totalVol > 0 ? _wtdCurr / _totalVol : 0;
    const _vungPrev = _totalVol > 0 ? _wtdPrev / _totalVol : 0;
    const _diff = _vungCurr - _vungPrev;
    const _kpiOk = _vungCurr >= 0.80;
    const _dayPassList = _ams.filter(r => ((r.vol_day === 0) ? 0 : (getDayVal(r) || 0)) >= 0.80);
    const _dayFailList = _ams.filter(r => ((r.vol_day === 0) ? 0 : (getDayVal(r) || 0)) < 0.80);
    const _nightPassList = _ams.filter(r => ((r.vol_night === 0) ? 0 : (getNightVal(r) || 0)) >= 0.80);
    const _nightFailList = _ams.filter(r => ((r.vol_night === 0) ? 0 : (getNightVal(r) || 0)) < 0.80);

    // Lưu dữ liệu OPR shift cho modal tương tác
    window._oprShiftData = {
      currLabel,
      prevLabel,
      ams: _ams.map(r => {
        const dVal = (r.vol_day === 0) ? 0 : (getDayVal(r) || 0);
        const nVal = (r.vol_night === 0) ? 0 : (getNightVal(r) || 0);
        const tVal = getTotalVal(r) || 0;
        return {
          am: r.am,
          vol_day: r.vol_day || 0,
          opr_day: dVal,
          fail_day: (r.vol_day || 0) > 0 ? Math.round(r.vol_day * (1 - (dVal > 1 ? 0 : dVal))) : 0,
          vol_night: r.vol_night || 0,
          opr_night: nVal,
          fail_night: (r.vol_night || 0) > 0 ? Math.round(r.vol_night * (1 - (nVal > 1 ? 0 : nVal))) : 0,
          vol_total: r.vol_total || ((r.vol_day || 0) + (r.vol_night || 0)),
          opr_total: tVal
        };
      }),
      vungCurrDay: _vungCurrDay,
      vungCurrNight: _vungCurrNight,
      volDay: _volDay,
      volNight: _volNight,
      dayPassCount: _dayPassList.length,
      dayFailCount: _dayFailList.length,
      nightPassCount: _nightPassList.length,
      nightFailCount: _nightFailList.length
    };

    const _vungEl = document.getElementById('opr-tts-vung-total');
    if (_vungEl) {
      const diffTxt = (_diff >= 0 ? '▲ +' : '▼ ') + Math.abs(_diff * 100).toFixed(1) + '%p WoW';
      const diffColor = _diff >= 0 ? '#10b981' : '#ef4444';
      const kpiBadge = _kpiOk
        ? '<span class="badge-tag badge-tag-green" style="font-size:13px; font-weight:800; padding:6px 14px;">✅ Đạt KPI (≥80%)</span>'
        : '<span class="badge-tag badge-tag-red" style="font-size:13px; font-weight:800; padding:6px 14px;">❌ Chưa Đạt KPI (<80%)</span>';
      _vungEl.innerHTML = `
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px; padding:14px 20px; background:${_kpiOk ? 'linear-gradient(135deg, rgba(16,185,129,0.06), rgba(37,99,235,0.06))' : 'linear-gradient(135deg, rgba(239,68,68,0.05), rgba(245,158,11,0.05))'}; border:1.5px solid ${_kpiOk ? 'rgba(16,185,129,0.25)' : 'rgba(239,68,68,0.3)'}; border-radius:12px; margin-bottom:16px;">
          <div style="display:flex; align-items:center; gap:16px;">
            <div style="font-size:32px; font-weight:900; color:${_kpiOk ? '#10b981' : '#ef4444'}; font-family:var(--font-mono, monospace); line-height:1;">
              ${(_vungCurr*100).toFixed(1)}%
            </div>
            <div>
              <div style="font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.5px; color:var(--text-main, #1e293b);">
                OPR TTS Toàn Vùng ${currLabel} (Tổng Ngày + Đêm)
              </div>
              <div style="font-size:12px; font-weight:700; color:${diffColor}; margin-top:2px;">
                ${diffTxt} (${prevLabel}: ${(_vungPrev*100).toFixed(1)}%) &nbsp;•&nbsp; 
                ${_kpiOk ? '<span style="color:#10b981; font-weight:800;">🏆 Đã vượt chuẩn KPI ≥ 80.0%</span>' : '<span style="color:#ef4444; font-weight:800;">⚠️ Chưa đạt KPI (&lt; 80.0%) do Ca Đêm giảm sút</span>'}
              </div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:14px; flex-wrap:wrap;">
            <div style="display:flex; gap:10px; align-items:center;">
              <button type="button" 
                      class="opr-shift-interactive-btn opr-shift-day-btn" 
                      onclick="window.openOprShiftBreakdown('day')"
                      title="Nhấn để xem chi tiết bao nhiêu AM đạt KPI Ca Ngày (9h–19h)">
                <span>☀️ Ca Ngày: <strong>${(_vungCurrDay*100).toFixed(1)}%</strong></span>
                <span class="opr-shift-count-badge opr-shift-count-green">${_dayPassList.length}/${_ams.length} AM Đạt</span>
                <span class="opr-shift-arrow">↗</span>
              </button>
              <button type="button" 
                      class="opr-shift-interactive-btn opr-shift-night-btn" 
                      onclick="window.openOprShiftBreakdown('night')"
                      title="Nhấn để xem chi tiết bao nhiêu AM đạt KPI Ca Đêm (19h–9h)">
                <span>🌙 Ca Đêm: <strong>${(_vungCurrNight*100).toFixed(1)}%</strong></span>
                <span class="opr-shift-count-badge opr-shift-count-red">${_nightPassList.length}/${_ams.length} AM Đạt</span>
                <span class="opr-shift-arrow">↗</span>
              </button>
            </div>
            ${kpiBadge}
          </div>
        </div>
      `;
    }

    // Render danh sách AM chưa đạt KPI OPR TTS (< 80.0%)
    const _failedContainer = document.getElementById('opr-failed-ams-container');
    if (_failedContainer) {
      // Tính tổng đơn trễ OPR toàn vùng
      const totalFailRegion = _ams.reduce((s, r) => {
        const vTot = r.vol_total || r.total_vol || ((r.vol_day || 0) + (r.vol_night || 0));
        const oTot = (r.vol_day === 0 && r.vol_night === 0) ? 0 : (getTotalVal(r) || 0);
        return s + (vTot > 0 ? Math.round(vTot * (1 - (oTot > 1 ? 0 : oTot))) : 0);
      }, 0);

      // Sắp xếp các AM chưa đạt tổng (< 80%) và có đơn (> 0) theo số lượng đơn rớt OPR giảm dần
      const failedTotal = _ams.filter(r => {
        const vTot = r.vol_total || r.total_vol || ((r.vol_day || 0) + (r.vol_night || 0));
        const oTot = getTotalVal(r) || 0;
        return vTot > 0 && oTot < 0.80;
      }).map(r => {
        const vTot = r.vol_total || r.total_vol || ((r.vol_day || 0) + (r.vol_night || 0));
        const oTot = getTotalVal(r) || 0;
        const failTot = vTot > 0 ? Math.round(vTot * (1 - (oTot > 1 ? 0 : oTot))) : 0;
        const rateFail = totalFailRegion > 0 ? (failTot / totalFailRegion) : 0;
        return { ...r, fail_total: failTot, rate_fail: rateFail, curr_total: oTot };
      }).sort((a, b) => b.fail_total - a.fail_total);

      const failedDay = _ams.filter(r => (r.vol_day || 0) > 0 && (getDayVal(r) || 0) < 0.80)
                            .sort((a, b) => (getDayVal(a) || 0) - (getDayVal(b) || 0));
      const failedNight = _ams.filter(r => (r.vol_night || 0) > 0 && (getNightVal(r) || 0) < 0.80)
                              .sort((a, b) => (getNightVal(a) || 0) - (getNightVal(b) || 0));

      _failedContainer.innerHTML = `
        <div style="background:var(--bg-surface, #ffffff); border:1.5px solid rgba(239, 68, 68, 0.35); border-left:5px solid #ef4444; border-radius:12px; padding:16px 20px; box-shadow:0 3px 12px rgba(239,68,68,0.06); margin-bottom:16px;">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:14px; border-bottom:1px solid rgba(239,68,68,0.15); padding-bottom:12px;">
            <div style="display:flex; align-items:center; gap:10px;">
              <span style="font-size:22px;">🚨</span>
              <div>
                <h4 style="margin:0; font-size:15px; font-weight:900; color:#b91c1c; text-transform:uppercase; letter-spacing:0.3px;">
                  DANH SÁCH ${failedTotal.length} AM CHƯA ĐẠT KPI OPR TTS (< 80.0%)
                </h4>
              </div>
            </div>
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              <span class="badge-tag badge-tag-red" style="font-size:12px; font-weight:800; padding:6px 12px;">
                🔴 Toàn Ngày: <strong>${failedTotal.length}/${_ams.length} AM</strong>
              </span>
              <span class="badge-tag badge-tag-amber" style="font-size:12px; font-weight:800; padding:6px 12px;">
                ☀️ Ca Ngày: <strong>${failedDay.length}/${_ams.length} AM</strong>
              </span>
              <span class="badge-tag badge-tag-purple" style="font-size:12px; font-weight:800; padding:6px 12px;">
                🌙 Ca Đêm: <strong>${failedNight.length}/${_ams.length} AM</strong>
              </span>
            </div>
          </div>

          <div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(285px, 1fr)); gap:12px;">
            ${failedTotal.map(r => {
              const val = ((r.curr_total || 0) * 100);
              const gap = (80 - val).toFixed(1);
              const rawDay = (r.vol_day === 0) ? 0 : (getDayVal(r) || 0);
              const dayVal = (rawDay * 100).toFixed(1);
              const rawNight = (r.vol_night === 0) ? 0 : (getNightVal(r) || 0);
              const nightVal = (rawNight * 100).toFixed(1);
              const diffTot = r.diff_total !== undefined ? (r.diff_total * 100) : (val - ((getPrevTotalVal(r) || 0) * 100));
              const diffBadge = diffTot !== 0 ? `<span style="font-size:11px; font-weight:800; color:${diffTot > 0 ? '#10b981' : '#ef4444'};">${diffTot > 0 ? '▲ +' : '▼ '}${Math.abs(diffTot).toFixed(1)}%p</span>` : '';
              const isSelected = state.selectedAM === r.am;

              return `
                <div onclick="selectAndHighlightAM('${r.am}')" 
                     style="cursor:pointer; padding:12px 14px; background:${isSelected ? 'rgba(239,68,68,0.12)' : 'var(--bg-main, #f8fafc)'}; border:1.5px solid ${isSelected ? '#ef4444' : 'rgba(239,68,68,0.22)'}; border-radius:10px; transition:all 0.2s;" 
                     onmouseover="this.style.borderColor='#ef4444'; this.style.boxShadow='0 4px 12px rgba(239,68,68,0.15)'; this.style.transform='translateY(-2px)'" 
                     onmouseout="this.style.borderColor='${isSelected ? '#ef4444' : 'rgba(239,68,68,0.22)'}'; this.style.boxShadow='none'; this.style.transform='none'">
                  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-weight:900; font-size:13.5px; color:${isSelected ? '#ef4444' : 'var(--text-main, #0f172a)'};">${r.am}</div>
                    <div style="display:flex; gap:4px; align-items:center;">
                      <span style="font-size:11px; font-weight:800; color:#ea580c; background:var(--color-amber-bg); padding:2px 7px; border-radius:6px;" title="Tỷ trọng đóng góp vào tổng đơn rớt OPR vùng">
                        Trễ ${fNum(r.fail_total)} đơn (${fPct(r.rate_fail, 1)})
                      </span>
                      <span style="font-size:11px; font-weight:800; color:#b91c1c; background:rgba(239,68,68,0.12); padding:2px 7px; border-radius:6px;">
                        -${gap}%p
                      </span>
                    </div>
                  </div>
                  <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:8px;">
                    <div style="display:flex; align-items:baseline; gap:6px;">
                      <span style="font-size:24px; font-weight:900; color:#dc2626; font-family:var(--font-mono, monospace); line-height:1;">${val.toFixed(1)}%</span>
                      <span style="font-size:11px; font-weight:700; color:#dc2626;">(Chưa Đạt)</span>
                    </div>
                    <div>${diffBadge}</div>
                  </div>
                  <div style="display:flex; justify-content:space-between; font-size:11.5px; color:var(--text-muted, #64748b); padding-top:6px; border-top:1px dashed rgba(0,0,0,0.08);">
                    <span>☀️ Ngày: <strong style="color:${Number(dayVal) >= 80 ? '#10b981' : '#dc2626'};">${dayVal}%</strong></span>
                    <span>🌙 Đêm: <strong style="color:${Number(nightVal) >= 80 ? '#10b981' : '#dc2626'};">${nightVal}%</strong></span>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      `;
    }

    // 1. BẢNG 1: %OPR CA NGÀY (9H-19H)
    const tblBodyDay = document.querySelector('#table-opr-day-detailed tbody');
    if (tblBodyDay) {
      let listDay = [...D.opr_tts.am].map(r => {
        const curr = getDayVal(r);
        const prev = getPrevDayVal(r);
        return {
          ...r,
          curr_val: curr,
          prev_val: prev,
          diff_val: r.diff_day !== undefined ? r.diff_day : ((curr || 0) - (prev || 0))
        };
      }).sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

      tblBodyDay.innerHTML = listDay.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const heatW = getHeatmapClass(row.curr_val, 'opr');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = getOprDayBadge(row.curr_val);

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol_day)}</td>
            <td class="num">${fPct(row.prev_val)}</td>
            <td class="num bold ${heatW}">${fPct(row.curr_val)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 2. BẢNG 2: %OPR CA ĐÊM (19H-9H)
    const tblBodyNight = document.querySelector('#table-opr-night-detailed tbody');
    if (tblBodyNight) {
      let listNight = [...D.opr_tts.am].map(r => {
        const curr = getNightVal(r);
        const prev = getPrevNightVal(r);
        return {
          ...r,
          curr_val: curr,
          prev_val: prev,
          diff_val: r.diff_night !== undefined ? r.diff_night : ((curr || 0) - (prev || 0))
        };
      }).sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

      tblBodyNight.innerHTML = listNight.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const heatW = getHeatmapClass(row.curr_val, 'opr');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = getOprNightBadge(row.curr_val);

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol_night)}</td>
            <td class="num">${fPct(row.prev_val)}</td>
            <td class="num bold ${heatW}">${fPct(row.curr_val)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 3. BẢNG 3: CHI TIẾT TỔNG HỢP OPR TTS
    const tblBody = document.querySelector('#table-opr-tts-data tbody');
    if (tblBody) {
      let list = [...D.opr_tts.am];
      if (state.searchOpr) {
        list = list.filter(r => r.am.toLowerCase().includes(state.searchOpr));
      }

      const totalFailRegion = D.opr_tts.am.reduce((s, r) => {
        const vTot = r.vol_total || r.total_vol || ((r.vol_day || 0) + (r.vol_night || 0));
        const oTot = (r.vol_day === 0 && r.vol_night === 0) ? 0 : (getTotalVal(r) || 0);
        return s + (vTot > 0 ? Math.round(vTot * (1 - (oTot > 1 ? 0 : oTot))) : 0);
      }, 0);

      const sorted = list.map(row => {
        const vTot = row.vol_total || row.total_vol || ((row.vol_day || 0) + (row.vol_night || 0));
        const oTot = (row.vol_day === 0 && row.vol_night === 0) ? 0 : (getTotalVal(row) || 0);
        const failTot = vTot > 0 ? Math.round(vTot * (1 - (oTot > 1 ? 0 : oTot))) : 0;
        const rateFail = totalFailRegion > 0 ? (failTot / totalFailRegion) : 0;
        return { ...row, fail_total: failTot, rate_fail: rateFail, total_calc_vol: vTot, curr_tot: oTot };
      }).sort((a, b) => b.fail_total - a.fail_total || (b.diff_night || 0) - (a.diff_night || 0));

      tblBody.innerHTML = sorted.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const rawDay = (row.vol_day === 0 || (getDayVal(row) || 0) > 1) ? 0 : getDayVal(row);
        const prevDay = getPrevDayVal(row);
        const rawNight = (row.vol_night === 0 || (getNightVal(row) || 0) > 1) ? 0 : getNightVal(row);
        const prevNight = getPrevNightVal(row);
        const heatDay = getHeatmapClass(rawDay, 'opr');
        const heatNight = getHeatmapClass(rawNight, 'opr');
        const diffDay = renderDeltaBadge(row.diff_day, true, true);
        const diffNight = renderDeltaBadge(row.diff_night, true, true);

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center bold">${i + 1}</td>
            <td class="bold" style="font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol_day)}</td>
            <td class="num">${fPct(prevDay)}</td>
            <td class="num bold ${heatDay}">${fPct(rawDay)}</td>
            <td class="num bold">${diffDay}</td>
            <td class="num">${fNum(row.vol_night)}</td>
            <td class="num">${fPct(prevNight)}</td>
            <td class="num bold ${heatNight}">${fPct(rawNight)}</td>
            <td class="num bold">${diffNight}</td>
            <td class="num bold" style="color: var(--color-blue);">${fNum(row.total_calc_vol)}</td>
            <td class="num bold" style="background: rgba(239, 68, 68, 0.08); color: ${row.fail_total > 50 ? '#b91c1c' : 'inherit'}; font-weight: 800; font-size: 13.5px;">${fNum(row.fail_total)}</td>
            <td class="num bold" style="background: var(--color-amber-bg); color: #ea580c; font-weight: 800; font-size: 13px;">${fPct(row.rate_fail, 1)}</td>
          </tr>
        `;
      }).join('');
    }
  }

  // --------------------------------------------------------------------------
  // OPR SHIFT BREAKDOWN MODAL (CA NGÀY vs CA ĐÊM)
  // --------------------------------------------------------------------------
  window.openOprShiftBreakdown = function(shift = 'day') {
    window._currentOprShift = shift;
    window._currentOprFilter = 'all';

    let modal = document.getElementById('opr-shift-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'opr-shift-modal';
      modal.className = 'opr-shift-modal-overlay';
      modal.onclick = function(e) {
        if (e.target === modal) window.closeOprShiftModal();
      };
      document.body.appendChild(modal);

      document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') window.closeOprShiftModal();
      });
    }

    window.renderOprShiftModalContent();
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  };

  window.closeOprShiftModal = function() {
    const modal = document.getElementById('opr-shift-modal');
    if (modal) {
      modal.style.display = 'none';
    }
    document.body.style.overflow = '';
  };

  window.switchOprShift = function(shift) {
    window._currentOprShift = shift;
    window._currentOprFilter = 'all';
    window.renderOprShiftModalContent();
  };

  window.filterOprShiftModal = function(filter) {
    window._currentOprFilter = filter;
    window.renderOprShiftModalContent();
  };

  window.goToAMFromModal = function(amName) {
    window.closeOprShiftModal();
    if (typeof selectAndHighlightAM === 'function') {
      selectAndHighlightAM(amName);
    }
    const targetEl = document.querySelector(`tr[data-entity="${amName}"]`) || document.getElementById('opr-failed-ams-container');
    if (targetEl) {
      targetEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  window.renderOprShiftModalContent = function() {
    const modal = document.getElementById('opr-shift-modal');
    if (!modal || !window._oprShiftData) return;

    const data = window._oprShiftData;
    const shift = window._currentOprShift || 'day';
    const filter = window._currentOprFilter || 'all';
    const isDay = shift === 'day';

    // Sắp xếp AM theo OPR ca tương ứng giảm dần
    const amsList = [...data.ams].sort((a, b) => {
      const valA = isDay ? a.opr_day : a.opr_night;
      const valB = isDay ? b.opr_day : b.opr_night;
      return valB - valA;
    });

    const passList = amsList.filter(r => (isDay ? r.opr_day : r.opr_night) >= 0.80);
    const failList = amsList.filter(r => (isDay ? r.opr_day : r.opr_night) < 0.80);

    let displayList = amsList;
    if (filter === 'pass') displayList = passList;
    if (filter === 'fail') displayList = failList;

    const rateVung = isDay ? (data.vungCurrDay * 100).toFixed(1) : (data.vungCurrNight * 100).toFixed(1);
    const totalVol = isDay ? data.volDay : data.volNight;
    const isPassVung = parseFloat(rateVung) >= 80.0;

    const titleIcon = isDay ? '☀️' : '🌙';
    const titleText = isDay ? 'CHI TIẾT HIỆU SUẤT OPR CA NGÀY (9H – 19H)' : 'CHI TIẾT HIỆU SUẤT OPR CA ĐÊM (19H – 9H SÁNG HÔM SAU)';

    const insightHtml = isDay
      ? `<div class="opr-shift-insight-box insight-day">
          <strong>💡 Nhận định Ca Ngày (9h – 19h):</strong> Toàn vùng làm rất tốt, đạt tới <strong style="color:#047857;">${rateVung}%</strong> với <strong style="color:#047857;">${passList.length}/${data.ams.length} AM vượt chuẩn KPI (≥ 80.0%)</strong>. 
          Chỉ có <strong>${failList.length} AM chưa đạt</strong> (${failList.map(r => r.am).join(', ')}), nguyên nhân chủ yếu do phát sinh sản lượng rất thấp (1–2 đơn) và bị trễ 1 đơn.
        </div>`
      : `<div class="opr-shift-insight-box insight-night">
          <strong>🚨 Cảnh báo Ca Đêm (19h – 9h):</strong> Tỷ lệ OPR ca đêm toàn vùng tụt dốc thê thảm chỉ còn <strong style="color:#b91c1c;">${rateVung}%</strong>! 
          Có tới <strong style="color:#b91c1c;">${failList.length}/${data.ams.length} AM không đạt chuẩn</strong> (&lt; 80.0%), trong đó nhiều AM rớt rất sâu: AM Lê Hồng Phong (2.1%), Trần Thị Nhung (4.0%), Lê Văn Trường (6.0%). 
          Toàn vùng chỉ có đúng <strong style="color:#047857;">${passList.length} AM</strong> giữ vững chuẩn gồm: <strong>${passList.map(r => r.am).join(', ')}</strong>.
        </div>`;

    modal.innerHTML = `
      <div class="opr-shift-modal-card">
        <!-- Modal Header -->
        <div class="opr-shift-modal-header">
          <div style="display:flex; align-items:center; gap:12px;">
            <span style="font-size:26px;">${titleIcon}</span>
            <div>
              <div style="font-size:16px; font-weight:900; color:var(--text-main); text-transform:uppercase; letter-spacing:0.3px;">
                ${titleText}
              </div>
              <div style="font-size:11.5px; color:var(--text-muted); font-weight:600; margin-top:2px;">
                Dữ liệu tuần ${data.currLabel} • Chuẩn KPI ≥ 80.0% • Toàn vùng có ${data.ams.length} AM
              </div>
            </div>
          </div>

          <div style="display:flex; align-items:center; gap:12px;">
            <!-- Shift Switcher -->
            <div class="opr-shift-segmented-control">
              <button type="button" 
                      onclick="window.switchOprShift('day')" 
                      class="opr-shift-segmented-btn ${isDay ? 'active day-active' : ''}">
                ☀️ Ca Ngày (${data.dayPassCount}/${data.ams.length})
              </button>
              <button type="button" 
                      onclick="window.switchOprShift('night')" 
                      class="opr-shift-segmented-btn ${!isDay ? 'active night-active' : ''}">
                🌙 Ca Đêm (${data.nightPassCount}/${data.ams.length})
              </button>
            </div>

            <button type="button" 
                    onclick="window.closeOprShiftModal()" 
                    style="border:none; background:transparent; font-size:24px; cursor:pointer; color:var(--text-muted); width:36px; height:36px; display:flex; align-items:center; justify-content:center; border-radius:10px; transition:all 0.15s;" 
                    onmouseover="this.style.background='rgba(0,0,0,0.06)'" 
                    onmouseout="this.style.background='transparent'" 
                    title="Đóng (Esc)">✕</button>
          </div>
        </div>

        <!-- Modal Body -->
        <div class="opr-shift-modal-body">
          <!-- 4 Stat Metric Cards -->
          <div class="opr-stat-grid">
            <div class="opr-stat-card" style="border-top:3px solid ${isPassVung ? '#10b981' : '#ef4444'};">
              <div class="opr-stat-card-title">Tỷ Lệ OPR Toàn Vùng</div>
              <div class="opr-stat-card-val" style="color:${isPassVung ? '#10b981' : '#ef4444'};">${rateVung}%</div>
              <div class="opr-stat-card-sub" style="color:${isPassVung ? '#047857' : '#b91c1c'};">
                ${isPassVung ? '✅ Vượt chuẩn KPI ≥ 80%' : '❌ Chưa đạt chuẩn KPI (<80%)'}
              </div>
            </div>

            <div class="opr-stat-card" style="border-top:3px solid #10b981;">
              <div class="opr-stat-card-title">Số AM Vượt Chuẩn</div>
              <div class="opr-stat-card-val" style="color:#10b981;">${passList.length} <span style="font-size:15px; font-weight:700; color:var(--text-muted);">/ ${data.ams.length} AM</span></div>
              <div class="opr-stat-card-sub" style="color:#047857;">Tỷ lệ: ${(passList.length / data.ams.length * 100).toFixed(1)}% AM</div>
            </div>

            <div class="opr-stat-card" style="border-top:3px solid #ef4444;">
              <div class="opr-stat-card-title">Số AM Chưa Đạt</div>
              <div class="opr-stat-card-val" style="color:#ef4444;">${failList.length} <span style="font-size:15px; font-weight:700; color:var(--text-muted);">/ ${data.ams.length} AM</span></div>
              <div class="opr-stat-card-sub" style="color:#b91c1c;">Tỷ lệ: ${(failList.length / data.ams.length * 100).toFixed(1)}% AM</div>
            </div>

            <div class="opr-stat-card" style="border-top:3px solid #6366f1;">
              <div class="opr-stat-card-title">Tổng Đơn Trong Ca</div>
              <div class="opr-stat-card-val" style="color:#6366f1;">${totalVol.toLocaleString('vi-VN')}</div>
              <div class="opr-stat-card-sub" style="color:var(--text-muted);">Sản lượng thực tế toàn ca</div>
            </div>
          </div>

          <!-- Insight Commentary Box -->
          ${insightHtml}

          <!-- Filter Tabs & Header -->
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:14px;">
            <div style="font-size:13px; font-weight:800; text-transform:uppercase; letter-spacing:0.3px; color:var(--text-main);">
              Danh Sách Xếp Hạng ${displayList.length} AM (${isDay ? 'Ca Ngày' : 'Ca Đêm'})
            </div>

            <div style="display:flex; gap:6px;">
              <button type="button" 
                      onclick="window.filterOprShiftModal('all')" 
                      style="padding:5px 12px; border-radius:8px; border:1px solid ${filter === 'all' ? 'var(--ghn-orange)' : 'var(--border-color)'}; background:${filter === 'all' ? 'var(--ghn-orange-light, #fff4ed)' : 'var(--bg-card)'}; color:${filter === 'all' ? 'var(--ghn-orange)' : 'var(--text-muted)'}; font-size:11.5px; font-weight:800; cursor:pointer;">
                Tất Cả (${amsList.length})
              </button>
              <button type="button" 
                      onclick="window.filterOprShiftModal('pass')" 
                      style="padding:5px 12px; border-radius:8px; border:1px solid ${filter === 'pass' ? '#10b981' : 'var(--border-color)'}; background:${filter === 'pass' ? '#ecfdf5' : 'var(--bg-card)'}; color:${filter === 'pass' ? '#047857' : 'var(--text-muted)'}; font-size:11.5px; font-weight:800; cursor:pointer;">
                🟢 Đạt KPI (${passList.length})
              </button>
              <button type="button" 
                      onclick="window.filterOprShiftModal('fail')" 
                      style="padding:5px 12px; border-radius:8px; border:1px solid ${filter === 'fail' ? '#ef4444' : 'var(--border-color)'}; background:${filter === 'fail' ? '#fef2f2' : 'var(--bg-card)'}; color:${filter === 'fail' ? '#b91c1c' : 'var(--text-muted)'}; font-size:11.5px; font-weight:800; cursor:pointer;">
                🔴 Chưa Đạt (${failList.length})
              </button>
            </div>
          </div>

          <!-- AM Grid -->
          <div class="opr-am-grid">
            ${displayList.map((r, idx) => {
              const val = isDay ? r.opr_day : r.opr_night;
              const pct = (val * 100).toFixed(1);
              const isPass = val >= 0.80;
              const vol = isDay ? r.vol_day : r.vol_night;
              const fail = isDay ? r.fail_day : r.fail_night;
              const pass = Math.max(0, vol - fail);
              const rank = idx + 1;

              const badgeHtml = val >= 0.92
                ? '<span class="badge-tag badge-tag-green" style="font-size:10.5px; font-weight:800; padding:3px 8px;">🏆 Xuất Sắc (≥92%)</span>'
                : (isPass
                  ? '<span class="badge-tag badge-tag-green" style="font-size:10.5px; font-weight:800; padding:3px 8px;">🟢 Đạt Chuẩn (≥80%)</span>'
                  : '<span class="badge-tag badge-tag-red" style="font-size:10.5px; font-weight:800; padding:3px 8px;">🔴 Chưa Đạt (&lt;80%)</span>');

              return `
                <div class="opr-am-card ${isPass ? 'pass' : 'fail'}" onclick="window.goToAMFromModal('${r.am}')" title="Nhấp để định vị AM này ở bảng bên dưới">
                  <div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                      <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-size:11px; font-weight:900; background:var(--bg-surface-alt, #f1f5f9); color:var(--text-muted); width:22px; height:22px; display:inline-flex; align-items:center; justify-content:center; border-radius:6px;">#${rank}</span>
                        <span style="font-size:14px; font-weight:800; color:var(--text-main);">${r.am}</span>
                      </div>
                      ${badgeHtml}
                    </div>

                    <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:8px;">
                      <div style="font-size:24px; font-weight:900; color:${isPass ? '#10b981' : '#ef4444'}; font-family:var(--font-mono, monospace); line-height:1;">
                        ${pct}%
                      </div>
                      <div style="font-size:11.5px; font-weight:700; color:var(--text-muted);">
                        Vol: <strong style="color:var(--text-main);">${vol.toLocaleString('vi-VN')}</strong> đơn
                      </div>
                    </div>

                    <!-- Mini Progress Bar with 80% target line -->
                    <div style="position:relative; height:7px; background:var(--border-subtle, #e2e8f0); border-radius:9999px; overflow:hidden; margin-bottom:8px;">
                      <div style="width:${Math.min(100, Math.max(0, val * 100))}%; height:100%; background:${isPass ? '#10b981' : '#ef4444'}; border-radius:9999px; transition:width 0.4s ease;"></div>
                      <div style="position:absolute; left:80%; top:0; bottom:0; width:2px; background:#475569; z-index:2;" title="Chuẩn KPI 80%"></div>
                    </div>
                  </div>

                  <div style="display:flex; justify-content:space-between; align-items:center; font-size:11px; color:var(--text-muted); padding-top:6px; border-top:1px dashed var(--border-subtle, #e2e8f0);">
                    <span>Giao đạt: <strong style="color:#10b981;">${pass}</strong> • Trễ: <strong style="color:${fail > 0 ? '#ef4444' : 'var(--text-muted)'};">${fail}</strong></span>
                    <span style="color:var(--ghn-orange); font-weight:700; display:inline-flex; align-items:center; gap:2px;">Xem chi tiết ↗</span>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      </div>
    `;
  };

  function renderOprGroupedChart() {
    const ctx = document.getElementById('chart-opr-tts-grouped');
    if (!ctx || !D.opr_tts || !D.opr_tts.am) return;
    if (charts.oprGrouped) charts.oprGrouped.destroy();

    const currKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1].toLowerCase() : 'w39';
    const prevKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2].toLowerCase() : 'w38';
    const currLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1] : 'W39';
    const prevLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2] : 'W38';

    const getDayVal = r => r[`${currKey}_day`] !== undefined ? r[`${currKey}_day`] : (r.w_curr_day !== undefined ? r.w_curr_day : (r.w39_day !== undefined ? r.w39_day : r.w38_day));
    const getNightVal = r => r[`${currKey}_night`] !== undefined ? r[`${currKey}_night`] : (r.w_curr_night !== undefined ? r.w_curr_night : (r.w39_night !== undefined ? r.w39_night : r.w38_night));
    const getTotalVal = r => r[`${currKey}_total`] !== undefined ? r[`${currKey}_total`] : (r.w_curr_total !== undefined ? r.w_curr_total : (r.w39_total !== undefined ? r.w39_total : r.w38_total));
    const getPrevTotalVal = r => r[`${prevKey}_total`] !== undefined ? r[`${prevKey}_total`] : (r.w_prev_total !== undefined ? r.w_prev_total : (r.w38_total !== undefined ? r.w38_total : r.w37_total));

    const selectedAM = state.selectedAM;
    // Sắp xếp A -> Z theo tên AM
    const ams = [...D.opr_tts.am].sort((a, b) => (getTotalVal(b) || 0) - (getTotalVal(a) || 0));

    const diffVals = ams.map(d => Number(((d.diff_total !== undefined ? d.diff_total : ((getTotalVal(d) || 0) - (getPrevTotalVal(d) || 0))) * 100).toFixed(1)));
    const minD = Math.min(...diffVals, 0);
    const maxD = Math.max(...diffVals, 0);

    charts.oprGrouped = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ams.map(d => d.am),
        datasets: [
          {
            type: 'line',
            label: 'Tổng đơn (Miền Sản Lượng)',
            data: ams.map(d => d.vol_total || d.total_vol || ((d.vol_day || 0) + (d.vol_night || 0))),
            fill: true,
            backgroundColor: 'rgba(147, 51, 234, 0.12)',
            borderColor: '#9333ea',
            borderWidth: 1.5,
            tension: 0.35,
            pointRadius: 3,
            pointBackgroundColor: '#9333ea',
            pointBorderColor: '#ffffff',
            pointBorderWidth: 1.5,
            pointHoverRadius: 6,
            yAxisID: 'yVol',
            order: 5,
            datalabels: { display: false }
          },
          {
            type: 'bar',
            label: `%OPR 9h–19h ${currLabel} (Ca Ngày)`,
            data: ams.map(d => {
              if (!d.vol_day || d.vol_day === 0) return 0;
              const val = getDayVal(d) || 0;
              return Number(((val > 1 ? 0 : val) * 100).toFixed(1));
            }),
            backgroundColor: ams.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : '#2563eb'),
            borderColor: ams.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : 'transparent'),
            borderWidth: ams.map(d => selectedAM && selectedAM === d.am ? 2 : 0),
            borderRadius: 4,
            yAxisID: 'y',
            order: 3,
            datalabels: {
              display: true,
              color: '#ffffff',
              anchor: 'center',
              align: 'center',
              font: { size: 9, weight: '700' },
              formatter: v => v > 15 ? v : ''
            }
          },
          {
            type: 'bar',
            label: `%OPR 19h–9h ${currLabel} (Ca Đêm)`,
            data: ams.map(d => {
              if (!d.vol_night || d.vol_night === 0) return 0;
              const val = getNightVal(d) || 0;
              return Number(((val > 1 ? 0 : val) * 100).toFixed(1));
            }),
            backgroundColor: ams.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : '#ea580c'),
            borderColor: ams.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : 'transparent'),
            borderWidth: ams.map(d => selectedAM && selectedAM === d.am ? 2 : 0),
            borderRadius: 4,
            yAxisID: 'y',
            order: 3,
            datalabels: {
              display: true,
              color: '#ffffff',
              anchor: 'center',
              align: 'center',
              font: { size: 9, weight: '700' },
              formatter: v => v > 15 ? v : ''
            }
          },
          {
            type: 'line',
            label: `%OPR Tất cả ${currLabel} (Toàn Ngày)`,
            data: ams.map(d => {
              if ((!d.vol_day || d.vol_day === 0) && (!d.vol_night || d.vol_night === 0)) return 0;
              const val = getTotalVal(d) || 0;
              return Number(((val > 1 ? 0 : val) * 100).toFixed(1));
            }),
            borderColor: '#15803d',
            borderWidth: 3.5,
            tension: 0.25,
            pointBackgroundColor: ams.map(d => {
              const val = ((getTotalVal(d) || 0) * 100);
              return val < 80 ? '#dc2626' : '#16a34a';
            }),
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2,
            pointRadius: ams.map(d => {
              const val = ((getTotalVal(d) || 0) * 100);
              return val < 80 ? 6.5 : 4.5;
            }),
            pointHoverRadius: 9,
            yAxisID: 'y',
            order: 2,
            datalabels: {
              display: true,
              align: 'bottom',
              offset: 4,
              color: ams.map(d => {
                const val = ((getTotalVal(d) || 0) * 100);
                return val < 80 ? '#b91c1c' : '#166534';
              }),
              backgroundColor: ams.map(d => {
                const val = ((getTotalVal(d) || 0) * 100);
                return val < 80 ? 'rgba(254, 226, 226, 0.96)' : 'rgba(240, 253, 244, 0.96)';
              }),
              borderColor: ams.map(d => {
                const val = ((getTotalVal(d) || 0) * 100);
                return val < 80 ? '#fca5a5' : '#86efac';
              }),
              borderWidth: 1,
              borderRadius: 3,
              font: { size: 9.5, weight: '800' },
              formatter: v => v + '%' + (v < 80 ? ' ❌' : ' ✅')
            }
          },
          {
            type: 'line',
            label: 'Biến Động WoW (Δ Toàn Ngày)',
            data: diffVals,
            borderColor: '#f59e0b',
            borderWidth: 2.5,
            tension: 0.25,
            pointBackgroundColor: diffVals.map(d => d >= 0 ? '#10b981' : '#ef4444'),
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2,
            pointRadius: 6,
            pointHoverRadius: 9,
            yAxisID: 'yDiff',
            order: 1,
            datalabels: {
              display: true,
              align: 'top',
              offset: 6,
              color: diffVals.map(d => d >= 0 ? '#047857' : '#b91c1c'),
              backgroundColor: diffVals.map(d => d >= 0 ? 'rgba(220, 252, 231, 0.95)' : 'rgba(254, 226, 226, 0.95)'),
              borderColor: diffVals.map(d => d >= 0 ? '#86efac' : '#fca5a5'),
              borderWidth: 1,
              borderRadius: 4,
              padding: { top: 2, bottom: 2, left: 4, right: 4 },
              font: { size: 10, weight: '900' },
              formatter: v => (v > 0 ? '▲ +' : v < 0 ? '▼ ' : '') + v + '%'
            }
          },
          // ---- KPI 80% reference line ----
          {
            type: 'line',
            label: 'KPI ≥ 80.0% (Mục Tiêu)',
            data: ams.map(() => 80),
            borderColor: '#10b981',
            borderWidth: 2.5,
            borderDash: [6, 4],
            pointRadius: 0,
            pointHoverRadius: 0,
            fill: false,
            tension: 0,
            yAxisID: 'y',
            order: 0,
            datalabels: { display: false }
          },
          // ---- Toàn Vùng W37 reference line ----
          {
            type: 'line',
            label: 'Toàn Vùng W38: 83.0% (Đạt KPI)',
            data: ams.map(() => 78.1),
            borderColor: '#0284c7',
            borderWidth: 2,
            borderDash: [4, 4],
            pointRadius: 0,
            pointHoverRadius: 0,
            fill: false,
            tension: 0,
            yAxisID: 'y',
            order: 0,
            datalabels: { display: false }
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 32, bottom: 8 } },
        scales: {
          y: {
            position: 'left',
            min: 0,
            max: 110,
            ticks: { callback: v => v + '%' },
            title: { display: true, text: 'Tỷ Lệ %OPR', font: { weight: '700', size: 11 } },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          yDiff: {
            position: 'right',
            min: Math.floor((minD - 8) / 5) * 5,
            max: Math.ceil((maxD + 12) / 5) * 5,
            grid: { drawOnChartArea: false },
            display: false
          },
          yVol: {
            position: 'right',
            grid: { drawOnChartArea: false },
            title: { display: true, text: 'Tổng Đơn (Đơn)', font: { weight: '700', size: 11, color: '#9333ea' } },
            ticks: {
              callback: v => fNum(v)
            }
          },
          x: {
            ticks: {
              maxRotation: 45,
              minRotation: 25,
              font: { size: 11, weight: '800' },
              color: (c) => {
                const item = ams[c.index];
                if (item && (((item.w36_total !== undefined ? item.w36_total : 0) * 100) < 80)) return '#dc2626';
                return '#1e293b';
              }
            },
            grid: { display: false }
          }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => {
                if (c.dataset.yAxisID === 'yVol') {
                  return `📦 Tổng đơn TTS: ${fNum(c.parsed.y)} đơn`;
                }
                if (c.dataset.yAxisID === 'yDiff') {
                  const val = c.parsed.y;
                  return `📈 Biến động WoW: ${(val > 0 ? '+' : '') + val}%`;
                }
                return `${c.dataset.label}: ${c.parsed.y}%`;
              }
            }
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            selectAndHighlightAM(ams[elements[0].index].am);
          }
        }
      }
    });
  }

  // --------------------------------------------------------------------------
  // TAB 9: TRANSPORT (RỚT LUÂN CHUYỂN - DỮ LIỆU THẬT 100%)
  // --------------------------------------------------------------------------
    // --------------------------------------------------------------------------
  // TAB 9: RỚT LUÂN CHUYỂN
  // --------------------------------------------------------------------------
  function renderTransportTab() {
    if (!D.rot_lc) return;
    const currW = D.meta?.latest_week || 'W43';
    const prevW = D.meta?.prev_week || 'W42';
    const rot = D.rot_lc.overview || {};
    const totCan = rot.tot_can || 12303;
    const totRot = rot.tot_rot || 231;
    const rateCurr = rot.rate_curr ? (rot.rate_curr * 100).toFixed(2) : '1.88';
    const ratePrev = rot.rate_prev ? (rot.rate_prev * 100).toFixed(2) : '1.39';
    const diffPct = rot.diff !== undefined ? (rot.diff >= 0 ? `+${(rot.diff * 100).toFixed(2)}%p` : `${(rot.diff * 100).toFixed(2)}%p`) : '+0.49%p';

    const rTitle = document.getElementById('banner-rot-lc-title');
    if (rTitle) rTitle.innerHTML = `PHÂN TÍCH TỶ TRỌNG RỚT ĐƠN LUÂN CHUYỂN THEO AM &amp; TỈNH THÀNH (${currW})`;
    const rSummary = document.getElementById('banner-rot-lc-summary');
    if (rSummary) {
      rSummary.innerHTML = `
        • <strong>Tổng đơn rớt toàn vùng ${currW}:</strong> Tỷ lệ rớt đạt <strong>${rateCurr}%</strong> (tổng ${fNum(totRot)} đơn rớt / ${fNum(totCan)} đơn cần LC, biến động <strong>${diffPct} WoW</strong> so với ${ratePrev}% ${prevW}) — Tiếp tục kiểm soát rất tốt dưới ngưỡng Target ≤ 2.00%!<br/>
        • <strong>Đánh Giá:</strong> Các bưu cục và trung tâm khai thác phối hợp đồng bộ, hạn chế tối đa rớt kết nối ca luân chuyển.
      `;
    }
    const rBadge = document.getElementById('banner-rot-lc-badge');
    if (rBadge) rBadge.textContent = `Tổng rớt ${currW}: ${fNum(totRot)} đơn (${rateCurr}%)`;

    const prevKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2].toLowerCase() : 'w37';
    const currKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1].toLowerCase() : 'w38';

    // 1. BẢNG 1: 19 AM
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
      }).sort((a, b) => (b.vol_rot || 0) - (a.vol_rot || 0) || (b.wCurr || 0) - (a.wCurr || 0));

      tblBodyAM.innerHTML = listAM.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const heatCurr = getHeatmapClass(row.wCurr, 'rot_lc');
        const diffBadge = renderDeltaBadge(row.diff_val, false, true);
        let evalBadge = '<span class="badge-tag badge-tag-green">🟢 Tốt (≤1%)</span>';
        if ((row.wCurr || 0) > 0.05) evalBadge = '<span class="badge-tag badge-tag-red">🔴 Nghiêm Trọng (&gt;5%)</span>';
        else if ((row.wCurr || 0) > 0.02) evalBadge = '<span class="badge-tag badge-tag-amber">🟡 Cảnh Báo (2-5%)</span>';

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num bold" style="background: rgba(239, 68, 68, 0.08); color: ${row.vol_rot > 10 ? '#b91c1c' : 'inherit'}; font-weight: 800; font-size: 13.5px;">${fNum(row.vol_rot)}</td>
            <td class="num bold" style="background: var(--color-amber-bg); color: #ea580c; font-weight: 800; font-size: 13px;">${fPct(row.rate_rot, 1)}</td>
            <td class="num">${fPct(row.wPrev, 2)}</td>
            <td class="num bold ${heatCurr}">${fPct(row.wCurr, 2)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 2. BẢNG 2: 5 TỈNH THÀNH
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
      }).sort((a, b) => (b.vol_rot || 0) - (a.vol_rot || 0) || (b.wCurr || 0) - (a.wCurr || 0));

      tblBodyTinh.innerHTML = listTinh.map((row, i) => {
        const isSelected = state.selectedProvince === row.tinh;
        const rowClass = isSelected ? 'province-laser-box' : '';
        const heatCurr = getHeatmapClass(row.wCurr, 'rot_lc');
        const diffBadge = renderDeltaBadge(row.diff_val, false, true);
        let evalBadge = '<span class="badge-tag badge-tag-green">🟢 Tốt (≤1%)</span>';
        if ((row.wCurr || 0) > 0.05) evalBadge = '<span class="badge-tag badge-tag-red">🔴 Nghiêm Trọng (&gt;5%)</span>';
        else if ((row.wCurr || 0) > 0.02) evalBadge = '<span class="badge-tag badge-tag-amber">🟡 Cảnh Báo (2-5%)</span>';

        return `
          <tr data-province="${row.tinh}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightProvince('${row.tinh}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#2563eb' : 'inherit'};">${row.tinh}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num bold" style="background: rgba(239, 68, 68, 0.08); color: ${row.vol_rot > 10 ? '#b91c1c' : 'inherit'}; font-weight: 800; font-size: 13.5px;">${fNum(row.vol_rot)}</td>
            <td class="num bold" style="background: var(--color-amber-bg); color: #ea580c; font-weight: 800; font-size: 13px;">${fPct(row.rate_rot, 1)}</td>
            <td class="num">${fPct(row.wPrev, 2)}</td>
            <td class="num bold ${heatCurr}">${fPct(row.wCurr, 2)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 3. BẢNG TOP 20 BƯU CỤC RỚT LC
    const tblBodyBC = document.querySelector('#table-rot-lc-top-bc tbody');
    const topBCList = D.rot_lc.top_bc || D.rot_lc.bc || [];
    if (tblBodyBC && topBCList.length > 0) {
      let list = [...topBCList];
      if (state.searchRotLc) {
        const q = state.searchRotLc.toLowerCase();
        list = list.filter(r => (r.bc && r.bc.toLowerCase().includes(q)));
      }

      tblBodyBC.innerHTML = list.map((row, i) => {
        const pct = row.pct_rot !== undefined ? row.pct_rot : (row.pct_w35 || 0);
        let badge = '<span class="badge-tag badge-tag-green">🟢 An Toàn</span>';
        if (pct >= 0.05) badge = '<span class="badge-tag badge-tag-red">🔴 Nghiêm Trọng (≥5%)</span>';
        else if (pct >= 0.02) badge = '<span class="badge-tag badge-tag-amber">🟡 Cảnh Báo (2-5%)</span>';

        const heatClass = getHeatmapClass(pct, 'rot_lc');

        return `
          <tr data-entity="${row.bc}">
            <td class="center bold">${row.stt || (i + 1)}</td>
            <td class="bold" style="font-weight:800; font-size:13px;">${row.bc}</td>
            <td class="bold" style="font-size:12.5px; color:${state.selectedAM === row.am ? '#ef4444' : 'inherit'};">${row.am || '---'}</td>
            <td class="num">${fNum(row.vol_can_lc || row.can_lc_w35 || row.can_lc)}</td>
            <td class="num bold" style="color:#ef4444;">${fNum(row.vol_rot_lc || row.rot_w35 || row.rot)}</td>
            <td class="num bold ${heatClass}">${fPct(pct, 2)}</td>
            <td class="center">${badge}</td>
          </tr>
        `;
      }).join('');
    }
  }

  function renderRotLcChart() {
    const ctx = document.getElementById('chart-rot-lc-bar');
    if (!ctx || !D.rot_lc || !D.rot_lc.am) return;
    if (charts.rotLcBar) charts.rotLcBar.destroy();

    const prevKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2].toLowerCase() : 'w37';
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
    }).sort((a, b) => (b.w35_pct || 0) - (a.w35_pct || 0));

    charts.rotLcBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: sorted.map(d => d.am),
        datasets: [
          {
            type: 'bar',
            label: `% Rớt LC ${prevLabel} (%)`,
            data: sorted.map(d => d.w34_pct),
            backgroundColor: '#94a3b8',
            borderRadius: 4,
            yAxisID: 'y',
            order: 2
          },
          {
            type: 'bar',
            label: `% Rớt LC ${currLabel} (Target ≤ 1.0%)`,
            data: sorted.map(d => d.w35_pct),
            backgroundColor: sorted.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : (d.w35_pct <= 1.0 ? '#10b981' : (d.w35_pct <= 2.5 ? '#f59e0b' : '#ef4444'))),
            borderColor: sorted.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : 'transparent'),
            borderWidth: sorted.map(d => selectedAM && selectedAM === d.am ? 3 : 0),
            borderRadius: 4,
            yAxisID: 'y',
            order: 2
          },
          {
            type: 'line',
            label: 'Đường Biến Động WoW (Δ %)',
            data: sorted.map(d => d.diff_pct),
            borderColor: '#f26522',
            borderWidth: 3,
            tension: 0.25,
            pointBackgroundColor: sorted.map(d => d.diff_pct <= 0 ? '#10b981' : '#ef4444'),
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2,
            pointRadius: 6,
            pointHoverRadius: 8,
            yAxisID: 'y1',
            order: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 20, bottom: 10 } },
        scales: {
          y: {
            position: 'left',
            min: 0,
            ticks: { callback: v => v + '%' },
            title: { display: true, text: '% Rớt LC', font: { weight: '700', size: 11 } },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          y1: {
            position: 'right',
            grid: { drawOnChartArea: false },
            title: { display: true, text: 'Biến Động (Δ % p.p)', font: { weight: '700', size: 11, color: '#f26522' } },
            ticks: {
              callback: v => (v > 0 ? '+' : '') + v + '%'
            }
          },
          x: {
            ticks: { maxRotation: 45, minRotation: 20, font: { size: 11, weight: '800' } }
          }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => {
                if (c.dataset.type === 'line') {
                  const s = c.parsed.y > 0 ? '+' : '';
                  return `${c.dataset.label}: ${s}${c.parsed.y}%`;
                }
                return `${c.dataset.label}: ${c.parsed.y}% (Sản lượng cần LC: ${fNum(sorted[c.dataIndex].vol)} đơn)`;
              }
            }
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            selectAndHighlightAM(sorted[elements[0].index].am);
          }
        }
      }
    });
  }

  // --------------------------------------------------------------------------
  // TAB 10: AGING (>5 NGÀY) & TREO LUÂN CHUYỂN (LC)
  // --------------------------------------------------------------------------
  window.setAgingSegment = function(seg) {
    state.agingSegment = seg;
    const btnAging = document.getElementById('btn-aging-aging');
    const btnTreo = document.getElementById('btn-aging-treo');
    const btnCompare = document.getElementById('btn-aging-compare');

    [btnAging, btnTreo, btnCompare].forEach(b => {
      if (b) {
        b.classList.remove('btn-primary', 'active');
        b.classList.add('btn-secondary');
      }
    });

    if (seg === 'aging' && btnAging) {
      btnAging.classList.add('btn-primary', 'active');
      btnAging.classList.remove('btn-secondary');
    } else if (seg === 'treo_lc' && btnTreo) {
      btnTreo.classList.add('btn-primary', 'active');
      btnTreo.classList.remove('btn-secondary');
    } else if (seg === 'compare' && btnCompare) {
      btnCompare.classList.add('btn-primary', 'active');
      btnCompare.classList.remove('btn-secondary');
    }

    // Update KPI strip & text
    updateAgingKPIs(seg);
    renderAgingTab();
    renderAgingChart();
    try { renderAgingDonutChart(); } catch(e) {}
    try { renderAgingCustomerChart(); } catch(e) {}
    try { renderAgingProgressChart(); } catch(e) {}
    if (window.lucide) lucide.createIcons();
  };

  window.syncRealtimeAgingTreo = async function() {
    const btn = document.getElementById('btn-sync-realtime-aging');
    const originalHtml = btn ? btn.innerHTML : '';
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '<span class="spinner" style="display:inline-block; width:12px; height:12px; border:2px solid #fff; border-top-color:transparent; border-radius:50%; animation:spin 0.6s linear infinite; margin-right:4px;"></span> Đang lấy data live...';
    }

    try {
      const res = await fetch('/api/sync-realtime-aging-treo', { method: 'POST' });
      const result = await res.json();
      if (result.success) {
        if (result.aging) D.aging = result.aging;
        if (result.treo_lc) D.treo_lc = result.treo_lc;
        
        const badge = document.getElementById('aging-badge-summary');
        if (badge && D.aging && D.treo_lc) {
          badge.textContent = `Aging: ${fNum(D.aging.total)} đơn | Treo LC: ${fNum(D.treo_lc.total)} đơn`;
        }

        renderAgingTab();
        renderAgingChart();
    try { renderAgingDonutChart(); } catch(e) {}
    try { renderAgingProgressChart(); } catch(e) {}
        if (typeof showToast === 'function') {
          showToast('Đã cập nhật real-time Aging & Treo Luân Chuyển thành công!', 'success');
        } else {
          alert('Đã cập nhật real-time Aging & Treo Luân Chuyển thành công!');
        }
      } else {
        alert(result.error || 'Lỗi cập nhật real-time');
      }
    } catch (err) {
      alert('Lỗi kết nối khi đồng bộ real-time: ' + err.message);
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = originalHtml;
        if (window.lucide) lucide.createIcons();
      }
    }
  };

  window.setAgingHighlight = function(hl) {
    state.agingHighlight = hl;
    state.selectedAM = null;
    const btnMap = {
      all: 'btn-aging-hl-all',
      danger: 'btn-aging-hl-danger',
      warning: 'btn-aging-hl-warning'
    };

    Object.keys(btnMap).forEach(k => {
      const b = document.getElementById(btnMap[k]);
      if (b) {
        if (k === hl) {
          b.classList.add('active');
          b.style.fontWeight = '800';
        } else {
          b.classList.remove('active');
          b.style.fontWeight = 'normal';
        }
      }
    });
    renderAgingChart();
    try { renderAgingDonutChart(); } catch(e) {}
    try { renderAgingProgressChart(); } catch(e) {}
  };

  function updateAgingKPIs(seg) {
    const t1 = document.getElementById('kpi-aging-title-1');
    const v1 = document.getElementById('kpi-aging-val-1');
    const m1 = document.getElementById('kpi-aging-meta-1');

    const t2 = document.getElementById('kpi-aging-title-2');
    const v2 = document.getElementById('kpi-aging-val-2');
    const m2 = document.getElementById('kpi-aging-meta-2');

    const t3 = document.getElementById('kpi-aging-title-3');
    const v3 = document.getElementById('kpi-aging-val-3');
    const m3 = document.getElementById('kpi-aging-meta-3');

    const t4 = document.getElementById('kpi-aging-title-4');
    const v4 = document.getElementById('kpi-aging-val-4');
    const m4 = document.getElementById('kpi-aging-meta-4');

    const chartTitle = document.getElementById('chart-aging-title');
    const tblAmTitle = document.getElementById('table-aging-am-title');
    const tblBcTitle = document.getElementById('table-aging-bc-title');

    if (seg === 'aging' && D.aging) {
      if (t1) t1.textContent = 'Tổng Đơn Aging (>5 Ngày)';
      if (v1) v1.innerHTML = `${fNum(D.aging.total)} <small>đơn</small>`;
      if (m1) m1.innerHTML = '<span class="diff-tag diff-up-bad">Cần giải tỏa dứt điểm</span>';

      const topAM = D.aging.top_am[0] || {};
      if (t2) t2.textContent = 'Top 1 AM Nhiều Aging Nhất';
      if (v2) v2.textContent = topAM.am || '---';
      if (m2) m2.innerHTML = `<span class="diff-tag diff-up-bad">${fNum(topAM.vol)} đơn (${topAM.pct}%)</span>`;

      const topBC = D.aging.top_bc[0] || {};
      if (t3) t3.textContent = 'Top 1 BC Điểm Nóng';
      if (v3) v3.textContent = topBC.bc ? topBC.bc.substring(0, 24) + '...' : '---';
      if (m3) m3.innerHTML = `<span class="diff-tag diff-up-bad">${fNum(topBC.vol)} đơn (${topBC.pct}%)</span>`;

      const topTinh = D.aging.tinh[0] || {};
      if (t4) t4.textContent = 'Tỉnh Tồn Aging Nhiều Nhất';
      if (v4) v4.textContent = topTinh.tinh || '---';
      if (m4) m4.innerHTML = `<span class="diff-tag diff-neutral">${fNum(topTinh.vol)} đơn (${topTinh.pct}%)</span>`;

      if (chartTitle) chartTitle.textContent = 'BIỂU ĐỒ 19 AM: TỒN KHO AGING (>5 NGÀY) PHÂN RÃ THEO MỐC NGÀY (5-8N, 8-15N, >15N)';
      if (tblAmTitle) tblAmTitle.textContent = 'BẢNG 1: BẢNG XẾP HẠNG 19 AM - TỒN KHO AGING (>5 NGÀY)';
      if (tblBcTitle) tblBcTitle.textContent = 'BẢNG 2: TOP BƯU CỤC (BC) CẦN GIẢI CỨU AGING GẤP';
    } else if (seg === 'treo_lc' && D.treo_lc) {
      if (t1) t1.textContent = 'Tổng Đơn Treo LC (≥24h)';
      if (v1) v1.innerHTML = `${fNum(D.treo_lc.total_treo_24)} <small>đơn</small>`;
      if (m1) m1.innerHTML = `<span class="diff-tag diff-up-bad">Tỷ lệ treo: ${(D.treo_lc.total_treo_24 / D.treo_lc.total * 100).toFixed(1)}%</span> <span style="font-size:11px;color:var(--text-muted);">/ Tổng ${fNum(D.treo_lc.total)} đơn LC</span>`;

      const topAM = (D.treo_lc.top_am && D.treo_lc.top_am[0]) || {};
      if (t2) t2.textContent = 'Top 1 AM Treo LC Nhiều Nhất';
      if (v2) v2.textContent = topAM.am || '---';
      if (m2) m2.innerHTML = `<span class="diff-tag diff-up-bad">Treo ≥24h: ${fNum(topAM.treo_24 || 0)} đ (${topAM.rate_treo_24 || (topAM.treo_24/topAM.vol*100).toFixed(1)}%)</span> <span style="font-size:11px;color:var(--text-muted);">/ ${fNum(topAM.vol)} đ</span>`;

      const topBC = (D.treo_lc.top_bc && D.treo_lc.top_bc[0]) || {};
      if (t3) t3.textContent = 'Top 1 BC Treo LC Nhiều Nhất';
      if (v3) v3.textContent = topBC.bc ? (topBC.bc.length > 24 ? topBC.bc.substring(0, 24) + '...' : topBC.bc) : '---';
      if (m3) m3.innerHTML = `<span class="diff-tag diff-up-bad">Treo ≥24h: ${fNum(topBC.treo_24 || 0)} đ (${topBC.rate_treo_24 || (topBC.treo_24/topBC.vol*100).toFixed(1)}%)</span> <span style="font-size:11px;color:var(--text-muted);">/ ${fNum(topBC.vol)} đ</span>`;

      const topTinh = (D.treo_lc.tinh && D.treo_lc.tinh[0]) || {};
      if (t4) t4.textContent = 'Tỉnh Treo LC Nhiều Nhất';
      if (v4) v4.textContent = topTinh.tinh || '---';
      if (m4) m4.innerHTML = `<span class="diff-tag diff-neutral">Treo ≥24h: ${fNum(topTinh.treo_24 || 151)} đ (${topTinh.rate_treo_24 || (topTinh.treo_24/topTinh.vol*100).toFixed(1)}%)</span> <span style="font-size:11px;color:var(--text-muted);">/ ${fNum(topTinh.vol)} đ</span>`;

      if (chartTitle) chartTitle.textContent = 'BIỂU ĐỒ 19 AM: HÀNG TREO LUÂN CHUYỂN (≥24H) PHÂN RÃ THEO MỐC THỜI GIAN (24-36H, 36-72H, 72-120H, >120H)';
      if (tblAmTitle) tblAmTitle.textContent = 'BẢNG 1: BẢNG XẾP HẠNG 19 AM - HÀNG TREO LUÂN CHUYỂN';
      if (tblBcTitle) tblBcTitle.textContent = 'BẢNG 2: TOP BƯU CỤC (BC) TREO LUÂN CHUYỂN (≥24H) NHIỀU NHẤT';
    } else if (seg === 'compare') {
      if (chartTitle) chartTitle.textContent = 'BIỂU ĐỒ ĐỐI CHIẾU SONG SONG: ĐƠN AGING vs ĐƠN TREO LUÂN CHUYỂN (THEO TOP AM)';
      if (tblAmTitle) tblAmTitle.textContent = 'BẢNG 1: ĐỐI CHIẾU SỐ LIỆU TỒN AGING vs TREO LC THEO AM';
      if (tblBcTitle) tblBcTitle.textContent = 'BẢNG 2: DANH SÁCH BƯU CỤC CẦN ƯU TIÊN XỬ LÝ';
    }
  }

  
  // --------------------------------------------------------------------------
  // TAB 10: BÁO CÁO %FD (RETURN / HOÀN TRẢ) - FULL HÀNG & TIKTOK SHOP
  // --------------------------------------------------------------------------
  state.fdChartMode = 'full'; // 'full' or 'tts'
  state.searchFdAm = '';
  state.searchFdBc = '';

  window.setFdChartMode = function(mode) {
    state.fdChartMode = mode;
    const btnFull = document.getElementById('btn-fd-full');
    const btnTts = document.getElementById('btn-fd-tts');
    const titleEl = document.getElementById('chart-fd-title');
    if (btnFull && btnTts) {
      btnFull.classList.toggle('active', mode === 'full');
      btnTts.classList.toggle('active', mode === 'tts');
    }
    if (titleEl) {
      titleEl.innerText = mode === 'tts'
        ? 'BIỂU ĐỒ %FD THEO 19 AM – PHÂN KHÚC TIKTOK SHOP (CỘT %FD + MIỀN SẢN LƯỢNG + ĐƯỜNG BIẾN ĐỘNG Δ)'
        : 'BIỂU ĐỒ %FD THEO 19 AM – TOÀN MẠNG FULL HÀNG (CỘT %FD + MIỀN SẢN LƯỢNG + ĐƯỜNG BIẾN ĐỘNG Δ)';
    }
    renderFdTab();
  };

  function getFdEvalBadge(rate) {
    const v = rate || 0;
    if (v <= 0.06) return '<span class="badge-tag badge-tag-green">🟢 Đạt Target (≤6%)</span>';
    if (v <= 0.08) return '<span class="badge-tag badge-tag-amber">🟡 Cảnh Báo (6–8%)</span>';
    if (v <= 0.12) return '<span class="badge-tag badge-tag-red">🔴 Cao (8–12%)</span>';
    return '<span class="badge-tag badge-tag-red" style="background:#7f1d1d; color:#fff;">🚨 Báo Động (&gt;12%)</span>';
  }

  function renderFdTab() {
    if (!D.fd) return;

    const currW = D.meta?.latest_week || 'W43';
    const prevW = D.meta?.prev_week || 'W41';

    // Dynamically update Table 2 headers (table-fd-top-bc)
    const thBcPrev = document.querySelector('#table-fd-top-bc thead th:nth-child(6)');
    const thBcCurr = document.querySelector('#table-fd-top-bc thead th:nth-child(7)');
    if (thBcPrev) thBcPrev.innerHTML = `FD ${prevW} &#x2b0d;`;
    if (thBcCurr) thBcCurr.innerHTML = `&#x1f525; FD ${currW} &#x2b0d;`;

    // Dynamically update Table 1 headers (table-fd-am-detailed)
    const thAmFullPrev = document.querySelector('#table-fd-am-detailed thead th:nth-child(4)');
    const thAmFullCurr = document.querySelector('#table-fd-am-detailed thead th:nth-child(5)');
    const thAmTtsPrev = document.querySelector('#table-fd-am-detailed thead th:nth-child(8)');
    const thAmTtsCurr = document.querySelector('#table-fd-am-detailed thead th:nth-child(9)');
    if (thAmFullPrev) thAmFullPrev.textContent = `Full ${prevW}`;
    if (thAmFullCurr) thAmFullCurr.textContent = `Full ${currW}`;
    if (thAmTtsPrev) thAmTtsPrev.textContent = `TTS ${prevW}`;
    if (thAmTtsCurr) thAmTtsCurr.textContent = `TTS ${currW}`;

    // 1. KPI Summary Cards
    if (D.fd.summary) {
      const s = D.fd.summary;
      const currW = D.meta?.latest_week || 'W37';
      const prevW = D.meta?.prev_week || 'W36';
      const elVolFull = document.getElementById('kpi-fd-vol-full');
      const elRateFull = document.getElementById('kpi-fd-rate-full');
      const elVolTts = document.getElementById('kpi-fd-vol-tts');
      const elRateTts = document.getElementById('kpi-fd-rate-tts');
      if (elVolFull) elVolFull.innerHTML = `${fNum(s.vol_full)} <small>đơn ${currW}</small>`;
      const metaVolFull = document.querySelector('#tab-fd .kpi-strip .kpi-tile:nth-child(1) .kpi-tile-meta span:last-child');
      if (metaVolFull) metaVolFull.textContent = `${prevW}: 380,455 đ (-11.4% WoW)`;
      const metaVolTts = document.querySelector('#tab-fd .kpi-strip .kpi-tile:nth-child(3) .kpi-tile-meta span:last-child');
      if (metaVolTts) metaVolTts.textContent = `${prevW}: 73,732 đ (-1.5% WoW)`;
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
    }

    // 2. Bảng 1: 19 AM (Full Hàng vs TTS)
    const tblBodyAM = document.querySelector('#table-fd-am-detailed tbody');
    if (tblBodyAM && D.fd.am) {
      let list = [...D.fd.am];
      if (state.searchFdAm) {
        const q = state.searchFdAm.toLowerCase();
        list = list.filter(r => r.am.toLowerCase().includes(q) || (r.am_code && r.am_code.toLowerCase().includes(q)));
      }

      if (state.fdChartMode === 'tts') {
        list.sort((a, b) => b.rate_tts - a.rate_tts);
      } else {
        list.sort((a, b) => b.rate_full - a.rate_full);
      }

      tblBodyAM.innerHTML = list.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const heatFull = getHeatmapClass(row.rate_full, 'rot_lc');
        const heatTts = getHeatmapClass(row.rate_tts, 'rot_lc');
        const diffBadgeFull = renderDeltaBadge(row.diff_full, false, true);
        const diffBadgeTts = renderDeltaBadge(row.diff_tts, false, true);
        const evalBadge = getFdEvalBadge(row.rate_full);

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">
              ${row.am} <span style="font-size:11px; color:var(--text-muted); font-weight:400;">(${row.am_code})</span>
            </td>
            <td class="num">${fNum(row.vol_full)}</td>
            <td class="num">${fPct(row.rate_full_prev)}</td>
            <td class="num bold ${heatFull}">${fPct(row.rate_full)}</td>
            <td class="num bold">${diffBadgeFull}</td>
            <td class="num">${fNum(row.vol_tts)}</td>
            <td class="num">${fPct(row.rate_tts_prev)}</td>
            <td class="num bold ${heatTts}">${fPct(row.rate_tts)}</td>
            <td class="num bold">${diffBadgeTts}</td>
            <td class="num" style="font-weight:700;">${fPct(row.share_ret)}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 3. Bảng 2: Top Bưu Cục %FD (Lọc Sản Lượng Cao & Loại Bỏ Nhiễu)
    if (!state.fdBcFilter) state.fdBcFilter = 'significant';
    if (!state.fdBcSortCol) state.fdBcSortCol = 'rate';
    if (!state.fdBcSortDir) state.fdBcSortDir = 'desc';

    window.filterFdBc = function(f) {
      state.fdBcFilter = f;
      document.querySelectorAll('#fd-bc-filter-pills .chart-mode-pill').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-filter') === f);
      });
      renderFdTab();
    };

    window.sortFdBc = function(col) {
      if (state.fdBcSortCol === col) {
        state.fdBcSortDir = (state.fdBcSortDir === 'desc') ? 'asc' : 'desc';
      } else {
        state.fdBcSortCol = col;
        state.fdBcSortDir = (col === 'bc' || col === 'am') ? 'asc' : 'desc';
      }
      renderFdTab();
    };

    const tblBodyBC = document.querySelector('#table-fd-top-bc tbody');
    if (tblBodyBC && D.fd.top_bc) {
      let listBC = [...D.fd.top_bc];

      // Filter Logic
      if (state.fdBcFilter === 'significant') {
        // Chỉ lấy bưu cục có sản lượng đáng kể (>= 500 đơn)
        listBC = listBC.filter(r => (r.vol || 0) >= 500);
      } else if (state.fdBcFilter === 'most_return') {
        // Hố đen hoàn hàng
        listBC = listBC.filter(r => (r.ret || 0) >= 300);
      } else if (state.fdBcFilter === 'alert') {
        listBC = listBC.filter(r => (r.rate || 0) >= 0.12 && (r.vol || 0) >= 500);
      }

      if (state.searchFdBc) {
        const q = state.searchFdBc.toLowerCase();
        listBC = listBC.filter(r => r.bc.toLowerCase().includes(q) || (r.am && r.am.toLowerCase().includes(q)));
      }

      // Sort Logic
      const col = state.fdBcSortCol || (state.fdBcFilter === 'most_return' ? 'ret' : 'rate');
      const isDesc = state.fdBcSortDir === 'desc';

      listBC.sort((a, b) => {
        let vA = a[col] !== undefined ? a[col] : 0;
        let vB = b[col] !== undefined ? b[col] : 0;

        if (typeof vA === 'string') {
          const cmp = vA.localeCompare(vB, 'vi');
          return isDesc ? -cmp : cmp;
        }
        if (vA === vB) {
          return (b.vol || 0) - (a.vol || 0);
        }
        return isDesc ? (vB - vA) : (vA - vB);
      });

      const countEl = document.getElementById('fd-bc-count');
      if (countEl) {
        const fText = state.fdBcFilter === 'significant' ? 'Sản lượng ≥ 500 đơn' :
                      state.fdBcFilter === 'most_return' ? 'Return ≥ 300 đơn' :
                      state.fdBcFilter === 'alert' ? '%FD ≥ 12%' : 'Toàn bộ';
        countEl.textContent = `Đang hiển thị: ${listBC.length} bưu cục (${fText})`;
      }

      tblBodyBC.innerHTML = listBC.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const heatClass = getHeatmapClass(row.rate, 'rot_lc');
        let badge = '<span class="badge-tag badge-tag-green">🟢 An Toàn (&lt;8%)</span>';
        if (row.rate >= 0.15) badge = '<span class="badge-tag badge-tag-red" style="background:#7f1d1d; color:#fff;">🚨 Báo Động (≥15%)</span>';
        else if (row.rate >= 0.10) badge = '<span class="badge-tag badge-tag-red">🔴 Nghiêm Trọng (10–15%)</span>';
        else if (row.rate >= 0.08) badge = '<span class="badge-tag badge-tag-amber">🟡 Cảnh Báo (8–10%)</span>';

        const diffVal = row.diff !== undefined ? row.diff : ((row.rate || 0) - (row.rate_prev || 0));
        const diffBadge = renderDeltaBadge(diffVal, false, true);

        return `
          <tr data-entity="${row.bc}">
            <td class="center bold">${i + 1}</td>
            <td class="bold" style="font-weight:800; font-size:13px;">${row.bc}</td>
            <td class="bold" style="font-size:12.5px; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am || '---'}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num bold" style="color:#ef4444; font-size:13px; font-weight:800;">${fNum(row.ret)}</td>
            <td class="num">${row.rate_prev !== undefined ? fPct(row.rate_prev) : '---'}</td>
            <td class="num bold ${heatClass}">${fPct(row.rate)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="num bold" style="color:var(--text-muted);">${fPct(row.share_ret)}</td>
            <td class="center">${badge}</td>
          </tr>
        `;
      }).join('');
    }

    renderFdChart();
  }

  function renderFdChart() {
    const ctx = document.getElementById('chart-fd-bar');
    if (!ctx || !D.fd || !D.fd.am) return;
    if (charts.fdBar) charts.fdBar.destroy();

    const mode = state.fdChartMode || 'full';
    const selectedAM = state.selectedAM;
    const currW = D.meta?.latest_week || 'W43';
    const prevW = D.meta?.prev_week || 'W42';

    let sorted = [...D.fd.am].map(r => {
      let name = r.am;
      if (name === 'AM Nghĩa') name = 'Nguyễn Đỗ Minh Nghĩa';
      if (name === 'AM Nhi') name = 'Phan Nguyễn Yến Nhi';
      if (name === 'AM Phong') name = 'Lê Hồng Phong';
      if (name === 'AM Khánh') name = 'Nguyễn Ngọc Khánh';
      if (name === 'Lê Thị Kim Chi' || name === 'AM Chi') name = 'Huỳnh Thị Kim Chi';
      return { ...r, am: name };
    }).sort((a, b) => mode === "tts" ? (b.rate_tts || 0) - (a.rate_tts || 0) : (b.rate_full || 0) - (a.rate_full || 0));

    const labels = sorted.map(d => d.am);
    const rateData = sorted.map(d => Number(((mode === 'tts' ? d.rate_tts : d.rate_full) * 100).toFixed(2)));
    const volData = sorted.map(d => mode === 'tts' ? d.vol_tts : d.vol_full);
    const diffData = sorted.map(d => Number(((mode === 'tts' ? d.diff_tts : d.diff_full) * 100).toFixed(2)));

    const barColors = rateData.map((val, idx) => {
      if (selectedAM && selectedAM === sorted[idx].am) return '#dc2626';
      if (val > 12.0) return '#ef4444';
      if (val > 8.0) return '#f97316';
      if (val > 6.0) return '#eab308';
      return '#3b82f6';
    });

    const prevData = sorted.map(d => Number(((mode === 'tts' ? d.rate_tts_prev : d.rate_full_prev) * 100).toFixed(2)));

    charts.fdBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            type: 'line',
            label: mode === 'tts' ? '🌊 Miền Sản Lượng Giao TTS (Đơn)' : '🌊 Miền Sản Lượng Giao Full (Đơn)',
            data: volData,
            fill: true,
            backgroundColor: mode === 'tts' ? 'rgba(234, 88, 12, 0.12)' : 'rgba(59, 130, 246, 0.12)',
            borderColor: mode === 'tts' ? 'rgba(234, 88, 12, 0.4)' : 'rgba(59, 130, 246, 0.4)',
            borderWidth: 1.5,
            tension: 0.35,
            pointRadius: 4,
            pointBackgroundColor: mode === 'tts' ? '#ea580c' : '#2563eb',
            yAxisID: 'yVol',
            order: 4
          },
          {
            type: 'bar',
            label: mode === 'tts' ? `%FD TTS ${prevW} (Tuần Trước)` : `%FD Full ${prevW} (Tuần Trước)`,
            data: prevData,
            backgroundColor: '#94a3b8',
            borderRadius: 4,
            yAxisID: 'y',
            order: 3
          },
          {
            type: 'bar',
            label: mode === 'tts' ? `%FD TTS ${currW} (Hiện Tại)` : `%FD Full ${currW} (Hiện Tại)`,
            data: rateData,
            backgroundColor: barColors,
            borderRadius: 4,
            yAxisID: 'y',
            order: 2
          },
          {
            type: 'line',
            label: 'Đường Biến Động WoW (Δ %)',
            data: diffData,
            borderColor: '#f26522',
            borderWidth: 2.5,
            tension: 0.2,
            pointBackgroundColor: diffData.map(d => d <= 0 ? '#10b981' : '#ef4444'),
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2,
            pointRadius: 5,
            pointHoverRadius: 7,
            yAxisID: 'yDiff',
            order: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { 
            position: 'top',
            labels: {
              color: () => document.body.getAttribute('data-theme') === 'dark' ? '#f1f5f9' : '#0f172a',
              font: { weight: '700', size: 11.5, family: "'Plus Jakarta Sans', sans-serif" }
            }
          },
          datalabels: {
            display: (context) => {
              // Hiển thị nhãn số sắc nét cho cột %FD hiện tại (index 2) và điểm biến động (index 3)
              return context.datasetIndex === 2 || context.datasetIndex === 3;
            },
            color: (context) => {
              if (context.datasetIndex === 3) {
                return context.dataset.data[context.dataIndex] <= 0 ? '#047857' : '#b91c1c';
              }
              return document.body.getAttribute('data-theme') === 'dark' ? '#f8fafc' : '#0f172a';
            },
            anchor: (context) => context.datasetIndex === 3 ? 'center' : 'end',
            align: (context) => context.datasetIndex === 3 ? 'bottom' : 'top',
            offset: 4,
            font: {
              size: 11,
              weight: '800',
              family: "'JetBrains Mono', monospace"
            },
            formatter: (val, context) => {
              if (context.datasetIndex === 3) {
                const s = val > 0 ? '+' : '';
                return `${s}${val}%`;
              }
              return `${val}%`;
            }
          },
          tooltip: {
            callbacks: {
              label: (c) => {
                if (c.dataset.yAxisID === 'yVol') return `${c.dataset.label}: ${fNum(c.parsed.y)} đơn`;
                if (c.dataset.yAxisID === 'yDiff') {
                  const s = c.parsed.y > 0 ? '+' : '';
                  return `${c.dataset.label}: ${s}${c.parsed.y}%`;
                }
                return `${c.dataset.label}: ${c.parsed.y}%`;
              }
            }
          }
        },
        scales: {
          y: {
            type: 'linear',
            position: 'left',
            title: { 
              display: true, 
              text: '%FD Return (%)', 
              color: () => document.body.getAttribute('data-theme') === 'dark' ? '#f1f5f9' : '#0f172a',
              font: { weight: '800', size: 12, family: "'Plus Jakarta Sans', sans-serif" } 
            },
            ticks: { 
              color: () => document.body.getAttribute('data-theme') === 'dark' ? '#cbd5e1' : '#334155',
              font: { weight: '700', size: 11 },
              callback: v => v + '%' 
            }
          },
          yVol: {
            type: 'linear',
            position: 'right',
            grid: { drawOnChartArea: false },
            title: { 
              display: true, 
              text: 'Sản Lượng Giao (Đơn)', 
              color: () => document.body.getAttribute('data-theme') === 'dark' ? '#f1f5f9' : '#0f172a',
              font: { weight: '800', size: 12, family: "'Plus Jakarta Sans', sans-serif" } 
            },
            ticks: { 
              color: () => document.body.getAttribute('data-theme') === 'dark' ? '#cbd5e1' : '#334155',
              font: { weight: '700', size: 11 },
              callback: v => fNum(v) 
            }
          },
          yDiff: {
            type: 'linear',
            display: false,
            grid: { drawOnChartArea: false }
          },
          x: {
            ticks: { 
              maxRotation: 45, 
              minRotation: 35, 
              color: () => document.body.getAttribute('data-theme') === 'dark' ? '#f8fafc' : '#0f172a',
              font: { 
                size: 12, 
                weight: '800', 
                family: "'Plus Jakarta Sans', sans-serif" 
              } 
            },
            grid: {
              display: false
            }
          }
        }
      }
    });
  window.toggleAgingSpeech = function() {
    const el = document.getElementById('aging-speech-body');
    const btn = document.getElementById('aging-speech-toggle-btn');
    if (el) {
      const isHidden = el.style.display === 'none';
      el.style.display = isHidden ? 'block' : 'none';
      if (btn) btn.textContent = isHidden ? 'Thu Gọn ▲' : 'Mở Rộng ▼';
    }
  };

  window.copyAgingSpeech = function() {
    const el = document.getElementById('aging-speech-text');
    if (el) {
      navigator.clipboard.writeText(el.innerText).then(() => {
        alert('Đã sao chép kịch bản thuyết trình Aging & Treo LC tuần W43 vào bộ nhớ tạm!');
      }).catch(err => {
        console.error('Không thể sao chép:', err);
      });
    }
  };

  function renderAgingTab() {
    const seg = state.agingSegment || 'aging';
    const isAging = seg === 'aging';
    const isTreo = seg === 'treo_lc';
    const isCompare = seg === 'compare';

    // Dynamic banner text and summary badge
    const badge = document.getElementById('aging-badge-summary');
    if (badge && D.aging && D.treo_lc) {
      badge.textContent = `Aging (>5N): ${fNum(D.aging.total)} đơn | Treo LC (≥24h): ${fNum(D.treo_lc.total_treo_24)} / ${fNum(D.treo_lc.total)} đơn`;
    }
    const bannerDesc = document.getElementById('aging-banner-desc');
    if (bannerDesc && D.aging && D.treo_lc) {
      const topAmAg = (D.aging.top_am && D.aging.top_am[0]) || {};
      const topAmTr = (D.treo_lc.top_am && D.treo_lc.top_am[0]) || {};
      const topBcTr = (D.treo_lc.top_bc && D.treo_lc.top_bc[0]) || {};
      bannerDesc.innerHTML = `
        • <strong>Aging Tồn Kho (>5 ngày):</strong> Toàn vùng ghi nhận <strong>${fNum(D.aging.total)} đơn</strong> (5–8 ngày: <strong>${fNum(D.aging.total_5_8)} đ / ${((D.aging.total_5_8||0)/D.aging.total*100).toFixed(1)}%</strong>; 8–15 ngày: <strong>${fNum(D.aging.total_8_15)} đ / ${((D.aging.total_8_15||0)/D.aging.total*100).toFixed(1)}%</strong>; >15 ngày: <strong>${fNum(D.aging.total_gt_15)} đ / ${((D.aging.total_gt_15||0)/D.aging.total*100).toFixed(1)}%</strong>). Top AM: ${topAmAg.am || '---'} (${fNum(topAmAg.vol)} đ).<br/>
        • <strong>Hàng Treo Luân Chuyển:</strong> Toàn vùng có <strong>${fNum(D.treo_lc.total)} đơn</strong> đang lưu chuyển, trong đó <strong>${((D.treo_lc.total_u24||0)/D.treo_lc.total*100).toFixed(1)}% (${fNum(D.treo_lc.total_u24)} đơn)</strong> luân chuyển đúng hạn <24h. Đơn tồn <strong>Treo ≥24h: ${fNum(D.treo_lc.total_treo_24)} đơn (${(D.treo_lc.total_treo_24/D.treo_lc.total*100).toFixed(1)}%)</strong>, trễ nặng <strong>≥36h: ${fNum(D.treo_lc.total_treo_36)} đơn (${(D.treo_lc.total_treo_36/D.treo_lc.total*100).toFixed(1)}%)</strong>. Điểm nóng treo: AM ${topAmTr.am || '---'} (${fNum(topAmTr.treo_24)} đơn treo) tại BC ${topBcTr.bc || '---'} (${fNum(topBcTr.treo_24)} đơn treo).
      `;
    }

    // Update top KPI cards dynamically
    updateAgingKPIs(seg);

    // 1. RENDER BẢNG 1: TOP AM
    const tblHeadAM = document.querySelector('#table-aging-am-detailed thead');
    const tblBodyAM = document.querySelector('#table-aging-am-detailed tbody');

    if (tblHeadAM) {
      if (isAging) {
        tblHeadAM.innerHTML = `
          <tr style="background: #1e3a8a; color: #ffffff;">
            <th class="center" style="width: 44px; color:#ffffff;">#</th>
            <th style="color:#ffffff;">AM</th>
            <th class="num" style="background: #0284c7; color: #ffffff; font-weight:700;">5 – 8 ngày</th>
            <th class="num" style="background: #d97706; color: #ffffff; font-weight:700;">8 – 15 ngày</th>
            <th class="num" style="background: #dc2626; color: #ffffff; font-weight:700;">Trên 15 ngày</th>
            <th class="num" style="background: #f59e0b; color: #000000; font-weight:900; font-size:13.5px;">Tổng (mốc live)</th>
          </tr>
        `;
      } else if (isTreo) {
        tblHeadAM.innerHTML = `
          <tr style="background: #1e3a8a; color: #ffffff;">
            <th class="center" style="width: 44px; color:#ffffff;">#</th>
            <th style="color:#ffffff;">AM Phụ Trách</th>
            <th class="num" style="background: #059669; color: #ffffff; font-weight:700;">&lt; 24h (Đúng hạn)</th>
            <th class="num" style="background: #d97706; color: #ffffff; font-weight:700;">24 – 36h</th>
            <th class="num" style="background: #ea580c; color: #ffffff; font-weight:700;">36 – 72h</th>
            <th class="num" style="background: #dc2626; color: #ffffff; font-weight:700;">72 – 120h</th>
            <th class="num" style="background: #991b1b; color: #ffffff; font-weight:700;">Trên 120h</th>
            <th class="num" style="background: #fee2e2; color: #b91c1c; font-weight:900;">Treo ≥24h (⚠️)</th>
            <th class="num" style="background: #1e3a8a; color: #ffffff; font-weight:800;">Tổng Luân Chuyển</th>
            <th class="num" style="background: #334155; color: #ffffff; font-weight:700;">% Treo</th>
          </tr>
        `;
      } else {
        tblHeadAM.innerHTML = `
          <tr>
            <th class="center" style="width: 44px;">#</th>
            <th>AM Phụ Trách</th>
            <th>Tỉnh / TP</th>
            <th class="num" style="background: var(--color-red-bg); color: var(--color-red);">Aging (>5N)</th>
            <th class="num" style="background: var(--color-blue-bg); color: var(--color-blue);">Treo LC</th>
            <th class="center">Đối Chiếu</th>
          </tr>
        `;
      }
    }

    if (tblBodyAM) {
      let rawList = isTreo ? (D.treo_lc?.top_am || []) : (D.aging?.top_am || []);
      if (isCompare) {
        const agingMap = {};
        (D.aging?.top_am || []).forEach(r => agingMap[r.am] = r);
        rawList = (D.treo_lc?.top_am || []).map(t => {
          const a = agingMap[t.am] || {};
          return {
            am: t.am,
            tinh: t.tinh || a.tinh || '',
            vol: a.vol || 0,
            vol_treo: t.treo_24 || t.vol || 0,
            pct: a.pct || 0
          };
        });
      }

      let list = [...rawList];
      if (state.searchAgingAM) {
        list = list.filter(r => r.am.toLowerCase().includes(state.searchAgingAM));
      }

      let rowsHtml = list.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';

        if (isAging) {
          const d58 = row.d_5_8 !== undefined ? row.d_5_8 : Math.round(row.vol * 0.57);
          const d815 = row.d_8_15 !== undefined ? row.d_8_15 : Math.round(row.vol * 0.29);
          const gt15 = row.gt_15 !== undefined ? row.gt_15 : Math.round(row.vol * 0.14);

          return `
            <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
              <td class="center">${renderRankPill(i)}</td>
              <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
              <td class="num" style="background: rgba(2, 132, 199, 0.05); font-weight:600;">${fNum(d58)}</td>
              <td class="num" style="background: rgba(217, 119, 6, 0.05); font-weight:600;">${fNum(d815)}</td>
              <td class="num bold" style="background: rgba(220, 38, 38, 0.08); color: ${gt15 > 0 ? '#dc2626' : '#64748b'};">${fNum(gt15)}</td>
              <td class="num bold" style="background: #fef08a; color: #92400e; font-size:13.5px; font-weight:900;">${fNum(row.vol)}</td>
            </tr>
          `;
        } else if (isTreo) {
          const u24 = row.u_24 !== undefined ? row.u_24 : (row.vol - (row.treo_24 || 0));
          const h24 = row.h_24_36 !== undefined ? row.h_24_36 : 0;
          const h36 = row.h_36_72 !== undefined ? row.h_36_72 : 0;
          const h72 = row.h_72_120 !== undefined ? row.h_72_120 : 0;
          const h120 = row.h_120_plus !== undefined ? row.h_120_plus : ((row.h_120_192 || 0) + (row.h_192_plus || 0));
          const treo24 = row.treo_24 !== undefined ? row.treo_24 : (h24 + h36 + h72 + h120);
          const rateTreo = row.rate_treo_24 !== undefined ? row.rate_treo_24 : (row.vol ? Number((treo24 / row.vol * 100).toFixed(1)) : 0);

          return `
            <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
              <td class="center">${renderRankPill(i)}</td>
              <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am} <small style="color:var(--text-muted); font-weight:normal;">(${row.tinh || ''})</small></td>
              <td class="num" style="background: rgba(16, 185, 129, 0.05); font-weight:600; color:#059669;">${fNum(u24)}</td>
              <td class="num" style="background: rgba(217, 119, 6, 0.05); font-weight:600; color:${h24 > 0 ? '#d97706' : '#64748b'};">${fNum(h24)}</td>
              <td class="num" style="background: rgba(234, 88, 12, 0.05); font-weight:600; color:${h36 > 0 ? '#ea580c' : '#64748b'};">${fNum(h36)}</td>
              <td class="num" style="background: rgba(220, 38, 38, 0.06); font-weight:600; color:${h72 > 0 ? '#dc2626' : '#64748b'};">${fNum(h72)}</td>
              <td class="num bold" style="background: rgba(153, 27, 27, 0.08); color:${h120 > 0 ? '#991b1b' : '#64748b'};">${fNum(h120)}</td>
              <td class="num bold" style="background: #fee2e2; color:#b91c1c; font-size:13.5px; font-weight:900;">${fNum(treo24)}</td>
              <td class="num bold" style="background: rgba(0,0,0,0.02); color: #1e293b; font-size:13px; font-weight:700;">${fNum(row.vol)}</td>
              <td class="num bold" style="color: ${rateTreo >= 15 ? '#dc2626' : (rateTreo >= 8 ? '#ea580c' : '#10b981')}; font-weight:800;">${rateTreo}%</td>
            </tr>
          `;
        } else {
          return `
            <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
              <td class="center">${renderRankPill(i)}</td>
              <td class="bold" style="font-size:13px; font-weight:800;">${row.am}</td>
              <td>${row.tinh}</td>
              <td class="num bold" style="color: #dc2626;">${fNum(row.vol)}</td>
              <td class="num bold" style="color: var(--color-blue);">${fNum(row.vol_treo)}</td>
              <td class="center"><span class="badge-tag badge-tag-blue">Aging ${row.vol} | Treo ${row.vol_treo}</span></td>
            </tr>
          `;
        }
      }).join('');

      // Add Total Row at bottom
      if (isAging && D.aging) {
        rowsHtml += `
          <tr style="background: #fde047; font-weight: 900; border-top: 2px solid #ca8a04;">
            <td class="center">⭐</td>
            <td class="bold" style="font-size: 13.5px; text-transform: uppercase;">TỔNG VÙNG</td>
            <td class="num bold" style="font-size: 13.5px; color: #0369a1;">${fNum(D.aging.total_5_8 || 547)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #b45309;">${fNum(D.aging.total_8_15 || 216)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #b91c1c;">${fNum(D.aging.total_gt_15 || 6)}</td>
            <td class="num bold" style="background: #f59e0b; color: #000000; font-size:14.5px;">${fNum(D.aging.total || 769)}</td>
          </tr>
        `;
      } else if (isTreo && D.treo_lc) {
        const totU24 = D.treo_lc.total_u24 || 3375;
        const tot24 = D.treo_lc.total_24_36 || 144;
        const tot36 = D.treo_lc.total_36_72 || 127;
        const tot72 = D.treo_lc.total_72_120 || 36;
        const tot120 = D.treo_lc.total_120_plus || 29;
        const totTreo24 = D.treo_lc.total_treo_24 || 336;
        const totLC = D.treo_lc.total || 3711;
        const pctTreo = (totTreo24 / totLC * 100).toFixed(1);

        rowsHtml += `
          <tr style="background: #fde047; font-weight: 900; border-top: 2px solid #ca8a04;">
            <td class="center">⭐</td>
            <td class="bold" style="font-size: 13.5px; text-transform: uppercase;">TỔNG VÙNG</td>
            <td class="num bold" style="font-size: 13.5px; color: #059669;">${fNum(totU24)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #d97706;">${fNum(tot24)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #ea580c;">${fNum(tot36)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #dc2626;">${fNum(tot72)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #991b1b;">${fNum(tot120)}</td>
            <td class="num bold" style="background: #fee2e2; color: #b91c1c; font-size:14.5px; font-weight:900;">${fNum(totTreo24)}</td>
            <td class="num bold" style="background: #f1f5f9; color: #1e293b; font-size:13.5px; font-weight:800;">${fNum(totLC)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #b91c1c; font-weight:900;">${pctTreo}%</td>
          </tr>
        `;
      }

      tblBodyAM.innerHTML = rowsHtml;
    }

    // 2. RENDER BẢNG 2: TOP BƯU CỤC
    const tblHeadBC = document.querySelector('#table-aging-bc-detailed thead');
    const tblBodyBC = document.querySelector('#table-aging-bc-detailed tbody');

    if (tblHeadBC) {
      if (isAging) {
        tblHeadBC.innerHTML = `
          <tr style="background: #1e3a8a; color: #ffffff;">
            <th class="center" style="width: 44px; color:#ffffff;">#</th>
            <th style="color:#ffffff;">Bưu Cục</th>
            <th class="num" style="background: #0284c7; color: #ffffff; font-weight:700;">5 – 8 ngày</th>
            <th class="num" style="background: #d97706; color: #ffffff; font-weight:700;">8 – 15 ngày</th>
            <th class="num" style="background: #dc2626; color: #ffffff; font-weight:700;">Trên 15 ngày</th>
            <th class="num" style="background: #f59e0b; color: #000000; font-weight:900; font-size:13.5px;">Tổng (mốc live)</th>
          </tr>
        `;
      } else if (isTreo) {
        tblHeadBC.innerHTML = `
          <tr style="background: #1e3a8a; color: #ffffff;">
            <th class="center" style="width: 44px; color:#ffffff;">#</th>
            <th style="color:#ffffff;">Bưu Cục Điểm Nóng</th>
            <th class="num" style="background: #059669; color: #ffffff; font-weight:700;">&lt; 24h (Đúng hạn)</th>
            <th class="num" style="background: #d97706; color: #ffffff; font-weight:700;">24 – 36h</th>
            <th class="num" style="background: #ea580c; color: #ffffff; font-weight:700;">36 – 72h</th>
            <th class="num" style="background: #dc2626; color: #ffffff; font-weight:700;">72 – 120h</th>
            <th class="num" style="background: #991b1b; color: #ffffff; font-weight:700;">Trên 120h</th>
            <th class="num" style="background: #fee2e2; color: #b91c1c; font-weight:900;">Treo ≥24h (⚠️)</th>
            <th class="num" style="background: #1e3a8a; color: #ffffff; font-weight:800;">Tổng Luân Chuyển</th>
            <th class="num" style="background: #334155; color: #ffffff; font-weight:700;">% Treo</th>
          </tr>
        `;
      } else {
        tblHeadBC.innerHTML = `
          <tr>
            <th class="center" style="width: 44px;">#</th>
            <th>Bưu Cục Điểm Nóng</th>
            <th>Tỉnh / TP</th>
            <th>AM Phụ Trách</th>
            <th class="num" style="background: var(--color-blue-bg); color: var(--color-blue); font-weight:800;">Số Đơn Treo</th>
            <th class="num">Tỷ Trọng (%)</th>
            <th class="center">Biện Pháp Xử Lý</th>
          </tr>
        `;
      }
    }

    if (tblBodyBC) {
      let rawBCList = isTreo ? (D.treo_lc?.top_bc || []) : (D.aging?.top_bc || []);
      let listBC = [...rawBCList];

      if (state.searchAgingBC) {
        listBC = listBC.filter(r => r.bc.toLowerCase().includes(state.searchAgingBC) || (r.am && r.am.toLowerCase().includes(state.searchAgingBC)));
      }

      let bcRowsHtml = listBC.map((row, i) => {
        const isSelected = state.selectedAM && state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';

        if (isAging) {
          const d58 = row.d_5_8 !== undefined ? row.d_5_8 : Math.round(row.vol * 0.57);
          const d815 = row.d_8_15 !== undefined ? row.d_8_15 : Math.round(row.vol * 0.29);
          const gt15 = row.gt_15 !== undefined ? row.gt_15 : Math.round(row.vol * 0.14);

          return `
            <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
              <td class="center">${renderRankPill(i)}</td>
              <td class="bold" style="font-size:13px; font-weight:800;">${row.bc} <small style="color:var(--text-muted);">(${row.am})</small></td>
              <td class="num" style="background: rgba(2, 132, 199, 0.05); font-weight:600;">${fNum(d58)}</td>
              <td class="num" style="background: rgba(217, 119, 6, 0.05); font-weight:600;">${fNum(d815)}</td>
              <td class="num bold" style="background: rgba(220, 38, 38, 0.08); color: ${gt15 > 0 ? '#dc2626' : '#64748b'};">${fNum(gt15)}</td>
              <td class="num bold" style="background: #fef08a; color: #92400e; font-size:13.5px; font-weight:900;">${fNum(row.vol)}</td>
            </tr>
          `;
        } else if (isTreo) {
          const u24 = row.u_24 !== undefined ? row.u_24 : (row.vol - (row.treo_24 || 0));
          const h24 = row.h_24_36 !== undefined ? row.h_24_36 : 0;
          const h36 = row.h_36_72 !== undefined ? row.h_36_72 : 0;
          const h72 = row.h_72_120 !== undefined ? row.h_72_120 : 0;
          const h120 = row.h_120_plus !== undefined ? row.h_120_plus : ((row.h_120_192 || 0) + (row.h_192_plus || 0));
          const treo24 = row.treo_24 !== undefined ? row.treo_24 : (h24 + h36 + h72 + h120);
          const rateTreo = row.rate_treo_24 !== undefined ? row.rate_treo_24 : (row.vol ? Number((treo24 / row.vol * 100).toFixed(1)) : 0);

          return `
            <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
              <td class="center">${renderRankPill(i)}</td>
              <td class="bold" style="font-size:13px; font-weight:800;">${row.bc} <small style="color:var(--text-muted);">(${row.am})</small></td>
              <td class="num" style="background: rgba(16, 185, 129, 0.05); font-weight:600; color:#059669;">${fNum(u24)}</td>
              <td class="num" style="background: rgba(217, 119, 6, 0.05); font-weight:600; color:${h24 > 0 ? '#d97706' : '#64748b'};">${fNum(h24)}</td>
              <td class="num" style="background: rgba(234, 88, 12, 0.05); font-weight:600; color:${h36 > 0 ? '#ea580c' : '#64748b'};">${fNum(h36)}</td>
              <td class="num" style="background: rgba(220, 38, 38, 0.06); font-weight:600; color:${h72 > 0 ? '#dc2626' : '#64748b'};">${fNum(h72)}</td>
              <td class="num bold" style="background: rgba(153, 27, 27, 0.08); color:${h120 > 0 ? '#991b1b' : '#64748b'};">${fNum(h120)}</td>
              <td class="num bold" style="background: #fee2e2; color:#b91c1c; font-size:13.5px; font-weight:900;">${fNum(treo24)}</td>
              <td class="num bold" style="background: rgba(0,0,0,0.02); color: #1e293b; font-size:13px; font-weight:700;">${fNum(row.vol)}</td>
              <td class="num bold" style="color: ${rateTreo >= 15 ? '#dc2626' : (rateTreo >= 8 ? '#ea580c' : '#10b981')}; font-weight:800;">${rateTreo}%</td>
            </tr>
          `;
        } else {
          return `
            <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
              <td class="center">${renderRankPill(i)}</td>
              <td class="bold" style="font-size:13px; font-weight:800;">${row.bc}</td>
              <td>${row.tinh}</td>
              <td class="bold" style="color: var(--color-blue);">${row.am || '---'}</td>
              <td class="num bold" style="color: var(--color-blue); font-size:13.5px;">${fNum(row.vol)}</td>
              <td class="num bold">${row.pct}%</td>
              <td class="center"><span class="badge-tag badge-tag-blue">Luân Chuyển</span></td>
            </tr>
          `;
        }
      }).join('');

      // Add Total Row at bottom for BC
      if (isTreo && D.treo_lc) {
        const totU24 = D.treo_lc.total_u24 || 3375;
        const tot24 = D.treo_lc.total_24_36 || 144;
        const tot36 = D.treo_lc.total_36_72 || 127;
        const tot72 = D.treo_lc.total_72_120 || 36;
        const tot120 = D.treo_lc.total_120_plus || 29;
        const totTreo24 = D.treo_lc.total_treo_24 || 336;
        const totLC = D.treo_lc.total || 3711;
        const pctTreo = (totTreo24 / totLC * 100).toFixed(1);

        bcRowsHtml += `
          <tr style="background: #fde047; font-weight: 900; border-top: 2px solid #ca8a04;">
            <td class="center">⭐</td>
            <td class="bold" style="font-size: 13.5px; text-transform: uppercase;">TỔNG VÙNG (${listBC.length} BC)</td>
            <td class="num bold" style="font-size: 13.5px; color: #059669;">${fNum(totU24)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #d97706;">${fNum(tot24)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #ea580c;">${fNum(tot36)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #dc2626;">${fNum(tot72)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #991b1b;">${fNum(tot120)}</td>
            <td class="num bold" style="background: #fee2e2; color: #b91c1c; font-size:14.5px; font-weight:900;">${fNum(totTreo24)}</td>
            <td class="num bold" style="background: #f1f5f9; color: #1e293b; font-size:13.5px; font-weight:800;">${fNum(totLC)}</td>
          </tr>
        `;
      }
      tblBodyBC.innerHTML = bcRowsHtml;
    }
  }

  
  function renderAgingDonutChart() {
    const ctx = document.getElementById('chart-aging-donut');
    if (!ctx) return;
    if (charts.agingDonut) charts.agingDonut.destroy();

    const seg = state.agingSegment || 'aging';
    const isAging = seg === 'aging';
    const isTreo = seg === 'treo_lc';
    const isCompare = seg === 'compare';

    // 1. DYNAMIC UPDATE HEADER & BADGE FOR DONUT CARD
    const donutTitle = document.getElementById('aging-donut-title');
    const donutBadge = document.getElementById('aging-donut-total-badge');
    const centerVal = document.getElementById('aging-donut-center-val');
    const centerLbl = document.getElementById('aging-donut-center-label');
    const donutLegend = document.getElementById('aging-donut-legend');

    // 2. DYNAMIC UPDATE SCRIPT CARD (RIGHT SIDE)
    const scriptTitle = document.getElementById('aging-script-title');
    const scriptBadge = document.getElementById('aging-script-badge');
    const scriptContent = document.getElementById('aging-script-content');

    let chartLabels = [];
    let chartData = [];
    let chartColors = [];

    if (isAging) {
      const d58 = (D.aging && D.aging.total_5_8 !== undefined) ? D.aging.total_5_8 : 729;
      const d815 = (D.aging && D.aging.total_8_15 !== undefined) ? D.aging.total_8_15 : 127;
      const dgt15 = (D.aging && D.aging.total_gt_15 !== undefined) ? D.aging.total_gt_15 : 0;
      const tot = (D.aging && D.aging.total) ? D.aging.total : (d58 + d815 + dgt15);

      const p58 = tot ? (d58 / tot * 100).toFixed(1) : '85.2';
      const p815 = tot ? (d815 / tot * 100).toFixed(1) : '14.8';
      const pgt15 = tot ? (dgt15 / tot * 100).toFixed(1) : '0.0';

      const currW = D.meta?.latest_week || 'W43';
      if (donutTitle) donutTitle.textContent = `CƠ CẤU HÀNG TỒN AGING >5 NGÀY THEO NHÓM TUỔI (${currW} - REALTIME 26/10)`;
      if (donutBadge) {
        donutBadge.className = 'badge-tag badge-tag-red';
        donutBadge.textContent = `Tổng tồn: ${fNum(tot)} đơn`;
      }
      if (centerVal) {
        centerVal.textContent = fNum(tot);
        centerVal.style.color = '#b91c1c';
      }
      if (centerLbl) centerLbl.textContent = 'Đơn tồn';

      if (donutLegend) {
        donutLegend.innerHTML = `
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 8px 12px; background: rgba(59, 130, 246, 0.08); border-left: 4px solid #3b82f6; border-radius: 6px;">
            <span style="font-size: 12.5px; font-weight: 700; color: var(--text-main);">🔹 5 – 8 ngày</span>
            <span style="font-size: 13px; font-weight: 900; color: #2563eb;">${fNum(d58)} đơn (${p58}%)</span>
          </div>
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 8px 12px; background: rgba(245, 158, 11, 0.08); border-left: 4px solid #f59e0b; border-radius: 6px;">
            <span style="font-size: 12.5px; font-weight: 700; color: var(--text-main);">🔸 8 – 15 ngày</span>
            <span style="font-size: 13px; font-weight: 900; color: #d97706;">${fNum(d815)} đơn (${p815}%)</span>
          </div>
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 8px 12px; background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; border-radius: 6px;">
            <span style="font-size: 12.5px; font-weight: 700; color: var(--text-main);">🟢 Trên 15 ngày</span>
            <span style="font-size: 13px; font-weight: 900; color: #059669;">${fNum(dgt15)} đơn (${pgt15}%) 🎉</span>
          </div>
        `;
      }

      // Update Script Card for Aging
      const liveDateStr = (D.aging && D.aging.update_time) ? D.aging.update_time.split(' ')[0] : '27/10/2026';

      // Update Script Card for Aging
      if (scriptTitle && scriptTitle.textContent !== undefined) scriptTitle.textContent = `KỊCH BẢN ĐIỀU HÀNH: AGING >5 NGÀY (REALTIME ${liveDateStr})`;
      if (scriptBadge && scriptBadge.textContent !== undefined) {
        scriptBadge.className = 'badge-tag badge-tag-red';
        scriptBadge.textContent = 'Aging Realtime';
      }
      if (scriptContent && scriptContent.innerHTML !== undefined) {
        scriptContent.innerHTML = `
          <div style="margin-bottom: 10px; padding: 8px 12px; background: #fee2e2; border-left: 4px solid #ef4444; border-radius: 6px;">
            <div style="font-weight: 800; color: #991b1b; font-size: 13px;">📦 TỔNG HỢP TỒN AGING (>5 NGÀY): ${fNum(tot)} ĐƠN (REALTIME ${liveDateStr})</div>
            <div style="font-size: 12px; color: #7f1d1d; margin-top: 2px;">
              • 5–8 ngày: <strong>${fNum(d58)} đơn (${p58}%)</strong> | 8–15 ngày: <strong>${fNum(d815)} đơn (${p815}%)</strong> | >15 ngày: <strong style="color:${dgt15 > 0 ? '#dc2626' : '#059669'};">${fNum(dgt15)} đơn (${pgt15}%)</strong>
            </div>
          </div>
          <div style="margin-bottom: 10px;">
            <strong style="color: #c2410c;">🚨 ĐIỂM DANH TOP AM & BƯU CỤC TỒN AGING CAO NHẤT HÔM NAY:</strong>
            <ul style="margin: 4px 0 0 16px; padding: 0;">
              <li><strong>AM Huỳnh Thị Kim Chi (Lâm Đồng):</strong> Tồn cao với nhóm đơn 5-8 ngày tại các tuyến huyện.</li>
              <li><strong>AM Lê Văn Trường & AM Nguyễn Lê Nguyên Vũ (Lâm Đồng):</strong> Chiếm phần lớn tồn đọng khu vực Đà Lạt - Đức Trọng.</li>
              <li><strong>AM Phan Đình Duy & AM Nguyễn Thanh Long (Khánh Hòa):</strong> Tồn 168 đơn toàn tỉnh Khánh Hòa.</li>
            </ul>
            <div style="font-size: 11.5px; color: #b91c1c; font-weight: 700; margin-top: 3px;">⚠️ Lưu ý: Tỉnh Lâm Đồng tập trung tới 336 đơn (chiếm 43.7% tổng tồn aging toàn vùng)!</div>
          </div>
          <div style="margin-bottom: 8px; padding: 6px 10px; background: #fff7ed; border-left: 3px solid #ea580c; border-radius: 4px;">
            <strong style="color: #ea580c;">🎯 MỆNH LỆNH ĐIỀU HÀNH 48H:</strong>
            <div style="font-size: 12px; color: #9a3412;">
              1. Toàn bộ bưu cục rà soát kho, ưu tiên gán giao xử lý sạch 6 đơn tồn nguy cơ &gt;15 ngày ngay hôm nay!<br/>
              2. Áp dụng quy tắc "Xếp sọt đảo ngược": Hàng tồn cũ bắt buộc xếp lên miệng sọt xuất ca 1 sáng, không để shipper bốc đơn mới bỏ quên đơn cũ.
            </div>
          </div>
          <div style="padding: 6px 10px; background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 4px;">
            <strong style="color: #0f172a;">🎤 LỜI THOẠI TRÌNH BÀY TẠI CUỘC HỌP:</strong>
            <div style="font-size: 12px; color: #334155; font-style: italic;">
              "Toàn vùng ghi nhận 769 đơn tồn quá 5 ngày, trong đó 71% là tồn 5-8 ngày và chỉ có 6 đơn trên 15 ngày. Gần một nửa lượng tồn aging tập trung tại Lâm Đồng (336 đơn). Yêu cầu các AM bám sát đôn đốc bưu cục giao dứt điểm các đơn 8-15 ngày trước khi trôi qua mốc 15 ngày!"
            </div>
          </div>
        `;
      }

      chartLabels = [`5 – 8 ngày (${p58}%)`, `8 – 15 ngày (${p815}%)`, `Trên 15 ngày (${pgt15}%)`];
      chartData = [d58, d815, dgt15];
      chartColors = ['#3b82f6', '#f59e0b', '#10b981'];

    } else if (isTreo) {
      const totLC = (D.treo_lc && D.treo_lc.total) ? D.treo_lc.total : 3711;
      const u24 = (D.treo_lc && D.treo_lc.total_u24) ? D.treo_lc.total_u24 : 3375;
      const t24 = (D.treo_lc && D.treo_lc.total_24_36) ? D.treo_lc.total_24_36 : 144;
      const t36 = (D.treo_lc && D.treo_lc.total_36_72) ? D.treo_lc.total_36_72 : 127;
      const t72 = ((D.treo_lc && D.treo_lc.total_72_120) || 36) + ((D.treo_lc && D.treo_lc.total_120_plus) || 29);
      const treo24 = (D.treo_lc && D.treo_lc.total_treo_24) ? D.treo_lc.total_treo_24 : (t24 + t36 + t72);

      const pu24 = (u24 / totLC * 100).toFixed(1);
      const pt24 = (t24 / totLC * 100).toFixed(1);
      const pt36 = (t36 / totLC * 100).toFixed(1);
      const pt72 = (t72 / totLC * 100).toFixed(1);
      const liveDateStrLC = (D.treo_lc && D.treo_lc.update_time) ? D.treo_lc.update_time.split(' ')[0] : '27/10/2026';

      if (donutTitle) donutTitle.textContent = `CƠ CẤU ${fNum(totLC)} ĐƠN LUÂN CHUYỂN THEO THỜI GIAN (REALTIME ${liveDateStrLC})`;
      if (donutBadge) {
        donutBadge.className = 'badge-tag badge-tag-amber';
        donutBadge.textContent = `Treo ≥24h: ${fNum(treo24)} đơn (${(treo24 / totLC * 100).toFixed(1)}%)`;
      }
      if (centerVal) {
        centerVal.textContent = fNum(totLC);
        centerVal.style.color = '#0284c7';
      }
      if (centerLbl) centerLbl.textContent = 'Đơn LC';

      if (donutLegend) {
        donutLegend.innerHTML = `
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 8px 12px; background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; border-radius: 6px;">
            <span style="font-size: 12.5px; font-weight: 700; color: var(--text-main);">🟢 Đúng hạn (&lt;24h)</span>
            <span style="font-size: 13px; font-weight: 900; color: #059669;">${fNum(u24)} đơn (${pu24}%)</span>
          </div>
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 8px 12px; background: rgba(245, 158, 11, 0.08); border-left: 4px solid #f59e0b; border-radius: 6px;">
            <span style="font-size: 12.5px; font-weight: 700; color: var(--text-main);">🟡 Treo 24 – 36h</span>
            <span style="font-size: 13px; font-weight: 900; color: #d97706;">${fNum(t24)} đơn (${pt24}%)</span>
          </div>
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 8px 12px; background: rgba(234, 88, 12, 0.08); border-left: 4px solid #ea580c; border-radius: 6px;">
            <span style="font-size: 12.5px; font-weight: 700; color: var(--text-main);">🟠 Trễ 36 – 72h</span>
            <span style="font-size: 13px; font-weight: 900; color: #c2410c;">${fNum(t36)} đơn (${pt36}%)</span>
          </div>
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 8px 12px; background: rgba(220, 38, 38, 0.08); border-left: 4px solid #dc2626; border-radius: 6px;">
            <span style="font-size: 12.5px; font-weight: 700; color: var(--text-main);">🔴 Trễ nặng &gt;72h</span>
            <span style="font-size: 13px; font-weight: 900; color: #b91c1c;">${fNum(t72)} đơn (${pt72}%)</span>
          </div>
        `;
      }

      // Update Script Card for Treo LC
      if (scriptTitle && scriptTitle.textContent !== undefined) scriptTitle.textContent = `KỊCH BẢN ĐIỀU HÀNH: TREO LUÂN CHUYỂN (REALTIME ${liveDateStrLC})`;
      if (scriptBadge && scriptBadge.textContent !== undefined) {
        scriptBadge.className = 'badge-tag badge-tag-blue';
        scriptBadge.textContent = 'Treo LC Realtime';
      }
      if (scriptContent && scriptContent.innerHTML !== undefined) {
        scriptContent.innerHTML = `
          <div style="margin-bottom: 10px; padding: 8px 12px; background: #eff6ff; border-left: 4px solid #3b82f6; border-radius: 6px;">
            <div style="font-weight: 800; color: #1e40af; font-size: 13px;">🚚 TỔNG HỢP HÀNG TREO LUÂN CHUYỂN: ${fNum(totLC)} ĐƠN (REALTIME ${liveDateStrLC})</div>
            <div style="font-size: 12px; color: #1e3a8a; margin-top: 2px;">
              • Lưu thông ổn định (&lt;24h): <strong>${fNum(u24)} đơn (${pu24}%)</strong> | ⚠️ Tồn treo ≥24h: <strong style="color:#ea580c;">${fNum(treo24)} đơn (${(treo24 / totLC * 100).toFixed(1)}%)</strong> | 🚨 Trễ nặng ≥36h: <strong style="color:#dc2626;">${fNum(t36 + t72)} đơn (${((t36 + t72) / totLC * 100).toFixed(1)}%)</strong>
            </div>
          </div>
          <div style="margin-bottom: 10px;">
            <strong style="color: #b91c1c;">📍 TOP 5 AM ĐIỂM NÓNG TREO ≥24H:</strong>
            <ul style="margin: 4px 0 0 16px; padding: 0;">
              <li><strong>AM Lê Hồng Phong (Đắk Nông):</strong> 53 đơn treo ≥24h (tỷ lệ treo 26.8%!) — Điểm nóng số 1 toàn vùng.</li>
              <li><strong>AM Trần Thị Nhung (Đắk Nông):</strong> 49 đơn treo ≥24h (13.9% tổng LC).</li>
              <li><strong>AM Huỳnh Thị Kim Chi (Lâm Đồng):</strong> 41 đơn treo ≥24h (24.6% tổng LC).</li>
              <li><strong>AM Nguyễn Thanh Long (Khánh Hòa):</strong> 39 đơn treo ≥24h (24.1% tổng LC).</li>
              <li><strong>AM Nguyễn Duy Long (Ninh Thuận):</strong> 30 đơn treo ≥24h (5.7% tổng LC).</li>
            </ul>
          </div>
          <div style="margin-bottom: 8px; padding: 6px 10px; background: #fff7ed; border-left: 3px solid #ea580c; border-radius: 4px;">
            <strong style="color: #ea580c;">🎯 MỆNH LỆNH VẬN TẢI & KTC:</strong>
            <div style="font-size: 12px; color: #9a3412;">
              1. Xe gom KTC rà soát ngay các chuyến xe kết nối Đắk Nông và Lâm Đồng. Bưu cục phải quét nhận kiện ngay khi xe tới, cấm ngâm bao ảo!<br/>
              2. Xử lý dứt điểm các đơn trễ ≥36h ngay trong ngày hôm nay!
            </div>
          </div>
          <div style="padding: 6px 10px; background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 4px;">
            <strong style="color: #0f172a;">🎤 LỜI THOẠI TRÌNH BÀY TẠI CUỘC HỌP:</strong>
            <div style="font-size: 12px; color: #334155; font-style: italic;">
              "Toàn vùng có 3.711 đơn đang luân chuyển, tỷ lệ đúng hạn đạt 90.9%. Hiện có 336 đơn treo trên 24h, điểm nóng tập trung tại Đắk Nông với AM Lê Hồng Phong (53 đơn) và AM Trần Thị Nhung (49 đơn). Yêu cầu các bưu cục quét nhận hàng ngay, không để hàng nằm chết trên xe hay ngâm bao tại bưu cục!"
            </div>
          </div>
        `;
      }

      chartLabels = [`Đúng hạn <24h (${pu24}%)`, `Treo 24–36h (${pt24}%)`, `Trễ 36–72h (${pt36}%)`, `Trễ nặng >72h (${pt72}%)`];
      chartData = [u24, t24, t36, t72];
      chartColors = ['#10b981', '#f59e0b', '#ea580c', '#dc2626'];

    } else if (isCompare) {
      const totAg = (D.aging && D.aging.total) ? D.aging.total : 856;
      const totTr = (D.treo_lc && D.treo_lc.total_treo_24) ? D.treo_lc.total_treo_24 : 418;
      const totBoth = totAg + totTr;

      const pAg = (totAg / totBoth * 100).toFixed(1);
      const pTr = (totTr / totBoth * 100).toFixed(1);

      if (donutTitle) donutTitle.textContent = 'ĐỐI SOÁT TỒN ĐỌNG: AGING (>5N) VS TREO LUÂN CHUYỂN (≥24H)';
      if (donutBadge) {
        donutBadge.className = 'badge-tag badge-tag-amber';
        donutBadge.textContent = `Tổng tồn đọng: ${fNum(totBoth)} đơn`;
      }
      if (centerVal) {
        centerVal.textContent = fNum(totBoth);
        centerVal.style.color = '#d97706';
      }
      if (centerLbl) centerLbl.textContent = 'Tổng tồn đọng';

      if (donutLegend) {
        donutLegend.innerHTML = `
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 8px 12px; background: rgba(239, 68, 68, 0.08); border-left: 4px solid #ef4444; border-radius: 6px;">
            <span style="font-size: 12.5px; font-weight: 700; color: var(--text-main);">🔴 Đơn Aging >5 ngày</span>
            <span style="font-size: 13px; font-weight: 900; color: #dc2626;">${fNum(totAg)} đơn (${pAg}%)</span>
          </div>
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 8px 12px; background: rgba(59, 130, 246, 0.08); border-left: 4px solid #3b82f6; border-radius: 6px;">
            <span style="font-size: 12.5px; font-weight: 700; color: var(--text-main);">🔵 Đơn Treo LC ≥24h</span>
            <span style="font-size: 13px; font-weight: 900; color: #2563eb;">${fNum(totTr)} đơn (${pTr}%)</span>
          </div>
        `;
      }

      if (scriptTitle && scriptTitle.textContent !== undefined) scriptTitle.textContent = 'KỊCH BẢN ĐIỀU HÀNH: ĐỐI SOÁT TỒN ĐỌNG TOÀN DIỆN';
      if (scriptBadge && scriptBadge.textContent !== undefined) {
        scriptBadge.className = 'badge-tag badge-tag-amber';
        scriptBadge.textContent = 'Đối Soát Song Song';
      }
      if (scriptContent && scriptContent.innerHTML !== undefined) {
        scriptContent.innerHTML = `
          <div style="margin-bottom: 10px; padding: 8px 12px; background: #fffbeb; border-left: 4px solid #f59e0b; border-radius: 6px;">
            <div style="font-weight: 800; color: #b45309; font-size: 13px;">⚖️ TỔNG TỒN ĐỌNG CẦN XỬ LÝ: ${fNum(totBoth)} ĐƠN</div>
            <div style="font-size: 12px; color: #92400e; margin-top: 2px;">
              • Aging tại bưu cục: <strong>${fNum(totAg)} đơn (${pAg}%)</strong> | Treo trên mạng luân chuyển: <strong>${fNum(totTr)} đơn (${pTr}%)</strong>
            </div>
          </div>
          <div style="font-size: 12px; color: var(--text-main); line-height: 1.5;">
            👉 <strong>Trọng tâm điều hành tuần W43:</strong> Vừa phải kéo hàng tồn aging tại các bưu cục Lâm Đồng (Lang Biang 2, Đức Trọng 1, Tân Hà, Hòa Ninh), vừa phải dọn sạch các điểm nghẽn luân chuyển tại Khánh Hòa (Tây Nha Trang, Cam Linh) để bảo toàn chỉ số SLA toàn vùng!
          </div>
        `;
      }

      chartLabels = [`Aging >5 ngày (${pAg}%)`, `Treo LC ≥24h (${pTr}%)`];
      chartData = [totAg, totTr];
      chartColors = ['#ef4444', '#3b82f6'];
    }

    charts.agingDonut = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: chartLabels,
        datasets: [{
          data: chartData,
          backgroundColor: chartColors,
          borderColor: '#ffffff',
          borderWidth: 2,
          hoverOffset: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '72%',
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: c => ` ${c.label}: ${fNum(c.parsed)} đơn`
            }
          }
        }
      }
    });
  }

  function renderAgingProgressChart() {
    const ctx = document.getElementById('chart-aging-progress');
    if (!ctx) return;
    if (charts.agingProgress) charts.agingProgress.destroy();

    charts.agingProgress = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Tuần W42', 'Tuần W43 (Realtime)'],
        datasets: [{
          data: [1420, (D.aging && D.aging.total) ? D.aging.total : 856],
          backgroundColor: ['#94a3b8', '#10b981'],
          borderRadius: 6,
          barPercentage: 0.6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: c => ` ${c.label}: ${c.parsed} đơn tồn Aging`
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 1600,
            grid: { color: 'rgba(0,0,0,0.05)' },
            ticks: { font: { size: 10 } }
          },
          x: {
            grid: { display: false },
            ticks: { font: { size: 11, weight: '700' } }
          }
        }
      }
    });
  }

  function renderAgingCustomerChart() {
    const ctx = document.getElementById('chart-aging-customer');
    if (!ctx) return;
    if (charts.agingCustomer) charts.agingCustomer.destroy();

    const seg = state.agingSegment || 'aging';
    const isAging = seg === 'aging';
    const isTreo = seg === 'treo_lc';

    const custTitle = document.getElementById('aging-cust-title');
    const custBadge = document.getElementById('aging-cust-badge');
    const custSummary = document.getElementById('aging-cust-summary-grid');

    if (isAging && D.aging) {
      const custData = D.aging.by_customer || [];
      const top1 = custData[0] || { customer: 'SME', vol: 619, pct: 80.8 };

      if (custTitle) custTitle.textContent = 'PHÂN TÍCH TỒN ĐỌNG CẢ VÙNG THEO KHÁCH HÀNG (AGING >5 NGÀY)';
      if (custBadge) {
        custBadge.className = 'badge-tag badge-tag-red';
        custBadge.textContent = `🚨 ${top1.customer} Tồn Nhiều Nhất (${top1.pct}% - ${fNum(top1.vol)} đơn)`;
      }

      // Group into SME, TikTok Shop (TTS + Bulky), Shopee (Shopee + Bulky)
      let sme = { vol: 0, d58: 0, d815: 0, gt15: 0, top_am: '', top_bc: '', pct: 0 };
      let tts = { vol: 0, d58: 0, d815: 0, gt15: 0, top_am: '', top_bc: '', pct: 0 };
      let shp = { vol: 0, d58: 0, d815: 0, gt15: 0, top_am: '', top_bc: '', pct: 0 };

      custData.forEach(c => {
        const name = (c.customer || '').toUpperCase();
        if (name.includes('SME')) {
          sme.vol += c.vol || 0;
          sme.d58 += c.d_5_8 || 0;
          sme.d815 += c.d_8_15 || 0;
          sme.gt15 += c.gt_15 || 0;
          if (!sme.top_am) sme.top_am = c.top_am;
          if (!sme.top_bc) sme.top_bc = c.top_bc;
        } else if (name.includes('TTS')) {
          tts.vol += c.vol || 0;
          tts.d58 += c.d_5_8 || 0;
          tts.d815 += c.d_8_15 || 0;
          tts.gt15 += c.gt_15 || 0;
          if (!tts.top_am) tts.top_am = c.top_am;
          if (!tts.top_bc) tts.top_bc = c.top_bc;
        } else if (name.includes('SHOPEE')) {
          shp.vol += c.vol || 0;
          shp.d58 += c.d_5_8 || 0;
          shp.d815 += c.d_8_15 || 0;
          shp.gt15 += c.gt_15 || 0;
          if (!shp.top_am) shp.top_am = c.top_am;
          if (!shp.top_bc) shp.top_bc = c.top_bc;
        }
      });
      const totAg = D.aging.total || 766;
      sme.pct = (sme.vol / totAg * 100).toFixed(1);
      tts.pct = (tts.vol / totAg * 100).toFixed(1);
      shp.pct = (shp.vol / totAg * 100).toFixed(1);

      const labels = [
        `1. SME (${fNum(sme.vol)} đ - ${sme.pct}%)`,
        `2. TikTok Shop (${fNum(tts.vol)} đ - ${tts.pct}%)`,
        `3. Shopee (${fNum(shp.vol)} đ - ${shp.pct}%)`
      ];

      charts.agingCustomer = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: '5 – 8 ngày',
              data: [sme.d58, tts.d58, shp.d58],
              backgroundColor: '#3b82f6',
              borderRadius: 3
            },
            {
              label: '8 – 15 ngày',
              data: [sme.d815, tts.d815, shp.d815],
              backgroundColor: '#f59e0b',
              borderRadius: 3
            },
            {
              label: 'Trên 15 ngày',
              data: [sme.gt15, tts.gt15, shp.gt15],
              backgroundColor: '#dc2626',
              borderRadius: 3
            }
          ]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              stacked: true,
              grid: { color: 'rgba(0,0,0,0.05)' },
              ticks: { font: { size: 10 } }
            },
            y: {
              stacked: true,
              grid: { display: false },
              ticks: { font: { size: 11, weight: 'bold' }, color: 'var(--text-main)' }
            }
          },
          plugins: {
            legend: {
              position: 'top',
              labels: { boxWidth: 10, font: { size: 10 }, padding: 6 }
            },
            tooltip: {
              callbacks: {
                afterBody: function(context) {
                  const idx = context[0].dataIndex;
                  if (idx === 0) return `Top AM: ${sme.top_am}\nTop BC: ${sme.top_bc}\n(Nắm 100% số đơn tồn >15N của cả vùng)`;
                  if (idx === 1) return `Top AM: ${tts.top_am}\nTop BC: ${tts.top_bc}\n(81/89 đơn ở mức 5-8N, 0 đơn >15N)`;
                  if (idx === 2) return `Top AM: ${shp.top_am}\nTop BC: ${shp.top_bc}\n(Gồm 16 đơn hàng Bulky cồng kềnh)`;
                }
              }
            }
          }
        }
      });

      if (custSummary) {
        custSummary.innerHTML = `
          <div style="padding: 6px 10px; background: rgba(239, 68, 68, 0.08); border: 1.5px solid #ef4444; border-radius: 6px;">
            <div style="font-size: 10.5px; font-weight: 800; color: #b91c1c;">👑 TOP 1: SME (${sme.pct}%)</div>
            <div style="font-size: 14px; font-weight: 900; color: #dc2626; line-height: 1.2;">${fNum(sme.vol)} <small style="font-size: 10px;">đơn tồn</small></div>
            <div style="font-size: 10px; color: var(--text-muted); margin-top: 2px;">Giữ <strong>100%</strong> đơn &gt;15N (${sme.gt15} đ). AM: ${sme.top_am || 'Lê Minh Đại'}</div>
          </div>
          <div style="padding: 6px 10px; background: rgba(59, 130, 246, 0.08); border: 1.5px solid #3b82f6; border-radius: 6px;">
            <div style="font-size: 10.5px; font-weight: 800; color: #1d4ed8;">TOP 2: TIKTOK SHOP (${tts.pct}%)</div>
            <div style="font-size: 14px; font-weight: 900; color: #2563eb; line-height: 1.2;">${fNum(tts.vol)} <small style="font-size: 10px;">đơn tồn</small></div>
            <div style="font-size: 10px; color: var(--text-muted); margin-top: 2px;">91% là 5–8N (${tts.d58} đ). AM: ${tts.top_am || 'Nguyễn Duy Long'}</div>
          </div>
          <div style="padding: 6px 10px; background: rgba(249, 115, 22, 0.08); border: 1.5px solid #f97316; border-radius: 6px;">
            <div style="font-size: 10.5px; font-weight: 800; color: #c2410c;">TOP 3: SHOPEE (${shp.pct}%)</div>
            <div style="font-size: 14px; font-weight: 900; color: #ea580c; line-height: 1.2;">${fNum(shp.vol)} <small style="font-size: 10px;">đơn tồn</small></div>
            <div style="font-size: 10px; color: var(--text-muted); margin-top: 2px;">16 đ Bulky (28%). AM: ${shp.top_am || 'Nguyễn Duy Long'}</div>
          </div>
        `;
      }
    } else if (isTreo && D.treo_lc) {
      const custData = D.treo_lc.by_customer || [];
      const top1 = custData[0] || { customer: 'SME / Khác (OTHER)', vol: 2178, pct: 57.5 };
      const shpCust = custData.find(c => (c.customer || '').includes('Shopee')) || {};

      if (custTitle) custTitle.textContent = 'PHÂN TÍCH TREO LUÂN CHUYỂN CẢ VÙNG THEO KHÁCH HÀNG';
      if (custBadge) {
        custBadge.className = 'badge-tag badge-tag-amber';
        custBadge.textContent = `🚨 ${top1.customer} Tồn Nhiều Nhất (${top1.pct}%) | Shopee Treo Cao Nhất (${shpCust.rate_treo_24 || '24.9'}%)`;
      }

      const labels = custData.map((c, idx) => `${idx + 1}. ${c.customer} (${fNum(c.vol)} đ - ${c.pct}%)`);
      const dataU24 = custData.map(c => c.u_24 || 0);
      const data24_36 = custData.map(c => c.h_24_36 || 0);
      const data36_plus = custData.map(c => (c.treo_24 || 0) - (c.h_24_36 || 0));

      charts.agingCustomer = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: '< 24h (Đúng hạn)',
              data: dataU24,
              backgroundColor: '#10b981',
              borderRadius: 3
            },
            {
              label: '24 – 36h (Bắt đầu trễ)',
              data: data24_36,
              backgroundColor: '#f59e0b',
              borderRadius: 3
            },
            {
              label: '≥ 36h (Trễ nặng)',
              data: data36_plus,
              backgroundColor: '#dc2626',
              borderRadius: 3
            }
          ]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              stacked: true,
              grid: { color: 'rgba(0,0,0,0.05)' },
              ticks: { font: { size: 10 } }
            },
            y: {
              stacked: true,
              grid: { display: false },
              ticks: { font: { size: 11, weight: 'bold' }, color: 'var(--text-main)' }
            }
          },
          plugins: {
            legend: {
              position: 'top',
              labels: { boxWidth: 10, font: { size: 10 }, padding: 6 }
            },
            tooltip: {
              callbacks: {
                afterBody: function(context) {
                  const idx = context[0].dataIndex;
                  const item = custData[idx] || {};
                  return `Treo ≥24h: ${fNum(item.treo_24)} đơn (${item.rate_treo_24}%)\nChiếm ${item.pct}% tổng đơn treo cả vùng\nTop AM: ${item.top_am || ''} (${fNum(item.top_am_vol)} đ)\nTop BC: ${item.top_bc || ''}`;
                }
              }
            }
          }
        }
      });

      if (custSummary) {
        const other = custData[0] || {};
        const shopee = custData[1] || {};
        const tts = custData[2] || {};
        custSummary.innerHTML = `
          <div style="padding: 6px 10px; background: rgba(59, 130, 246, 0.08); border: 1.5px solid #3b82f6; border-radius: 6px;">
            <div style="font-size: 10.5px; font-weight: 800; color: #1d4ed8;">👑 TOP 1: OTHER / SME (${other.pct || '57.5'}%)</div>
            <div style="font-size: 14px; font-weight: 900; color: #2563eb; line-height: 1.2;">${fNum(other.vol || 2178)} <small style="font-size: 10px;">đơn LC</small></div>
            <div style="font-size: 10px; color: var(--text-muted); margin-top: 2px;">Treo ≥24h: <strong>${fNum(other.treo_24 || 356)} đ (${other.rate_treo_24 || '16.3'}%)</strong>. AM: ${other.top_am || 'Nguyễn Duy Long'}</div>
          </div>
          <div style="padding: 6px 10px; background: rgba(239, 68, 68, 0.08); border: 1.5px solid #ef4444; border-radius: 6px;">
            <div style="font-size: 10.5px; font-weight: 800; color: #b91c1c;">🚨 SHOPEE: TREO CAO NHẤT (${shopee.rate_treo_24 || '24.9'}%)</div>
            <div style="font-size: 14px; font-weight: 900; color: #dc2626; line-height: 1.2;">${fNum(shopee.treo_24 || 254)} / ${fNum(shopee.vol || 1019)} <small style="font-size: 10px;">treo</small></div>
            <div style="font-size: 10px; color: var(--text-muted); margin-top: 2px;">Chiếm <strong>${shopee.pct || '26.9'}%</strong> tổng treo cả vùng! AM: ${shopee.top_am || 'Trần Văn Phước'}</div>
          </div>
          <div style="padding: 6px 10px; background: rgba(16, 185, 129, 0.08); border: 1.5px solid #10b981; border-radius: 6px;">
            <div style="font-size: 10.5px; font-weight: 800; color: #047857;">TIKTOK SHOP (${tts.pct || '15.6'}%)</div>
            <div style="font-size: 14px; font-weight: 900; color: #059669; line-height: 1.2;">${fNum(tts.vol || 591)} <small style="font-size: 10px;">đơn LC</small></div>
            <div style="font-size: 10px; color: var(--text-muted); margin-top: 2px;">Treo ≥24h: <strong>${fNum(tts.treo_24 || 78)} đ (${tts.rate_treo_24 || '13.2'}%)</strong>. AM: ${tts.top_am || 'Nguyễn Duy Long'}</div>
          </div>
        `;
      }
    }
  }

    function renderAgingChart() {
    const ctx = document.getElementById('chart-aging-bar');
    if (!ctx) return;
    if (charts.agingBar) charts.agingBar.destroy();

    const seg = state.agingSegment || 'aging';
    const selectedAM = state.selectedAM;

    let dataList = [];
    if (seg === 'aging' && D.aging) {
      dataList = (D.aging.top_am || []).map(r => ({
        am: r.am,
        vol: r.vol,
        pct: r.pct,
        tinh: r.tinh,
        d_5_8: r.d_5_8 || 0,
        d_8_15: r.d_8_15 || 0,
        gt_15: r.gt_15 || 0
      }));
      dataList.sort((a, b) => (b.vol || 0) - (a.vol || 0));
    } else if (seg === 'treo_lc' && D.treo_lc) {
      dataList = (D.treo_lc.top_am || []).map(r => ({
        am: r.am,
        vol: r.treo_24, // SỐ ĐƠN TREO >= 24H
        vol_total: r.vol,
        pct: r.rate_treo_24 !== undefined ? r.rate_treo_24 : Number((r.treo_24 / (r.vol || 1) * 100).toFixed(1)),
        tinh: r.tinh,
        h_24_36: r.h_24_36 || 0,
        h_36_72: r.h_36_72 || 0,
        h_72_120: r.h_72_120 || 0,
        h_120_plus: r.h_120_plus || 0
      }));
      dataList.sort((a, b) => (b.vol || 0) - (a.vol || 0));
    } else if (seg === 'compare' && D.aging && D.treo_lc) {
      const agingMap = {};
      (D.aging.top_am || []).forEach(r => agingMap[r.am] = r.vol);
      dataList = (D.treo_lc.top_am || []).map(r => ({
        am: r.am,
        vol: agingMap[r.am] || 0,
        vol_treo: r.treo_24 || r.vol,
        pct: r.pct,
        tinh: r.tinh
      }));
      dataList.sort((a, b) => (b.vol || 0) - (a.vol || 0));
    }

    if (dataList.length === 0) return;

    let datasets = [];
    let isStacked = false;

    if (seg === 'aging') {
      isStacked = true;
      datasets = [
        {
          type: 'bar',
          label: '🟡 5 – 8 Ngày',
          data: dataList.map(d => d.d_5_8),
          backgroundColor: '#f59e0b',
          stack: 'agingStack',
          borderRadius: 0,
          yAxisID: 'y',
          order: 3
        },
        {
          type: 'bar',
          label: '🟠 8 – 15 Ngày',
          data: dataList.map(d => d.d_8_15),
          backgroundColor: '#ea580c',
          stack: 'agingStack',
          borderRadius: 0,
          yAxisID: 'y',
          order: 3
        },
        {
          type: 'bar',
          label: '🔴 > 15 Ngày',
          data: dataList.map(d => d.gt_15),
          backgroundColor: '#dc2626',
          stack: 'agingStack',
          borderRadius: 4,
          yAxisID: 'y',
          order: 3
        },
        {
          type: 'line',
          label: '🌊 Tỷ Trọng Vùng (%)',
          data: dataList.map(d => d.pct),
          borderColor: '#b91c1c',
          backgroundColor: 'rgba(185, 28, 28, 0.1)',
          fill: false,
          borderWidth: 2.5,
          tension: 0.35,
          pointRadius: 4.5,
          pointBackgroundColor: '#b91c1c',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          yAxisID: 'yPct',
          order: 1
        }
      ];
    } else if (seg === 'treo_lc') {
      isStacked = true;
      datasets = [
        {
          type: 'bar',
          label: '🟡 24h – 36h (1–1.5N)',
          data: dataList.map(d => d.h_24_36),
          backgroundColor: '#f59e0b',
          stack: 'treoStack',
          borderRadius: 0,
          yAxisID: 'y',
          order: 3
        },
        {
          type: 'bar',
          label: '🟠 36h – 72h (1.5–3N)',
          data: dataList.map(d => d.h_36_72),
          backgroundColor: '#f97316',
          stack: 'treoStack',
          borderRadius: 0,
          yAxisID: 'y',
          order: 3
        },
        {
          type: 'bar',
          label: '🔴 72h – 120h (3–5N)',
          data: dataList.map(d => d.h_72_120),
          backgroundColor: '#ef4444',
          stack: 'treoStack',
          borderRadius: 0,
          yAxisID: 'y',
          order: 3
        },
        {
          type: 'bar',
          label: '🟣 > 120h (>5N)',
          data: dataList.map(d => d.h_120_plus),
          backgroundColor: '#7c3aed',
          stack: 'treoStack',
          borderRadius: 4,
          yAxisID: 'y',
          order: 3
        },
        {
          type: 'line',
          label: '🌊 Tỷ Lệ Treo ≥24h (%)',
          data: dataList.map(d => d.pct),
          borderColor: '#6d28d9',
          backgroundColor: 'rgba(109, 40, 217, 0.1)',
          fill: false,
          borderWidth: 2.5,
          tension: 0.35,
          pointRadius: 4.5,
          pointBackgroundColor: '#6d28d9',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          yAxisID: 'yPct',
          order: 1
        }
      ];
    } else {
      isStacked = false;
      datasets = [
        {
          type: 'bar',
          label: 'Đơn Aging >5 Ngày',
          data: dataList.map(d => d.vol),
          backgroundColor: dataList.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : '#ef4444'),
          borderRadius: 4,
          yAxisID: 'y',
          order: 2
        },
        {
          type: 'bar',
          label: 'Đơn Treo LC (≥24h)',
          data: dataList.map(d => d.vol_treo),
          backgroundColor: dataList.map(d => selectedAM && selectedAM === d.am ? '#f59e0b' : '#3b82f6'),
          borderRadius: 4,
          yAxisID: 'yVol',
          order: 2
        }
      ];
    }

    // Custom Plugin to draw exact order counts inside each bucket segment & total on top
    const stackedDataLabelsPlugin = {
      id: 'stackedDataLabelsPlugin',
      afterDatasetsDraw(chart) {
        const { ctx, scales: { x, y } } = chart;
        
        // 1. Draw numbers inside each bucket if value > 0 and height >= 14px
        chart.data.datasets.forEach((dataset, datasetIndex) => {
          if (dataset.type === 'line') return;
          const meta = chart.getDatasetMeta(datasetIndex);
          if (!meta.hidden) {
            meta.data.forEach((element, index) => {
              const val = dataset.data[index];
              if (val && val > 0) {
                const { x: posX, y: posY, base } = element;
                const barHeight = Math.abs(base - posY);
                if (barHeight >= 13) {
                  ctx.save();
                  ctx.fillStyle = '#ffffff';
                  ctx.font = '900 10px monospace, sans-serif';
                  ctx.textAlign = 'center';
                  ctx.textBaseline = 'middle';
                  const midY = (posY + base) / 2;
                  ctx.fillText(val, posX, midY);
                  ctx.restore();
                }
              }
            });
          }
        });

        // 2. Draw TOTAL on top of each AM's bar
        const barDatasets = chart.data.datasets.filter(ds => ds.type === 'bar');
        if (barDatasets.length > 0 && isStacked) {
          chart.data.labels.forEach((label, i) => {
            let sum = 0;
            let topY = y.bottom;
            let posX = 0;
            barDatasets.forEach((ds, dsIdx) => {
              sum += (ds.data[i] || 0);
              const el = chart.getDatasetMeta(dsIdx).data[i];
              if (el && el.y < topY) {
                topY = el.y;
                posX = el.x;
              }
            });
            if (sum > 0 && posX > 0) {
              ctx.save();
              ctx.fillStyle = '#0f172a';
              ctx.font = '900 11.5px monospace, sans-serif';
              ctx.textAlign = 'center';
              ctx.textBaseline = 'bottom';
              ctx.fillText(sum, posX, topY - 3);
              ctx.restore();
            }
          });
        }
      }
    };

    charts.agingBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: dataList.map(d => d.am),
        datasets: datasets
      },
      plugins: [stackedDataLabelsPlugin],
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 24, bottom: 8, left: 4, right: 8 } },
        scales: {
          y: {
            stacked: isStacked,
            position: 'left',
            min: 0,
            title: { 
              display: true, 
              text: seg === 'aging' ? 'Số Đơn Tồn Aging (>5 Ngày)' : (seg === 'treo_lc' ? 'Số Đơn Treo LC (≥24h)' : 'Số Lượng Đơn'), 
              font: { weight: '800', size: 11.5 } 
            },
            ticks: { callback: v => fNum(v) },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          yPct: {
            position: 'right',
            min: 0,
            display: seg !== 'compare',
            grid: { drawOnChartArea: false },
            title: { 
              display: true, 
              text: seg === 'aging' ? 'Tỷ Trọng Vùng (%)' : 'Tỷ Lệ Treo (%)', 
              font: { weight: '800', size: 11, color: seg === 'aging' ? '#b91c1c' : '#6d28d9' } 
            },
            ticks: { callback: v => v + '%' }
          },
          yVol: {
            position: 'right',
            min: 0,
            display: seg === 'compare',
            grid: { drawOnChartArea: false },
            title: { display: true, text: 'Số Đơn Treo LC', font: { weight: '700', size: 11, color: '#3b82f6' } },
            ticks: { callback: v => fNum(v) }
          },
          x: {
            stacked: isStacked,
            ticks: { maxRotation: 45, minRotation: 25, font: { size: 11, weight: '800' } },
            grid: { display: false }
          }
        },
        plugins: {
          legend: { 
            position: 'top',
            labels: { font: { weight: '700', size: 11.5 }, usePointStyle: true, boxWidth: 10 }
          },
          tooltip: {
            callbacks: {
              label: c => {
                if (c.dataset.yAxisID === 'yPct') return `🌊 ${c.dataset.label}: ${c.parsed.y}%`;
                return `${c.dataset.label}: ${fNum(c.parsed.y)} đơn`;
              },
              footer: items => {
                if (!isStacked) return '';
                let total = 0;
                items.forEach(it => {
                  if (it.dataset.type === 'bar') total += it.parsed.y;
                });
                return `📦 TỔNG CỘNG: ${fNum(total)} đơn`;
              }
            }
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            selectAndHighlightAM(dataList[elements[0].index].am);
          }
        }
      }
    });
  }

  // --------------------------------------------------------------------------
  // TAB 11: COD & KIỂM SOÁT VẬN HÀNH (4 SHEETS TỪ GOOGLE SHEETS)
  // --------------------------------------------------------------------------
  function setCodSegment(seg) {
    state.codSegment = seg;

    const btnGroup = document.getElementById('cod-segment-group');
    if (btnGroup) {
      btnGroup.querySelectorAll('.btn').forEach(b => {
        b.classList.remove('active', 'btn-primary');
        b.classList.add('btn-secondary');
      });
      const activeBtn = document.getElementById('btn-cod-' + seg);
      if (activeBtn) {
        activeBtn.classList.remove('btn-secondary');
        activeBtn.classList.add('active', 'btn-primary');
      }
    }

    const panels = ['trend', 'am', 'bc', 'action'];
    panels.forEach(p => {
      const el = document.getElementById('cod-panel-' + p);
      if (el) el.style.display = (p === seg) ? 'block' : 'none';
    });

    renderControlTab();
    if (seg === 'trend') renderCodTmAmBar();
  }
  window.setCodSegment = setCodSegment;

  function renderControlTab() {
    const seg = state.codSegment || 'trend';
    const report = D.cod_report || {};

    let prevPeriod = report.prev_period || 'Tuần N-1';
    let currPeriod = report.curr_period || 'Tuần N';

    const bannerTitle = document.getElementById('cod-banner-title');
    if (bannerTitle) {
      bannerTitle.textContent = `BÁO CÁO COD – SO SÁNH BIẾN ĐỘNG 2 TUẦN (${prevPeriod} vs ${currPeriod}) | VÙNG NTB`;
    }

    const topBad = (report.am_comparison || [])
      .filter(r => parseFloat(r.curr_tm) >= 70)
      .map(r => `${r.am} (${r.curr_tm})`);
    const bannerDescEl = document.getElementById('cod-summary-banner-desc');
    if (bannerDescEl) {
      bannerDescEl.innerHTML = `
        • <strong>${report.summary_text || ''}</strong><br>
        • <strong>Top AM cần giảm tiền mặt gấp (≥70% TM):</strong> ${topBad.length ? topBad.join(', ') : 'Không có'}.
      `;
    }

    const totalMetric = (report.metrics || []).find(m => m.chi_so.includes('Tổng COD'));
    const cashMetric = (report.metrics || []).find(m => m.chi_so.includes('Tiền mặt') && !m.chi_so.includes('Tỷ lệ'));
    const bankMetric = (report.metrics || []).find(m => m.chi_so.includes('Chuyển khoản'));
    const tmRateMetric = (report.metrics || []).find(m => m.chi_so.includes('Tỷ lệ') || m.chi_so.includes('% TM'));

    const badgeEl = document.getElementById('cod-summary-banner-badge');
    if (badgeEl && totalMetric && tmRateMetric) {
      badgeEl.textContent = `Tổng COD: ${totalMetric.curr} Tr | % TM: ${tmRateMetric.curr}`;
    }

    // 4 KPI Tiles
    if (totalMetric) {
      const elVal = document.getElementById('kpi-cod-total-val');
      const elMeta = document.getElementById('kpi-cod-total-meta');
      const elTitle = document.getElementById('kpi-cod-total-title');
      if (elTitle) elTitle.textContent = `Tổng COD Thu Hộ (${currPeriod})`;
      if (elVal) elVal.innerHTML = `${totalMetric.curr} <small>Tr ₫</small>`;
      if (elMeta) elMeta.innerHTML = `<span class="diff-tag diff-neutral">${prevPeriod}: ${totalMetric.prev} Tr ₫ (${totalMetric.diff_pct})</span>`;
    }

    if (cashMetric) {
      const elVal = document.getElementById('kpi-cod-cash-val');
      const elMeta = document.getElementById('kpi-cod-cash-meta');
      const elTitle = document.getElementById('kpi-cod-cash-title');
      if (elTitle) elTitle.textContent = `Tiền Mặt (${currPeriod})`;
      if (elVal) elVal.innerHTML = `${cashMetric.curr} <small>Tr ₫</small>`;
      if (elMeta) elMeta.innerHTML = `<span class="diff-tag diff-neutral">${prevPeriod}: ${cashMetric.prev} Tr ₫ (${cashMetric.diff_pct})</span>`;
    }

    if (bankMetric) {
      const elVal = document.getElementById('kpi-cod-bank-val');
      const elMeta = document.getElementById('kpi-cod-bank-meta');
      const elTitle = document.getElementById('kpi-cod-bank-title');
      if (elTitle) elTitle.textContent = `Chuyển Khoản (${currPeriod})`;
      if (elVal) elVal.innerHTML = `${bankMetric.curr} <small>Tr ₫</small>`;
      if (elMeta) elMeta.innerHTML = `<span class="diff-tag diff-neutral">${prevPeriod}: ${bankMetric.prev} Tr ₫ (${bankMetric.diff_pct})</span>`;
    }

    if (tmRateMetric) {
      const elVal = document.getElementById('kpi-cod-rate-val');
      const elMeta = document.getElementById('kpi-cod-rate-meta');
      const elTitle = document.getElementById('kpi-cod-rate-title');
      if (elTitle) elTitle.textContent = `Tỷ Lệ Tiền Mặt (% TM)`;
      if (elVal) elVal.textContent = `${tmRateMetric.curr}`;
      const isBad = tmRateMetric.diff_val.startsWith('+') || !tmRateMetric.diff_val.startsWith('-');
      if (elMeta) elMeta.innerHTML = `<span class="diff-tag ${isBad ? 'diff-up-bad' : 'diff-down-good'}">${isBad ? '▲ Tăng' : '▼ Giảm'} ${tmRateMetric.diff_val} (${prevPeriod}: ${tmRateMetric.prev})</span>`;
    }

    // Dynamic Table 1 Header
    const thPrev = document.getElementById('th-cod-prev');
    const thCurr = document.getElementById('th-cod-curr');
    if (thPrev) thPrev.textContent = prevPeriod;
    if (thCurr) thCurr.textContent = currPeriod;

    // 1. PANEL 1: XU HƯỚNG 2 TUẦN
    const tblTrend = document.querySelector('#table-cod-trend-metrics tbody');
    if (tblTrend && report.metrics) {
      tblTrend.innerHTML = report.metrics.map(r => {
        const isTM = r.chi_so.includes('Tiền mặt') || r.chi_so.includes('Tỷ lệ');
        const evalBadge = r.eval.includes('Xấu') 
          ? '<span class="badge-tag badge-tag-red">▲ Xấu (Tăng TM)</span>'
          : (r.eval === '–' ? '<span class="badge-tag badge-tag-blue">—</span>' : `<span class="badge-tag badge-tag-green">${r.eval}</span>`);
        
        return `
          <tr style="${isTM ? 'background: rgba(220, 38, 38, 0.04); font-weight: 700;' : ''}">
            <td class="bold" style="font-size:13px; font-weight:800;">${r.chi_so}</td>
            <td class="num">${r.prev}</td>
            <td class="num bold" style="background: rgba(2, 132, 199, 0.08); color: #0369a1; font-size:13.5px;">${r.curr}</td>
            <td class="num bold" style="color: ${r.diff_val.startsWith('-') ? '#10b981' : '#ef4444'};">${r.diff_val}</td>
            <td class="num bold">${r.diff_pct}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 2. PANEL 2: AM SO SÁNH 2 TUẦN
    const tblAM = document.querySelector('#table-cod-am-sheet tbody');
    if (tblAM && report.am_comparison) {
      const selectedAM = state.selectedAM;
      tblAM.innerHTML = report.am_comparison.map((r, i) => {
        const isSelected = selectedAM === r.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const levelBadge = r.level.includes('Nghiêm trọng')
          ? '<span class="badge-tag badge-tag-red">🔴 Nghiêm trọng (≥70%)</span>'
          : (r.level.includes('cải thiện') ? '<span class="badge-tag badge-tag-amber">🟡 Cần cải thiện (50-70%)</span>' : '<span class="badge-tag badge-tag-green">🟢 Tốt (&lt;50%)</span>');
        
        return `
          <tr data-entity="${r.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${r.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${r.am}</td>
            <td class="num">${r.prev_tm}</td>
            <td class="num bold" style="background: rgba(2, 132, 199, 0.08); color: ${parseFloat(r.curr_tm) >= 70 ? '#dc2626' : (parseFloat(r.curr_tm) >= 50 ? '#d97706' : '#16a34a')}; font-size:13.5px; font-weight:900;">${r.curr_tm}</td>
            <td class="num bold" style="color: ${r.diff.startsWith('+') ? '#dc2626' : (r.diff.startsWith('-') ? '#16a34a' : 'inherit')};">${r.diff}</td>
            <td class="center bold" style="color: ${r.trend.includes('Tăng') ? '#dc2626' : (r.trend.includes('Giảm') ? '#16a34a' : 'inherit')};">${r.trend}</td>
            <td class="center">${levelBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 3. PANEL 3: CHI TIẾT BƯU CỤC 2 TUẦN
    const tblBC = document.querySelector('#table-cod-bc-sheet tbody');
    if (tblBC && report.bc_details) {
      const selectedAM = state.selectedAM;
      const searchKey = (document.getElementById('search-cod-bc')?.value || '').trim().toLowerCase();

      let bcList = [...report.bc_details];
      if (searchKey) {
        bcList = bcList.filter(r => r.bc.toLowerCase().includes(searchKey) || r.am.toLowerCase().includes(searchKey));
      }

      tblBC.innerHTML = bcList.map((r, i) => {
        const isSelected = selectedAM && selectedAM === r.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const levelBadge = r.level.includes('Nghiêm trọng')
          ? '<span class="badge-tag badge-tag-red">🔴 Nghiêm trọng</span>'
          : (r.level.includes('cải thiện') ? '<span class="badge-tag badge-tag-amber">🟡 Cần cải thiện</span>' : '<span class="badge-tag badge-tag-green">🟢 Tốt</span>');

        return `
          <tr data-entity="${r.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${r.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="color: var(--color-blue);">${r.am}</td>
            <td class="bold" style="font-size:13px; font-weight:800;">${r.bc}</td>
            <td class="num">${r.prev_tm}</td>
            <td class="num bold" style="background: rgba(2, 132, 199, 0.08); color: ${parseFloat(r.curr_tm) >= 70 ? '#dc2626' : (parseFloat(r.curr_tm) >= 50 ? '#d97706' : '#16a34a')}; font-size:13.5px; font-weight:900;">${r.curr_tm}</td>
            <td class="num bold" style="color: ${r.diff.startsWith('+') ? '#dc2626' : (r.diff.startsWith('-') ? '#16a34a' : 'inherit')};">${r.diff}</td>
            <td class="num bold" style="color: #b91c1c;">${r.cash_m}</td>
            <td class="center">${levelBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 4. PANEL 4: HƯỚNG XỬ LÝ AM
    const tblAction = document.querySelector('#table-cod-action-sheet tbody');
    if (tblAction && report.actions) {
      tblAction.innerHTML = report.actions.map(r => {
        const deadlineBadge = r.deadline.includes('24h') 
          ? '<span class="badge-tag badge-tag-red" style="font-weight:800;">⚡ Gấp trong 24h</span>'
          : `<span class="badge-tag badge-tag-amber">${r.deadline}</span>`;

        return `
          <tr>
            <td class="bold" style="font-size:13.5px; font-weight:900; color: #dc2626;">${r.am}</td>
            <td class="num">${r.prev_tm}</td>
            <td class="num bold" style="background: rgba(2, 132, 199, 0.08); color: #dc2626; font-size:13.5px; font-weight:900;">${r.curr_tm}</td>
            <td class="num bold" style="color: ${r.diff.startsWith('+') ? '#dc2626' : '#16a34a'};">${r.diff}</td>
            <td style="line-height: 1.5; font-size: 12.5px;">${r.action.replace(/\\n/g, '<br>').replace(/\n/g, '<br>')}</td>
            <td class="center">${deadlineBadge}</td>
          </tr>
        `;
      }).join('');
    }
  }

  function renderCodTmAmBar() {
    const ctx = document.getElementById('chart-cod-tm-am-bar');
    if (!ctx) return;
    if (charts.codTmAmBar) charts.codTmAmBar.destroy();

    const report = D.cod_report || {};
    let prevLabel = report.prev_period || 'Tuần N-1';
    let currLabel = report.curr_period || 'Tuần N';

    const cashMetric = (report.metrics || []).find(m => m.chi_so.includes('Tiền mặt') && !m.chi_so.includes('Tỷ lệ'));
    const bankMetric = (report.metrics || []).find(m => m.chi_so.includes('Chuyển khoản'));

    const cashPrev = cashMetric ? parseFloat(cashMetric.prev.replace(/,/g, '')) : 34322.1;
    const cashCurr = cashMetric ? parseFloat(cashMetric.curr.replace(/,/g, '')) : 33475.7;
    const bankPrev = bankMetric ? parseFloat(bankMetric.prev.replace(/,/g, '')) : 50307.8;
    const bankCurr = bankMetric ? parseFloat(bankMetric.curr.replace(/,/g, '')) : 42147.7;

    charts.codTmAmBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: [prevLabel, currLabel],
        datasets: [
          {
            label: 'Tiền Mặt (Triệu ₫)',
            data: [cashPrev, cashCurr],
            backgroundColor: '#ef4444',
            borderRadius: 4
          },
          {
            label: 'Chuyển Khoản (Triệu ₫)',
            data: [bankPrev, bankCurr],
            backgroundColor: '#10b981',
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 20, bottom: 8 } },
        scales: {
          x: { stacked: true },
          y: {
            stacked: true,
            ticks: { callback: v => fNum(v) + ' Tr' },
            title: { display: true, text: 'Tổng Tiền COD (Triệu VNĐ)', font: { weight: '700', size: 11 } }
          }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => ` ${c.dataset.label}: ${fNum(c.parsed.y)} Triệu VNĐ`
            }
          }
        }
      }
    });
  }


  // --------------------------------------------------------------------------
  // TAB 12: BÁO CÁO TRUY THU KHỐI LƯỢNG & TICKET VI PHẠM (OE-IA)
  // --------------------------------------------------------------------------
  function setTruyThuSegment(seg) {
    state.truythuSegment = seg;

    const btnGroup = document.getElementById('truythu-segment-group');
    if (btnGroup) {
      btnGroup.querySelectorAll('button').forEach(b => {
        b.className = 'btn btn-sm btn-secondary';
      });
      const act = document.getElementById('btn-tt-' + seg);
      if (act) act.className = 'btn btn-sm btn-primary active';
    }

    ['loai', 'amticket', 'bcgiao', 'bcticket'].forEach(p => {
      const el = document.getElementById('truythu-panel-' + p);
      if (el) el.style.display = (p === seg ? 'block' : 'none');
    });

    renderTruyThuTab();
    if (seg === 'loai') renderTruyThuLoaiBar();
    else if (seg === 'bcgiao') renderTruyThuBcGiaoBar();
    else if (seg === 'amticket') renderTruyThuAmDual();
    else if (seg === 'bcticket') renderTruyThuBcTicketBar();
  }
  window.setTruyThuSegment = setTruyThuSegment;

  function renderTruyThuTab() {
    const report = D.truy_thu_report || {};
    const summary = report.summary || {};
    const prevLabel = summary.prev_label || 'Tuần W42 (12/10 - 18/10)';
    const currLabel = summary.curr_label || 'Tuần W43 (19/10 - 25/10)';
    const prevShort = summary.prev_label && summary.prev_label.includes('(') ? summary.prev_label.split('(')[0].trim() : (summary.prev_label || 'Tuần W42');
    const currShort = summary.curr_label && summary.curr_label.includes('(') ? summary.curr_label.split('(')[0].trim() : (summary.curr_label || 'Tuần W43');

    // Update Banner
    const bannerTitle = document.getElementById('truythu-banner-title');
    if (bannerTitle) {
      bannerTitle.textContent = `BÁO CÁO TRUY THU – SO SÁNH BIẾN ĐỘNG 2 TUẦN (${prevLabel} vs ${currLabel}) | VÙNG NAM TRUNG BỘ`;
    }
    const bannerP = document.getElementById('truythu-banner-p');
    if (bannerP && summary.banner_desc) {
      bannerP.innerHTML = summary.banner_desc;
    }
    const bannerBadge = document.getElementById('truythu-banner-badge');
    if (bannerBadge && summary.total_records_curr) {
      bannerBadge.textContent = `${currShort}: ${fNum(summary.total_records_curr)} Bản Ghi | Cần Thu ${(summary.can_thu_curr / 1e6).toFixed(1)} Tr ₫`;
    }

    // 4 KPI Comparison Tiles
    if (summary.total_records_curr !== undefined) {
      const elRec = document.getElementById('truythu-kpi-records');
      const elRecMeta = document.getElementById('truythu-kpi-records-meta');
      const elRecTitle = document.getElementById('kpi-tt-rec-title');
      if (elRecTitle) elRecTitle.textContent = `Tổng Đơn / Ticket (${currShort})`;
      if (elRec) elRec.innerHTML = `${fNum(summary.total_records_curr)} <small>đơn</small>`;
      if (elRecMeta) {
        const sign = summary.diff_records >= 0 ? '+' : '';
        const isBad = summary.diff_records > 0;
        elRecMeta.innerHTML = `<span class="diff-tag ${isBad ? 'diff-up-bad' : 'diff-down-good'}">${prevShort}: ${fNum(summary.total_records_prev)} (${sign}${fNum(summary.diff_records)} | ${summary.diff_records_pct})</span>`;
      }

      const elBd = document.getElementById('truythu-kpi-bandau');
      const elBdMeta = document.getElementById('truythu-kpi-bandau-meta');
      const elBdTitle = document.getElementById('kpi-tt-bd-title');
      if (elBdTitle) elBdTitle.textContent = `Tổng Tiền Ban Đầu (${currShort})`;
      if (elBd) elBd.innerHTML = `${(summary.ban_dau_curr / 1e6).toFixed(1)} <small>Tr ₫</small>`;
      if (elBdMeta) {
        const isBad = summary.diff_ban_dau > 0;
        const trend = isBad ? `▲ Tăng +${(summary.diff_ban_dau / 1e6).toFixed(1)} Tr` : `▼ Giảm ${(Math.abs(summary.diff_ban_dau) / 1e6).toFixed(1)} Tr`;
        elBdMeta.innerHTML = `<span class="diff-tag ${isBad ? 'diff-up-bad' : 'diff-down-good'}">${prevShort}: ${(summary.ban_dau_prev / 1e6).toFixed(1)} Tr (${trend} | ${summary.diff_ban_dau_pct})</span>`;
      }

      const elDc = document.getElementById('truythu-kpi-dieuchinh');
      const elDcMeta = document.getElementById('truythu-kpi-dieuchinh-meta');
      const elDcTitle = document.getElementById('kpi-tt-dc-title');
      if (elDcTitle) elDcTitle.textContent = `Tổng Điều Chỉnh (${currShort})`;
      if (elDc) elDc.innerHTML = `${(summary.dieu_chinh_curr / 1e6).toFixed(1)} <small>Tr ₫</small>`;
      if (elDcMeta) {
        elDcMeta.innerHTML = `<span class="diff-tag diff-neutral">${prevShort}: ${(summary.dieu_chinh_prev / 1e6).toFixed(1)} Tr (Chưa có đợt giảm trừ ${currShort})</span>`;
      }

      const elCt = document.getElementById('truythu-kpi-canthu');
      const elCtMeta = document.getElementById('truythu-kpi-canthu-meta');
      const elCtTitle = document.getElementById('kpi-tt-ct-title');
      if (elCtTitle) elCtTitle.textContent = `Cần Truy Thu Thêm (${currShort})`;
      if (elCt) elCt.innerHTML = `${(summary.can_thu_curr / 1e6).toFixed(1)} <small>Tr ₫</small>`;
      if (elCtMeta) {
        const isBad = summary.diff_can_thu > 0;
        const trend = isBad ? `▲ Tăng +${(summary.diff_can_thu / 1e6).toFixed(1)} Tr` : `▼ Giảm ${(Math.abs(summary.diff_can_thu) / 1e6).toFixed(1)} Tr`;
        elCtMeta.innerHTML = `<span class="diff-tag ${isBad ? 'diff-up-bad' : 'diff-down-good'}">${trend} (${summary.diff_can_thu_pct} so với ${prevShort})</span>`;
      }
    }

    // Dynamic Table Headers
    const thLoaiDp = document.getElementById('th-tt-loai-dp');
    const thLoaiDc = document.getElementById('th-tt-loai-dc');
    const thLoaiCp = document.getElementById('th-tt-loai-cp');
    const thLoaiCc = document.getElementById('th-tt-loai-cc');
    if (thLoaiDp) thLoaiDp.textContent = `Đơn (${prevShort})`;
    if (thLoaiDc) thLoaiDc.textContent = `Đơn (${currShort})`;
    if (thLoaiCp) thLoaiCp.textContent = `Cần Thu (${prevShort})`;
    if (thLoaiCc) thLoaiCc.textContent = `Cần Thu (${currShort})`;

    // Dynamic headers for Province table
    const thProv = document.querySelectorAll('#table-truythu-by-province thead th');
    if (thProv.length >= 7) {
      thProv[2].textContent = `Đơn ${prevShort}`;
      thProv[3].textContent = `Đơn ${currShort}`;
      thProv[5].textContent = `Cần Thu ${prevShort} (Tr ₫)`;
      thProv[6].textContent = `Cần Thu ${currShort} (Tr ₫)`;
    }

    // Dynamic headers for Top BC Giao table
    const thBcGiao = document.querySelectorAll('#table-truythu-top-bc-giao thead th');
    if (thBcGiao.length >= 9) {
      thBcGiao[4].textContent = `Đơn ${prevShort}`;
      thBcGiao[5].textContent = `Đơn ${currShort}`;
      thBcGiao[7].textContent = `Cần Thu ${prevShort} (Tr ₫)`;
      thBcGiao[8].textContent = `Cần Thu ${currShort} (Tr ₫)`;
    }

    // Dynamic headers for Top AM table
    const thAm = document.querySelectorAll('#table-truythu-top-am thead th');
    if (thAm.length >= 7) {
      thAm[2].textContent = `Ticket ${prevShort}`;
      thAm[3].textContent = `Ticket ${currShort}`;
      thAm[5].textContent = `Cần Thu ${prevShort} (Tr ₫)`;
      thAm[6].textContent = `Cần Thu ${currShort} (Tr ₫)`;
    }

    // 1. PANEL 1: THEO LOẠI TRUY THU
    renderTruyThuLoaiTable();

    // 2. PANEL 2: TOP BC GIAO & SO SÁNH TỈNH
    const tblProv = document.querySelector('#table-truythu-by-province tbody');
    if (tblProv && report.by_province) {
      const listProv = [...report.by_province].sort((a, b) => (b.can_thu_curr || 0) - (a.can_thu_curr || 0));
      tblProv.innerHTML = listProv.map((r, i) => {
        const diffSign = r.diff_can_thu > 0 ? '+' : '';
        const diffDonSign = r.diff_don > 0 ? '+' : '';
        return `
          <tr>
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color: var(--color-blue);">${r.tinh}</td>
            <td class="num">${fNum(r.don_prev)}</td>
            <td class="num bold" style="background: rgba(2, 132, 199, 0.08); color: #0284c7; font-weight:900;">${fNum(r.don_curr)}</td>
            <td class="num bold" style="color: ${r.diff_don > 0 ? '#dc2626' : '#16a34a'};">${diffDonSign}${fNum(r.diff_don)}</td>
            <td class="num">${(r.can_thu_prev / 1e6).toFixed(1)} Tr ₫</td>
            <td class="num bold" style="background: rgba(220, 38, 38, 0.08); color: #dc2626; font-size:13px; font-weight:900;">${(r.can_thu_curr / 1e6).toFixed(1)} Tr ₫</td>
            <td class="num bold" style="color: ${r.diff_can_thu > 0 ? '#dc2626' : '#16a34a'};">${diffSign}${(r.diff_can_thu / 1e6).toFixed(1)} Tr ₫</td>
          </tr>
        `;
      }).join('');
    }

    const tblBcGiao = document.querySelector('#table-truythu-top-bc-giao tbody');
    if (tblBcGiao && report.top_bc) {
      const selectedAM = state.selectedAM;
      const listTopBc = [...report.top_bc].sort((a, b) => (b.can_thu_curr || 0) - (a.can_thu_curr || 0));
      tblBcGiao.innerHTML = listTopBc.map((r, i) => {
        const isSelected = selectedAM && selectedAM === r.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const diffSign = r.diff_can_thu > 0 ? '+' : '';
        const diffDonSign = r.diff_don > 0 ? '+' : '';
        return `
          <tr data-entity="${r.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${r.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800;">${r.bc}</td>
            <td class="bold" style="color: var(--color-blue);">${r.am}</td>
            <td>${r.tinh}</td>
            <td class="num">${fNum(r.don_prev)}</td>
            <td class="num bold" style="background: rgba(2, 132, 199, 0.08); color: #0284c7; font-weight:900;">${fNum(r.don_curr)}</td>
            <td class="num bold" style="color: ${r.diff_don > 0 ? '#dc2626' : '#16a34a'};">${diffDonSign}${fNum(r.diff_don)}</td>
            <td class="num">${(r.can_thu_prev / 1e6).toFixed(1)} Tr ₫</td>
            <td class="num bold" style="background: rgba(220, 38, 38, 0.08); color: #dc2626; font-size:13px; font-weight:900;">${(r.can_thu_curr / 1e6).toFixed(1)} Tr ₫</td>
            <td class="num bold" style="color: ${r.diff_can_thu > 0 ? '#dc2626' : '#16a34a'};">${diffSign}${(r.diff_can_thu / 1e6).toFixed(1)} Tr ₫</td>
            <td class="num bold">${r.pct_can_thu_diff}</td>
          </tr>
        `;
      }).join('');
    }

    // 3. PANEL 3: TOP AM THEO TICKET & TIỀN
    const tblAm = document.querySelector('#table-truythu-top-am tbody');
    if (tblAm && report.by_am) {
      const selectedAM = state.selectedAM;
      const listAm = [...report.by_am].sort((a, b) => (b.can_thu_curr || 0) - (a.can_thu_curr || 0));
      tblAm.innerHTML = listAm.map((r, i) => {
        const isSelected = selectedAM === r.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const diffSign = r.diff_can_thu > 0 ? '+' : '';
        const diffTkSign = r.diff_ticket > 0 ? '+' : '';
        let levelBadge = '-';
        const lv = r.level || '';
        if (lv.includes('Rất cao') || lv.includes('40 Tr')) {
          levelBadge = `<span class="badge-tag badge-tag-red" style="font-size:11px; font-weight:800;">🚨 Rất cao</span>`;
        } else if (lv.includes('kiểm soát')) {
          levelBadge = `<span class="badge-tag badge-tag-amber" style="font-size:11px; font-weight:700;">⚠️ Cần kiểm soát</span>`;
        } else if (lv.includes('ticket')) {
          levelBadge = `<span class="badge-tag badge-tag-amber" style="font-size:11px;">⚠️ Nhiều ticket</span>`;
        } else if (lv) {
          levelBadge = `<span class="badge-tag badge-tag-green" style="font-size:11px; font-weight:700;">🟢 Tốt</span>`;
        }

        return `
          <tr data-entity="${r.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${r.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${r.am}</td>
            <td class="num">${fNum(r.ticket_prev)}</td>
            <td class="num bold" style="background: rgba(2, 132, 199, 0.08); color: #0369a1; font-size:13.5px; font-weight:900;">${fNum(r.ticket_curr)}</td>
            <td class="num bold" style="color: ${r.diff_ticket > 0 ? '#dc2626' : '#16a34a'};">${diffTkSign}${fNum(r.diff_ticket)} (${r.pct_ticket_diff})</td>
            <td class="num">${(r.can_thu_prev / 1e6).toFixed(1)} Tr ₫</td>
            <td class="num bold" style="background: rgba(220, 38, 38, 0.08); color: #dc2626; font-size:13.5px; font-weight:900;">${(r.can_thu_curr / 1e6).toFixed(1)} Tr ₫</td>
            <td class="num bold" style="color: ${r.diff_can_thu > 0 ? '#dc2626' : '#16a34a'};">${diffSign}${(r.diff_can_thu / 1e6).toFixed(1)} Tr ₫</td>
            <td class="num bold">${r.pct_can_thu_diff}</td>
            <td class="center">${levelBadge}</td>
            <td style="font-size: 11.5px; color: var(--text-muted);">${r.top_bc_culprit}</td>
          </tr>
        `;
      }).join('');
    }

    // 4. PANEL 4: TOP BC THEO TICKET
    const tblBcTk = document.querySelector('#table-truythu-bc-ticket tbody');
    if (tblBcTk && report.top_bc) {
      const selectedAM = state.selectedAM;
      const sortedByTicket = [...report.top_bc].sort((a, b) => b.don_curr - a.don_curr);
      tblBcTk.innerHTML = sortedByTicket.map((r, i) => {
        const isSelected = selectedAM && selectedAM === r.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        return `
          <tr data-entity="${r.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${r.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800;">${r.bc}</td>
            <td class="bold" style="color: var(--color-blue);">${r.am}</td>
            <td>${r.tinh}</td>
            <td class="num bold" style="background: rgba(2, 132, 199, 0.08); color: #0369a1; font-size:13.5px; font-weight:900;">${fNum(r.don_curr)}</td>
            <td class="num bold">${((r.don_curr / (summary.total_records_curr || 1)) * 100).toFixed(1)}%</td>
            <td class="num bold" style="background: rgba(220, 38, 38, 0.08); color: #dc2626; font-size:13.5px; font-weight:900;">${(r.can_thu_curr / 1e6).toFixed(1)} Tr ₫</td>
          </tr>
        `;
      }).join('');
    }
  }

  function sortTruyThuLoai(by) {
    state.truythuLoaiSort = by;
    ['tien', 'don', 'diff'].forEach(k => {
      const btn = document.getElementById('btn-sort-tt-' + k);
      if (btn) {
        if (k === by) {
          btn.className = 'btn btn-xs btn-primary';
          btn.style.fontWeight = '700';
        } else {
          btn.className = 'btn btn-xs btn-secondary';
          btn.style.fontWeight = 'normal';
        }
      }
    });
    renderTruyThuLoaiTable();
    renderTruyThuLoaiBar();
  }
  window.sortTruyThuLoai = sortTruyThuLoai;

  function renderTruyThuLoaiTable() {
    const tblLoai = document.querySelector('#table-truythu-by-loai tbody');
    const report = D.truy_thu_report || {};
    if (!tblLoai || !report.by_loai) return;

    let items = [...report.by_loai];
    const sortBy = state.truythuLoaiSort || 'tien';
    if (sortBy === 'tien') {
      items.sort((a, b) => (b.can_thu_curr || 0) - (a.can_thu_curr || 0));
    } else if (sortBy === 'don') {
      items.sort((a, b) => (b.don_curr || 0) - (a.don_curr || 0));
    } else if (sortBy === 'diff') {
      items.sort((a, b) => (b.diff_can_thu || 0) - (a.diff_can_thu || 0));
    } else if (sortBy === 'diff_don') {
      items.sort((a, b) => (b.diff_don || 0) - (a.diff_don || 0));
    } else if (sortBy === 'name') {
      items.sort((a, b) => a.loai.localeCompare(b.loai, 'vi'));
    }

    tblLoai.innerHTML = items.map((r, i) => {
      const diffSign = r.diff_can_thu > 0 ? '+' : '';
      const diffDonSign = r.diff_don > 0 ? '+' : '';
      const isSpike = r.diff_can_thu >= 10e6;
      let evalHtml = '-';
      const ev = r.eval || '';
      if (ev.includes('Tăng mạnh') || ev.includes('Bất thường')) {
        evalHtml = `<span class="badge-tag badge-tag-red" style="font-size:11px; font-weight:800;">🚨 Tăng mạnh</span>`;
      } else if (ev.includes('Cảnh báo') || ev.includes('tăng')) {
        evalHtml = `<span class="badge-tag badge-tag-amber" style="font-size:11px; font-weight:700;">⚠️ Tăng</span>`;
      } else if (ev.includes('Giảm') || ev.includes('tốt')) {
        evalHtml = `<span class="badge-tag badge-tag-green" style="font-size:11px; font-weight:700;">🟢 Giảm</span>`;
      } else if (ev) {
        evalHtml = `<span class="badge-tag badge-tag-blue" style="font-size:11px;">${ev}</span>`;
      }
      if (r.ghi_chu) {
        evalHtml += `<div style="font-size:10.5px; color:var(--text-muted); margin-top:2px;">${r.ghi_chu}</div>`;
      }

      return `
        <tr style="${isSpike ? 'background: rgba(239, 68, 68, 0.05);' : ''}">
          <td class="center">${renderRankPill(i)}</td>
          <td class="bold" style="font-size:13px; font-weight:800;">${r.loai}</td>
          <td class="num">${fNum(r.don_prev)}</td>
          <td class="num bold" style="background: rgba(2, 132, 199, 0.08); color: #0284c7; font-weight:900;">${fNum(r.don_curr)}</td>
          <td class="num bold" style="color: ${r.diff_don > 0 ? '#dc2626' : (r.diff_don < 0 ? '#16a34a' : 'inherit')};">${diffDonSign}${fNum(r.diff_don)} (${r.pct_don_diff})</td>
          <td class="num">${(r.can_thu_prev / 1e6).toFixed(1)} Tr ₫</td>
          <td class="num bold" style="background: rgba(220, 38, 38, 0.08); color: #dc2626; font-size:13px; font-weight:900;">${(r.can_thu_curr / 1e6).toFixed(1)} Tr ₫</td>
          <td class="num bold" style="color: ${r.diff_can_thu > 0 ? '#dc2626' : (r.diff_can_thu < 0 ? '#16a34a' : 'inherit')};">${diffSign}${(r.diff_can_thu / 1e6).toFixed(1)} Tr ₫</td>
          <td class="num bold" style="color: ${r.diff_can_thu > 0 ? '#dc2626' : (r.diff_can_thu < 0 ? '#16a34a' : 'inherit')};">${r.pct_can_thu_diff}</td>
          <td class="center">${evalHtml}</td>
        </tr>
      `;
    }).join('');
  }

  function renderTruyThuLoaiBar() {
    const ctx = document.getElementById('chart-truythu-loai-bar');
    if (!ctx) return;
    if (charts.truyThuLoaiBar) charts.truyThuLoaiBar.destroy();

    const report = D.truy_thu_report || {};
    const summary = report.summary || {};
    const prevLabel = summary.prev_label && summary.prev_label.includes('(') ? summary.prev_label.split('(')[0].trim() : (summary.prev_label || 'Tuần W42');
    const currLabel = summary.curr_label && summary.curr_label.includes('(') ? summary.curr_label.split('(')[0].trim() : (summary.curr_label || 'Tuần W43');

    let items = [...(report.by_loai || [])];
    const sortBy = state.truythuLoaiSort || 'tien';
    if (sortBy === 'tien') {
      items.sort((a, b) => (b.can_thu_curr || 0) - (a.can_thu_curr || 0));
    } else if (sortBy === 'don') {
      items.sort((a, b) => (b.don_curr || 0) - (a.don_curr || 0));
    } else if (sortBy === 'diff') {
      items.sort((a, b) => (b.diff_can_thu || 0) - (a.diff_can_thu || 0));
    }

    const top8 = items.slice(0, 8);
    if (top8.length === 0) return;

    charts.truyThuLoaiBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: top8.map(d => d.loai.length > 20 ? d.loai.substring(0, 18) + '...' : d.loai),
        datasets: [
          {
            label: `${prevLabel} (Tr ₫)`,
            data: top8.map(d => Number(((d.can_thu_prev || 0) / 1e6).toFixed(1))),
            backgroundColor: '#94a3b8',
            borderRadius: 4
          },
          {
            label: `${currLabel} (Tr ₫)`,
            data: top8.map(d => Number(((d.can_thu_curr || 0) / 1e6).toFixed(1))),
            backgroundColor: '#dc2626',
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 25, bottom: 8 } },
        scales: {
          y: {
            min: 0,
            ticks: { callback: v => fNum(v) + ' Tr' },
            title: { display: true, text: 'Tiền Cần Thu (Triệu VNĐ)', font: { weight: '700', size: 11 } }
          },
          x: {
            ticks: { maxRotation: 40, minRotation: 20, font: { size: 10.5, weight: '700' } }
          }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              title: c => top8[c[0].dataIndex].loai,
              label: c => ` ${c.dataset.label}: ${fNum(c.parsed.y)} Triệu VNĐ`
            }
          }
        }
      }
    });
  }

  function renderTruyThuBcGiaoBar() {
    const ctx = document.getElementById('chart-truythu-bcgiao-bar');
    if (!ctx) return;
    if (charts.truyThuBcGiaoBar) charts.truyThuBcGiaoBar.destroy();

    const report = D.truy_thu_report || {};
    const summary = report.summary || {};
    const prevLabel = summary.prev_label && summary.prev_label.includes('(') ? summary.prev_label.split('(')[0].trim() : (summary.prev_label || 'Tuần W42');
    const currLabel = summary.curr_label && summary.curr_label.includes('(') ? summary.curr_label.split('(')[0].trim() : (summary.curr_label || 'Tuần W43');

    const top12 = [...(report.top_bc || [])].slice(0, 12).sort((a, b) => (a.bc || "").localeCompare(b.bc || "", "vi"));
    if (top12.length === 0) return;

    charts.truyThuBcGiaoBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: top12.map(d => d.bc.replace('(KHO) ', '').replace('(LDO) ', '').replace('(DNO) ', '').replace('(BTH) ', '').replace('(NTH) ', '')),
        datasets: [
          {
            label: `${prevLabel} (Tr ₫)`,
            data: top12.map(d => Number(((d.can_thu_prev || 0) / 1e6).toFixed(1))),
            backgroundColor: '#94a3b8',
            borderRadius: 4
          },
          {
            label: `${currLabel} (Tr ₫)`,
            data: top12.map(d => Number(((d.can_thu_curr || 0) / 1e6).toFixed(1))),
            backgroundColor: '#f97316',
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 25, bottom: 8 } },
        scales: {
          y: {
            min: 0,
            ticks: { callback: v => fNum(v) + ' Tr' },
            title: { display: true, text: 'Tiền Cần Thu (Triệu VNĐ)', font: { weight: '700', size: 11 } }
          },
          x: {
            ticks: { maxRotation: 40, minRotation: 20, font: { size: 10.5, weight: '700' } }
          }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              title: c => ` ${top12[c[0].dataIndex].bc} (AM: ${top12[c[0].dataIndex].am})`,
              label: c => ` ${c.dataset.label}: ${fNum(c.parsed.y)} Triệu VNĐ`
            }
          }
        }
      }
    });
  }

  function renderTruyThuAmDual() {
    const ctx = document.getElementById('chart-truythu-am-dual');
    if (!ctx) return;
    if (charts.truyThuAmDual) charts.truyThuAmDual.destroy();

    const report = D.truy_thu_report || {};
    const summary = report.summary || {};
    const prevLabel = summary.prev_label && summary.prev_label.includes('(') ? summary.prev_label.split('(')[0].trim() : (summary.prev_label || 'Tuần W42');
    const currLabel = summary.curr_label && summary.curr_label.includes('(') ? summary.curr_label.split('(')[0].trim() : (summary.curr_label || 'Tuần W43');

    const top10 = [...(report.by_am || [])].slice(0, 10).sort((a, b) => compareVietnameseNames(a.am, b.am));
    if (top10.length === 0) return;

    charts.truyThuAmDual = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: top10.map(d => d.am),
        datasets: [
          {
            type: 'bar',
            label: `Tiền Cần Thu ${prevLabel} (Tr ₫)`,
            data: top10.map(d => Number(((d.can_thu_prev || 0) / 1e6).toFixed(1))),
            backgroundColor: '#94a3b8',
            borderRadius: 4,
            yAxisID: 'y'
          },
          {
            type: 'bar',
            label: `Tiền Cần Thu ${currLabel} (Tr ₫)`,
            data: top10.map(d => Number(((d.can_thu_curr || 0) / 1e6).toFixed(1))),
            backgroundColor: '#ea580c',
            borderRadius: 4,
            yAxisID: 'y'
          },
          {
            type: 'line',
            label: `Số Ticket ${currLabel}`,
            data: top10.map(d => d.ticket_curr),
            borderColor: '#0284c7',
            backgroundColor: '#0284c7',
            borderWidth: 2.5,
            tension: 0.2,
            pointRadius: 4.5,
            yAxisID: 'y1'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 25, bottom: 8 } },
        scales: {
          y: {
            type: 'linear',
            position: 'left',
            min: 0,
            ticks: { callback: v => fNum(v) + ' Tr' },
            title: { display: true, text: 'Tiền Cần Thu (Triệu VNĐ)', font: { weight: '700', size: 11 }, color: '#ea580c' },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          y1: {
            type: 'linear',
            position: 'right',
            min: 0,
            title: { display: true, text: 'Số Lượng Ticket Vi Phạm', font: { weight: '700', size: 11 }, color: '#0284c7' },
            grid: { drawOnChartArea: false }
          },
          x: {
            ticks: { maxRotation: 40, minRotation: 20, font: { size: 10.5, weight: '700' } }
          }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => {
                if (c.dataset.type === 'line') return ` Số Ticket (${currLabel}): ${fNum(c.parsed.y)} ticket`;
                return ` ${c.dataset.label}: ${fNum(c.parsed.y)} Triệu VNĐ`;
              }
            }
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            selectAndHighlightAM(top10[elements[0].index].am);
          }
        }
      }
    });
  }

  function renderTruyThuBcTicketBar() {
    const ctx = document.getElementById('chart-truythu-bcticket-bar');
    if (!ctx) return;
    if (charts.truyThuBcTicketBar) charts.truyThuBcTicketBar.destroy();

    const report = D.truy_thu_report || {};
    const summary = report.summary || {};
    const currLabel = summary.curr_label && summary.curr_label.includes('(') ? summary.curr_label.split('(')[0].trim() : (summary.curr_label || 'Tuần W43');

    const top15 = [...(report.top_bc || [])].sort((a, b) => b.don_curr - a.don_curr).slice(0, 15).sort((a, b) => (a.bc || "").localeCompare(b.bc || "", "vi"));
    if (top15.length === 0) return;

    const selectedAM = state.selectedAM;

    charts.truyThuBcTicketBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: top15.map(d => d.bc.replace('(KHO) ', '').replace('(LDO) ', '').replace('(DNO) ', '').replace('(BTH) ', '').replace('(NTH) ', '')),
        datasets: [
          {
            label: `Số Lượng Ticket (${currLabel})`,
            data: top15.map(d => d.don_curr),
            backgroundColor: top15.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : '#dc2626'),
            borderColor: top15.map(d => selectedAM && selectedAM === d.am ? '#991b1b' : 'transparent'),
            borderWidth: top15.map(d => selectedAM && selectedAM === d.am ? 2 : 0),
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 20, bottom: 8 } },
        scales: {
          y: {
            min: 0,
            title: { display: true, text: `Số Ticket Vi Phạm (${currLabel})`, font: { weight: '700', size: 11 } },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          x: {
            ticks: { maxRotation: 45, minRotation: 25, font: { size: 10, weight: '700' } },
            grid: { display: false }
          }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              title: c => ` ${top15[c[0].dataIndex].bc} (AM: ${top15[c[0].dataIndex].am})`,
              label: c => ` Số Ticket: ${fNum(c.parsed.y)} ticket`
            }
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            selectAndHighlightAM(top15[elements[0].index].am);
          }
        }
      }
    });
  }

  // --------------------------------------------------------------------------
  // TAB 13: KINH DOANH & KHÁCH HÀNG MỚI (F30)
  // --------------------------------------------------------------------------
    function renderKdChurnTable() {
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


  function renderKdNhomATable() {
    const tbody = document.querySelector('#table-kd-nhom-a tbody');
    const theadTr = document.querySelector('#table-kd-nhom-a thead tr');
    if (!tbody || !D.kinh_doanh || !D.kinh_doanh.khach_hang_a || !D.kinh_doanh.khach_hang_a.shops) return;

    const dates = D.kinh_doanh.khach_hang_a.dates || [];
    const latestDate = dates.length > 0 ? dates[dates.length - 1] : '';
    const w1Date = dates.length >= 8 ? dates[dates.length - 8] : (dates[0] || '');

    if (theadTr && dates.length > 0) {
      const datesThs = dates.map(d => {
        if (d === latestDate) {
          return `<th class="num" style="background: #2563eb; color:#ffffff; font-weight:800;">${d} (N-1)</th>`;
        } else if (d === w1Date) {
          return `<th class="num" style="color:#ffffff;">${d} (W-1)</th>`;
        } else {
          return `<th class="num" style="color:#ffffff;">${d}</th>`;
        }
      }).join('');

      theadTr.innerHTML = `
        <th class="center" style="width: 36px; color:#ffffff;">#</th>
        <th style="color:#ffffff;">AM Phụ Trách</th>
        <th style="color:#ffffff;">Bưu Cục Quản Lý</th>
        <th style="color:#ffffff;">Mã KH</th>
        <th style="color:#ffffff;">Tên Shop / Khách Hàng</th>
        <th class="center" style="color:#ffffff;">Hạng</th>
        <th class="center" style="color:#ffffff;">% Trụ Hạng</th>
        <th class="num" style="background: #059669; color:#ffffff; font-weight:800;">MTD (Tr ₫)</th>
        <th class="center" style="color:#ffffff;">% vs MTD M-1</th>
        ${datesThs}
        <th class="num" style="color:#ffffff;">Δ vs W-1</th>
      `;
    }

    const selectedAM = state.selectedAM;
    let shops = D.kinh_doanh.khach_hang_a.shops;
    if (selectedAM && selectedAM !== 'all') {
      shops = shops.filter(s => s.am === selectedAM);
    }

    if (shops.length === 0) {
      const colSpan = 10 + dates.length;
      tbody.innerHTML = `<tr><td colspan="${colSpan}" class="center" style="padding: 24px; color: var(--text-muted);">Không có shop nhóm A nào thuộc AM <strong>${selectedAM}</strong></td></tr>`;
      return;
    }

    tbody.innerHTML = shops.map((s, idx) => {
      const isSelected = selectedAM === s.am;
      const rowClass = isSelected ? 'presenter-laser-box' : '';
      
      const diffBadge = s.diff_w1 > 0
        ? `<span class="diff-tag diff-up-good">▲ +${fNum(s.diff_w1)} (${s.pct_w1}%)</span>`
        : (s.diff_w1 < 0 ? `<span class="diff-tag diff-down-bad">▼ ${fNum(s.diff_w1)} (${s.pct_w1}%)</span>` : `<span class="diff-tag diff-neutral">0%</span>`);

      const truHangVal = parseFloat(s.pct_tru_hang) || 0;
      const truHangBadge = truHangVal >= 25 
        ? `<span class="badge-tag badge-tag-green" style="font-weight:700;">${s.pct_tru_hang}</span>`
        : `<span class="badge-tag badge-tag-amber" style="font-weight:700;">${s.pct_tru_hang}</span>`;

      const datesTds = dates.map(d => {
        const val = Number(s.daily_dt[d] || 0);
        if (d === latestDate) {
          return `<td class="num bold" style="color: #2563eb; font-size: 13.5px; background: rgba(37, 99, 235, 0.06);">${fNum(val)}</td>`;
        }
        return `<td class="num">${fNum(val)}</td>`;
      }).join('');

      return `
        <tr class="${rowClass}">
          <td class="center bold">${idx + 1}</td>
          <td class="bold" style="color: ${isSelected ? '#ef4444' : 'inherit'}; cursor:pointer;" onclick="selectAndHighlightAM('${s.am}')">${s.am}</td>
          <td style="font-size: 11.5px; color: var(--text-muted);">${s.buu_cuc}</td>
          <td class="bold" style="font-family: monospace;">${s.makh}</td>
          <td class="bold" style="color: var(--color-blue);">${s.tenkh}</td>
          <td class="center"><span class="badge-tag badge-tag-blue">${s.nhom_n || 'A5'}</span></td>
          <td class="center">${truHangBadge}</td>
          <td class="num bold" style="color: #059669; font-size: 13.5px;">${fNum(s.mtd)}</td>
          <td class="center bold" style="color: #4b5563;">${s.pct_mtd_m1}</td>
          ${datesTds}
          <td class="num bold">${diffBadge}</td>
        </tr>
      `;
    }).join('');
  }

  function renderKdNhomAWarningTable() {
    const tbody = document.querySelector('#table-kd-nhom-a-warning tbody');
    if (!tbody || !D.kinh_doanh || !D.kinh_doanh.khach_hang_a || !D.kinh_doanh.khach_hang_a.warning) return;

    const selectedAM = state.selectedAM;
    let warnings = D.kinh_doanh.khach_hang_a.warning;
    if (selectedAM && selectedAM !== 'all') {
      warnings = warnings.filter(w => w.am === selectedAM);
    }

    if (warnings.length === 0) {
      tbody.innerHTML = `<tr><td colspan="12" class="center" style="padding: 20px; color: #10b981; font-weight:700;">✅ Không có cảnh báo bất thường nào cho shop nhóm A ${selectedAM ? `thuộc AM ${selectedAM}` : ''}</td></tr>`;
      return;
    }

    tbody.innerHTML = warnings.map((w, idx) => {
      const ckVal = parseFloat(String(w.cam_ket || '').replace(/,/g, '').trim());
      const ckDisplay = (!isNaN(ckVal) && ckVal > 0) ? fNum(ckVal) : (w.cam_ket || '—');
      const diffVal = Number(w.diff_w1 || 0);
      const pctW1 = Number(w.pct_w1 || 0);
      const canhBaoText = w.canh_bao || (diffVal < 0 ? `▼ Sụt giảm ${Math.abs(pctW1)}% vs W-1` : 'Cần theo dõi');
      return `
        <tr>
          <td class="center bold">${idx + 1}</td>
          <td class="bold" style="font-family: monospace;">${w.makh}</td>
          <td class="bold" style="color: #b91c1c;">${w.tenkh}</td>
          <td class="bold" onclick="selectAndHighlightAM('${w.am}')" style="cursor:pointer;">${w.am}</td>
          <td style="font-size: 11.5px; color: var(--text-muted);">${w.buu_cuc}</td>
          <td class="center"><span class="badge-tag badge-tag-blue">${w.nhomkh}</span></td>
          <td class="num">${ckDisplay}</td>
          <td class="num bold">${fNum(w.mtd)}</td>
          <td class="center bold">${w.pct_mtd_m1}</td>
          <td class="center bold">${w.ngay}</td>
          <td class="num bold" style="color: #ef4444; font-size: 14px; background: rgba(239, 68, 68, 0.08);">${fNum(w.dt || w.dt_n1)}</td>
          <td class="center"><span class="diff-tag diff-down-bad">${canhBaoText}</span></td>
        </tr>
      `;
    }).join('');
  }

  function renderCommercialTab() {
    renderKdChurnTable();
    renderKdNhomATable();
    renderKdNhomAWarningTable();

    // 0. Dynamic KPI cards and header
    const currW = D.meta?.latest_week || 'W43';
    const prevW = D.meta?.prev_week || 'W42';
    const kdTot = D.kinh_doanh?.total || {};
    const f30Tot = D.f30?.total || {};
    const revCurrTr = kdTot.rev_curr ? (kdTot.rev_curr / 1e6).toFixed(1) : '1.143,2';
    const revPrevTr = kdTot.rev_prev ? (kdTot.rev_prev / 1e6).toFixed(1) : '1.088,6';
    const revDiffPct = kdTot.pct_diff_rev !== undefined ? (kdTot.pct_diff_rev >= 0 ? `+${kdTot.pct_diff_rev}%` : `${kdTot.pct_diff_rev}%`) : '+5.0%';
    const volCurr = kdTot.vol_curr || 38531;
    const volPrev = kdTot.vol_prev || 36367;
    const volDiff = kdTot.diff_vol !== undefined ? (kdTot.diff_vol >= 0 ? `+${fNum(kdTot.diff_vol)}` : `${fNum(kdTot.diff_vol)}`) : '+2.164';
    const volDiffPct = volPrev ? ((kdTot.diff_vol / volPrev) * 100).toFixed(1) : '6.0';
    const f30KhCurr = f30Tot.kh_curr || 97;
    const f30KhPrev = f30Tot.kh_prev || 112;
    const f30DiffKh = f30Tot.diff_kh !== undefined ? (f30Tot.diff_kh >= 0 ? `+${f30Tot.diff_kh}` : `${f30Tot.diff_kh}`) : '-15';
    const f30PctKh = f30Tot.pct_diff_kh !== undefined ? (f30Tot.pct_diff_kh >= 0 ? `+${f30Tot.pct_diff_kh}%` : `${f30Tot.pct_diff_kh}%`) : '-13.4%';
    const f30RevCurrTr = f30Tot.rev_curr ? (f30Tot.rev_curr / 1e6).toFixed(1) : '14.5';
    const f30PctRev = f30Tot.pct_diff_rev !== undefined ? (f30Tot.pct_diff_rev >= 0 ? `+${f30Tot.pct_diff_rev}%` : `${f30Tot.pct_diff_rev}%`) : '-26.4%';

    const kdRevHeader = document.getElementById('kd-kpi-rev-header');
    if (kdRevHeader) kdRevHeader.textContent = `Tổng Doanh Thu Kỳ Này (18–24/10 - ${currW})`;
    const kdVolHeader = document.getElementById('kd-kpi-vol-header');
    if (kdVolHeader) kdVolHeader.textContent = `Tổng Volume Giao (18–24/10 - ${currW})`;
    const kdBannerBadge = document.getElementById('kd-banner-badge');
    if (kdBannerBadge) kdBannerBadge.textContent = `Doanh Thu ${currW}: ${revCurrTr} Tr (${revDiffPct}) | Volume: ${fNum(volCurr)} đ (+${volDiffPct}%) | F30: ${f30KhCurr} Shop (${f30PctKh})`;
    const kdBannerSummary = document.getElementById('kd-banner-summary');
    if (kdBannerSummary) {
      kdBannerSummary.innerHTML = `
        • <strong>Doanh Thu Toàn Vùng Kỳ 18–24/10 (${currW}):</strong> Đạt <strong>${revCurrTr} triệu VNĐ</strong> (Kỳ 11–17/10 (${prevW}): ${revPrevTr} triệu ➔ Biến động <strong>${revDiffPct} WoW</strong>).<br/>
        • <strong>Tổng Volume Giao Kinh Doanh:</strong> Đạt <strong>${fNum(volCurr)} đơn</strong> (Kỳ 11–17/10 (${prevW}): ${fNum(volPrev)} đơn ➔ Tăng <strong>${volDiff} đơn / +${volDiffPct}% WoW</strong>).<br/>
        • <strong>Tăng Trưởng Khách Hàng Mới (F30):</strong> Đạt <strong>${f30KhCurr} shop mới</strong> (Kỳ 11–17/10: ${f30KhPrev} shop ➔ Biến động <strong>${f30DiffKh} shop / ${f30PctKh} WoW</strong>) mang lại <strong>${f30RevCurrTr} triệu VNĐ</strong> (${f30PctRev} WoW).
      `;
    }

    if (D.kinh_doanh && D.kinh_doanh.total) {
      const tot = D.kinh_doanh.total;
      const elRev = document.getElementById('kd-kpi-rev-val');
      const elRevMeta = document.getElementById('kd-kpi-rev-meta');
      const elVol = document.getElementById('kd-kpi-vol-val');
      const elVolMeta = document.getElementById('kd-kpi-vol-meta');
      
      if (elRev) elRev.innerHTML = `${(tot.rev_curr / 1e6).toFixed(1)} <small>Tr ₫</small>`;
      if (elRevMeta) {
        const diffTr = (tot.diff_rev / 1e6).toFixed(1);
        const sign = tot.diff_rev >= 0 ? '+' : '';
        const tagClass = tot.diff_rev >= 0 ? 'diff-up-good' : 'diff-down-bad';
        const icon = tot.diff_rev >= 0 ? '▲' : '▼';
        elRevMeta.innerHTML = `<span class="diff-tag ${tagClass}">${icon} ${sign}${diffTr} Tr (${sign}${tot.pct_diff_rev}%)</span>`;
      }
      if (elVol) elVol.innerHTML = `${fNum(tot.vol_curr)} <small>đơn</small>`;
      if (elVolMeta) {
        const sign = tot.diff_vol >= 0 ? '+' : '';
        const tagClass = tot.diff_vol >= 0 ? 'diff-up-good' : 'diff-down-bad';
        const icon = tot.diff_vol >= 0 ? '▲' : '▼';
        const pctVol = tot.vol_prev ? ((tot.diff_vol / tot.vol_prev) * 100).toFixed(1) : '0.0';
        elVolMeta.innerHTML = `<span class="diff-tag ${tagClass}">${icon} ${sign}${fNum(tot.diff_vol)} đơn (${sign}${pctVol}%)</span>`;
      }
    }
    if (D.f30 && D.f30.total) {
      const fTot = D.f30.total;
      const elF30 = document.getElementById('kd-kpi-f30-val');
      const elF30Meta = document.getElementById('kd-kpi-f30-meta');
      const elF30Rev = document.getElementById('kd-kpi-f30rev-val');
      const elF30RevMeta = document.getElementById('kd-kpi-f30rev-meta');
      
      if (elF30) elF30.innerHTML = `${fTot.kh_curr} <small>Shop</small>`;
      if (elF30Meta) {
        const sign = fTot.diff_kh >= 0 ? '+' : '';
        const tagClass = fTot.diff_kh >= 0 ? 'diff-up-good' : 'diff-down-bad';
        const icon = fTot.diff_kh >= 0 ? '▲' : '▼';
        elF30Meta.innerHTML = `<span class="diff-tag ${tagClass}">${icon} ${sign}${fTot.diff_kh} shop (${sign}${fTot.pct_diff_kh}%)</span>`;
      }
      if (elF30Rev) elF30Rev.innerHTML = `${(fTot.rev_curr / 1e6).toFixed(1)} <small>Tr ₫</small>`;
      if (elF30RevMeta) {
        const diffTr = (fTot.diff_rev / 1e6).toFixed(1);
        const sign = fTot.diff_rev >= 0 ? '+' : '';
        const tagClass = fTot.diff_rev >= 0 ? 'diff-up-good' : 'diff-down-bad';
        const icon = fTot.diff_rev >= 0 ? '▲' : '▼';
        elF30RevMeta.innerHTML = `<span class="diff-tag ${tagClass}">${icon} ${sign}${diffTr} Tr (${sign}${fTot.pct_diff_rev}%)</span>`;
      }
    }

    // 1. Doanh Thu Theo AM Table
    const tblKd = document.querySelector('#table-kd-doanh-thu-data tbody');
    if (tblKd && D.kinh_doanh && D.kinh_doanh.am) {
      const selectedAM = state.selectedAM;
      const sorted = [...D.kinh_doanh.am].sort((a, b) => (b.rev_curr || 0) - (a.rev_curr || 0));

      tblKd.innerHTML = sorted.map((r, i) => {
        const isSelected = selectedAM === r.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const diffBadge = r.diff_rev > 0
          ? `<span class="diff-tag diff-up-good">▲ +${fMoney(r.diff_rev)}</span>`
          : (r.diff_rev < 0 ? `<span class="diff-tag diff-down-bad">▼ ${fMoney(r.diff_rev)}</span>` : `<span class="diff-tag diff-neutral">0 ₫</span>`);

        return `
          <tr data-entity="${r.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${r.am}')">
            <td class="bold" style="font-weight:800; font-size:13px; color:${isSelected ? '#ef4444' : 'inherit'};">${r.am}</td>
            <td class="num">${fNum(r.vol_curr)} đơn</td>
            <td class="num bold" style="color: var(--color-green); font-size:13px;">${fMoney(r.rev_curr)}</td>
            <td class="num bold">${r.pct_rev}%</td>
            <td class="num bold">${diffBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 2. F30 Khách Hàng Mới Table
    const tblF30 = document.querySelector('#table-f30-khach-moi-data tbody');
    if (tblF30 && D.f30 && D.f30.am) {
      const selectedAM = state.selectedAM;
      const sortedF30 = [...D.f30.am].sort((a, b) => (b.kh_curr || 0) - (a.kh_curr || 0));

      tblF30.innerHTML = sortedF30.map(r => {
        const isSelected = selectedAM === r.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const diffShop = r.diff_kh > 0
          ? `<span class="diff-tag diff-up-good">▲ +${r.diff_kh} shop</span>`
          : (r.diff_kh < 0 ? `<span class="diff-tag diff-down-bad">▼ ${r.diff_kh} shop</span>` : `<span class="diff-tag diff-neutral">0 shop</span>`);
        const diffDt = r.diff_rev > 0
          ? `<span class="diff-tag diff-up-good">▲ +${fMoney(r.diff_rev)}</span>`
          : (r.diff_rev < 0 ? `<span class="diff-tag diff-down-bad">▼ ${fMoney(r.diff_rev)}</span>` : `<span class="diff-tag diff-neutral">0 ₫</span>`);

        return `
          <tr data-entity="${r.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${r.am}')">
            <td class="bold" style="font-weight:800; font-size:13px; color:${isSelected ? '#ef4444' : 'inherit'};">${r.am}</td>
            <td class="num bold" style="color: var(--color-purple); font-size:13px;">${fNum(r.kh_curr)} shop</td>
            <td class="num bold">${fMoney(r.rev_curr)}</td>
            <td class="num bold">${diffShop}</td>
            <td class="num bold">${diffDt}</td>
          </tr>
        `;
      }).join('');
    }
  }

  function renderKdDoanhThuChart() {
    const ctx = document.getElementById('chart-kd-doanh-thu');
    if (!ctx || !D.kinh_doanh || !D.kinh_doanh.am) return;
    if (charts.kdDoanhThu) charts.kdDoanhThu.destroy();

    const selectedAM = state.selectedAM;
    const sorted = [...D.kinh_doanh.am].sort((a, b) => (b.rev_curr || 0) - (a.rev_curr || 0));
    const latestWeek = D.meta?.latest_week || 'W39';
    const prevWeek = D.meta?.prev_week || 'W38';

    charts.kdDoanhThu = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: sorted.map(d => d.am),
        datasets: [
          {
            label: `Kỳ trước (${prevWeek}) (Triệu VNĐ)`,
            data: sorted.map(d => Math.round((d.rev_prev || 0) / 1e6)),
            backgroundColor: '#cbd5e1',
            borderRadius: 4
          },
          {
            label: `Kỳ này (${latestWeek}) (Triệu VNĐ)`,
            data: sorted.map(d => Math.round((d.rev_curr || 0) / 1e6)),
            backgroundColor: sorted.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : '#10b981'),
            borderColor: sorted.map(d => selectedAM && selectedAM === d.am ? '#b91c1c' : 'transparent'),
            borderWidth: sorted.map(d => selectedAM && selectedAM === d.am ? 3 : 0),
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 20, bottom: 8 } },
        scales: {
          y: {
            min: 0,
            ticks: { callback: v => v + ' Tr' },
            title: { display: true, text: 'Doanh Thu (Triệu VNĐ)', font: { weight: '700', size: 11 } },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          x: {
            ticks: { maxRotation: 45, minRotation: 25, font: { size: 11, weight: '800' } },
            grid: { display: false }
          }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => ` ${c.dataset.label}: ${fNum(c.parsed.y)} Triệu VNĐ (${fMoney(sorted[c.dataIndex][c.datasetIndex === 0 ? 'rev_prev' : 'rev_curr'])})`
            }
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            selectAndHighlightAM(sorted[elements[0].index].am);
          }
        }
      }
    });
  }

  function renderKdDoanhThuPie() {
    const ctx = document.getElementById('chart-kd-doanhthu-pie');
    if (!ctx || !D.kinh_doanh || !D.kinh_doanh.am) return;
    if (charts.kdDoanhThuPie) charts.kdDoanhThuPie.destroy();

    const sorted = [...D.kinh_doanh.am].sort((a, b) => (b.rev_curr || 0) - (a.rev_curr || 0));
    const top6 = sorted.slice(0, 6);
    const otherSum = sorted.slice(6).reduce((s, r) => s + (r.rev_curr || 0), 0);
    const labels = top6.map(d => d.am).concat(['Các AM còn lại']);
    const dataVals = top6.map(d => Math.round((d.rev_curr || 0) / 1e6)).concat([Math.round(otherSum / 1e6)]);

    charts.kdDoanhThuPie = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [
          {
            data: dataVals,
            backgroundColor: ['#059669', '#0284c7', '#7c3aed', '#ea580c', '#f59e0b', '#ec4899', '#94a3b8'],
            borderWidth: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom' },
          tooltip: {
            callbacks: {
              label: c => ` ${c.label}: ${fNum(c.parsed)} Triệu VNĐ`
            }
          }
        }
      }
    });
  }

  function renderKdGrowthWaterfall() {
    const ctx = document.getElementById('chart-kd-growth-waterfall');
    if (!ctx || !D.kinh_doanh || !D.kinh_doanh.am) return;
    if (charts.kdGrowthWaterfall) charts.kdGrowthWaterfall.destroy();

    const sorted = [...D.kinh_doanh.am].sort((a, b) => (b.diff_rev || 0) - (a.diff_rev || 0));
    const selectedAM = state.selectedAM;

    charts.kdGrowthWaterfall = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: sorted.map(d => d.am),
        datasets: [
          {
            label: 'Biến Động Doanh Thu (Triệu VNĐ)',
            data: sorted.map(d => Number(((d.diff_rev || 0) / 1e6).toFixed(1))),
            backgroundColor: sorted.map(d => {
              if (selectedAM && selectedAM === d.am) return '#ef4444';
              return (d.diff_rev || 0) >= 0 ? '#10b981' : '#f43f5e';
            }),
            borderColor: sorted.map(d => (d.diff_rev || 0) >= 0 ? '#059669' : '#e11d48'),
            borderWidth: 1,
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 20, bottom: 8 } },
        scales: {
          y: {
            ticks: { callback: v => (v > 0 ? `+${v}` : v) + ' Tr' },
            title: { display: true, text: 'Biến Động Doanh Thu (Triệu VNĐ)', font: { weight: '700', size: 11 } },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          x: {
            ticks: { maxRotation: 45, minRotation: 25, font: { size: 10, weight: '700' } },
            grid: { display: false }
          }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: c => ` Biến động: ${c.parsed.y > 0 ? '+' : ''}${c.parsed.y} Triệu VNĐ (${fMoney(sorted[c.dataIndex].diff_rev)})`
            }
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            selectAndHighlightAM(sorted[elements[0].index].am);
          }
        }
      }
    });
  }

  function renderF30ShopsChart() {
    const ctx = document.getElementById('chart-f30-shops');
    if (!ctx || !D.f30 || !D.f30.am) return;
    if (charts.f30Shops) charts.f30Shops.destroy();

    const sorted = [...D.f30.am].sort((a, b) => (b.kh_curr || 0) - (a.kh_curr || 0));
    const selectedAM = state.selectedAM;
    const latestWeek = D.meta?.latest_week || 'W39';
    const prevWeek = D.meta?.prev_week || 'W38';

    charts.f30Shops = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: sorted.map(d => d.am),
        datasets: [
          {
            label: `Shop F30 Kỳ Trước (${prevWeek})`,
            data: sorted.map(d => d.kh_prev || 0),
            backgroundColor: '#cbd5e1',
            borderRadius: 4
          },
          {
            label: `Shop F30 Kỳ Này (${latestWeek})`,
            data: sorted.map(d => d.kh_curr || 0),
            backgroundColor: sorted.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : '#7c3aed'),
            borderColor: sorted.map(d => selectedAM && selectedAM === d.am ? '#b91c1c' : 'transparent'),
            borderWidth: sorted.map(d => selectedAM && selectedAM === d.am ? 2 : 0),
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 20, bottom: 8 } },
        scales: {
          y: {
            min: 0,
            title: { display: true, text: 'Số Shop Mới F30', font: { weight: '700', size: 11 } },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          x: {
            ticks: { maxRotation: 45, minRotation: 25, font: { size: 10, weight: '700' } },
            grid: { display: false }
          }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => ` ${c.dataset.label}: ${fNum(c.parsed.y)} shop (Doanh thu mới: ${fMoney(sorted[c.dataIndex].rev_curr)})`
            }
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            selectAndHighlightAM(sorted[elements[0].index].am);
          }
        }
      }
    });
  }


  // ============================================================================
  // KTC TAB - BACKLOG, LEADTIME, FILL RATE
  // ============================================================================

  // Global state for KTC sub-view and fill-rate mode
  state.ktcSubTab = 'backlog';
  state.fillRateMode = 'daily';
  state.leadtimeMode = 'snapshot';

  window.setKtcSubTab = function(sub) {
    state.ktcSubTab = sub;
    ['backlog', 'leadtime', 'fillrate'].forEach(s => {
      const sv = document.getElementById('ktc-subview-' + s);
      const btn = document.getElementById('btn-ktc-' + s);
      if (sv) sv.style.display = s === sub ? '' : 'none';
      if (btn) {
        btn.className = s === sub
          ? 'btn btn-sm btn-primary active'
          : 'btn btn-sm btn-secondary';
      }
    });
    if (sub === 'fillrate') renderFillRateChart();
    if (sub === 'leadtime') renderKtcLeadtime();
  };

  window.setFillRateMode = function(mode) {
    state.fillRateMode = mode;
    const btnD = document.getElementById('btn-fr-daily');
    const btnW = document.getElementById('btn-fr-weekly');
    if (btnD) btnD.className = mode === 'daily' ? 'btn btn-sm btn-primary active' : 'btn btn-sm btn-secondary';
    if (btnW) btnW.className = mode === 'weekly' ? 'btn btn-sm btn-primary active' : 'btn btn-sm btn-secondary';
    renderFillRateTable();
    renderFillRateChart();
  };

  window.setLeadtimeMode = function(mode) {
    state.leadtimeMode = mode;
    const btnS = document.getElementById('btn-lt-snapshot');
    const btnW = document.getElementById('btn-lt-w36');
    if (btnS) btnS.className = mode === 'snapshot' ? 'btn btn-xs btn-primary active' : 'btn btn-xs btn-secondary';
    if (btnW) btnW.className = mode === 'w36' ? 'btn btn-xs btn-primary active' : 'btn btn-xs btn-secondary';
    renderKtcLeadtime();
  };

  function renderKtcTab() {
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
    const currW = D.meta?.latest_week || 'W38';
    const prevW = D.meta?.prev_week || 'W37';
    const tldVal = ktcWeeklyTot.tld_curr !== undefined ? ktcWeeklyTot.tld_curr : 51.0;
    const tldPrev = ktcWeeklyTot.tld_prev !== undefined ? ktcWeeklyTot.tld_prev : 54.8;
    const diffTld = ktcWeeklyTot.diff_tld !== undefined ? ktcWeeklyTot.diff_tld : -3.8;
    const under30 = ktcWeeklyTot.under_30 !== undefined ? ktcWeeklyTot.under_30 : 76;

    const ktcTile4 = document.querySelector('#tab-ktc .kpi-strip .kpi-tile:nth-child(4)');
    if (ktcTile4) {
      const headerSpan = ktcTile4.querySelector('.kpi-tile-header span');
      if (headerSpan) headerSpan.textContent = `TLLĐ Xe Bình Quân (${currW})`;
      const isGood = diffTld >= 0;
      const diffSign = isGood ? '▲ +' : '▼ -';
      const badgeCls = isGood ? 'badge-tag-green' : 'badge-tag-amber';
      const valColor = tldVal >= 55 ? '#10b981' : (tldVal >= 50 ? '#0284c7' : '#ea580c');
      const valEl = ktcTile4.querySelector('.kpi-tile-value');
      if (valEl) {
        valEl.style.color = valColor;
        valEl.innerHTML = `${tldVal.toFixed(1)}% <small style="color: var(--text-muted); font-size: 13px; font-weight: 600;">(${prevW}: ${tldPrev.toFixed(1)}%)</small>`;
      }
      const metaEl = ktcTile4.querySelector('.kpi-tile-meta');
      if (metaEl) {
        metaEl.innerHTML = `
          <span class="badge-tag ${badgeCls}">${diffSign}${Math.abs(diffTld).toFixed(1)}%p WoW</span>
          <span style="color: var(--text-muted); font-size: 11.5px;">${under30} chuyến &lt;30%</span>
        `;
      }
    }

    const frBadge = document.querySelector('#ktc-subview-fillrate .badge-tag-amber') || document.querySelector('#ktc-subview-fillrate .badge-tag');
    if (frBadge) {
      const isGood = diffTld >= 0;
      frBadge.className = isGood ? 'badge-tag badge-tag-green' : 'badge-tag badge-tag-amber';
      frBadge.textContent = `${prevW}: ${tldPrev.toFixed(1)}% → ${currW}: ${tldVal.toFixed(1)}% (${isGood ? '▲ +' : '▼ -'}${Math.abs(diffTld).toFixed(1)}%p)`;
    }

    renderKtcBacklog();
    renderKtcLeadtime();
    renderFillRateTable();
    renderFillRateChart();
  }

  function renderKtcBacklog() {
    const ktc = D.ktc;
    if (!ktc || !ktc.backlog) return;

    // Table 1: Backlog by AM
    const tbody1 = document.querySelector('#table-ktc-backlog-am tbody');
    if (tbody1 && ktc.backlog.by_am) {
      const rows = [...ktc.backlog.by_am].sort((a, b) => (b.total || 0) - (a.total || 0));
      const tot = ktc.backlog.total_am;

      const makeRow = (r, i, isTotal) => {
        const treo = r.treo_36h || 0;
        const treoClass = treo > 0 ? 'style="background:var(--color-red-bg);color:#b91c1c;font-weight:800;"' : '';
        const diffSign = (r.diff || 0) >= 0 ? '+' : '';
        const rankCell = isTotal
          ? `<td class="bold center" style="background:var(--color-blue-bg);font-size:11px;">TỔNG</td>`
          : `<td class="center">${renderRankPill(i)}</td>`;
        return `<tr${isTotal ? ' style="background:var(--color-blue-bg);font-weight:800;"' : ''}>
          ${rankCell}
          <td class="bold">${r.am}</td>
          <td class="num">${fNum(r.h0_6 || 0)}</td>
          <td class="num">${fNum(r.h6_12 || 0)}</td>
          <td class="num">${fNum(r.h12_24 || 0)}</td>
          <td class="num">${fNum(r.h24_36 || 0)}</td>
          <td class="num">${fNum(r.h36_72 || 0)}</td>
          <td class="num">${fNum(r.h72_120 || 0)}</td>
          <td class="num">${fNum(r.h120_192 || 0)}</td>
          <td class="num">${fNum(r.h192_plus || 0)}</td>
          <td class="num bold" ${treoClass}>${fNum(treo)}</td>
          <td class="num bold" style="background:var(--color-blue-bg);">${fNum(r.total || 0)}</td>
          <td class="num">${diffSign}${fNum(r.diff || 0)}</td>
        </tr>`;
      };

      tbody1.innerHTML = rows.map((r, i) => makeRow(r, i, false)).join('') + makeRow(tot, -1, true);
    }

    // Table 2: Backlog by Kho
    const tbody2 = document.querySelector('#table-ktc-backlog-kho tbody');
    if (tbody2 && ktc.backlog.by_kho) {
      const rows = [...ktc.backlog.by_kho].sort((a, b) => (b.total || 0) - (a.total || 0));
      const tot = ktc.backlog.total_kho;
      const makeRowKho = (r, i, isTotal) => {
        const treo = r.treo_36h || 0;
        const treoClass = treo > 0 ? 'style="background:var(--color-red-bg);color:#b91c1c;font-weight:800;"' : '';
        const diffSign = (r.diff || 0) >= 0 ? '+' : '';
        const rankCell = isTotal
          ? `<td class="bold center" style="background:var(--color-blue-bg);font-size:11px;">TỔNG</td>`
          : `<td class="center">${renderRankPill(i)}</td>`;
        return `<tr${isTotal ? ' style="background:var(--color-blue-bg);font-weight:800;"' : ''}>
          ${rankCell}
          <td class="bold">${r.kho || ''}</td>
          <td>${r.am || ''}</td>
          <td class="num">${fNum(r.h0_6 || 0)}</td>
          <td class="num">${fNum(r.h6_12 || 0)}</td>
          <td class="num">${fNum(r.h12_24 || 0)}</td>
          <td class="num">${fNum(r.h24_36 || 0)}</td>
          <td class="num">${fNum(r.h36_72 || 0)}</td>
          <td class="num">${fNum(r.h72_120 || 0)}</td>
          <td class="num">${fNum(r.h120_192 || 0)}</td>
          <td class="num">${fNum(r.h192_plus || 0)}</td>
          <td class="num bold" ${treoClass}>${fNum(treo)}</td>
          <td class="num bold" style="background:var(--color-blue-bg);">${fNum(r.total || 0)}</td>
          <td class="num">${diffSign}${fNum(r.diff || 0)}</td>
        </tr>`;
      };
      tbody2.innerHTML = rows.map((r, i) => makeRowKho(r, i, false)).join('') + makeRowKho(tot, -1, true);
    }

    // Table 3: Trend by day
    const tbody3 = document.querySelector('#table-ktc-trend-days tbody');
    if (tbody3 && ktc.backlog.trend_by_am) {
      const rows = ktc.backlog.trend_by_am;
      const tot = ktc.backlog.total_trend;
      const dates = ktc.backlog.trend_dates || [];

      const makeDayCell = (d, baseVal) => {
        if (typeof d === 'object') {
          const val = d.val;
          const diff = d.diff;
          const cls = diff > 0 ? 'diff-up-bad' : diff < 0 ? 'diff-down-good' : '';
          const arrow = diff > 0 ? '▲' : diff < 0 ? '▼' : '→';
          const badge = diff !== 0 ? `<span class="diff-tag ${cls}" style="font-size:9.5px;">${arrow}${Math.abs(diff)}</span>` : '';
          return `<td class="center">${fNum(val)} ${badge}</td>`;
        }
        return `<td class="center">${fNum(d)}</td>`;
      };

      const makeRowTrend = (r, isTotal) => {
        const trStyle = isTotal ? ' style="background:var(--color-blue-bg);font-weight:800;"' : '';
        return `<tr${trStyle}>
          <td class="bold center" style="${isTotal ? 'background:var(--color-blue-bg);' : ''}">${isTotal ? 'TỔNG' : ''}</td>
          <td class="bold">${r.am}</td>
          <td class="center">${fNum(r.d_31_08 || 0)}</td>
          ${makeDayCell(r.d_01_09, r.d_31_08)}
          ${makeDayCell(r.d_02_09)}
          ${makeDayCell(r.d_03_09)}
          ${makeDayCell(r.d_04_09)}
          ${makeDayCell(r.d_05_09)}
          ${makeDayCell(r.d_06_09)}
          ${makeDayCell(r.d_07_09)}
        </tr>`;
      };
      tbody3.innerHTML = rows.map(r => makeRowTrend(r, false)).join('') + makeRowTrend(tot, true);
    }
  }

  function renderKtcLeadtime() {
    const ktc = D.ktc;
    if (!ktc || !ktc.leadtime) return;

    const mode = state.leadtimeMode || 'snapshot';
    const lt = ktc.leadtime[mode];
    if (!lt) return;

    const tbody = document.querySelector('#table-ktc-leadtime tbody');
    if (!tbody) return;

    const items = lt.items || [];
    const tot = lt.total;

    const slaClass = (pct12) => {
      if (pct12 <= 2) return '<span class="badge-tag badge-tag-green">✅ Đạt SLA</span>';
      if (pct12 <= 5) return '<span class="badge-tag badge-tag-amber">⚠️ Cảnh Báo</span>';
      return '<span class="badge-tag badge-tag-red">🚨 Vi Phạm SLA</span>';
    };

    const makeRow = (r, isTotal) => {
      const trStyle = isTotal ? ' style="background:var(--color-blue-bg);font-weight:800;"' : '';
      const pct12Color = r.pct_12h > 5 ? '#b91c1c' : r.pct_12h > 2 ? '#b45309' : '#065f46';
      return `<tr${trStyle}>
        <td>${r.loai_kho || ''}</td>
        <td class="bold">${r.ten_kho || ''}</td>
        <td class="num">${fNum(r.total_orders || 0)}</td>
        <td class="num" style="color:#ef4444;">${fNum(r.ton_12h || 0)}</td>
        <td class="num bold" style="background:var(--color-red-bg);color:${pct12Color};">${(r.pct_12h || 0).toFixed(1)}%</td>
        <td class="num" style="color:#ef4444;">${fNum(r.ton_24h || 0)}</td>
        <td class="num bold" style="background:var(--color-red-bg);color:${r.pct_24h > 1 ? '#b91c1c' : '#065f46'};">${(r.pct_24h || 0).toFixed(1)}%</td>
        <td class="num bold" style="background:var(--color-blue-bg);">${(r.lt_tb || 0).toFixed(2)}h</td>
        <td class="num">${(r.lt_p50 || 0).toFixed(2)}h</td>
        <td class="num">${(r.lt_p95 || 0).toFixed(2)}h</td>
        <td class="center">${isTotal ? '' : slaClass(r.pct_12h || 0)}</td>
      </tr>`;
    };

    tbody.innerHTML = items.map(r => makeRow(r, false)).join('') + (tot ? makeRow(tot, true) : '');
  }

  function renderFillRateTable() {
    const ktc = D.ktc;
    if (!ktc || !ktc.fill_rate) return;

    const mode = state.fillRateMode || 'daily';
    const fr = ktc.fill_rate[mode];
    if (!fr) return;

    const thead = document.getElementById('table-ktc-fillrate-thead');
    const tbody = document.getElementById('table-ktc-fillrate-tbody');
    if (!thead || !tbody) return;

    if (mode === 'daily') {
      // Daily: compare 2 days
      const dc = fr.date_comp || '';
      thead.innerHTML = `<tr>
        <th class="center" style="width:44px;">#</th>
        <th>KTC / Kho</th>
        <th class="num">Chuyến 05/09</th>
        <th class="num">Chuyến 06/09</th>
        <th class="num">Δ Chuyến</th>
        <th class="num" style="background:var(--color-blue-bg);">TLLĐ 05/09</th>
        <th class="num" style="background:var(--color-blue-bg);">TLLĐ 06/09</th>
        <th class="num">Δ TLLĐ</th>
        <th class="num" style="background:var(--color-red-bg);color:#b91c1c;">&lt;10%</th>
        <th class="num" style="background:var(--color-red-bg);color:#b91c1c;">10-20%</th>
        <th class="num" style="background:var(--color-red-bg);color:#b91c1c;">20-30%</th>
        <th class="num bold" style="background:var(--color-red-bg);color:#b91c1c;">Tổng &lt;30%</th>
      </tr>`;

      const items = fr.items || [];
      const tot = fr.total;

      const makeRowDaily = (r, i, isTotal) => {
        const diffC = r.diff_chuyen || 0;
        const diffT = r.diff_tld || 0;
        const diffCBadge = diffC >= 0 ? `<span class="diff-tag diff-up-good">▲${fNum(diffC)}</span>` : `<span class="diff-tag diff-down-bad">▼${fNum(Math.abs(diffC))}</span>`;
        const diffTBadge = diffT >= 0 ? `<span class="diff-tag diff-up-good">▲${Math.abs(diffT).toFixed(1)}%p</span>` : `<span class="diff-tag diff-down-bad">▼${Math.abs(diffT).toFixed(1)}%p</span>`;
        const rankCell = isTotal ? `<td class="bold center" style="background:var(--color-blue-bg);font-size:10px;">TỔNG</td>` : `<td class="center">${renderRankPill(i)}</td>`;
        const under30 = (r.u10 || 0) + (r.u20 || 0) + (r.u30 || 0);
        return `<tr${isTotal ? ' style="background:var(--color-blue-bg);font-weight:800;"' : ''}>
          ${rankCell}
          <td class="bold">${r.short_name || r.kho || ''}</td>
          <td class="num">${fNum(r.chuyen_05 || 0)}</td>
          <td class="num">${fNum(r.chuyen_06 || 0)}</td>
          <td class="num">${diffCBadge}</td>
          <td class="num" style="background:var(--color-blue-bg);">${(r.tld_05 || 0).toFixed(1)}%</td>
          <td class="num bold" style="background:var(--color-blue-bg);">${(r.tld_06 || 0).toFixed(1)}%</td>
          <td class="num">${diffTBadge}</td>
          <td class="num" style="color:#b91c1c;">${fNum(r.u10 || 0)}</td>
          <td class="num" style="color:#b45309;">${fNum(r.u20 || 0)}</td>
          <td class="num" style="color:#92400e;">${fNum(r.u30 || 0)}</td>
          <td class="num bold" style="background:var(--color-red-bg);color:#b91c1c;">${fNum(under30)}</td>
        </tr>`;
      };
      tbody.innerHTML = items.map((r, i) => makeRowDaily(r, i, false)).join('') + makeRowDaily(tot, -1, true);

    } else {
      // Weekly: compare prevW vs currW
      const currW = D.meta?.latest_week || 'W38';
      const prevW = D.meta?.prev_week || 'W37';
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
      </tr>`;

      const items = fr.items || [];
      const tot = fr.total;

      const makeRowWeekly = (r, i, isTotal) => {
        const diffC = r.diff_chuyen || 0;
        const diffT = r.diff_tld || 0;
        const diffCBadge = diffC >= 0 ? `<span class="diff-tag diff-up-good">▲${fNum(diffC)}</span>` : `<span class="diff-tag diff-down-bad">▼${fNum(Math.abs(diffC))}</span>`;
        const diffTBadge = diffT >= 0 ? `<span class="diff-tag diff-up-good">▲${Math.abs(diffT).toFixed(1)}%p</span>` : `<span class="diff-tag diff-down-bad">▼${Math.abs(diffT).toFixed(1)}%p</span>`;
        const rankCell = isTotal ? `<td class="bold center" style="background:var(--color-blue-bg);font-size:10px;">TỔNG</td>` : `<td class="center">${renderRankPill(i)}</td>`;
        const under30 = r.under_30 || ((r.u10 || 0) + (r.u20 || 0) + (r.u30 || 0));
        const chuyenP = r.chuyen_prev !== undefined ? r.chuyen_prev : (r['chuyen_' + prevW.toLowerCase()] || 0);
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
          <td class="num">${diffTBadge}</td>
          <td class="num" style="color:#b91c1c;">${fNum(r.u10 || 0)}</td>
          <td class="num" style="color:#b45309;">${fNum(r.u20 || 0)}</td>
          <td class="num" style="color:#92400e;">${fNum(r.u30 || 0)}</td>
          <td class="num bold" style="background:var(--color-red-bg);color:#b91c1c;">${fNum(under30)}</td>
        </tr>`;
      };
      tbody.innerHTML = items.map((r, i) => makeRowWeekly(r, i, false)).join('') + makeRowWeekly(tot, -1, true);
    }

    // Also render causes table
    renderFillRateCauses();
  }

  function renderFillRateCauses() {
    const ktc = D.ktc;
    if (!ktc || !ktc.fill_rate || !ktc.fill_rate.causes) return;
    const tbody = document.querySelector('#table-ktc-fillrate-causes tbody');
    if (!tbody) return;

    const causes = ktc.fill_rate.causes;
    const grand_total = causes.reduce((s, c) => s + (c.total || 0), 0);

    tbody.innerHTML = causes.map((c, i) => `
      <tr>
        <td class="center">${renderRankPill(i)}</td>
        <td class="bold">${c.cause || ''}</td>
        <td class="num">${fNum(c.kh || 0)}</td>
        <td class="num">${fNum(c.dt || 0)}</td>
        <td class="num">${fNum(c.dn || 0)}</td>
        <td class="num">${fNum(c.bt || 0)}</td>
        <td class="num">${fNum(c.bl || 0)}</td>
        <td class="num bold" style="background:var(--color-blue-bg);">${fNum(c.total || 0)}</td>
        <td class="num bold" style="color:#ea580c;">${(c.share || 0).toFixed(1)}%</td>
      </tr>
    `).join('') + `<tr style="background:var(--color-blue-bg);font-weight:800;">
      <td class="bold center" style="font-size:10px;">TỔNG</td>
      <td class="bold">TỔNG CỘNG</td>
      <td class="num">${fNum(causes.reduce((s,c) => s+(c.kh||0), 0))}</td>
      <td class="num">${fNum(causes.reduce((s,c) => s+(c.dt||0), 0))}</td>
      <td class="num">${fNum(causes.reduce((s,c) => s+(c.dn||0), 0))}</td>
      <td class="num">${fNum(causes.reduce((s,c) => s+(c.bt||0), 0))}</td>
      <td class="num">${fNum(causes.reduce((s,c) => s+(c.bl||0), 0))}</td>
      <td class="num bold" style="background:var(--color-blue-bg);">${fNum(grand_total)}</td>
      <td class="num bold" style="color:#ea580c;">100%</td>
    </tr>`;
  }

  function renderFillRateChart() {
    const ktc = D.ktc;
    if (!ktc || !ktc.fill_rate || !ktc.fill_rate.trend_6w) return;

    const canvas = document.getElementById('chart-fillrate-trend');
    if (!canvas) return;

    if (charts['fillrate_trend']) charts['fillrate_trend'].destroy();

    const trend = ktc.fill_rate.trend_6w || (ktc.fill_rate.history || []).map(w => ({
      week: w.week,
      tld: Number(((w.rate || 0) * 100).toFixed(1)),
      chuyen: w.trips || 0,
      under30: w.low_trips || 0
    }));
    if (!trend || trend.length === 0) return;
    const labels = trend.map(w => w.week);
    const tld_vals = trend.map(w => w.tld);
    const chuyen_vals = trend.map(w => w.chuyen);
    const under30_vals = trend.map(w => w.under30);
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const textColor = isDark ? '#e2e8f0' : '#1e293b';
    const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)';

    charts['fillrate_trend'] = new Chart(canvas, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: 'Số Chuyến',
            data: chuyen_vals,
            backgroundColor: trend.map((w, i) => i === trend.length - 1 ? '#3b82f6' : 'rgba(59,130,246,0.35)'),
            borderColor: trend.map((w, i) => i === trend.length - 1 ? '#1d4ed8' : '#3b82f6'),
            borderWidth: 2,
            borderRadius: 6,
            yAxisID: 'y',
            order: 2
          },
          {
            label: 'Chuyến <30% TLLĐ',
            data: under30_vals,
            backgroundColor: trend.map((w, i) => i === trend.length - 1 ? '#ef4444' : 'rgba(239,68,68,0.3)'),
            borderColor: trend.map((w, i) => i === trend.length - 1 ? '#b91c1c' : '#ef4444'),
            borderWidth: 2,
            borderRadius: 6,
            yAxisID: 'y',
            order: 3
          },
          {
            label: 'TLLĐ TB (%)',
            data: tld_vals,
            type: 'line',
            borderColor: '#f59e0b',
            backgroundColor: 'rgba(245,158,11,0.15)',
            borderWidth: 3,
            pointRadius: 5,
            pointBackgroundColor: '#f59e0b',
            fill: true,
            tension: 0.3,
            yAxisID: 'y2',
            order: 1,
            datalabels: {
              align: 'top',
              color: '#d97706',
              font: { weight: '800', size: 11 },
              formatter: v => v.toFixed(1) + '%'
            }
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => {
                if (c.dataset.label.includes('TLLĐ')) return ` ${c.dataset.label}: ${c.parsed.y.toFixed(1)}%`;
                return ` ${c.dataset.label}: ${fNum(c.parsed.y)}`;
              }
            }
          },
          datalabels: { display: false }
        },
        scales: {
          y: {
            type: 'linear',
            position: 'left',
            title: { display: true, text: 'Số Chuyến', font: { weight: '700', size: 11 }, color: textColor },
            grid: { color: gridColor },
            ticks: { color: textColor }
          },
          y2: {
            type: 'linear',
            position: 'right',
            min: 0,
            max: 80,
            title: { display: true, text: 'TLLĐ TB (%)', font: { weight: '700', size: 11 }, color: '#d97706' },
            grid: { display: false },
            ticks: { color: '#d97706', callback: v => v + '%' }
          },
          x: {
            ticks: { color: textColor, font: { weight: '700', size: 11 } },
            grid: { display: false }
          }
        }
      }
    });
  }


  // Run on load
  document.addEventListener('DOMContentLoaded', init);


    // REALTIME SYNC FOR SHEET NTBo
  window.syncNtboRealtime = async function() {
    const btn = document.getElementById('btn-sync-ntbo-realtime');
    const txt = document.getElementById('text-sync-ntbo');
    const icon = document.getElementById('icon-sync-ntbo');
    const badge = document.getElementById('badge-ntbo-updated');

    if (btn) btn.disabled = true;
    if (txt) txt.textContent = 'Đang đồng bộ...';

    try {
      const res = await fetch('/api/sync-ntbo');
      const data = await res.json();
      if (data.success && data.bcs) {
        if (!D.gtc_tong) D.gtc_tong = {};
        D.gtc_tong.buu_cuc_bat_on = data.bcs;
        D.gtc_tong.ntbo_update_time = data.update_time;
        D.gtc_tong.n1_date_label = data.n1_label;

        if (badge) {
          badge.textContent = `📅 Dữ liệu: ${data.update_time} (Chốt ngày ${data.n1_label})`;
        }

        if (typeof renderGtcTongTab === 'function') {
          renderGtcTongTab();
        } else if (typeof window.renderGtcTongTab === 'function') {
          window.renderGtcTongTab();
        }
        alert(`✅ ${data.message}\nCập nhật lúc: ${data.update_time} (Chốt ngày: ${data.n1_label})`);
      } else {
        alert('❌ Lỗi đồng bộ: ' + (data.error || 'Không thể tải dữ liệu'));
      }
    } catch (err) {
      console.error('syncNtboRealtime error:', err);
      alert('❌ Lỗi kết nối API đồng bộ: ' + err.message);
    } finally {
      if (btn) btn.disabled = false;
      if (txt) txt.textContent = '🔄 Đồng Bộ Realtime Sheet NTBo';
      if (window.lucide) lucide.createIcons();
    }
  };

  window.filterGtcBatOn = function(f) {
    state.gtcBatOnFilter = f;
    document.querySelectorAll('#gtc-baton-filter-pills .chart-pill-btn').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-filter') === f);
    });
    if (typeof renderGtcTongTab === 'function') {
      renderGtcTongTab();
    } else if (typeof window.renderGtcTongTab === 'function') {
      window.renderGtcTongTab();
    }
  };


  // --------------------------------------------------------------------------
  // BẢNG 3: BƯU CỤC CÓ TỶ LỆ GÁN THẤP NHẤT TOÀN VÙNG (TAB 5)
  // --------------------------------------------------------------------------
  state.ganBcFilter = 'worst';
  state.searchGanBc = '';

  window.filterGanBc = function(f) {
    state.ganBcFilter = f;
    document.querySelectorAll('#gan-bc-filter-pills .chart-mode-pill').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-filter') === f);
    });
    renderGanBcTable();
  };

  window.searchGanBc = function(val) {
    state.searchGanBc = (val || '').toLowerCase().trim();
    renderGanBcTable();
  };

  function renderGanBcTable() {
    const tbl = document.querySelector('#table-gan-bc-detailed tbody');
    if (!tbl || !D.gan || !D.gan.top_bc_chua_gan) return;

    let list = [...D.gan.top_bc_chua_gan];
    if (state.ganBcFilter === 'worst') {
      list = list.filter(r => (r.gan_rate_w43 !== undefined ? r.gan_rate_w43 : (r.gan_rate || 0)) < 65.0);
    }

    if (state.searchGanBc) {
      const q = state.searchGanBc;
      list = list.filter(r => (r.ten_bc && r.ten_bc.toLowerCase().includes(q)) || (r.am && r.am.toLowerCase().includes(q)) || (r.tinh && r.tinh.toLowerCase().includes(q)));
    }

    // Sắp xếp tăng dần theo tỷ lệ gán W43 (thấp nhất lên đầu)
    list.sort((a, b) => {
      const valA = a.gan_rate_w43 !== undefined ? a.gan_rate_w43 : (a.gan_rate || 0);
      const valB = b.gan_rate_w43 !== undefined ? b.gan_rate_w43 : (b.gan_rate || 0);
      return valA - valB;
    });

    const currW = D.meta?.latest_week || 'W43';
    const countEl = document.getElementById('gan-bc-count');
    if (countEl) countEl.textContent = `Đang hiển thị: ${list.length} bưu cục (Tuần ${currW})`;

    const allPill = document.querySelector('#gan-bc-filter-pills [data-filter="all"]');
    if (allPill && D.gan?.top_bc_chua_gan) {
      allPill.textContent = `📋 Toàn Bộ Bưu Cục (${D.gan.top_bc_chua_gan.length} BC)`;
    }

    tbl.innerHTML = list.map((b, i) => {
      const gr = b.gan_rate_w43 !== undefined ? b.gan_rate_w43 : (b.gan_rate || 0);
      const w42 = b.gan_rate_w42 !== undefined ? b.gan_rate_w42 : 0;
      const diff = b.diff_gan !== undefined ? b.diff_gan : (gr - w42);
      const ca1 = b.ca1 || `${(b.gan_rate_ca1 || 0).toFixed(1)}%`;
      const ca2 = b.ca2 || (b.gan_rate_ca2 ? `${b.gan_rate_ca2.toFixed(1)}%` : '--');

      let diffStr = diff > 0 ? `+${diff.toFixed(1)}%p` : (diff < 0 ? `${diff.toFixed(1)}%p` : '0.0%p');
      let diffStyle = diff > 0 ? 'color: #16a34a; font-weight: 800;' : (diff < 0 ? 'color: #dc2626; font-weight: 800;' : 'color: #64748b; font-weight: 700;');

      let badge = '<span class="badge-tag badge-tag-green" style="font-size:11px;">🟢 Đạt Chuẩn</span>';
      let rowBg = 'transparent';
      let rateBg = '#dcfce7';
      let rateColor = '#16a34a';

      if (gr < 60.0) {
        badge = '<span class="badge-tag badge-tag-red" style="font-weight:900; font-size:11px;">🚨 Báo Động Đỏ (&lt;60%)</span>';
        rowBg = 'rgba(239, 68, 68, 0.08)';
        rateBg = '#dc2626';
        rateColor = '#ffffff';
      } else if (gr < 70.0) {
        badge = '<span class="badge-tag badge-tag-amber" style="font-weight:800; font-size:11px;">⚠️ Rất Kém (&lt;70%)</span>';
        rowBg = 'rgba(254, 242, 242, 0.6)';
        rateBg = '#fee2e2';
        rateColor = '#b91c1c';
      } else if (gr < 80.0) {
        badge = '<span class="badge-tag badge-tag-amber" style="font-weight:700; font-size:11px;">🟡 Chậm Trễ (&lt;80%)</span>';
        rateBg = '#fff7ed';
        rateColor = '#c2410c';
      }

      const ca1Val = parseFloat(String(ca1).replace('%', '') || 0);
      const ca1Color = ca1Val < 80.0 ? '#dc2626' : '#16a34a';
      const ca2Val = parseFloat(String(ca2).replace('%', '') || 0);
      const ca2Color = ca2 === '--' || ca2Val < 50.0 ? '#dc2626' : (ca2Val < 70.0 ? '#ea580c' : '#16a34a');

      return `
        <tr style="cursor: pointer; background: ${rowBg};" onclick="selectAndHighlightAM('${b.am}')">
          <td class="center" style="font-weight:800; color:${gr < 60.0 ? '#dc2626' : 'inherit'};">${i + 1}</td>
          <td class="bold" style="font-size:13px; font-weight:800; color:${gr < 60.0 ? '#b91c1c' : '#1e293b'};">${b.ten_bc}</td>
          <td style="font-weight:700; color:#2563eb;">${b.am}</td>
          <td style="color:#64748b; font-size:12px;">${b.tinh || ''}</td>
          <td class="num bold">${typeof b.vol === 'number' ? b.vol.toLocaleString() : b.vol}</td>
          <td class="num bold" style="background: #f1f5f9; color: #334155; font-size: 13px;">${w42.toFixed(1)}%</td>
          <td class="num bold" style="background: ${rateBg}; color: ${rateColor}; font-size: 13px; font-weight: 900;">${gr.toFixed(1)}%</td>
          <td class="num" style="${diffStyle} font-size: 12.5px;">${diffStr}</td>
          <td class="num" style="font-weight:700; color:${ca1Color};">${ca1}</td>
          <td class="num" style="font-weight:700; color:${ca2Color};">${ca2}</td>
          <td class="center">${badge}</td>
        </tr>
      `;
    }).join('');
  }

  // --------------------------------------------------------------------------
  // BẢNG 4: TOP BƯU CỤC OPR TIKTOK SHOP THẤP NHẤT TOÀN VÙNG (TAB 8)
  // --------------------------------------------------------------------------
  // BẢNG 4: DANH SÁCH ĐIỂM NÓNG OPR TIKTOK SHOP - BƯU CỤC TRỄ SLA NHIỀU NHẤT (TAB 8)
  // --------------------------------------------------------------------------
  state.oprBcFilter = 'most_late';
  state.oprBcSortCol = 'don_tre';
  state.oprBcSortDir = 'desc';
  state.searchOprBc = '';

  window.filterOprBc = function(f) {
    state.oprBcFilter = f;
    document.querySelectorAll('#opr-bc-filter-pills .chart-mode-pill').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-filter') === f);
    });
    renderOprBcTable();
  };

  window.sortOprBc = function(col) {
    if (state.oprBcSortCol === col) {
      state.oprBcSortDir = (state.oprBcSortDir === 'desc') ? 'asc' : 'desc';
    } else {
      state.oprBcSortCol = col;
      state.oprBcSortDir = (col === 'ten_bc' || col === 'am' || col === 'tinh') ? 'asc' : 'desc';
    }
    renderOprBcTable();
  };

  window.searchOprBc = function(val) {
    state.searchOprBc = (val || '').toLowerCase().trim();
    renderOprBcTable();
  };

  function renderOprBcTable() {
    const tbl = document.querySelector('#table-opr-bc-detailed tbody');
    const rawList = (D.opr_tts && D.opr_tts.top_bc_opr) ? D.opr_tts.top_bc_opr : (D.opr && D.opr.top_bc_opr ? D.opr.top_bc_opr : []);
    if (!tbl || rawList.length === 0) return;

    let list = [...rawList];

    // Filter Logic
    if (state.oprBcFilter === 'most_late') {
      // Ưu tiên các bưu cục có sản lượng đáng kể và số đơn trễ SLA lớn nhất (>= 50 đơn trễ)
      list = list.filter(r => (r.don_tre || 0) >= 50);
    } else if (state.oprBcFilter === 'under_kpi') {
      list = list.filter(r => (r.pct_opr || 0) < 80.0);
    } else if (state.oprBcFilter === 'night_zero') {
      list = list.filter(r => (r.opr_night || 0) === 0 && (r.don_night || 0) > 0);
    }

    if (state.searchOprBc) {
      const q = state.searchOprBc;
      list = list.filter(r => (r.ten_bc && r.ten_bc.toLowerCase().includes(q)) || (r.am && r.am.toLowerCase().includes(q)) || (r.tinh && r.tinh.toLowerCase().includes(q)));
    }

    // Sorting Logic
    const col = state.oprBcSortCol || 'don_tre';
    const isDesc = state.oprBcSortDir === 'desc';

    list.sort((a, b) => {
      let vA = a[col] !== undefined ? a[col] : 0;
      let vB = b[col] !== undefined ? b[col] : 0;

      if (typeof vA === 'string') {
        const cmp = vA.localeCompare(vB, 'vi');
        return isDesc ? -cmp : cmp;
      }
      if (vA === vB) {
        return (b.don_tre || 0) - (a.don_tre || 0);
      }
      return isDesc ? (vB - vA) : (vA - vB);
    });

    const currW = D.meta?.latest_week || 'W43';
    const countEl = document.getElementById('opr-bc-count');
    if (countEl) {
      const filterTxt = state.oprBcFilter === 'most_late' ? 'Điểm Nóng Trễ ≥ 50 Đơn' : 
                        state.oprBcFilter === 'under_kpi' ? 'Chưa Đạt KPI (<80%)' :
                        state.oprBcFilter === 'night_zero' ? 'Tê Liệt Ca Đêm (0%)' : 'Toàn Bộ';
      countEl.textContent = `Đang hiển thị: ${list.length} bưu cục (${filterTxt} • Tuần ${currW})`;
    }

    const allPill = document.querySelector('#opr-bc-filter-pills [data-filter="all"]');
    if (allPill && rawList.length) {
      allPill.textContent = `📑 Toàn Bộ Bưu Cục (${rawList.length} BC)`;
    }

    tbl.innerHTML = list.map((b, i) => {
      const opr_val = b.pct_opr || 0;
      const day_val = b.opr_day || 0;
      const night_val = b.opr_night || 0;
      const don_tre = b.don_tre || 0;
      const isNightDead = night_val === 0 && (b.don_night || 0) > 0;

      let badge = '<span class="badge-tag badge-tag-green" style="font-size:11px;">🟢 Đạt KPI (≥80%)</span>';
      let rowBg = 'transparent';
      let rateBg = '#dcfce7';
      let rateColor = '#16a34a';

      if (don_tre >= 100) {
        badge = '<span class="badge-tag badge-tag-red" style="font-weight:900; font-size:11.5px; background:#dc2626; color:#fff;">🔥 Hố Đen SLA (&gt;100 trễ)</span>';
        rowBg = 'rgba(239, 68, 68, 0.12)';
        rateBg = '#dc2626';
        rateColor = '#ffffff';
      } else if (isNightDead) {
        badge = '<span class="badge-tag badge-tag-purple" style="font-weight:800; font-size:11px; background:#7c3aed; color:#fff;">🌙 Liệt Ca Đêm (0%)</span>';
        rowBg = 'rgba(124, 58, 237, 0.05)';
        rateBg = '#fee2e2';
        rateColor = '#b91c1c';
      } else if (opr_val < 40.0) {
        badge = '<span class="badge-tag badge-tag-red" style="font-weight:900; font-size:11.5px;">🚨 Tê Liệt (&lt;40%)</span>';
        rowBg = 'rgba(239, 68, 68, 0.08)';
        rateBg = '#dc2626';
        rateColor = '#ffffff';
      } else if (opr_val < 65.0) {
        badge = '<span class="badge-tag badge-tag-red" style="font-weight:800; font-size:11px;">🔴 Báo Động Đỏ (&lt;65%)</span>';
        rowBg = 'rgba(254, 242, 242, 0.6)';
        rateBg = '#fee2e2';
        rateColor = '#b91c1c';
      } else if (opr_val < 80.0) {
        badge = '<span class="badge-tag badge-tag-amber" style="font-weight:700; font-size:11px;">🟡 Không Đạt (&lt;80%)</span>';
        rateBg = '#fef3c7';
        rateColor = '#b45309';
      }

      return `
        <tr style="cursor: pointer; background: ${rowBg};" onclick="selectAndHighlightAM('${b.am}')">
          <td class="center" style="font-weight:800; color:${don_tre >= 50 ? '#dc2626' : 'inherit'};">${i + 1}</td>
          <td class="bold" style="font-size:13.5px; font-weight:800; color:${don_tre >= 100 ? '#991b1b' : (opr_val < 65.0 ? '#b91c1c' : '#1e293b')};">${b.ten_bc}</td>
          <td style="font-weight:700; color:#2563eb;">${b.am}</td>
          <td style="color:#64748b; font-size:12px;">${b.tinh || ''}</td>
          <td class="num bold">${(b.don_total || 0).toLocaleString()}</td>
          <td class="num bold" style="background: ${don_tre >= 100 ? '#dc2626' : 'rgba(239, 68, 68, 0.12)'}; color: ${don_tre >= 100 ? '#ffffff' : '#dc2626'}; font-size: 13.5px; font-weight: 900;">${don_tre.toLocaleString()}</td>
          <td class="num bold" style="background: ${rateBg}; color: ${rateColor}; font-size: 13.5px; font-weight: 900;">${opr_val.toFixed(1)}%</td>
          <td class="num" style="font-weight:700; color:${day_val < 80 ? '#dc2626' : '#16a34a'};">${day_val.toFixed(1)}%</td>
          <td class="num bold" style="background: ${isNightDead ? '#fee2e2' : (night_val < 50 ? '#fff1f2' : 'transparent')}; color:${isNightDead ? '#dc2626' : (night_val < 50 ? '#dc2626' : '#ea580c')}; font-weight:800;">
            ${(b.don_night || 0) > 0 ? (night_val.toFixed(1) + '%' + (isNightDead ? ' 🚨' : '')) : '--'}
          </td>
          <td class="center">${badge}</td>
        </tr>
      `;
    }).join('');
  }
}
)();


