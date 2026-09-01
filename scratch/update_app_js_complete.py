import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

# 1. New renderGanTab & renderGanBarChart
new_gan_code = """  // --------------------------------------------------------------------------
  // TAB 5: % GÁN VẬN HÀNH (CA 1, CA 2 & GÁN TỔNG)
  // --------------------------------------------------------------------------
  function renderGanTab() {
    if (!D.gan || !D.gan.am) return;

    // 1. BẢNG 1: GÁN CA 1+TỒN
    const tblBodyCa1 = document.querySelector('#table-gan-ca1-detailed tbody');
    if (tblBodyCa1) {
      let listCa1 = [...D.gan.am].map(r => ({
        ...r,
        diff_val: r.ca1ton_diff !== undefined ? r.ca1ton_diff : ((r.ca1ton_w35 || 0) - (r.ca1ton_w34 || 0))
      })).sort((a, b) => (b.ca1ton_w35 || 0) - (a.ca1ton_w35 || 0));

      tblBodyCa1.innerHTML = listCa1.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const heatW35 = getHeatmapClass(row.ca1ton_w35, 'gan');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = (row.ca1ton_w35 || 0) >= 0.90
          ? '<span class="badge-tag badge-tag-green">🟢 Đạt Chuẩn (≥90%)</span>'
          : '<span class="badge-tag badge-tag-amber">🟡 Cần Tăng Tốc (&lt;90%)</span>';

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.ca1ton_w34)}</td>
            <td class="num bold ${heatW35}">${fPct(row.ca1ton_w35)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 2. BẢNG 2: GÁN CA 2 & GÁN TỔNG
    const tblBodyCa2 = document.querySelector('#table-gan-ca2-detailed tbody');
    if (tblBodyCa2) {
      let listCa2 = [...D.gan.am].map(r => ({
        ...r,
        diff_val: r.tong_diff !== undefined ? r.tong_diff : ((r.tong_w35 || 0) - (r.tong_w34 || 0))
      })).sort((a, b) => (b.tong_w35 || 0) - (a.tong_w35 || 0));

      tblBodyCa2.innerHTML = listCa2.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const heatTong = getHeatmapClass(row.tong_w35, 'gan');
        const heatCa2 = getHeatmapClass(row.ca2_w35, 'gan');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = (row.tong_w35 || 0) >= 0.90
          ? '<span class="badge-tag badge-tag-green">🏆 Đạt Target (≥90%)</span>'
          : ((row.tong_w35 || 0) >= 0.80 ? '<span class="badge-tag badge-tag-amber">🟡 Cảnh Báo (80-90%)</span>' : '<span class="badge-tag badge-tag-red">🔴 Thấp (&lt;80%)</span>');

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num ${heatCa2}">${fPct(row.ca2_w35)}</td>
            <td class="num">${fPct(row.tong_w34)}</td>
            <td class="num bold ${heatTong}" style="font-weight:800;">${fPct(row.tong_w35)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }
  }

  function renderGanBarChart() {
    const ctx = document.getElementById('chart-gan-am-bar');
    if (!ctx || !D.gan || !D.gan.am) return;
    if (charts.ganBar) charts.ganBar.destroy();

    const selectedAM = state.selectedAM;
    const sorted = [...D.gan.am].map(r => ({
      ...r,
      ca1_pct: Number(((r.ca1ton_w35 || 0) * 100).toFixed(1)),
      ca2_pct: Number(((r.ca2_w35 || 0) * 100).toFixed(1)),
      tong_pct: Number(((r.tong_w35 || 0) * 100).toFixed(1))
    })).sort((a, b) => b.tong_pct - a.tong_pct);

    charts.ganBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: sorted.map(d => d.am),
        datasets: [
          {
            label: '% Gán Ca 1 + Tồn (W35)',
            data: sorted.map(d => d.ca1_pct),
            backgroundColor: '#c084fc',
            borderRadius: 4
          },
          {
            label: '% Gán Ca 2 (W35)',
            data: sorted.map(d => d.ca2_pct),
            backgroundColor: '#9333ea',
            borderRadius: 4
          },
          {
            label: '% Gán Tổng W35 (Target ≥90%)',
            data: sorted.map(d => d.tong_pct),
            backgroundColor: sorted.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : (d.tong_pct >= 90 ? '#10b981' : '#f59e0b')),
            borderColor: sorted.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : 'transparent'),
            borderWidth: sorted.map(d => selectedAM && selectedAM === d.am ? 3 : 0),
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            min: 0,
            max: 105,
            ticks: { callback: v => v + '%' },
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
  }"""

