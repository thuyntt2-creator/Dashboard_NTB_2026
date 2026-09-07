# -*- coding: utf-8 -*-
"""
Add KTC Tab rendering JavaScript to app.js and update data.js with KTC fill rate data.
"""
import sys, json, os, re
sys.stdout.reconfigure(encoding='utf-8')

# ========================
# 1. Build KTC data.js embed
# ========================
with open('data.js', 'r', encoding='utf-8') as f:
    data_js = f.read()

with open('scratch/ktc_processed.json', 'r', encoding='utf-8') as f:
    ktc_data = json.load(f)

# Check if ktc is already in data.js
if '"ktc"' in data_js:
    print("KTC already in data.js — skipping embed")
else:
    # Insert ktc before the closing of DASHBOARD_DATA
    ktc_json = json.dumps(ktc_data, ensure_ascii=False, separators=(',', ':'))
    # Find the last property before closing brace
    insert_point = data_js.rfind('};')
    if insert_point < 0:
        insert_point = data_js.rfind('}')
    
    # Find last proper field before closing
    data_js = data_js[:insert_point] + ',\n"ktc": ' + ktc_json + '\n' + data_js[insert_point:]
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(data_js)
    print("✅ Added KTC to data.js")

# ========================
# 2. Add KTC rendering to app.js
# ========================
with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# A) Add renderKtcTab() to renderAll()
old_renderall = "    renderFdTab();\n    renderAgingTab();"
new_renderall  = "    renderFdTab();\n    renderKtcTab();\n    renderAgingTab();"
if 'renderKtcTab' not in app_js:
    app_js = app_js.replace(old_renderall, new_renderall, 1)
    print("✅ Added renderKtcTab() to renderAll()")
else:
    print("renderKtcTab already in renderAll")

# B) Add tab-ktc case to renderTabCharts
old_fd_case = "} else if (tabId === 'tab-aging') {\n      renderAgingChart();"
new_fd_case  = "} else if (tabId === 'tab-ktc') {\n      renderKtcTab();\n      renderFillRateChart();\n    } else if (tabId === 'tab-aging') {\n      renderAgingChart();"
if "tab-ktc" not in app_js:
    app_js = app_js.replace(old_fd_case, new_fd_case, 1)
    print("✅ Added tab-ktc to renderTabCharts()")
else:
    print("tab-ktc already in renderTabCharts")

# C) Add the KTC render functions before the closing })();
ktc_js = r"""
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

"""

# Insert before closing of the IIFE
if 'renderKtcTab' not in app_js or 'function renderKtcTab' not in app_js:
    close_marker = "  // Run on load\n  document.addEventListener('DOMContentLoaded', init);\n})();"
    if close_marker in app_js:
        app_js = app_js.replace(close_marker, ktc_js + "\n  // Run on load\n  document.addEventListener('DOMContentLoaded', init);\n})();")
        print("✅ Added KTC rendering functions to app.js")
    else:
        print("❌ Could not find insertion point for KTC JS functions")
else:
    print("KTC render functions already present")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
print("✅ app.js saved")
print("Done!")
