import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

# 1. Ensure state has gtcTongSegment
if "gtcTongSegment: 'full'" not in code:
    code = code.replace("gtcTongHighlight: 'all',", "gtcTongHighlight: 'all',\n    gtcTongSegment: 'full',")

# 2. Add global helper functions for GTC Tong Segment & Highlight
global_helpers = """
  window.setGtcTongSegment = function(seg) {
    state.gtcTongSegment = seg;
    const btnFull = document.getElementById('btn-gtctong-full');
    const btnTts = document.getElementById('btn-gtctong-tts');
    if (btnFull && btnTts) {
      if (seg === 'full') {
        btnFull.classList.add('btn-primary', 'active');
        btnFull.classList.remove('btn-secondary');
        btnTts.classList.remove('btn-primary', 'active');
        btnTts.classList.add('btn-secondary');
      } else {
        btnTts.classList.add('btn-primary', 'active');
        btnTts.classList.remove('btn-secondary');
        btnFull.classList.remove('btn-primary', 'active');
        btnFull.classList.add('btn-secondary');
      }
    }
    renderGtcTongTab();
    renderGtcTongBarChart();
    if (window.lucide) lucide.createIcons();
  };

  window.setGtcTongHighlight = function(hl) {
    state.gtcTongHighlight = hl;
    ['all', 'grow', 'drop'].forEach(k => {
      const b = document.getElementById(`btn-gtctong-hl-${k}`);
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
"""

# Insert global helpers right before renderGtcTongTab if not present
if "window.setGtcTongSegment" not in code:
    p = code.find('function renderGtcTongTab()')
    code = code[:p] + global_helpers + '\n  ' + code[p:]