# 2. New renderOdrTab & renderOdrChart
new_odr_code = """  // --------------------------------------------------------------------------
  // TAB 6: %ODR - GIAO ĐÚNG HẸN
  // --------------------------------------------------------------------------
  function renderOdrTab() {
    if (!D.odr) return;

    // 1. BẢNG 1: 18 AM
    const tblBodyAM = document.querySelector('#table-odr-detailed tbody');
    if (tblBodyAM && D.odr.am) {
      let list = [...D.odr.am].map(r => ({
        ...r,
        diff_val: r.diff !== undefined ? r.diff : ((r.w35 || 0) - (r.w34 || 0))
      })).sort((a, b) => b.diff_val - a.diff_val);

      tblBodyAM.innerHTML = list.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const heatW35 = getHeatmapClass(row.w35, 'odr');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = (row.w35 || 0) >= 0.92
          ? '<span class="badge-tag badge-tag-green">🟢 Đạt Chuẩn SLA (≥92%)</span>'
          : '<span class="badge-tag badge-tag-red">🔴 Chưa Đạt (&lt;92%)</span>';

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.w32)}</td>
            <td class="num">${fPct(row.w33)}</td>
            <td class="num">${fPct(row.w34)}</td>
            <td class="num bold ${heatW35}">${fPct(row.w35)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 2. BẢNG 2: 5 TỈNH THÀNH
    const tblBodyTinh = document.querySelector('#table-odr-tinh-detailed tbody');
    if (tblBodyTinh && D.odr.tinh) {
      let listTinh = [...D.odr.tinh].map(r => ({
        ...r,
        diff_val: r.diff !== undefined ? r.diff : ((r.w35 || 0) - (r.w34 || 0))
      })).sort((a, b) => (b.w35 || 0) - (a.w35 || 0));

      tblBodyTinh.innerHTML = listTinh.map((row, i) => {
        const heatW35 = getHeatmapClass(row.w35, 'odr');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = (row.w35 || 0) >= 0.92
          ? '<span class="badge-tag badge-tag-green">🟢 Đạt Chuẩn SLA (≥92%)</span>'
          : '<span class="badge-tag badge-tag-red">🔴 Cần Thúc Đẩy (&lt;92%)</span>';

        return `
          <tr>
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800;">${row.tinh}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.w32)}</td>
            <td class="num">${fPct(row.w33)}</td>
            <td class="num">${fPct(row.w34)}</td>
            <td class="num bold ${heatW35}">${fPct(row.w35)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }
  }

  function renderOdrChart() {
    const ctx = document.getElementById('chart-odr-bar');
    if (!ctx || !D.odr || !D.odr.am) return;
    if (charts.odrBar) charts.odrBar.destroy();

    const selectedAM = state.selectedAM;
    const sorted = [...D.odr.am].map(r => ({
      ...r,
      pct: Number(((r.w35 || 0) * 100).toFixed(1)),
      diff_pct: Number((((r.w35 || 0) - (r.w34 || 0)) * 100).toFixed(1))
    })).sort((a, b) => b.pct - a.pct);

    charts.odrBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: sorted.map(d => d.am),
        datasets: [{
          label: '%ODR W35 (Target ≥92%)',
          data: sorted.map(d => d.pct),
          backgroundColor: sorted.map(d => selectedAM ? (selectedAM === d.am ? '#ef4444' : 'rgba(148, 163, 184, 0.22)') : (d.pct >= 92.0 ? '#10b981' : '#ef4444')),
          borderColor: sorted.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : 'transparent'),
          borderWidth: sorted.map(d => selectedAM && selectedAM === d.am ? 3 : 0),
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { min: 50, max: 100, ticks: { callback: v => v + '%' }, grid: { color: 'rgba(0,0,0,0.06)' } },
          x: { ticks: { maxRotation: 45, minRotation: 30, font: { size: 11, weight: '600' } } }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => `%ODR W35: ${c.parsed.y}% (Sản lượng: ${fNum(sorted[c.dataIndex].vol)} đơn)`
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
  }"""

