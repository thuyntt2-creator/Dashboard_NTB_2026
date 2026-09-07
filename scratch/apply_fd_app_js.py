import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update renderRotLcTab() to include row.am
old_tbl_bc_row = '''          <tr data-entity="${row.bc}">
            <td class="center bold">${row.stt || (i + 1)}</td>
            <td class="bold" style="font-weight:800; font-size:13px;">${row.bc}</td>
            <td class="num">${fNum(row.vol_can_lc || row.can_lc_w35 || row.can_lc)}</td>
            <td class="num bold" style="color:#ef4444;">${fNum(row.vol_rot_lc || row.rot_w35 || row.rot)}</td>
            <td class="num bold ${heatClass}">${fPct(pct, 2)}</td>
            <td class="center">${badge}</td>
          </tr>'''

new_tbl_bc_row = '''          <tr data-entity="${row.bc}">
            <td class="center bold">${row.stt || (i + 1)}</td>
            <td class="bold" style="font-weight:800; font-size:13px;">${row.bc}</td>
            <td class="bold" style="font-size:12.5px; color:${state.selectedAM === row.am ? '#ef4444' : 'inherit'};">${row.am || '---'}</td>
            <td class="num">${fNum(row.vol_can_lc || row.can_lc_w35 || row.can_lc)}</td>
            <td class="num bold" style="color:#ef4444;">${fNum(row.vol_rot_lc || row.rot_w35 || row.rot)}</td>
            <td class="num bold ${heatClass}">${fPct(pct, 2)}</td>
            <td class="center">${badge}</td>
          </tr>'''

if old_tbl_bc_row in js:
    js = js.replace(old_tbl_bc_row, new_tbl_bc_row)
    print("Updated Tab 9 Top BC row renderer with AM column!")

# 2. Add Tab 10 FD variables & functions
fd_functions = '''
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
            <td class="num bold ${heatFull}">${fPct(row.rate_full)}</td>
            <td class="num bold">${diffBadgeFull}</td>
            <td class="num">${fNum(row.vol_tts)}</td>
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
            order: 3
          },
          {
            type: 'bar',
            label: mode === 'tts' ? '%FD Return TikTok Shop (%)' : '%FD Return Full Hàng (%)',
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
            borderColor: '#8b5cf6',
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
'''

if 'function renderFdTab' not in js:
    # Insert before renderAgingTab
    pos = js.find('// TAB 8: AGING')
    if pos == -1:
        pos = js.find('function renderAgingTab')
    assert pos != -1, "Aging anchor not found!"
    js = js[:pos] + fd_functions + '\n  ' + js[pos:]
    print("Added renderFdTab and renderFdChart to app.js!")

# 3. Hook search-fd-am and search-fd-bc input listeners
search_listeners_old = '''    const searchRotBc = document.getElementById('search-rotlc-bc');
    if (searchRotBc) {
      searchRotBc.addEventListener('input', (e) => {
        state.searchRotLc = e.target.value.trim();
        renderRotLcTab();
      });
    }'''

search_listeners_new = '''    const searchRotBc = document.getElementById('search-rotlc-bc');
    if (searchRotBc) {
      searchRotBc.addEventListener('input', (e) => {
        state.searchRotLc = e.target.value.trim();
        renderRotLcTab();
      });
    }

    const searchFdAm = document.getElementById('search-fd-am');
    if (searchFdAm) {
      searchFdAm.addEventListener('input', (e) => {
        state.searchFdAm = e.target.value.trim();
        renderFdTab();
      });
    }

    const searchFdBc = document.getElementById('search-fd-bc');
    if (searchFdBc) {
      searchFdBc.addEventListener('input', (e) => {
        state.searchFdBc = e.target.value.trim();
        renderFdTab();
      });
    }'''

if search_listeners_old in js:
    js = js.replace(search_listeners_old, search_listeners_new)
    print("Added search listeners for search-fd-am and search-fd-bc!")

# 4. Hook renderFdTab into switchTab and initial load
tab_hook_old = '''    if (tabId === 'tab-rot-lc') renderRotLcTab();'''
tab_hook_new = '''    if (tabId === 'tab-rot-lc') renderRotLcTab();
    if (tabId === 'tab-fd') renderFdTab();'''

if tab_hook_old in js:
    js = js.replace(tab_hook_old, tab_hook_new)
    print("Hooked tab-fd into switchTab!")

init_hook_old = '''      renderRotLcTab();'''
init_hook_new = '''      renderRotLcTab();
      renderFdTab();'''

if init_hook_old in js:
    js = js.replace(init_hook_old, init_hook_new)
    print("Hooked renderFdTab into initial page load!")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("app.js updated successfully with full FD support!")
