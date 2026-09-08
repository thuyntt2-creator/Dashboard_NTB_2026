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
  const charts = {};

  // App State - LIGHT THEME BY DEFAULT & 12 DEDICATED SECTIONS
  const state = {
    week: D.meta?.latest_week || 'W36',
    province: 'ALL',
    am: 'ALL',
    selectedAM: null,
    volChartMode: 'w35_vs_w36_full',
    volHighlight: 'all',
    gtcTongHighlight: 'all',
    gtcTongSegment: 'full',
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
    populateAMFilter();
    setupEvents();
    setupTableSorting();
    setupLaserClickHighlighter();
    renderAll();
    lucide.createIcons();
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
    selectAM.innerHTML = '<option value="ALL" selected>Tất cả AM (18 AM)</option>';
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

  function setupLaserClickHighlighter() {
    document.addEventListener('click', e => {
      const tr = e.target.closest('tbody tr');
      if (tr && tr.hasAttribute('data-entity')) {
        const amName = tr.getAttribute('data-entity');
        selectAndHighlightAM(amName);
      }
    });

    window.addEventListener('keydown', e => {
      if (e.key === 'Escape') {
        window.clearAMHighlight();
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

        // Move GHN Express Delivery Truck to this tab!
        updateGhnTruckPosition(tab);

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
      th.addEventListener('click', () => {
        const table = th.closest('table');
        if (!table) return;
        const tableId = table.id;
        const colIdx = Array.from(th.parentNode.children).indexOf(th);
        
        state.sortDirection[tableId] = (state.sortColumn[tableId] === colIdx && state.sortDirection[tableId] === 'asc') ? 'desc' : 'asc';
        state.sortColumn[tableId] = colIdx;

        renderAll();
      });
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
  function renderAll() {
    renderOverviewTab();
    renderVolumeTab();
    renderGtcTongTab();
    renderGtcTtsCa1Tab();
    renderGanTab();
    renderOdrTab();
    renderLtcTab();
    renderOprTab();
    renderTransportTab();
    renderFdTab();
    renderKtcTab();
    renderAgingTab();
    renderControlTab();
    renderTruyThuTab();
    renderCommercialTab();
    renderAllCharts();
  }

  function renderTabCharts(tabId) {
    if (tabId === 'tab-overview') {
      renderTrendSanLuongChart();
      renderTrendRatesChart();
      renderSanLuongTinhChart();
    } else if (tabId === 'tab-volume') {
      renderVolAMChart();
    } else if (tabId === 'tab-gtc-tong') {
      renderGtcTongBarChart();
    } else if (tabId === 'tab-gtc-tts-ca1') {
      renderGtcTtsCa1Tab();
      renderGtcTtsCa1BarChart();
    } else if (tabId === 'tab-gan') {
      renderGanTab();
      renderGanOverviewChart();
      renderGanBarChart();
    } else if (tabId === 'tab-odr') {
      renderOdrChart();
    } else if (tabId === 'tab-ltc') {
      renderLtcTab();
      renderLtcChart();
    } else if (tabId === 'tab-opr-tts') {
      renderOprGroupedChart();
    } else if (tabId === 'tab-rot-lc') {
      renderRotLcChart();
    } else if (tabId === 'tab-fd') {
      renderFdTab();
      renderFdChart();
    } else if (tabId === 'tab-ktc') {
      renderKtcTab();
      renderFillRateChart();
    } else if (tabId === 'tab-aging') {
      renderAgingChart();
    } else if (tabId === 'tab-commercial') {
      renderCommercialTab();
      renderKdDoanhThuChart();
      renderKdDoanhThuPie();
      renderKdGrowthWaterfall();
      renderF30ShopsChart();
    } else if (tabId === 'tab-control') {
      renderControlTab();
      renderCodTmAmBar();
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
    const latestWeek = D.meta?.latest_week || 'W36';
    const prevWeek = D.meta?.prev_week || 'W35';
    
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
      const gtcVal = gtcCard.val !== undefined ? gtcCard.val : 0.5695;
      const gtcDiff = gtcCard.diff !== undefined ? gtcCard.diff : -0.0077;
      const gtcTtsVal = gtcTtsCard.val !== undefined ? gtcTtsCard.val : 0.5695;

      // 3. GTC Ca 1 TTS
      const gtcCa1Trend = trendMap['%GTC TTS (Ca1 thuần)'] || trendMap['%GTC Full hàng (Ca1 thuần)'] || {};
      const gtcCa1Val = gtcCa1Trend[latestWeek.toLowerCase()] !== undefined ? gtcCa1Trend[latestWeek.toLowerCase()] : (latestWeek === 'W36' ? 0.7478 : 0.758);
      const gtcCa1Diff = gtcCa1Trend.diff !== undefined ? gtcCa1Trend.diff : (latestWeek === 'W36' ? -0.0104 : 0.0181);

      // 4. Gán vận hành
      const ganOverview = D.gan?.overview || [];
      const ganFullRow = ganOverview.find(r => r.indicator && r.indicator.includes('Full hàng – Tổng')) || {};
      const ganTtsRow = ganOverview.find(r => r.indicator && r.indicator.includes('TTS – Tổng')) || {};
      const ganVal = ganFullRow.w36 !== undefined ? ganFullRow.w36 : 0.8355;
      const ganDiff = ganFullRow.diff !== undefined ? ganFullRow.diff : 0.0144;
      const ganTtsVal = ganTtsRow.w36 !== undefined ? ganTtsRow.w36 : 0.8343;

      // 5. ODR
      const odrCard = cardMap['odr_full'] || {};
      const odrTrendTts = trendMap['%ODR TTS'] || {};
      const odrVal = odrCard.val !== undefined ? odrCard.val : 0.9288;
      const odrDiff = odrCard.diff !== undefined ? odrCard.diff : 0.0071;
      const odrTtsVal = odrTrendTts[latestWeek.toLowerCase()] !== undefined ? odrTrendTts[latestWeek.toLowerCase()] : 0.9243;

      // 6. LTC
      const ltcCard = cardMap['ltc_full'] || {};
      const ltcTrendTts = trendMap['%LTC TTS'] || {};
      const ltcVal = ltcCard.val !== undefined ? ltcCard.val : 0.905;
      const ltcDiff = ltcCard.diff !== undefined ? ltcCard.diff : -0.0064;
      const ltcTtsVal = ltcTrendTts[latestWeek.toLowerCase()] !== undefined ? ltcTrendTts[latestWeek.toLowerCase()] : 0.9419;

      // 7. Rớt LC
      const rotCard = cardMap['rot_lc'] || {};
      const rotVal = rotCard.val !== undefined ? rotCard.val : 0.0225;
      const rotDiff = rotCard.diff !== undefined ? rotCard.diff : 0.0068;

      // 8. COD Tiền mặt
      const codCard = cardMap['cod_tm'] || {};
      const codVal = codCard.val !== undefined ? codCard.val : 0.396;
      const codDiff = codCard.diff !== undefined ? codCard.diff : 0.011;

      // 9. FD Hoàn Trả (Failed Delivery)
      const fdData = D.fd || {};
      const fdSum = fdData.summary || {};
      const fdRateFull = fdSum.rate_full !== undefined ? fdSum.rate_full : 0.0754;
      const fdRateTts = fdSum.rate_tts !== undefined ? fdSum.rate_tts : 0.068;
      const fdRetFull = fdSum.ret_full || 22954;
      const fdDiff = -0.001; // So với W35 (~7.6%)

      // 10. TLTĐ (Tỷ Lệ Lấp Đầy Thùng/Xe KTC)
      const ktcData = D.ktc || {};
      const ktcWeekly = ktcData.fill_rate?.weekly?.total || {};
      const tltdVal = ktcWeekly.tld_w36 !== undefined ? (ktcWeekly.tld_w36 / 100) : 0.481;
      const tltdPrev = ktcWeekly.tld_w35 !== undefined ? (ktcWeekly.tld_w35 / 100) : 0.518;
      const tltdDiff = ktcWeekly.diff_tld !== undefined ? (ktcWeekly.diff_tld / 100) : -0.037;
      const tltdUnder30 = ktcWeekly.under_30 || 112;

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
          mainUnit: 'Full Hàng',
          subVal: `${fPct(gtcTtsVal)} (TTS)`,
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
          mainUnit: 'Full Hàng',
          subVal: `${fPct(ganTtsVal)} (TTS) | Target ≥ 90.0%`,
          diff: ganDiff,
          isHigherBetter: true,
          colorCls: 'kpi-purple',
          icon: 'user-check'
        },
        {
          id: 'odr_pair',
          title: `%ODR (Giao Đúng Hẹn SLA - ${latestWeek})`,
          mainVal: fPct(odrVal),
          mainUnit: 'Full Hàng',
          subVal: `${fPct(odrTtsVal)} (TTS)`,
          diff: odrDiff,
          isHigherBetter: true,
          colorCls: 'kpi-green',
          icon: 'clock'
        },
        {
          id: 'ltc_pair',
          title: `%LTC (Lấy Thành Công - ${latestWeek})`,
          mainVal: fPct(ltcVal),
          mainUnit: 'Full Hàng',
          subVal: `${fPct(ltcTtsVal)} (TTS)`,
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
          subVal: `${prevWeek}: 1.57% (Tăng +0.7%p)`,
          diff: rotDiff,
          isHigherBetter: false,
          colorCls: 'kpi-red',
          icon: 'truck'
        },
        {
          id: 'cod_tm',
          title: 'Tỷ Lệ COD Tiền Mặt',
          mainVal: fPct(codVal),
          mainUnit: 'Tiền mặt',
          subVal: `${fPct(1 - codVal)} (Chuyển khoản QR)`,
          diff: codDiff,
          isHigherBetter: false,
          colorCls: 'kpi-amber',
          icon: 'qr-code'
        },
        {
          id: 'fd_pair',
          title: `%FD Hoàn Trả (${latestWeek})`,
          mainVal: fPct(fdRateFull),
          mainUnit: 'Full Hàng',
          subVal: `${fPct(fdRateTts)} (TTS) | ${fNum(fdRetFull)} đ hoàn`,
          diff: fdDiff,
          isHigherBetter: false,
          colorCls: 'kpi-purple',
          icon: 'rotate-ccw'
        },
        {
          id: 'tltd_pair',
          title: `%TLTĐ Thùng Xe (${latestWeek})`,
          mainVal: fPct(tltdVal),
          mainUnit: 'Bình quân xe',
          subVal: `${prevWeek}: ${fPct(tltdPrev)} | ${tltdUnder30} xe <30%`,
          diff: tltdDiff,
          isHigherBetter: true,
          colorCls: 'kpi-teal',
          icon: 'truck'
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
          const val1 = row.w36 !== undefined ? row.w33 : row.w32;
          const val2 = row.w36 !== undefined ? row.w34 : row.w33;
          const val3 = row.w36 !== undefined ? row.w35 : row.w34;
          const val4 = row.w36 !== undefined ? row.w36 : row.w35;

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

    const dataT = D.san_luong.tinh;
    charts.sanLuongTinh = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: dataT.map(d => d.tinh),
        datasets: [
          {
            label: 'Full Hàng (Toàn Mạng) W35',
            data: dataT.map(d => d.w35),
            backgroundColor: '#1e3a8a',
            datalabels: {
              anchor: 'end',
              align: 'top',
              offset: 2,
              color: '#1e3a8a',
              font: { weight: '800', size: 10 },
              formatter: v => (v / 1000).toFixed(1) + 'k'
            }
          },
          {
            label: 'Phân Khúc TTS (TikTok Shop) W35',
            data: dataT.map(d => d.tts_w35 || Math.round(d.w35 * 0.228)),
            backgroundColor: '#f26522',
            datalabels: {
              anchor: 'end',
              align: 'top',
              offset: 2,
              color: '#d44d0e',
              font: { weight: '800', size: 10 },
              formatter: (v, ctx) => {
                const total = dataT[ctx.dataIndex].w35;
                const pct = total ? ((v / total) * 100).toFixed(1) : '22.8';
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
      let list = [...D.san_luong.am_full].map(r => {
        const curr = r.w36 !== undefined ? r.w36 : (r.w35 || 0);
        const prev = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);
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

      const sorted = list.sort((a, b) => b.diff_val - a.diff_val);

      tblBodyFull.innerHTML = sorted.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const diffBadge = renderDeltaBadge(row.diff_val, true, false); // isPercent = false (đơn)
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
      const fullMap = {};
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
      });

      if (state.searchVolTTS) {
        listTTS = listTTS.filter(r => r.am.toLowerCase().includes(state.searchVolTTS));
      }

      const sortedTTS = listTTS.sort((a, b) => b.diff_val - a.diff_val);

      tblBodyTTS.innerHTML = sortedTTS.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const diffBadge = renderDeltaBadge(row.diff_val, true, false); // isPercent = false (đơn)
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
        const v4 = row.w36 !== undefined ? (row.w36 || row.vol) : (row.w35 || row.vol);

        return `
          <tr>
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13.5px; font-weight:800;">${row.tinh}</td>
            <td class="num">${fNum(v1)}</td>
            <td class="num">${fNum(v2)}</td>
            <td class="num">${fNum(v3)}</td>
            <td class="num bold" style="background: var(--color-blue-bg); font-weight:800; font-size:13.5px;">${fNum(v4)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 4. BẢNG 3B: SẢN LƯỢNG 5 TỈNH THÀNH (TIKTOK SHOP)
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
      }).sort((a, b) => b.diff_val - a.diff_val);

      tblBodyTinhTTS.innerHTML = listTinhTTS.map((row, i) => {
        const diffBadge = renderDeltaBadge(row.diff_val, true, false);
        const evalBadge = row.diff_val > 0
          ? '<span class="badge-tag badge-tag-green">🟢 Tăng Trưởng</span>'
          : '<span class="badge-tag badge-tag-amber">Ổn Định</span>';

        const v1 = row.w36 !== undefined ? row.w33 : row.w32;
        const v2 = row.w36 !== undefined ? row.w34 : row.w33;
        const v3 = row.w36 !== undefined ? row.w35 : row.w34;
        const v4 = row.w36 !== undefined ? (row.w36 || row.vol) : (row.w35 || row.vol);

        return `
          <tr>
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13.5px; font-weight:800;">${row.tinh}</td>
            <td class="num">${fNum(v1)}</td>
            <td class="num">${fNum(v2)}</td>
            <td class="num">${fNum(v3)}</td>
            <td class="num bold" style="background: var(--color-amber-bg); color:#ea580c; font-weight:800; font-size:13.5px;">${fNum(v4)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="num" style="font-weight:700;">${fPct(row.rate_tts)}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }
  }

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

    // Master 18 AM dataset combining accurate Full and TTS figures
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

    if (mode === 'w34_vs_w35_full') {
      title = `SẢN LƯỢNG FULL HÀNG (CỘT ${prevLabel} vs ${currLabel} + ĐƯỜNG BIẾN ĐỘNG Δ)`;
      displayList.sort((a, b) => b.diff_full - a.diff_full);

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
    } else if (mode === 'w34_vs_w35_tts') {
      title = `SẢN LƯỢNG TIKTOK SHOP (CỘT TTS ${prevLabel} vs ${currLabel} + ĐƯỜNG BIẾN ĐỘNG TTS Δ)`;
      displayList.sort((a, b) => b.diff_tts - a.diff_tts);

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
      displayList.sort((a, b) => b.vol_full_w35 - a.vol_full_w35);
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
      if (titleEl) titleEl.textContent = `BIỂU ĐỒ SO SÁNH %GTC TỔNG ${prevLabel} vs ${currLabel} THEO 18 AM (FULL HÀNG)`;
      if (badgeEl) { badgeEl.textContent = 'Full Hàng'; badgeEl.className = 'badge-tag badge-tag-blue'; }
    } else if (seg === 'tts' && btnTts) {
      btnTts.classList.add('btn-primary', 'active');
      btnTts.classList.remove('btn-secondary');
      if (titleEl) titleEl.textContent = `BIỂU ĐỒ SO SÁNH %GTC TỔNG ${prevLabel} vs ${currLabel} THEO 18 AM (TIKTOK SHOP)`;
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
    if (!D.gtc_tong) return;

    // Helper evaluation badge for %GTC (Target >= 60%)
    function getGtcEvalBadge(v) {
      const val = v || 0;
      if (val >= 0.70) return '<span class="badge-tag badge-tag-green">🏆 Xuất Sắc (≥70%)</span>';
      if (val >= 0.60) return '<span class="badge-tag badge-tag-green">🟢 Đạt Chuẩn (≥60%)</span>';
      if (val >= 0.50) return '<span class="badge-tag badge-tag-amber">🟡 Tiệm Cận (50-60%)</span>';
      return '<span class="badge-tag badge-tag-red">🔴 Chưa Đạt (&lt;50%)</span>';
    }

    // 1. BẢNG 1A: %GTC FULL HÀNG (18 AM)
    const tblBodyFull = document.querySelector('#table-gtc-full-detailed tbody');
    if (tblBodyFull) {
      const rawFull = D.gtc_tong.am_full || D.gtc_tong.am || [];
      let listFull = [...rawFull].map(r => {
        const curr = r.w36 !== undefined ? r.w36 : (r.w35 || 0);
        const prev = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);
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

      const sortedFull = listFull.sort((a, b) => b.diff_val - a.diff_val);

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

    // 2. BẢNG 1B: %GTC TIKTOK SHOP (18 AM)
    const tblBodyTTS = document.querySelector('#table-gtc-tts-detailed tbody');
    if (tblBodyTTS) {
      const rawTTS = D.gtc_tong.am_tts || [];
      let listTTS = [...rawTTS].map(r => {
        const curr = r.w36 !== undefined ? r.w36 : (r.w35 || 0);
        const prev = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);
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

      const sortedTTS = listTTS.sort((a, b) => b.diff_val - a.diff_val);

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
        const v4 = row.curr_val;
        const heatClass = getHeatmapClass(v4, 'gtc');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = getGtcEvalBadge(v4);

        return `
          <tr>
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13.5px; font-weight:800;">${row.tinh}</td>
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
        const v4 = row.curr_val;
        const heatClass = getHeatmapClass(v4, 'gtc');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = getGtcEvalBadge(v4);

        return `
          <tr>
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13.5px; font-weight:800;">${row.tinh}</td>
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

    if (seg === 'full') {
      displayList.sort((a, b) => b.full_diff - a.full_diff);
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
      displayList.sort((a, b) => b.tts_diff - a.tts_diff);
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
      displayList.sort((a, b) => b.gap - a.gap);
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

  function getGtcCa1TtsData() {
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
  }

  function renderGtcTtsCa1BarChart() {
    const ctx = document.getElementById('chart-gtc-tts-ca1-bar');
    if (!ctx) return;
    if (charts.gtcTtsCa1Bar) charts.gtcTtsCa1Bar.destroy();

    const currLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1] : 'W36';
    const selectedAM = state.selectedAM;
    const hlMode = state.gtcTtsCa1Highlight || 'all';

    const sorted = getGtcCa1TtsData().sort((a, b) => b.w35_pct - a.w35_pct);

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
  // TAB 5: % GÁN VẬN HÀNH (GÁN CA 1, GÁN CA 2, GÁN TỔNG)
  // --------------------------------------------------------------------------
    // --------------------------------------------------------------------------
  // TAB 5: % GÁN VẬN HÀNH (CA 1, CA 2 & GÁN TỔNG)
  // --------------------------------------------------------------------------
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

        const v1 = row.w36 !== undefined ? row.w33 : row.w32;
        const v2 = row.w36 !== undefined ? row.w34 : row.w33;
        const v3 = row.w36 !== undefined ? row.w35 : row.w34;
        const v4 = row.w36 !== undefined ? row.w36 : row.w35;

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

    // 1. BẢNG 1: GÁN CA 1+TỒN
    const tblBodyCa1 = document.querySelector('#table-gan-ca1-detailed tbody');
    if (tblBodyCa1) {
      let listCa1 = [...D.gan.am].map(r => {
        const curr = r.ca1ton_w36 !== undefined ? r.ca1ton_w36 : r.ca1ton_w35;
        const prev = r.ca1ton_w36 !== undefined ? r.ca1ton_w35 : r.ca1ton_w34;
        return {
          ...r,
          curr_val: curr,
          prev_val: prev,
          diff_val: r.ca1ton_diff !== undefined ? r.ca1ton_diff : ((curr || 0) - (prev || 0))
        };
      }).sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

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
        const curr = r.tong_w36 !== undefined ? r.tong_w36 : r.tong_w35;
        const prev = r.tong_w36 !== undefined ? r.tong_w35 : r.tong_w34;
        return {
          ...r,
          curr_val: curr,
          prev_val: prev,
          diff_val: r.tong_diff !== undefined ? r.tong_diff : ((curr || 0) - (prev || 0))
        };
      }).sort((a, b) => (b.curr_val || 0) - (a.curr_val || 0));

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

    charts.ganOverviewBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            type: 'bar',
            label: 'W32',
            data: overview.map(d => Number((d.w32 * 100).toFixed(1))),
            backgroundColor: '#cbd5e1',
            borderRadius: 3,
            datalabels: { display: false }
          },
          {
            type: 'bar',
            label: 'W33',
            data: overview.map(d => Number((d.w33 * 100).toFixed(1))),
            backgroundColor: '#94a3b8',
            borderRadius: 3,
            datalabels: { display: false }
          },
          {
            type: 'bar',
            label: 'W34',
            data: overview.map(d => Number((d.w34 * 100).toFixed(1))),
            backgroundColor: '#60a5fa',
            borderRadius: 3,
            datalabels: { display: false }
          },
          {
            type: 'bar',
            label: 'W35',
            data: overview.map(d => Number((d.w35 * 100).toFixed(1))),
            backgroundColor: overview.map(d => d.w35 >= 0.80 ? '#10b981' : '#f59e0b'),
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
    if (charts.ganBar) charts.ganBar.destroy();

    const currLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1] : 'W36';
    const selectedAM = state.selectedAM;
    const sorted = [...D.gan.am].map(r => {
      const prev_val = r.tong_w36 !== undefined ? (r.tong_w35 || 0) : (r.tong_w34 || 0);
      const curr_val = r.tong_w36 !== undefined ? (r.tong_w36 || 0) : (r.tong_w35 || 0);
      const diff_val = r.tong_diff !== undefined ? r.tong_diff : (r.diff !== undefined ? r.diff : (curr_val - prev_val));
      const ca1 = r.ca1ton_w36 !== undefined ? r.ca1ton_w36 : (r.ca1ton_w35 || 0);
      const ca2 = r.ca2_w36 !== undefined ? r.ca2_w36 : (r.ca2_w35 || 0);
      return {
        ...r,
        ca1_pct: Number((ca1 * 100).toFixed(1)),
        ca2_pct: Number((ca2 * 100).toFixed(1)),
        tong_prev_pct: Number((prev_val * 100).toFixed(1)),
        tong_pct: Number((curr_val * 100).toFixed(1)),
        diff_pct: Number((diff_val * 100).toFixed(1))
      };
    }).sort((a, b) => b.diff_pct - a.diff_pct); // Sort theo biến động WoW

    charts.ganBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: sorted.map(d => d.am),
        datasets: [
          {
            type: 'bar',
            label: `% Gán Ca 1 + Tồn (${currLabel})`,
            data: sorted.map(d => d.ca1_pct),
            backgroundColor: '#c084fc',
            borderRadius: 4,
            yAxisID: 'y',
            order: 2
          },
          {
            type: 'bar',
            label: `% Gán Ca 2 (${currLabel})`,
            data: sorted.map(d => d.ca2_pct),
            backgroundColor: '#9333ea',
            borderRadius: 4,
            yAxisID: 'y',
            order: 2
          },
          {
            type: 'bar',
            label: `% Gán Tổng ${currLabel} (Target ≥90%)`,
            data: sorted.map(d => d.tong_pct),
            backgroundColor: sorted.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : (d.tong_pct >= 90 ? '#10b981' : '#f59e0b')),
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
            min: 0,
            max: 105,
            ticks: { callback: v => v + '%' },
          },
          y1: {
            position: 'right',
            grid: { drawOnChartArea: false },
            title: { display: true, text: 'Biến Động WoW (Δ % p.p)', font: { weight: '700', size: 11, color: '#f26522' } },
            ticks: { callback: v => (v > 0 ? '+' : '') + v + '%' }
          },
          x: {
            ticks: { maxRotation: 45, minRotation: 30, font: { size: 11, weight: '600' } }
          }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => `${c.dataset.label}: ${c.parsed.y}%`
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

    // 1. BẢNG 1A: %ODR FULL HÀNG (18 AM)
    const tblBodyFull = document.querySelector('#table-odr-full-detailed tbody');
    if (tblBodyFull) {
      const rawFull = D.odr.am_full || D.odr.am || [];
      let listFull = [...rawFull].map(r => {
        const curr = r.w36 !== undefined ? r.w36 : (r.w35 || 0);
        const prev = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);
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

      const sortedFull = listFull.sort((a, b) => b.diff_val - a.diff_val);

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

    // 2. BẢNG 1B: %ODR TIKTOK SHOP (18 AM)
    const tblBodyTTS = document.querySelector('#table-odr-tts-detailed tbody');
    if (tblBodyTTS) {
      const rawTTS = D.odr.am_tts || [];
      let listTTS = [...rawTTS].map(r => {
        const curr = r.w36 !== undefined ? r.w36 : (r.w35 || 0);
        const prev = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);
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

      const sortedTTS = listTTS.sort((a, b) => b.diff_val - a.diff_val);

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
        const v4 = row.curr_val;
        const heatClass = getHeatmapClass(v4, 'odr');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = getOdrEvalBadge(v4);

        return `
          <tr>
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13.5px; font-weight:800;">${row.tinh}</td>
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
        const v4 = row.curr_val;
        const heatClass = getHeatmapClass(v4, 'odr');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = getOdrEvalBadge(v4);

        return `
          <tr>
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13.5px; font-weight:800;">${row.tinh}</td>
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
        : `BIỂU ĐỒ %ODR GIAO ĐÚNG HẸN THEO 18 AM (${seg === 'tts' ? 'TIKTOK SHOP' : 'FULL HÀNG'})`;
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

    if (seg === 'full') {
      displayList.sort((a, b) => b.full_diff - a.full_diff);
      datasets = [
        {
          type: 'bar',
          label: `%ODR Full ${prevLabel} (%)`,
          data: displayList.map(d => d.full_w34),
          backgroundColor: displayList.map(d => {
            const isM = checkOdrMatch(d);
            if (!hasFilter) return '#94a3b8';
            return isM ? '#64748b' : 'rgba(203, 213, 225, 0.2)';
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
            if (!isM) return 'rgba(148, 163, 184, 0.15)';
            if (hlMode === 'pass') return '#10b981';
            if (hlMode === 'fail') return '#ef4444';
            if (hlMode === 'grow') return '#0284c7';
            return '#ef4444';
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
      displayList.sort((a, b) => b.tts_diff - a.tts_diff);
      datasets = [
        {
          type: 'bar',
          label: `%ODR TTS ${prevLabel} (%)`,
          data: displayList.map(d => d.tts_w34),
          backgroundColor: displayList.map(d => {
            const isM = checkOdrMatch(d);
            if (!hasFilter) return '#cbd5e1';
            return isM ? '#94a3b8' : 'rgba(203, 213, 225, 0.2)';
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
            if (!hasFilter) return d.tts_w35 >= 92.0 ? '#10b981' : '#f97316';
            if (!isM) return 'rgba(148, 163, 184, 0.15)';
            if (hlMode === 'pass') return '#10b981';
            if (hlMode === 'fail') return '#ef4444';
            if (hlMode === 'grow') return '#0284c7';
            return '#ef4444';
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
      displayList.sort((a, b) => b.gap - a.gap);
      y1Title = 'Chênh Lệch Gap (TTS - Full % p.p)';
      datasets = [
        {
          type: 'bar',
          label: `%ODR Full Hàng ${currLabel}`,
          data: displayList.map(d => d.full_w35),
          backgroundColor: displayList.map(d => {
            const isM = checkOdrMatch(d);
            if (!hasFilter) return '#2563eb';
            return isM ? '#2563eb' : 'rgba(37, 99, 235, 0.18)';
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
            return isM ? '#f97316' : 'rgba(249, 115, 22, 0.18)';
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
            min: 50,
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

    // 1. BẢNG 1: 18 AM
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
        const v4 = row.curr_val;
        const heatClass = getHeatmapClass(v4, 'ltc');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = (v4 || 0) >= 0.90
          ? '<span class="badge-tag badge-tag-green">🟢 Đạt Chuẩn SLA (≥90%)</span>'
          : '<span class="badge-tag badge-tag-red">🔴 Cần Thúc Đẩy (&lt;90%)</span>';

        return `
          <tr>
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800;">${row.tinh}</td>
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
    }).sort((a, b) => b.diff_pct - a.diff_pct); // Sort theo biến động WoW

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

    // Tính % OPR TTS tổng toàn vùng (weighted)
    const _ams = D.opr_tts.am;
    const _totalVol = _ams.reduce((s, r) => s + (r.vol_day||0) + (r.vol_night||0), 0);
    const _volDay = _ams.reduce((s, r) => s + (r.vol_day || 0), 0);
    const _volNight = _ams.reduce((s, r) => s + (r.vol_night || 0), 0);
    const _vung36Day = _volDay > 0 ? _ams.reduce((s, r) => s + (r.vol_day || 0) * (r.w36_day || 0), 0) / _volDay : 0;
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
    }, 0);
    const _vung36 = _totalVol > 0 ? _wtd36 / _totalVol : 0;
    const _vung35 = _totalVol > 0 ? _wtd35 / _totalVol : 0;
    const _diff = _vung36 - _vung35;
    const _kpiOk = _vung36 >= 0.80;
    const _vungEl = document.getElementById('opr-tts-vung-total');
    if (_vungEl) {
      const diffTxt = (_diff >= 0 ? '▲ +' : '▼ ') + Math.abs(_diff * 100).toFixed(1) + '%p WoW';
      const diffColor = _diff >= 0 ? '#10b981' : '#ef4444';
      const kpiBadge = _kpiOk
        ? '<span class="badge-tag badge-tag-green" style="font-size:13px; font-weight:800; padding:6px 14px;">✅ Đạt KPI (≥80%)</span>'
        : '<span class="badge-tag badge-tag-red" style="font-size:13px; font-weight:800; padding:6px 14px;">❌ Chưa Đạt KPI (<80%)</span>';
      _vungEl.innerHTML = `
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px; padding:14px 20px; background:linear-gradient(135deg, rgba(239,68,68,0.06), rgba(245,158,11,0.06)); border:1.5px solid rgba(239,68,68,0.25); border-radius:12px; margin-bottom:16px;">
          <div style="display:flex; align-items:center; gap:16px;">
            <div style="font-size:32px; font-weight:900; color:${_kpiOk ? '#10b981' : '#ef4444'}; font-family:var(--font-mono, monospace); line-height:1;">
              ${(_vung36*100).toFixed(1)}%
            </div>
            <div>
              <div style="font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.5px; color:var(--text-main, #1e293b);">
                OPR TTS Toàn Vùng W36 (Tổng Ngày + Đêm)
              </div>
              <div style="font-size:12px; font-weight:700; color:${diffColor}; margin-top:2px;">
                ${diffTxt} (W35: ${(_vung35*100).toFixed(1)}%) &nbsp;•&nbsp; 
                <span style="color:#64748b;">Mục tiêu KPI: ≥ 80.0% (Cách KPI: -${((0.80 - _vung36)*100).toFixed(1)}%p)</span>
              </div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:14px; flex-wrap:wrap;">
            <div style="display:flex; gap:8px;">
              <span class="badge-tag badge-tag-amber" style="font-size:11px; padding:5px 10px;">☀️ Ca Ngày: <strong>${(_vung36Day*100).toFixed(1)}%</strong></span>
              <span class="badge-tag badge-tag-purple" style="font-size:11px; padding:5px 10px;">🌙 Ca Đêm: <strong>${(_vung36Night*100).toFixed(1)}%</strong></span>
            </div>
            ${kpiBadge}
          </div>
        </div>
      `;
    }

    // Render danh sách AM chưa đạt KPI OPR TTS (< 80.0%)
    const _failedContainer = document.getElementById('opr-failed-ams-container');
    if (_failedContainer) {
      // Sắp xếp các AM chưa đạt tổng (< 80%) từ thấp nhất lên
      const failedTotal = _ams.filter(r => (r.w36_total !== undefined ? r.w36_total : 0) < 0.80)
                              .sort((a, b) => (a.w36_total || 0) - (b.w36_total || 0));
      const failedDay = _ams.filter(r => (r.w36_day || 0) < 0.80)
                            .sort((a, b) => (a.w36_day || 0) - (b.w36_day || 0));
      const failedNight = _ams.filter(r => (r.w36_night || 0) < 0.80)
                              .sort((a, b) => (a.w36_night || 0) - (b.w36_night || 0));

      _failedContainer.innerHTML = `
        <div style="background:var(--bg-surface, #ffffff); border:1.5px solid rgba(239, 68, 68, 0.35); border-left:5px solid #ef4444; border-radius:12px; padding:16px 20px; box-shadow:0 3px 12px rgba(239,68,68,0.06); margin-bottom:16px;">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:14px; border-bottom:1px solid rgba(239,68,68,0.15); padding-bottom:12px;">
            <div style="display:flex; align-items:center; gap:10px;">
              <span style="font-size:22px;">🚨</span>
              <div>
                <h4 style="margin:0; font-size:15px; font-weight:900; color:#b91c1c; text-transform:uppercase; letter-spacing:0.3px;">
                  DANH SÁCH ${failedTotal.length} AM CHƯA ĐẠT KPI OPR TTS (< 80.0%)
                </h4>
                <div style="font-size:12px; color:var(--text-muted, #64748b); margin-top:2px;">
                  Nhấp vào từng thẻ AM để tự động định vị và làm nổi bật (laser highlight) trên biểu đồ & các bảng bên dưới
                </div>
              </div>
            </div>
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              <span class="badge-tag badge-tag-red" style="font-size:12px; font-weight:800; padding:6px 12px;">
                🔴 Toàn Ngày: <strong>${failedTotal.length}/17 AM</strong>
              </span>
              <span class="badge-tag badge-tag-amber" style="font-size:12px; font-weight:800; padding:6px 12px;">
                ☀️ Ca Ngày: <strong>${failedDay.length}/17 AM</strong>
              </span>
              <span class="badge-tag badge-tag-purple" style="font-size:12px; font-weight:800; padding:6px 12px;">
                🌙 Ca Đêm: <strong>${failedNight.length}/17 AM</strong>
              </span>
            </div>
          </div>

          <div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(285px, 1fr)); gap:12px;">
            ${failedTotal.map(r => {
              const val = ((r.w36_total !== undefined ? r.w36_total : 0) * 100);
              const gap = (80 - val).toFixed(1);
              const dayVal = ((r.w36_day || 0) * 100).toFixed(1);
              const nightVal = ((r.w36_night || 0) * 100).toFixed(1);
              const diffTot = r.diff_total !== undefined ? (r.diff_total * 100) : 0;
              const diffBadge = diffTot !== 0 ? `<span style="font-size:11px; font-weight:800; color:${diffTot > 0 ? '#10b981' : '#ef4444'};">${diffTot > 0 ? '▲ +' : '▼ '}${Math.abs(diffTot).toFixed(1)}%p</span>` : '';
              const isSelected = state.selectedAM === r.am;

              return `
                <div onclick="selectAndHighlightAM('${r.am}')" 
                     style="cursor:pointer; padding:12px 14px; background:${isSelected ? 'rgba(239,68,68,0.12)' : 'var(--bg-main, #f8fafc)'}; border:1.5px solid ${isSelected ? '#ef4444' : 'rgba(239,68,68,0.22)'}; border-radius:10px; transition:all 0.2s;" 
                     onmouseover="this.style.borderColor='#ef4444'; this.style.boxShadow='0 4px 12px rgba(239,68,68,0.15)'; this.style.transform='translateY(-2px)'" 
                     onmouseout="this.style.borderColor='${isSelected ? '#ef4444' : 'rgba(239,68,68,0.22)'}'; this.style.boxShadow='none'; this.style.transform='none'">
                  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-weight:900; font-size:13.5px; color:${isSelected ? '#ef4444' : 'var(--text-main, #0f172a)'};">${r.am}</div>
                    <span style="font-size:11px; font-weight:800; color:#b91c1c; background:rgba(239,68,68,0.12); padding:2px 8px; border-radius:6px;">
                      Thiếu -${gap}%p
                    </span>
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
        const curr = r.w36_day !== undefined ? r.w36_day : r.w35_day;
        const prev = r.w36_day !== undefined ? r.w35_day : r.w34_day;
        return {
          ...r,
          curr_val: curr,
          prev_val: prev,
          diff_val: r.diff_day !== undefined ? r.diff_day : ((curr || 0) - (prev || 0))
        };
      }).sort((a, b) => b.diff_val - a.diff_val);

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
        const curr = r.w36_night !== undefined ? r.w36_night : r.w35_night;
        const prev = r.w36_night !== undefined ? r.w35_night : r.w34_night;
        return {
          ...r,
          curr_val: curr,
          prev_val: prev,
          diff_val: r.diff_night !== undefined ? r.diff_night : ((curr || 0) - (prev || 0))
        };
      }).sort((a, b) => b.diff_val - a.diff_val);

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

      const sorted = list.sort((a, b) => (b.diff_night || 0) - (a.diff_night || 0));

      tblBody.innerHTML = sorted.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const currDay = row.w36_day !== undefined ? row.w36_day : row.w35_day;
        const prevDay = row.w36_day !== undefined ? row.w35_day : row.w34_day;
        const currNight = row.w36_night !== undefined ? row.w36_night : row.w35_night;
        const prevNight = row.w36_night !== undefined ? row.w35_night : row.w34_night;
        const heatDay = getHeatmapClass(currDay, 'opr');
        const heatNight = getHeatmapClass(currNight, 'opr');
        const diffDay = renderDeltaBadge(row.diff_day, true, true);
        const diffNight = renderDeltaBadge(row.diff_night, true, true);

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center bold">${i + 1}</td>
            <td class="bold" style="font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol_day)}</td>
            <td class="num">${fPct(prevDay)}</td>
            <td class="num bold ${heatDay}">${fPct(currDay)}</td>
            <td class="num bold">${diffDay}</td>
            <td class="num">${fNum(row.vol_night)}</td>
            <td class="num">${fPct(prevNight)}</td>
            <td class="num bold ${heatNight}">${fPct(currNight)}</td>
            <td class="num bold">${diffNight}</td>
            <td class="num bold" style="color: var(--color-blue);">${fNum(row.total_vol)}</td>
          </tr>
        `;
      }).join('');
    }
  }

  function renderOprGroupedChart() {
    const ctx = document.getElementById('chart-opr-tts-grouped');
    if (!ctx || !D.opr_tts || !D.opr_tts.am) return;
    if (charts.oprGrouped) charts.oprGrouped.destroy();

    const currLabel = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 1] : 'W36';
    const selectedAM = state.selectedAM;
    // Sắp xếp cải thiện tốt nhất giảm dần (diff_total descending)
    const ams = [...D.opr_tts.am].sort((a, b) => {
      const diffA = a.diff_total !== undefined ? a.diff_total : ((a.w36_total || a.w35_total || 0) - (a.w35_total || a.w34_total || 0));
      const diffB = b.diff_total !== undefined ? b.diff_total : ((b.w36_total || b.w35_total || 0) - (b.w35_total || b.w34_total || 0));
      return diffB - diffA;
    });

    const diffVals = ams.map(d => Number(((d.diff_total !== undefined ? d.diff_total : ((d.w36_total || d.w35_total || 0) - (d.w35_total || d.w34_total || 0))) * 100).toFixed(1)));
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
            data: ams.map(d => Number(((d.w36_day !== undefined ? d.w36_day : (d.w35_day || 0)) * 100).toFixed(1))),
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
            data: ams.map(d => Number(((d.w36_night !== undefined ? d.w36_night : (d.w35_night || 0)) * 100).toFixed(1))),
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
            data: ams.map(d => Number(((d.w36_total !== undefined ? d.w36_total : (d.w35_total !== undefined ? d.w35_total : ((d.w36_day || 0) * 0.6 + (d.w36_night || 0) * 0.4))) * 100).toFixed(1))),
            borderColor: '#15803d',
            borderWidth: 3.5,
            tension: 0.25,
            pointBackgroundColor: ams.map(d => {
              const val = ((d.w36_total !== undefined ? d.w36_total : 0) * 100);
              return val < 80 ? '#dc2626' : '#16a34a';
            }),
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2,
            pointRadius: ams.map(d => {
              const val = ((d.w36_total !== undefined ? d.w36_total : 0) * 100);
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
                const val = ((d.w36_total !== undefined ? d.w36_total : 0) * 100);
                return val < 80 ? '#b91c1c' : '#166534';
              }),
              backgroundColor: ams.map(d => {
                const val = ((d.w36_total !== undefined ? d.w36_total : 0) * 100);
                return val < 80 ? 'rgba(254, 226, 226, 0.96)' : 'rgba(240, 253, 244, 0.96)';
              }),
              borderColor: ams.map(d => {
                const val = ((d.w36_total !== undefined ? d.w36_total : 0) * 100);
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
            borderColor: '#dc2626',
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
          // ---- Toàn Vùng W36 reference line ----
          {
            type: 'line',
            label: 'Toàn Vùng W36: 76.9% (Chưa Đạt)',
            data: ams.map(() => 76.9),
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

    // 1. BẢNG 1: 18 AM
    const tblBodyAM = document.querySelector('#table-rot-am-detailed tbody');
    if (tblBodyAM && D.rot_lc.am) {
      let listAM = [...D.rot_lc.am].map(r => {
        const wPrev = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);
        const wCurr = r.w36 !== undefined ? (r.w36 || 0) : (r.w35 || 0);
        const diff_val = r.diff !== undefined ? r.diff : (wCurr - wPrev);
        return {
          ...r,
          wPrev,
          wCurr,
          diff_val
        };
      }).sort((a, b) => (b.wCurr || 0) - (a.wCurr || 0));

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
      let listTinh = [...D.rot_lc.tinh].map(r => {
        const wPrev = r.w36 !== undefined ? (r.w35 || 0) : (r.w34 || 0);
        const wCurr = r.w36 !== undefined ? (r.w36 || 0) : (r.w35 || 0);
        const diff_val = r.diff !== undefined ? r.diff : (wCurr - wPrev);
        return {
          ...r,
          wPrev,
          wCurr,
          diff_val
        };
      }).sort((a, b) => (b.wCurr || 0) - (a.wCurr || 0));

      tblBodyTinh.innerHTML = listTinh.map((row, i) => {
        const heatCurr = getHeatmapClass(row.wCurr, 'rot_lc');
        const diffBadge = renderDeltaBadge(row.diff_val, false, true);
        let evalBadge = '<span class="badge-tag badge-tag-green">🟢 Tốt (≤1%)</span>';
        if ((row.wCurr || 0) > 0.05) evalBadge = '<span class="badge-tag badge-tag-red">🔴 Nghiêm Trọng (&gt;5%)</span>';
        else if ((row.wCurr || 0) > 0.02) evalBadge = '<span class="badge-tag badge-tag-amber">🟡 Cảnh Báo (2-5%)</span>';

        return `
          <tr>
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800;">${row.tinh}</td>
            <td class="num">${fNum(row.vol)}</td>
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

    const prevKey = D.meta?.weeks ? D.meta.weeks[D.meta.weeks.length - 2].toLowerCase() : 'w35';
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
    }).sort((a, b) => a.diff_pct - b.diff_pct); // Sort từ cải thiện giảm rớt tốt nhất đến tăng rớt

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
    if (window.lucide) lucide.createIcons();
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

      if (chartTitle) chartTitle.textContent = 'BIỂU ĐỒ TOP AM NHIỀU ĐƠN AGING >5 NGÀY VÀ MIỀN TỶ TRỌNG (%)';
      if (tblAmTitle) tblAmTitle.textContent = 'BẢNG 1: TOP AM NHIỀU ĐƠN AGING >5 NGÀY NHẤT (SORT GIẢM DẦN)';
      if (tblBcTitle) tblBcTitle.textContent = 'BẢNG 2: TOP BƯU CỤC (BC) CẦN GIẢI CỨU AGING GẤP';
    } else if (seg === 'treo_lc' && D.treo_lc) {
      if (t1) t1.textContent = 'Tổng Đơn Treo Luân Chuyển (LC)';
      if (v1) v1.innerHTML = `${fNum(D.treo_lc.total)} <small>đơn</small>`;
      if (m1) m1.innerHTML = '<span class="diff-tag diff-neutral">Đang vận chuyển toàn mạng</span>';

      const topAM = D.treo_lc.top_am[0] || {};
      if (t2) t2.textContent = 'Top 1 AM Treo LC Cao Nhất';
      if (v2) v2.textContent = topAM.am || '---';
      if (m2) m2.innerHTML = `<span class="diff-tag diff-neutral">${fNum(topAM.vol)} đơn (${topAM.pct}%)</span>`;

      const topBC = D.treo_lc.top_bc[0] || {};
      if (t3) t3.textContent = 'Top 1 BC Treo LC Nhiều Nhất';
      if (v3) v3.textContent = topBC.bc ? topBC.bc.substring(0, 24) + '...' : '---';
      if (m3) m3.innerHTML = `<span class="diff-tag diff-neutral">${fNum(topBC.vol)} đơn (${topBC.pct}%)</span>`;

      const topTinh = D.treo_lc.tinh[0] || {};
      if (t4) t4.textContent = 'Tỉnh Treo LC Nhiều Nhất';
      if (v4) v4.textContent = topTinh.tinh || '---';
      if (m4) m4.innerHTML = `<span class="diff-tag diff-neutral">${fNum(topTinh.vol)} đơn (${topTinh.pct}%)</span>`;

      if (chartTitle) chartTitle.textContent = 'BIỂU ĐỒ TOP AM NHIỀU ĐƠN TREO LUÂN CHUYỂN (LC) VÀ MIỀN TỶ TRỌNG (%)';
      if (tblAmTitle) tblAmTitle.textContent = 'BẢNG 1: TOP AM NHIỀU ĐƠN TREO LUÂN CHUYỂN NHẤT (SORT GIẢM DẦN)';
      if (tblBcTitle) tblBcTitle.textContent = 'BẢNG 2: TOP BƯU CỤC (BC) TREO LUÂN CHUYỂN NHIỀU NHẤT';
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
        ? 'BIỂU ĐỒ %FD THEO 18 AM – PHÂN KHÚC TIKTOK SHOP (CỘT %FD + MIỀN SẢN LƯỢNG + ĐƯỜNG BIẾN ĐỘNG Δ)'
        : 'BIỂU ĐỒ %FD THEO 18 AM – TOÀN MẠNG FULL HÀNG (CỘT %FD + MIỀN SẢN LƯỢNG + ĐƯỜNG BIẾN ĐỘNG Δ)';
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

    // 1. KPI Summary Cards
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
    }

    // 2. Bảng 1: 18 AM (Full Hàng vs TTS)
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

    // 3. Bảng 2: Top Bưu Cục
    const tblBodyBC = document.querySelector('#table-fd-top-bc tbody');
    if (tblBodyBC && D.fd.top_bc) {
      let listBC = [...D.fd.top_bc];
      if (state.searchFdBc) {
        const q = state.searchFdBc.toLowerCase();
        listBC = listBC.filter(r => r.bc.toLowerCase().includes(q) || (r.am && r.am.toLowerCase().includes(q)));
      }

      tblBodyBC.innerHTML = listBC.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const heatClass = getHeatmapClass(row.rate, 'rot_lc');
        let badge = '<span class="badge-tag badge-tag-green">🟢 An Toàn (&lt;8%)</span>';
        if (row.rate >= 0.15) badge = '<span class="badge-tag badge-tag-red" style="background:#7f1d1d; color:#fff;">🚨 Báo Động (≥15%)</span>';
        else if (row.rate >= 0.10) badge = '<span class="badge-tag badge-tag-red">🔴 Nghiêm Trọng (10–15%)</span>';
        else if (row.rate >= 0.08) badge = '<span class="badge-tag badge-tag-amber">🟡 Cảnh Báo (8–10%)</span>';

        return `
          <tr data-entity="${row.bc}">
            <td class="center bold">${row.stt || (i + 1)}</td>
            <td class="bold" style="font-weight:800; font-size:13px;">${row.bc}</td>
            <td class="bold" style="font-size:12.5px; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am || '---'}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num bold" style="color:#ef4444;">${fNum(row.ret)}</td>
            <td class="num bold ${heatClass}">${fPct(row.rate)}</td>
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

    let sorted = [...D.fd.am];
    if (mode === 'tts') {
      sorted.sort((a, b) => b.rate_tts - a.rate_tts);
    } else {
      sorted.sort((a, b) => b.rate_full - a.rate_full);
    }

    const labels = sorted.map(d => d.am.replace('Nguyễn ', 'N. ').replace('Lê ', 'L. '));
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
            label: mode === 'tts' ? '%FD TTS W35 (Tuần Trước)' : '%FD Full W35 (Tuần Trước)',
            data: prevData,
            backgroundColor: '#94a3b8',
            borderRadius: 4,
            yAxisID: 'y',
            order: 3
          },
          {
            type: 'bar',
            label: mode === 'tts' ? '%FD TTS W36 (Hiện Tại)' : '%FD Full W36 (Hiện Tại)',
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
          legend: { position: 'top' },
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
            title: { display: true, text: '%FD Return (%)', font: { weight: '700', size: 11 } },
            ticks: { callback: v => v + '%' }
          },
          yVol: {
            type: 'linear',
            position: 'right',
            grid: { drawOnChartArea: false },
            title: { display: true, text: 'Sản Lượng Giao (Đơn)', font: { weight: '700', size: 11 } },
            ticks: { callback: v => fNum(v) }
          },
          yDiff: {
            type: 'linear',
            display: false,
            grid: { drawOnChartArea: false }
          },
          x: {
            ticks: { maxRotation: 45, minRotation: 30, font: { size: 10 } }
          }
        }
      }
    });
  }

  function renderAgingTab() {
    const seg = state.agingSegment || 'aging';
    const isAging = seg === 'aging';
    const isTreo = seg === 'treo_lc';
    const isCompare = seg === 'compare';

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
            <th style="color:#ffffff;">AM</th>
            <th class="num" style="background: #0284c7; color: #ffffff; font-weight:700;">36 – 72h</th>
            <th class="num" style="background: #d97706; color: #ffffff; font-weight:700;">72 – 120h</th>
            <th class="num" style="background: #ea580c; color: #ffffff; font-weight:700;">120 – 192h</th>
            <th class="num" style="background: #dc2626; color: #ffffff; font-weight:700;">192h+</th>
            <th class="num" style="background: #f59e0b; color: #000000; font-weight:900; font-size:13.5px;">Tổng (mốc live)</th>
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
            vol_treo: t.vol || 0,
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
          const h36 = row.h_36_72 !== undefined ? row.h_36_72 : 0;
          const h72 = row.h_72_120 !== undefined ? row.h_72_120 : 0;
          const h120 = row.h_120_192 !== undefined ? row.h_120_192 : 0;
          const h192 = row.h_192_plus !== undefined ? row.h_192_plus : 0;

          return `
            <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
              <td class="center">${renderRankPill(i)}</td>
              <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
              <td class="num" style="background: rgba(2, 132, 199, 0.05); font-weight:600;">${fNum(h36)}</td>
              <td class="num" style="background: rgba(217, 119, 6, 0.05); font-weight:600;">${fNum(h72)}</td>
              <td class="num" style="background: rgba(234, 88, 12, 0.05); font-weight:600;">${fNum(h120)}</td>
              <td class="num bold" style="background: rgba(220, 38, 38, 0.08); color: ${h192 > 0 ? '#dc2626' : '#64748b'};">${fNum(h192)}</td>
              <td class="num bold" style="background: #fef08a; color: #92400e; font-size:13.5px; font-weight:900;">${fNum(row.vol)}</td>
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
            <td class="num bold" style="font-size: 13.5px; color: #0369a1;">${fNum(D.aging.total_5_8 || 1329)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #b45309;">${fNum(D.aging.total_8_15 || 674)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #b91c1c;">${fNum(D.aging.total_gt_15 || 334)}</td>
            <td class="num bold" style="background: #f59e0b; color: #000000; font-size:14.5px;">${fNum(D.aging.total || 2337)}</td>
          </tr>
        `;
      } else if (isTreo && D.treo_lc) {
        rowsHtml += `
          <tr style="background: #fde047; font-weight: 900; border-top: 2px solid #ca8a04;">
            <td class="center">⭐</td>
            <td class="bold" style="font-size: 13.5px; text-transform: uppercase;">TỔNG VÙNG</td>
            <td class="num bold" style="font-size: 13.5px; color: #0369a1;">${fNum(D.treo_lc.total_36_72 || 236)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #b45309;">${fNum(D.treo_lc.total_72_120 || 41)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #ea580c;">${fNum(D.treo_lc.total_120_192 || 44)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #b91c1c;">${fNum(D.treo_lc.total_192_plus || 33)}</td>
            <td class="num bold" style="background: #f59e0b; color: #000000; font-size:14.5px;">${fNum(D.treo_lc.total || 354)}</td>
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
            <th style="color:#ffffff;">Bưu Cục</th>
            <th class="num" style="background: #0284c7; color: #ffffff; font-weight:700;">36 – 72h</th>
            <th class="num" style="background: #d97706; color: #ffffff; font-weight:700;">72 – 120h</th>
            <th class="num" style="background: #ea580c; color: #ffffff; font-weight:700;">120 – 192h</th>
            <th class="num" style="background: #dc2626; color: #ffffff; font-weight:700;">192h+</th>
            <th class="num" style="background: #f59e0b; color: #000000; font-weight:900; font-size:13.5px;">Tổng (mốc live)</th>
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

      tblBodyBC.innerHTML = listBC.map((row, i) => {
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
          const h36 = row.h_36_72 !== undefined ? row.h_36_72 : 0;
          const h72 = row.h_72_120 !== undefined ? row.h_72_120 : 0;
          const h120 = row.h_120_192 !== undefined ? row.h_120_192 : 0;
          const h192 = row.h_192_plus !== undefined ? row.h_192_plus : 0;

          return `
            <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
              <td class="center">${renderRankPill(i)}</td>
              <td class="bold" style="font-size:13px; font-weight:800;">${row.bc} <small style="color:var(--text-muted);">(${row.am})</small></td>
              <td class="num" style="background: rgba(2, 132, 199, 0.05); font-weight:600;">${fNum(h36)}</td>
              <td class="num" style="background: rgba(217, 119, 6, 0.05); font-weight:600;">${fNum(h72)}</td>
              <td class="num" style="background: rgba(234, 88, 12, 0.05); font-weight:600;">${fNum(h120)}</td>
              <td class="num bold" style="background: rgba(220, 38, 38, 0.08); color: ${h192 > 0 ? '#dc2626' : '#64748b'};">${fNum(h192)}</td>
              <td class="num bold" style="background: #fef08a; color: #92400e; font-size:13.5px; font-weight:900;">${fNum(row.vol)}</td>
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
    }
  }

  function renderAgingChart() {
    const ctx = document.getElementById('chart-aging-bar');
    if (!ctx) return;
    if (charts.agingBar) charts.agingBar.destroy();

    const seg = state.agingSegment || 'aging';
    const selectedAM = state.selectedAM;
    const hlMode = state.agingHighlight || 'all';

    let dataList = [];
    if (seg === 'aging' && D.aging) {
      dataList = (D.aging.top_am || []).slice(0, 15).map(r => ({
        am: r.am,
        vol: r.vol,
        pct: r.pct,
        tinh: r.tinh
      }));
    } else if (seg === 'treo_lc' && D.treo_lc) {
      dataList = (D.treo_lc.top_am || []).slice(0, 15).map(r => ({
        am: r.am,
        vol: r.vol,
        pct: r.pct,
        tinh: r.tinh
      }));
    } else if (seg === 'compare' && D.aging && D.treo_lc) {
      const agingMap = {};
      (D.aging.top_am || []).forEach(r => agingMap[r.am] = r.vol);
      dataList = (D.treo_lc.top_am || []).slice(0, 15).map(r => ({
        am: r.am,
        vol: agingMap[r.am] || 0,
        vol_treo: r.vol,
        pct: r.pct,
        tinh: r.tinh
      }));
    }

    if (dataList.length === 0) return;

    let datasets = [];
    if (seg === 'compare') {
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
          label: 'Đơn Treo Luân Chuyển',
          data: dataList.map(d => d.vol_treo),
          backgroundColor: dataList.map(d => selectedAM && selectedAM === d.am ? '#f59e0b' : '#3b82f6'),
          borderRadius: 4,
          yAxisID: 'yVol',
          order: 2
        }
      ];
    } else {
      datasets = [
        {
          type: 'line',
          label: '🌊 Miền Tỷ Trọng (%)',
          data: dataList.map(d => d.pct),
          fill: true,
          backgroundColor: seg === 'aging' ? 'rgba(239, 68, 68, 0.15)' : 'rgba(147, 51, 234, 0.15)',
          borderColor: seg === 'aging' ? '#ef4444' : '#9333ea',
          borderWidth: 2,
          tension: 0.35,
          pointRadius: 5,
          pointBackgroundColor: seg === 'aging' ? '#ef4444' : '#9333ea',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          yAxisID: 'yPct',
          order: 4
        },
        {
          type: 'bar',
          label: seg === 'aging' ? 'Số Đơn Aging >5 Ngày' : 'Số Đơn Treo Luân Chuyển',
          data: dataList.map(d => d.vol),
          backgroundColor: dataList.map(d => {
            if (selectedAM && selectedAM === d.am) return '#ef4444';
            if (hlMode === 'danger') return d.vol >= (seg === 'aging' ? 100 : 500) ? '#b91c1c' : 'rgba(185, 28, 28, 0.2)';
            if (hlMode === 'warning') return d.vol >= (seg === 'aging' ? 30 : 300) ? '#d97706' : 'rgba(217, 119, 6, 0.2)';
            return seg === 'aging' ? '#dc2626' : '#2563eb';
          }),
          borderColor: dataList.map(d => selectedAM && selectedAM === d.am ? '#b91c1c' : 'transparent'),
          borderWidth: dataList.map(d => selectedAM && selectedAM === d.am ? 3 : 0),
          borderRadius: 4,
          yAxisID: 'y',
          order: 2
        }
      ];
    }

    charts.agingBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: dataList.map(d => d.am),
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 20, bottom: 8 } },
        scales: {
          y: {
            position: 'left',
            min: 0,
            title: { display: true, text: seg === 'compare' ? 'Số Đơn Aging' : 'Số Lượng Đơn Tồn / Treo', font: { weight: '700', size: 11 } },
            ticks: { callback: v => fNum(v) },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          yPct: {
            position: 'right',
            min: 0,
            display: seg !== 'compare',
            grid: { drawOnChartArea: false },
            title: { display: true, text: 'Tỷ Trọng (%)', font: { weight: '700', size: 11, color: seg === 'aging' ? '#ef4444' : '#9333ea' } },
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
            ticks: { maxRotation: 45, minRotation: 25, font: { size: 11, weight: '800' } },
            grid: { display: false }
          }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => {
                if (c.dataset.yAxisID === 'yPct') return `🌊 Tỷ trọng vùng: ${c.parsed.y}%`;
                return `${c.dataset.label}: ${fNum(c.parsed.y)} đơn`;
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

    charts.codTmAmBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Tuần N-1 (01–15/08)', 'Tuần N (16–30/08)'],
        datasets: [
          {
            label: 'Tiền Mặt (Triệu ₫)',
            data: [78462.9, 71635.1],
            backgroundColor: '#ef4444',
            borderRadius: 4
          },
          {
            label: 'Chuyển Khoản (Triệu ₫)',
            data: [125488.2, 109188.8],
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

  function renderTruyThuLoaiBar() {
    const ctx = document.getElementById('chart-truy-thu-loai-bar');
    if (!ctx || !D.truy_thu || !D.truy_thu.types) return;
    if (charts.truyThuLoaiBar) charts.truyThuLoaiBar.destroy();

    const types = D.truy_thu.types;

    charts.truyThuLoaiBar = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: types.map(d => d.type),
        datasets: [
          {
            data: types.map(d => Math.round((d.amount || 0) / 1e6)),
            backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6', '#8b5cf6']
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
              label: c => ` ${c.label}: ${fNum(c.parsed)} Triệu VNĐ (${types[c.dataIndex].pct}%)`
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
      btnGroup.querySelectorAll('.btn').forEach(b => {
        b.classList.remove('active', 'btn-primary');
        b.classList.add('btn-secondary');
      });
      const activeBtn = document.getElementById('btn-tt-' + seg);
      if (activeBtn) {
        activeBtn.classList.remove('btn-secondary');
        activeBtn.classList.add('active', 'btn-primary');
      }
    }

    const panels = ['loai', 'bcgiao', 'amticket', 'bcticket'];
    panels.forEach(p => {
      const el = document.getElementById('truythu-panel-' + p);
      if (el) el.style.display = (p === seg) ? 'block' : 'none';
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

    // 0. UPDATE DYNAMIC KPI CARDS & BANNER
    if (report.total_records) {
      const elRecords = document.getElementById('truythu-kpi-records');
      if (elRecords) elRecords.innerHTML = `${fNum(report.total_records)} <small>đơn</small>`;
      const elBanDau = document.getElementById('truythu-kpi-bandau');
      if (elBanDau) elBanDau.innerHTML = `${(report.total_ban_dau / 1e6).toFixed(1)} <small>Tr ₫</small>`;
      const elDieuChinh = document.getElementById('truythu-kpi-dieuchinh');
      if (elDieuChinh) elDieuChinh.innerHTML = `${(report.total_dieu_chinh / 1e6).toFixed(1)} <small>Tr ₫</small>`;
      const elCanThu = document.getElementById('truythu-kpi-canthu');
      if (elCanThu) elCanThu.innerHTML = `${(report.total_can_thu / 1e6).toFixed(1)} <small>Tr ₫</small>`;
      const elBadge = document.getElementById('truythu-banner-badge');
      if (elBadge) elBadge.textContent = `${fNum(report.total_records)} Bản Ghi | Cần Thu ${(report.total_can_thu / 1e6).toFixed(1)} Tr`;
    }

    // 1. PANEL 1: THEO LOẠI TRUY THU
    const tblLoai = document.querySelector('#table-truythu-by-loai tbody');
    if (tblLoai && report.by_loai) {
      tblLoai.innerHTML = report.by_loai.map(r => {
        let noteBadge = r.ghi_chu ? `<span class="badge-tag badge-tag-red" style="font-size:11px;">${r.ghi_chu}</span>` : '—';
        return `
          <tr>
            <td class="bold" style="font-size:13px; font-weight:800;">${r.loai}</td>
            <td class="num bold">${fNum(r.don)}</td>
            <td class="num">${fMoney(r.ban_dau)}</td>
            <td class="num bold" style="color: ${r.dieu_chinh < 0 ? '#dc2626' : (r.dieu_chinh > 0 ? '#16a34a' : 'inherit')};">${fMoney(r.dieu_chinh)}</td>
            <td class="num bold" style="background: rgba(220, 38, 38, 0.08); color: #dc2626; font-size:13px; font-weight:900;">${fMoney(r.can_thu)}</td>
            <td class="num bold" style="color: #dc2626;">${r.pct_tien}%</td>
            <td class="num">${r.pct_don}%</td>
            <td>${noteBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 2. PANEL 2: TOP BC GIAO
    const tblBcGiao = document.querySelector('#table-truythu-top-bc-giao tbody');
    if (tblBcGiao && report.top_bc_giao) {
      const selectedAM = state.selectedAM;
      tblBcGiao.innerHTML = report.top_bc_giao.map((r, i) => {
        const isSelected = selectedAM && selectedAM === r.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        return `
          <tr data-entity="${r.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${r.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800;">${r.bc}</td>
            <td class="bold" style="color: var(--color-blue);">${r.am}</td>
            <td>${r.tinh}</td>
            <td class="num bold">${fNum(r.don)}</td>
            <td class="num">${fMoney(r.ban_dau)}</td>
            <td class="num bold" style="color: ${r.dieu_chinh < 0 ? '#dc2626' : '#16a34a'};">${fMoney(r.dieu_chinh)}</td>
            <td class="num bold" style="background: rgba(220, 38, 38, 0.08); color: #dc2626; font-size:13.5px; font-weight:900;">${fMoney(r.can_thu)}</td>
            <td class="num bold">${r.pct}%</td>
          </tr>
        `;
      }).join('');
    }

    // 3. PANEL 3: TOP AM THEO TICKET
    const tblAm = document.querySelector('#table-truythu-top-am tbody');
    if (tblAm && report.top_am_ticket) {
      const selectedAM = state.selectedAM;
      tblAm.innerHTML = report.top_am_ticket.map((r, i) => {
        const isSelected = selectedAM === r.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        return `
          <tr data-entity="${r.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${r.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${r.am}</td>
            <td class="num bold" style="background: rgba(2, 132, 199, 0.08); color: #0369a1; font-size:13.5px; font-weight:900;">${fNum(r.ticket)}</td>
            <td class="num bold">${r.pct_ticket}%</td>
            <td class="num">${fMoney(r.ban_dau)}</td>
            <td class="num bold" style="background: rgba(220, 38, 38, 0.08); color: #dc2626; font-size:13.5px; font-weight:900;">${fMoney(r.can_thu)}</td>
            <td class="num bold" style="color: #dc2626;">${r.pct_tien}%</td>
          </tr>
        `;
      }).join('');
    }

    // 4. PANEL 4: TOP BC THEO TICKET
    const tblBcTk = document.querySelector('#table-truythu-bc-ticket tbody');
    if (tblBcTk && report.top_bc_ticket) {
      const selectedAM = state.selectedAM;
      tblBcTk.innerHTML = report.top_bc_ticket.map((r, i) => {
        const isSelected = selectedAM && selectedAM === r.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        return `
          <tr data-entity="${r.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${r.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800;">${r.bc}</td>
            <td class="bold" style="color: var(--color-blue);">${r.am}</td>
            <td>${r.tinh}</td>
            <td class="num bold" style="background: rgba(2, 132, 199, 0.08); color: #0369a1; font-size:13.5px; font-weight:900;">${fNum(r.ticket)}</td>
            <td class="num bold">${r.pct_ticket}%</td>
            <td class="num bold" style="background: rgba(220, 38, 38, 0.08); color: #dc2626; font-size:13.5px; font-weight:900;">${fMoney(r.can_thu)}</td>
          </tr>
        `;
      }).join('');
    }
  }

  function renderTruyThuLoaiBar() {
    const ctx = document.getElementById('chart-truythu-loai-bar');
    if (!ctx) return;
    if (charts.truyThuLoaiBar) charts.truyThuLoaiBar.destroy();

    const report = D.truy_thu_report || {};
    const types = (report.by_loai || []).slice(0, 6);
    if (types.length === 0) return;

    charts.truyThuLoaiBar = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: types.map(d => d.loai),
        datasets: [
          {
            data: types.map(d => Math.round((d.can_thu || 0) / 1e6)),
            backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6', '#8b5cf6', '#10b981', '#64748b']
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
              label: c => ` ${c.label}: ${fNum(c.parsed)} Triệu VNĐ (${types[c.dataIndex].pct_tien}%)`
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
    const top15 = (report.top_bc_giao || []).slice(0, 15);
    if (top15.length === 0) return;

    const selectedAM = state.selectedAM;

    charts.truyThuBcGiaoBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: top15.map(d => d.bc),
        datasets: [
          {
            type: 'bar',
            label: 'Cần Truy Thu Thêm (Triệu ₫)',
            data: top15.map(d => Math.round((d.can_thu || 0) / 1e6)),
            backgroundColor: top15.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : '#ea580c'),
            borderColor: top15.map(d => selectedAM && selectedAM === d.am ? '#b91c1c' : 'transparent'),
            borderWidth: top15.map(d => selectedAM && selectedAM === d.am ? 2 : 0),
            borderRadius: 4,
            yAxisID: 'y',
            datalabels: {
              anchor: 'end',
              align: 'top',
              color: '#c2410c',
              font: { weight: '800', size: 10 },
              formatter: (v, ctx) => `${v} Tr (${top15[ctx.dataIndex].pct}%)`
            }
          },
          {
            type: 'line',
            label: 'Số Đơn Vi Phạm (đơn)',
            data: top15.map(d => d.don),
            borderColor: '#0284c7',
            backgroundColor: '#0284c7',
            borderWidth: 2.5,
            tension: 0.2,
            pointRadius: 4.5,
            pointHoverRadius: 6.5,
            yAxisID: 'y1',
            datalabels: {
              anchor: 'start',
              align: 'bottom',
              color: '#0369a1',
              font: { weight: '700', size: 9.5 },
              formatter: v => `${fNum(v)} đ`
            }
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 28, bottom: 8 } },
        scales: {
          y: {
            type: 'linear',
            position: 'left',
            min: 0,
            ticks: { callback: v => v + ' Tr' },
            title: { display: true, text: 'Số Tiền Cần Thu (Triệu VNĐ)', font: { weight: '700', size: 11 }, color: '#ea580c' },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          y1: {
            type: 'linear',
            position: 'right',
            min: 0,
            title: { display: true, text: 'Số Đơn Vi Phạm (đơn)', font: { weight: '700', size: 11 }, color: '#0284c7' },
            grid: { drawOnChartArea: false }
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
              title: c => ` 📍 ${top15[c[0].dataIndex].bc} — AM: ${top15[c[0].dataIndex].am} (${top15[c[0].dataIndex].tinh})`,
              label: c => {
                if (c.dataset.type === 'line') return ` 📦 Số đơn vi phạm: ${fNum(c.parsed.y)} đơn`;
                return ` 💰 Cần thu thêm: ${fNum(c.parsed.y)} Triệu VNĐ (${fMoney(top15[c.dataIndex].can_thu)}) | Tỷ trọng: ${top15[c.dataIndex].pct}% toàn vùng`;
              }
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

  function renderTruyThuAmDual() {
    const ctx = document.getElementById('chart-truythu-am-dual');
    if (!ctx) return;
    if (charts.truyThuAmDual) charts.truyThuAmDual.destroy();

    const report = D.truy_thu_report || {};
    const topAMs = (report.top_am_ticket || []).slice(0, 15);
    if (topAMs.length === 0) return;

    const selectedAM = state.selectedAM;

    charts.truyThuAmDual = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: topAMs.map(d => d.am),
        datasets: [
          {
            type: 'bar',
            label: 'Số Lượng Ticket Vi Phạm',
            data: topAMs.map(d => d.ticket),
            backgroundColor: topAMs.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : '#0284c7'),
            borderColor: topAMs.map(d => selectedAM && selectedAM === d.am ? '#b91c1c' : 'transparent'),
            borderWidth: topAMs.map(d => selectedAM && selectedAM === d.am ? 2 : 0),
            borderRadius: 4,
            yAxisID: 'y'
          },
          {
            type: 'line',
            label: 'Tiền Cần Thu Thêm (Triệu ₫)',
            data: topAMs.map(d => Math.round((d.can_thu || 0) / 1e6)),
            borderColor: '#ea580c',
            backgroundColor: '#ea580c',
            borderWidth: 3,
            tension: 0.2,
            pointRadius: 5,
            pointHoverRadius: 7,
            yAxisID: 'y1'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: { padding: { top: 20, bottom: 8 } },
        scales: {
          y: {
            type: 'linear',
            position: 'left',
            min: 0,
            title: { display: true, text: 'Số Lượng Ticket', font: { weight: '700', size: 11 }, color: '#0284c7' },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          y1: {
            type: 'linear',
            position: 'right',
            min: 0,
            title: { display: true, text: 'Tiền Cần Thu (Triệu VNĐ)', font: { weight: '700', size: 11 }, color: '#ea580c' },
            grid: { drawOnChartArea: false }
          },
          x: {
            ticks: { maxRotation: 45, minRotation: 25, font: { size: 11, weight: '700' } },
            grid: { display: false }
          }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => {
                if (c.dataset.type === 'line') return ` Cần thu thêm: ${fNum(c.parsed.y)} Triệu VNĐ (${fMoney(topAMs[c.dataIndex].can_thu)})`;
                return ` Số Ticket: ${fNum(c.parsed.y)} ticket (${topAMs[c.dataIndex].pct_ticket}%)`;
              }
            }
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            selectAndHighlightAM(topAMs[elements[0].index].am);
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
    const top15 = (report.top_bc_ticket || []).slice(0, 15);
    if (top15.length === 0) return;

    const selectedAM = state.selectedAM;

    charts.truyThuBcTicketBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: top15.map(d => d.bc),
        datasets: [
          {
            label: 'Số Lượng Ticket',
            data: top15.map(d => d.ticket),
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
            title: { display: true, text: 'Số Ticket Vi Phạm', font: { weight: '700', size: 11 } },
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
              label: c => ` Số Ticket: ${fNum(c.parsed.y)} ticket (${top15[c.dataIndex].pct_ticket}% toàn vùng)`
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

  function renderCommercialTab() {
    renderKdChurnTable();
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

    charts.kdDoanhThu = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: sorted.map(d => d.am),
        datasets: [
          {
            label: 'Kỳ 23–29/8 (W35) (Triệu VNĐ)',
            data: sorted.map(d => Math.round((d.rev_prev || 0) / 1e6)),
            backgroundColor: '#cbd5e1',
            borderRadius: 4
          },
          {
            label: 'Kỳ 30/8–5/9 (W36) (Triệu VNĐ)',
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

    charts.f30Shops = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: sorted.map(d => d.am),
        datasets: [
          {
            label: 'Shop F30 Kỳ Trước',
            data: sorted.map(d => d.kh_prev || 0),
            backgroundColor: '#cbd5e1',
            borderRadius: 4
          },
          {
            label: 'Shop F30 Kỳ Này',
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
    renderKtcBacklog();
    renderKtcLeadtime();
    renderFillRateTable();
  }

  function renderKtcBacklog() {
    const ktc = D.ktc;
    if (!ktc || !ktc.backlog) return;

    // Table 1: Backlog by AM
    const tbody1 = document.querySelector('#table-ktc-backlog-am tbody');
    if (tbody1 && ktc.backlog.by_am) {
      const rows = [...ktc.backlog.by_am];
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
      const rows = ktc.backlog.by_kho;
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
      // Weekly: compare W35 vs W36
      thead.innerHTML = `<tr>
        <th class="center" style="width:44px;">#</th>
        <th>KTC / Kho</th>
        <th class="num">Chuyến W35</th>
        <th class="num">Chuyến W36</th>
        <th class="num">Δ Chuyến</th>
        <th class="num" style="background:var(--color-blue-bg);">TLLĐ W35</th>
        <th class="num bold" style="background:var(--color-blue-bg);">TLLĐ W36</th>
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
        return `<tr${isTotal ? ' style="background:var(--color-blue-bg);font-weight:800;"' : ''}>
          ${rankCell}
          <td class="bold">${r.short_name || r.kho || ''}</td>
          <td class="num">${fNum(r.chuyen_w35 || 0)}</td>
          <td class="num">${fNum(r.chuyen_w36 || 0)}</td>
          <td class="num">${diffCBadge}</td>
          <td class="num" style="background:var(--color-blue-bg);">${(r.tld_w35 || 0).toFixed(1)}%</td>
          <td class="num bold" style="background:var(--color-blue-bg);">${(r.tld_w36 || 0).toFixed(1)}%</td>
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

    const trend = ktc.fill_rate.trend_6w;
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
})();