# 3. New renderLtcTab & renderLtcChart
new_ltc_code = """  // --------------------------------------------------------------------------
  // TAB 7: %LTC - LẤY THÀNH CÔNG
  // --------------------------------------------------------------------------
  function renderLtcTab() {
    if (!D.ltc) return;

    // 1. BẢNG 1: 18 AM
    const tblBodyAM = document.querySelector('#table-ltc-detailed tbody');
    if (tblBodyAM && D.ltc.am) {
      let list = [...D.ltc.am].map(r => ({
        ...r,
        diff_val: r.diff !== undefined ? r.diff : ((r.w35 || 0) - (r.w34 || 0))
      })).sort((a, b) => b.diff_val - a.diff_val);

      tblBodyAM.innerHTML = list.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const heatW35 = getHeatmapClass(row.w35, 'ltc');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = (row.w35 || 0) >= 0.90
          ? '<span class="badge-tag badge-tag-green">🟢 Đạt Chuẩn SLA (≥90%)</span>'
          : '<span class="badge-tag badge-tag-red">🔴 Chưa Đạt (&lt;90%)</span>';

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.w32)}</td>
            <td class="num">${fPct(row.w33)}</td>
            <td class="num">${fPct(row.w34)}</td>
            <td class="num bold ${heatW35}">${fPct(row.w35)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 2. BẢNG 2: 5 TỈNH THÀNH
    const tblBodyTinh = document.querySelector('#table-ltc-tinh-detailed tbody');
    if (tblBodyTinh && D.ltc.tinh) {
      let listTinh = [...D.ltc.tinh].map(r => ({
        ...r,
        diff_val: r.diff !== undefined ? r.diff : ((r.w35 || 0) - (r.w34 || 0))
      })).sort((a, b) => (b.w35 || 0) - (a.w35 || 0));

      tblBodyTinh.innerHTML = listTinh.map((row, i) => {
        const heatW35 = getHeatmapClass(row.w35, 'ltc');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);
        const evalBadge = (row.w35 || 0) >= 0.90
          ? '<span class="badge-tag badge-tag-green">🟢 Đạt Chuẩn SLA (≥90%)</span>'
          : '<span class="badge-tag badge-tag-red">🔴 Cần Thúc Đẩy (&lt;90%)</span>';

        return `
          <tr>
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800;">${row.tinh}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.w32)}</td>
            <td class="num">${fPct(row.w33)}</td>
            <td class="num">${fPct(row.w34)}</td>
            <td class="num bold ${heatW35}">${fPct(row.w35)}</td>
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

    const selectedAM = state.selectedAM;
    const sorted = [...D.ltc.am].map(r => ({
      ...r,
      pct: Number(((r.w35 || 0) * 100).toFixed(1))
    })).sort((a, b) => b.pct - a.pct);

    charts.ltcBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: sorted.map(d => d.am),
        datasets: [{
          label: '%LTC W35 (Target ≥90%)',
          data: sorted.map(d => d.pct),
          backgroundColor: sorted.map(d => selectedAM ? (selectedAM === d.am ? '#ef4444' : 'rgba(148, 163, 184, 0.22)') : (d.pct >= 90.0 ? '#2563eb' : '#ef4444')),
          borderColor: sorted.map(d => selectedAM && selectedAM === d.am ? '#ef4444' : 'transparent'),
          borderWidth: sorted.map(d => selectedAM && selectedAM === d.am ? 3 : 0),
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { min: 40, max: 100, ticks: { callback: v => v + '%' }, grid: { color: 'rgba(0,0,0,0.06)' } },
          x: { ticks: { maxRotation: 45, minRotation: 30, font: { size: 11, weight: '600' } } }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => `%LTC W35: ${c.parsed.y}% (Sản lượng: ${fNum(sorted[c.dataIndex].vol)} đơn)`
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
  }"""