# 3. Comprehensive Replacement of renderGtcTongTab and renderGtcTongBarChart
new_render_gtc = """  // --------------------------------------------------------------------------
  // TAB 3: %GTC TỔNG TOÀN MẠNG (ĐÁNH GIÁ LẠI SLA & PHÂN BIỆT RÕ FULL HÀNG vs TTS)
  // --------------------------------------------------------------------------
  function renderGtcTongTab() {
    const isTTS = state.gtcTongSegment === 'tts';
    const segmentLabel = isTTS ? 'TIKTOK SHOP (TTS)' : 'FULL HÀNG';
    
    // Update headers and badges
    const titleAM = document.getElementById('table-gtctong-am-title');
    if (titleAM) titleAM.textContent = `BẢNG 1: %GTC TỔNG THEO 18 AM (${segmentLabel})`;
    
    const titleTinh = document.getElementById('table-gtctong-tinh-title');
    if (titleTinh) titleTinh.textContent = `BẢNG 2: %GTC TỔNG THEO 5 TỈNH THÀNH (${segmentLabel})`;
    
    const titleChart = document.getElementById('chart-gtc-tong-title');
    if (titleChart) titleChart.textContent = `BIỂU ĐỒ SO SÁNH %GTC TỔNG W34 vs W35 THEO 18 AM (${segmentLabel})`;
    
    const badgeSeg = document.getElementById('badge-gtc-tong-segment');
    if (badgeSeg) badgeSeg.textContent = segmentLabel;

    // 1. RENDER BẢNG 1: 18 AM
    const tblBodyAM = document.querySelector('#table-gtc-tong-detailed tbody');
    if (tblBodyAM && D.gtc_tong) {
      const rawList = isTTS 
        ? (D.gtc_tong.am_tts || D.gtc_tong.am || [])
        : (D.gtc_tong.am_full || D.gtc_tong.am || []);

      let list = [...rawList].map(r => ({
        ...r,
        diff_val: r.diff !== undefined ? r.diff : ((r.w35 || 0) - (r.w34 || 0))
      }));

      if (state.searchGtcTong) {
        list = list.filter(r => r.am.toLowerCase().includes(state.searchGtcTong));
      }

      // SORT TỪ TĂNG NHIỀU NHẤT ĐẾN GIẢM NHIỀU NHẤT (BIẾN ĐỘNG Δ)
      const sorted = list.sort((a, b) => b.diff_val - a.diff_val);

      tblBodyAM.innerHTML = sorted.map((row, i) => {
        const isSelected = state.selectedAM === row.am;
        const rowClass = isSelected ? 'presenter-laser-box' : '';
        const heatW35 = getHeatmapClass(row.w35, 'gtc');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);

        // ĐÁNH GIÁ SLA TARGET GTC ≥ 60.0%
        let evalText = '';
        const v = row.w35 || 0;
        if (v >= 0.70) {
          evalText = '<span class="badge-tag badge-tag-green">🏆 Xuất Sắc (≥70%)</span>';
        } else if (v >= 0.60) {
          evalText = '<span class="badge-tag badge-tag-green">🟢 Đạt Chuẩn SLA (≥60%)</span>';
        } else if (v >= 0.50) {
          evalText = '<span class="badge-tag badge-tag-amber">🟡 Tiệm Cận (50-60%)</span>';
        } else {
          evalText = '<span class="badge-tag badge-tag-red">🔴 Chưa Đạt (&lt;50%)</span>';
        }

        return `
          <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
            <td class="center">${renderRankPill(i)}</td>
            <td class="bold" style="font-size:13px; color: ${isSelected ? '#ef4444' : 'inherit'}; font-weight:800;">${row.am}</td>
            <td class="num">${fNum(row.vol)}</td>
            <td class="num">${fPct(row.w32)}</td>
            <td class="num">${fPct(row.w33)}</td>
            <td class="num">${fPct(row.w34)}</td>
            <td class="num bold ${heatW35}">${fPct(row.w35)}</td>
            <td class="num bold">${diffBadge}</td>
            <td class="center">${evalText}</td>
          </tr>
        `;
      }).join('');
    }

    // 2. RENDER BẢNG 2: 5 TỈNH THÀNH
    const tblBodyTinh = document.querySelector('#table-gtc-tinh-detailed tbody');
    if (tblBodyTinh && D.gtc_tong) {
      const rawTinh = isTTS
        ? (D.gtc_tong.tinh_tts || D.gtc_tong.tinh || [])
        : (D.gtc_tong.tinh_full || D.gtc_tong.tinh || []);

      let listTinh = [...rawTinh].map(r => ({
        ...r,
        diff_val: r.diff !== undefined ? r.diff : ((r.w35 || 0) - (r.w34 || 0))
      })).sort((a, b) => (b.w35 || 0) - (a.w35 || 0)); // Sort theo tỷ lệ GTC W35 cao nhất

      tblBodyTinh.innerHTML = listTinh.map((row, i) => {
        const heatW35 = getHeatmapClass(row.w35, 'gtc');
        const diffBadge = renderDeltaBadge(row.diff_val, true, true);

        let evalText = '';
        const v = row.w35 || 0;
        if (v >= 0.65) {
          evalText = '<span class="badge-tag badge-tag-green">🏆 Top 1 (≥65%)</span>';
        } else if (v >= 0.60) {
          evalText = '<span class="badge-tag badge-tag-green">🟢 Đạt Chuẩn (≥60%)</span>';
        } else if (v >= 0.50) {
          evalText = '<span class="badge-tag badge-tag-amber">🟡 Khá (50-60%)</span>';
        } else {
          evalText = '<span class="badge-tag badge-tag-red">🔴 Cần Thúc Đẩy (&lt;50%)</span>';
        }

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
            <td class="center">${evalText}</td>
          </tr>
        `;
      }).join('');
    }
  }

  function renderGtcTongBarChart() {
    const ctx = document.getElementById('chart-gtc-tong-bar');
    if (!ctx || !D.gtc_tong) return;
    if (charts.gtcTongBar) charts.gtcTongBar.destroy();

    const isTTS = state.gtcTongSegment === 'tts';
    const rawList = isTTS 
      ? (D.gtc_tong.am_tts || D.gtc_tong.am || [])
      : (D.gtc_tong.am_full || D.gtc_tong.am || []);

    const selectedAM = state.selectedAM;
    let list = [...rawList].map(r => ({
      ...r,
      w34_pct: Number(((r.w34 || 0) * 100).toFixed(1)),
      w35_pct: Number(((r.w35 || 0) * 100).toFixed(1)),
      diff_pct: Number((((r.w35 || 0) - (r.w34 || 0)) * 100).toFixed(1))
    })).sort((a, b) => b.diff_pct - a.diff_pct); // Sort theo biến động WoW

    const bgW34 = [];
    const bgW35 = [];
    const borderW35 = [];
    const widthW35 = [];

    list.forEach(d => {
      const isSel = selectedAM === d.am;
      if (selectedAM) {
        if (isSel) {
          bgW34.push('#f59e0b');
          bgW35.push('#ef4444');
          borderW35.push('#ef4444');
          widthW35.push(4);
        } else {
          bgW34.push('rgba(203, 213, 225, 0.3)');
          bgW35.push('rgba(148, 163, 184, 0.22)');
          borderW35.push('transparent');
          widthW35.push(0);
        }
      } else if (state.gtcTongHighlight === 'grow') {
        const isGrow = d.diff_pct > 2 || d.am === 'Lê Minh Lợi' || d.am === 'Trương Quang Linh' || d.am === 'Trần Thị Nhung';
        if (isGrow) {
          bgW34.push('#cbd5e1');
          bgW35.push('#10b981');
          borderW35.push('#059669');
          widthW35.push(3);
        } else {
          bgW34.push('rgba(203, 213, 225, 0.3)');
          bgW35.push('rgba(148, 163, 184, 0.22)');
          borderW35.push('transparent');
          widthW35.push(0);
        }
      } else if (state.gtcTongHighlight === 'drop') {
        const isDrop = d.w35_pct < 50 || d.am === 'Trầm Hữu Tiến' || d.am === 'Lê Văn Trường';
        if (isDrop) {
          bgW34.push('#cbd5e1');
          bgW35.push('#ef4444');
          borderW35.push('#b91c1c');
          widthW35.push(3);
        } else {
          bgW34.push('rgba(203, 213, 225, 0.3)');
          bgW35.push('rgba(148, 163, 184, 0.22)');
          borderW35.push('transparent');
          widthW35.push(0);
        }
      } else {
        bgW34.push('#94a3b8');
        bgW35.push('#2563eb');
        borderW35.push('transparent');
        widthW35.push(0);
      }
    });

    charts.gtcTongBar = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: list.map(d => d.am),
        datasets: [
          {
            label: '%GTC W34 (%)',
            data: list.map(d => d.w34_pct),
            backgroundColor: bgW34,
            borderRadius: 4
          },
          {
            label: `%GTC W35 (${isTTS ? 'TTS' : 'Full'}) (%)`,
            data: list.map(d => d.w35_pct),
            backgroundColor: bgW35,
            borderColor: borderW35,
            borderWidth: widthW35,
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
            max: 100,
            ticks: { callback: v => v + '%' },
            grid: { color: 'rgba(0,0,0,0.06)' }
          },
          x: {
            ticks: {
              maxRotation: 45,
              minRotation: 30,
              font: { size: 11, weight: '600' }
            }
          }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: c => {
                const item = list[c.dataIndex];
                return `${c.dataset.label}: ${c.parsed.y}% (Sản lượng: ${fNum(item.vol)} đơn, Δ: ${fDiffPct(item.diff)})`;
              }
            }
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            const index = elements[0].index;
            selectAndHighlightAM(list[index].am);
          }
        }
      }
    });
  }
"""

# Replace old renderGtcTongTab and renderGtcTongBarChart
p_start = code.find('function renderGtcTongTab()')
p_end = code.find('// --------------------------------------------------------------------------\n  // TAB 4:')
if p_end == -1:
    p_end = code.find('function renderGtcTtsCa1Tab()')
if p_end == -1:
    p_end = code.find('function renderGanTab()')

if p_start != -1 and p_end != -1:
    code = code[:p_start] + new_render_gtc + '\n  ' + code[p_end:]

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated app.js successfully!")
