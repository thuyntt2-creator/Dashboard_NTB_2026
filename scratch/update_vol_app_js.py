import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

new_vol_code = """  // --------------------------------------------------------------------------
  // TAB 2: SẢN LƯỢNG GIAO (FULL HÀNG & PHÂN KHÚC TTS)
  // --------------------------------------------------------------------------
  function renderVolumeTab() {
    if (!D.san_luong) return;

    // 1. BẢNG 1: SẢN LƯỢNG FULL HÀNG
    const tblBodyFull = document.querySelector('#table-vol-full-detailed tbody');
    if (tblBodyFull && D.san_luong.am_full) {
      let list = [...D.san_luong.am_full].map(r => ({
        ...r,
        diff_val: r.diff !== undefined ? r.diff : ((r.w35 || 0) - (r.w34 || 0))
      }));

      if (state.searchVolFull) {
        list = list.filter(r => r.am.toLowerCase().includes(state.searchVolFull));
      }

      const sorted = list.sort((a, b) => b.diff_val - a.diff_val);

      tblBodyFull.innerHTML = sorted.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const diffBadge = renderDeltaBadge(row.diff_val, false, true);
        const evalBadge = row.diff_val > 0
          ? '<span class="badge-tag badge-tag-green">🟢 Tăng Trưởng</span>'
          : '<span class="badge-tag badge-tag-blue">Ổn Định</span>';

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.w34)}</td>
            <td class="num bold" style="background: var(--color-blue-bg); font-weight:800;">${fNum(row.w35)}</td>
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
      (D.san_luong.am_full || []).forEach(f => fullMap[f.am] = (f.w35 || 0));

      let listTTS = [...D.san_luong.am_tts].map(r => {
        const fullVol = fullMap[r.am] || 0;
        const rate = fullVol > 0 ? ((r.w35 || 0) / fullVol) : 0;
        return {
          ...r,
          rate_tts: rate,
          diff_val: r.diff !== undefined ? r.diff : ((r.w35 || 0) - (r.w34 || 0))
        };
      });

      if (state.searchVolTTS) {
        listTTS = listTTS.filter(r => r.am.toLowerCase().includes(state.searchVolTTS));
      }

      const sortedTTS = listTTS.sort((a, b) => b.diff_val - a.diff_val);

      tblBodyTTS.innerHTML = sortedTTS.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const diffBadge = renderDeltaBadge(row.diff_val, false, true);
        const evalBadge = row.diff_val > 0
          ? '<span class="badge-tag badge-tag-green">🟢 Tăng Trưởng</span>'
          : '<span class="badge-tag badge-tag-amber">Ổn Định</span>';

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.w34)}</td>
            <td class="num bold" style="background: var(--color-amber-bg); color:#ea580c; font-weight:800;">${fNum(row.w35)}</td>
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

    const mode = state.volChartMode || 'w34_vs_w35_full';
    const selectedAM = state.selectedAM;

    const amFullList = D.san_luong.am_full || [];
    const amTtsList = D.san_luong.am_tts || [];

    const fullMap = {};
    amFullList.forEach(f => fullMap[f.am] = f);

    const ttsMap = {};
    amTtsList.forEach(t => ttsMap[t.am] = t);

    // Combine by AM list
    let list = amFullList.map(r => {
      const tts = ttsMap[r.am] || {};
      return {
        am: r.am,
        vol_full_w34: r.w34 || 0,
        vol_full_w35: r.w35 || 0,
        diff_full: r.diff !== undefined ? r.diff : ((r.w35 || 0) - (r.w34 || 0)),
        vol_tts_w34: tts.w34 || 0,
        vol_tts_w35: tts.w35 || 0,
        diff_tts: tts.diff !== undefined ? tts.diff : ((tts.w35 || 0) - (tts.w34 || 0))
      };
    });

    let sortedList = [];
    let datasets = [];
    let title = '';

    if (mode === 'w34_vs_w35_full') {
      title = 'SẢN LƯỢNG FULL HÀNG (2 CỘT: W34 vs W35) — SORT THEO BIẾN ĐỘNG (Δ)';
      sortedList = [...list].sort((a, b) => b.diff_full - a.diff_full);

      datasets = [
        {
          label: 'Full Hàng W34 (Tuần Trước)',
          data: sortedList.map(d => d.vol_full_w34),
          backgroundColor: '#94a3b8',
          borderRadius: 4
        },
        {
          label: 'Full Hàng W35 (Hiện Tại)',
          data: sortedList.map(d => d.vol_full_w35),
          backgroundColor: sortedList.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : (d.diff_full > 0 ? '#10b981' : '#2563eb')),
          borderColor: sortedList.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : 'transparent'),
          borderWidth: sortedList.map(d => selectedAM && selectedAM === d.am ? 3 : 0),
          borderRadius: 4
        }
      ];
    }
    else if (mode === 'w34_vs_w35_tts') {
      title = 'SẢN LƯỢNG TIKTOK SHOP (2 CỘT: W34 vs W35) — SORT THEO SẢN LƯỢNG TTS';
      sortedList = [...list].sort((a, b) => b.vol_tts_w35 - a.vol_tts_w35);

      datasets = [
        {
          label: 'TTS W34 (Tuần Trước)',
          data: sortedList.map(d => d.vol_tts_w34),
          backgroundColor: '#cbd5e1',
          borderRadius: 4
        },
        {
          label: 'TTS W35 (Hiện Tại)',
          data: sortedList.map(d => d.vol_tts_w35),
          backgroundColor: sortedList.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : '#f97316'),
          borderColor: sortedList.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : 'transparent'),
          borderWidth: sortedList.map(d => selectedAM && selectedAM === d.am ? 3 : 0),
          borderRadius: 4
        }
      ];
    }
    else if (mode === 'full_vs_tts') {
      title = 'SẢN LƯỢNG GIAO (FULL HÀNG vs TIKTOK SHOP) THEO 18 AM — W35';
      sortedList = [...list].sort((a, b) => b.vol_full_w35 - a.vol_full_w35);

      datasets = [
        {
          label: 'Full Hàng W35',
          data: sortedList.map(d => d.vol_full_w35),
          backgroundColor: '#2563eb',
          borderRadius: 4
        },
        {
          label: 'Phân Khúc TTS W35',
          data: sortedList.map(d => d.vol_tts_w35),
          backgroundColor: '#f97316',
          borderRadius: 4
        }
      ];
    }

    const titleEl = document.getElementById('vol-chart-title');
    if (titleEl) titleEl.textContent = title;

    charts.volAM = new Chart(ctx, {
      type: 'bar',
      data: { labels: sortedList.map(d => d.am), datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            ticks: { callback: v => v >= 1000 ? (v / 1000).toFixed(0) + 'k' : v.toLocaleString() },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          x: {
            ticks: { maxRotation: 45, minRotation: 30, font: { size: 11, weight: '600' } }
          }
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
            selectAndHighlightAM(sortedList[elements[0].index].am);
          }
        }
      }
    });
  }"""

p1 = code.find('function renderVolumeTab()')
p2 = code.find('window.setGtcTongSegment = function')
if p2 == -1:
    p2 = code.find('function renderGtcTongTab()')

if p1 != -1 and p2 != -1:
    code = code[:p1] + new_vol_code + '\n\n  ' + code[p2:]

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated app.js volume rendering successfully!")