# 4. New renderOprTab & renderOprGroupedChart with Background Volume Line
new_opr_code = """  // --------------------------------------------------------------------------
  // TAB 8: %OPR TIKTOK SHOP (NGÀY 9H–19H vs ĐÊM 19H–9H)
  // --------------------------------------------------------------------------
  function renderOprTab() {
    if (!D.opr_tts || !D.opr_tts.am) return;

    // 1. BẢNG 1: CA NGÀY (9h–19h)
    const tblBodyDay = document.querySelector('#table-opr-day-detailed tbody');
    if (tblBodyDay) {
      let listDay = [...D.opr_tts.am].sort((a, b) => (b.diff_day || 0) - (a.diff_day || 0));
      tblBodyDay.innerHTML = listDay.map((row, i) => {
        const heat = getHeatmapClass(row.w35_day, 'opr');
        const diffBadge = renderDeltaBadge(row.diff_day, true, true);
        const evalBadge = (row.w35_day || 0) >= 0.92
          ? '<span class="badge-tag badge-tag-green">🟢 Đạt SLA (≥92%)</span>'
          : '<span class="badge-tag badge-tag-red">🔴 Chưa Đạt (&lt;92%)</span>';

        return `
          <tr data-entity="${row.am}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800;">${row.am}</td>
            <td class="num">${fNum(row.vol_day)}</td>
            <td class="num">${fPct(row.w34_day)}</td>
            <td class="num bold ${heat}">${fPct(row.w35_day)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 2. BẢNG 2: CA ĐÊM (19h–9h)
    const tblBodyNight = document.querySelector('#table-opr-night-detailed tbody');
    if (tblBodyNight) {
      let listNight = [...D.opr_tts.am].sort((a, b) => (b.diff_night || 0) - (a.diff_night || 0));
      tblBodyNight.innerHTML = listNight.map((row, i) => {
        const heat = getHeatmapClass(row.w35_night, 'opr');
        const diffBadge = renderDeltaBadge(row.diff_night, true, true);
        const evalBadge = (row.w35_night || 0) >= 0.88
          ? '<span class="badge-tag badge-tag-green">🟢 Đạt SLA (≥88%)</span>'
          : '<span class="badge-tag badge-tag-amber">🟡 Cần Đẩy Nhanh (&lt;88%)</span>';

        return `
          <tr data-entity="${row.am}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800;">${row.am}</td>
            <td class="num">${fNum(row.vol_night)}</td>
            <td class="num">${fPct(row.w34_night)}</td>
            <td class="num bold ${heat}">${fPct(row.w35_night)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 3. BẢNG TỔNG HỢP OPR TTS
    const tblBodyAll = document.querySelector('#table-opr-tts-data tbody');
    if (tblBodyAll) {
      let list = [...D.opr_tts.am];
      if (state.searchOpr) {
        list = list.filter(r => r.am.toLowerCase().includes(state.searchOpr));
      }
      const sorted = list.sort((a, b) => (b.vol_total || 0) - (a.vol_total || 0));

      tblBodyAll.innerHTML = sorted.map((row, i) => {
        const heatDay = getHeatmapClass(row.w35_day, 'opr');
        const heatNight = getHeatmapClass(row.w35_night, 'opr');
        const diffDay = renderDeltaBadge(row.diff_day, true, true);
        const diffNight = renderDeltaBadge(row.diff_night, true, true);

        return `
          <tr data-entity="${row.am}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center bold">${i + 1}</td>
            <td class="bold" style="font-weight:800;">${row.am}</td>
            <td class="num">${fNum(row.vol_day)}</td>
            <td class="num">${fPct(row.w34_day)}</td>
            <td class="num bold ${heatDay}">${fPct(row.w35_day)}</td>
            <td class="num bold">${diffDay}</td>
            <td class="num">${fNum(row.vol_night)}</td>
            <td class="num">${fPct(row.w34_night)}</td>
            <td class="num bold ${heatNight}">${fPct(row.w35_night)}</td>
            <td class="num bold">${diffNight}</td>
            <td class="num bold" style="font-weight:800; background: var(--bg-surface-alt);">${fNum(row.vol_total)}</td>
          </tr>
        `;
      }).join('');
    }
  }

  function renderOprGroupedChart() {
    const ctx = document.getElementById('chart-opr-tts-grouped');
    if (!ctx || !D.opr_tts || !D.opr_tts.am) return;
    if (charts.oprGrouped) charts.oprGrouped.destroy();

    const ams = [...D.opr_tts.am].sort((a, b) => (b.vol_total || 0) - (a.vol_total || 0));

    charts.oprGrouped = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ams.map(d => d.am),
        datasets: [
          {
            type: 'line',
            label: 'Sản Lượng Đơn TTS (Đường mờ phía sau)',
            data: ams.map(d => d.vol_total || 0),
            yAxisID: 'y1',
            borderColor: 'rgba(168, 85, 247, 0.45)',
            backgroundColor: 'rgba(168, 85, 247, 0.08)',
            borderWidth: 2,
            borderDash: [5, 5],
            fill: true,
            tension: 0.35,
            pointRadius: 4,
            pointBackgroundColor: 'rgba(168, 85, 247, 0.7)',
            order: 1
          },
          {
            type: 'bar',
            label: '%OPR Ngày (9h–19h) W35',
            data: ams.map(d => Number(((d.w35_day || 0) * 100).toFixed(1))),
            yAxisID: 'y',
            backgroundColor: '#2563eb',
            borderRadius: 4,
            order: 2
          },
          {
            type: 'bar',
            label: '%OPR Đêm (19h–9h) W35',
            data: ams.map(d => Number(((d.w35_night || 0) * 100).toFixed(1))),
            yAxisID: 'y',
            backgroundColor: '#f59e0b',
            borderRadius: 4,
            order: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            type: 'linear',
            position: 'left',
            min: 0,
            max: 105,
            ticks: { callback: v => v + '%' },
            title: { display: true, text: 'Tỷ Lệ %OPR Đúng Hạn' },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          y1: {
            type: 'linear',
            position: 'right',
            grid: { display: false },
            ticks: { callback: v => v.toLocaleString('vi-VN') + ' đơn' },
            title: { display: true, text: 'Sản Lượng TTS (đơn)' }
          },
          x: {
            ticks: { maxRotation: 45, minRotation: 30, font: { size: 11, weight: '600' } }
          }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => {
                if (c.dataset.yAxisID === 'y1') {
                  return `${c.dataset.label}: ${c.parsed.y.toLocaleString('vi-VN')} đơn`;
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
  }"""

# 5. New renderTransportTab & renderRotLcChart
new_transport_code = """  // --------------------------------------------------------------------------
  // TAB 9: RỚT LUÂN CHUYỂN
  // --------------------------------------------------------------------------
  function renderTransportTab() {
    if (!D.rot_lc) return;

    // 1. BẢNG 1: 18 AM
    const tblBodyAM = document.querySelector('#table-rot-am-detailed tbody');
    if (tblBodyAM && D.rot_lc.am) {
      let listAM = [...D.rot_lc.am].map(r => ({
        ...r,
        diff_val: r.diff !== undefined ? r.diff : ((r.w35 || 0) - (r.w34 || 0))
      })).sort((a, b) => (b.w35 || 0) - (a.w35 || 0));

      tblBodyAM.innerHTML = listAM.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const heatW35 = getHeatmapClass(row.w35, 'rot_lc');
        const diffBadge = renderDeltaBadge(row.diff_val, false, true);
        let evalBadge = '<span class="badge-tag badge-tag-green">🟢 Tốt (≤1%)</span>';
        if ((row.w35 || 0) > 0.05) evalBadge = '<span class="badge-tag badge-tag-red">🔴 Nghiêm Trọng (&gt;5%)</span>';
        else if ((row.w35 || 0) > 0.02) evalBadge = '<span class="badge-tag badge-tag-amber">🟡 Cảnh Báo (2-5%)</span>';

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800; color:${isSelected ? '#ef4444' : 'inherit'};">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.w34, 2)}</td>
            <td class="num bold ${heatW35}">${fPct(row.w35, 2)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalBadge}</td>
          </tr>
        `;
      }).join('');
    }

    // 2. BẢNG 2: 5 TỈNH THÀNH
    const tblBodyTinh = document.querySelector('#table-rot-tinh-detailed tbody');
    if (tblBodyTinh && D.rot_lc.tinh) {
      let listTinh = [...D.rot_lc.tinh].map(r => ({
        ...r,
        diff_val: r.diff !== undefined ? r.diff : ((r.w35 || 0) - (r.w34 || 0))
      })).sort((a, b) => (b.w35 || 0) - (a.w35 || 0));

      tblBodyTinh.innerHTML = listTinh.map((row, i) => {
        const heatW35 = getHeatmapClass(row.w35, 'rot_lc');
        const diffBadge = renderDeltaBadge(row.diff_val, false, true);
        let evalBadge = '<span class="badge-tag badge-tag-green">🟢 Tốt (≤1%)</span>';
        if ((row.w35 || 0) > 0.05) evalBadge = '<span class="badge-tag badge-tag-red">🔴 Nghiêm Trọng (&gt;5%)</span>';
        else if ((row.w35 || 0) > 0.02) evalBadge = '<span class="badge-tag badge-tag-amber">🟡 Cảnh Báo (2-5%)</span>';

        return `
          <tr>
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; font-weight:800;">${row.tinh}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.w34, 2)}</td>
            <td class="num bold ${heatW35}">${fPct(row.w35, 2)}</td>
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

    const sorted = [...D.rot_lc.am].map(r => ({
      ...r,
      pct: Number(((r.w35 || 0) * 100).toFixed(2))
    })).sort((a, b) => a.pct - b.pct);

    charts.rotLcBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: sorted.map(d => d.am),
        datasets: [{
          label: '% Rớt LC W35 (Target ≤ 1.0%)',
          data: sorted.map(d => d.pct),
          backgroundColor: sorted.map(d => d.pct <= 1.0 ? '#10b981' : (d.pct <= 2.5 ? '#f59e0b' : '#ef4444')),
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { min: 0, ticks: { callback: v => v + '%' }, grid: { color: 'rgba(0,0,0,0.06)' } },
          x: { ticks: { maxRotation: 45, minRotation: 30, font: { size: 11, weight: '600' } } }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => `% Rớt LC W35: ${c.parsed.y}% (Sản lượng cần LC: ${fNum(sorted[c.dataIndex].vol)} đơn)`
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
  }"""

# Replace Gan
p1 = code.find('function renderGanTab()')
p2 = code.find('// --------------------------------------------------------------------------\n  // TAB 6: %ODR')
if p1 != -1 and p2 != -1:
    code = code[:p1] + new_gan_code + '\n\n' + code[p2:]

# Replace ODR
p1 = code.find('function renderOdrTab()')
p2 = code.find('// --------------------------------------------------------------------------\n  // TAB 7: %LTC')
if p1 != -1 and p2 != -1:
    code = code[:p1] + new_odr_code + '\n\n' + code[p2:]

# Replace LTC
p1 = code.find('function renderLtcTab()')
p2 = code.find('// --------------------------------------------------------------------------\n  // TAB 8: %OPR')
if p1 != -1 and p2 != -1:
    code = code[:p1] + new_ltc_code + '\n\n' + code[p2:]

# Replace OPR
p1 = code.find('function renderOprTab()')
p2 = code.find('// --------------------------------------------------------------------------\n  // TAB 9: RỚT')
if p1 != -1 and p2 != -1:
    code = code[:p1] + new_opr_code + '\n\n' + code[p2:]

# Replace Transport / Rot LC
p1 = code.find('function renderTransportTab()')
p2 = code.find('// --------------------------------------------------------------------------\n  // TAB 10: AGING')
if p2 == -1:
    p2 = code.find('function renderAgingTab()')
if p2 == -1:
    p2 = code.find('function renderCommercialTab()')

if p1 != -1 and p2 != -1:
    code = code[:p1] + new_transport_code + '\n\n' + code[p2:]

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated app.js with all tabs and chart volume overlay!")
