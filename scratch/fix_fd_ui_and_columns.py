import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the ugly broken KPI cards in Tab 10
old_kpi_block = '''      <!-- FD KPI Cards Grid -->
      <div class="kpi-grid" style="grid-template-columns: repeat(4, 1fr); margin-bottom: 16px;">
        <div class="kpi-card" style="border-left: 4px solid #2563eb;">
          <div class="kpi-card-header">
            <span class="kpi-card-title">SẢN LƯỢNG GIAO FULL HÀNG</span>
            <div class="kpi-icon" style="background: rgba(37, 99, 235, 0.1); color: #2563eb;">
              <i data-lucide="package"></i>
            </div>
          </div>
          <div class="kpi-card-value" id="kpi-fd-vol-full">304,308 <span class="kpi-unit">đơn</span></div>
          <div class="kpi-card-footer">
            <span class="badge-tag badge-tag-blue">Toàn Mạng W36</span>
            <span style="font-size: 11px; color: var(--text-muted);">84 Bưu Cục Quản Lý</span>
          </div>
        </div>

        <div class="kpi-card" style="border-left: 4px solid #ef4444;">
          <div class="kpi-card-header">
            <span class="kpi-card-title">%FD RETURN FULL HÀNG</span>
            <div class="kpi-icon" style="background: rgba(239, 68, 68, 0.1); color: #ef4444;">
              <i data-lucide="alert-triangle"></i>
            </div>
          </div>
          <div class="kpi-card-value" id="kpi-fd-rate-full" style="color: #ef4444;">7.54%</div>
          <div class="kpi-card-footer">
            <span class="kpi-badge kpi-badge-danger">22,954 đơn return</span>
            <span style="font-size: 11px; color: var(--text-muted);">Mục tiêu ≤ 6.0%</span>
          </div>
        </div>

        <div class="kpi-card" style="border-left: 4px solid #ea580c;">
          <div class="kpi-card-header">
            <span class="kpi-card-title">SẢN LƯỢNG TIKTOK SHOP</span>
            <div class="kpi-icon" style="background: rgba(234, 88, 12, 0.1); color: #ea580c;">
              <i data-lucide="flame"></i>
            </div>
          </div>
          <div class="kpi-card-value" id="kpi-fd-vol-tts">64,220 <span class="kpi-unit">đơn</span></div>
          <div class="kpi-card-footer">
            <span class="badge-tag badge-tag-amber">21.1% Sản Lượng</span>
            <span style="font-size: 11px; color: var(--text-muted);">Phân khúc TTS</span>
          </div>
        </div>

        <div class="kpi-card" style="border-left: 4px solid #8b5cf6;">
          <div class="kpi-card-header">
            <span class="kpi-card-title">%FD RETURN TIKTOK SHOP</span>
            <div class="kpi-icon" style="background: rgba(139, 92, 246, 0.1); color: #8b5cf6;">
              <i data-lucide="repeat"></i>
            </div>
          </div>
          <div class="kpi-card-value" id="kpi-fd-rate-tts" style="color: #8b5cf6;">6.80%</div>
          <div class="kpi-card-footer">
            <span class="badge-tag badge-tag-purple">4,365 đơn return</span>
            <span style="font-size: 11px; color: var(--text-muted);">Chuyển trả TTS</span>
          </div>
        </div>
      </div>'''

new_kpi_block = '''      <!-- FD KPI Cards Strip (Native Polished Tiles) -->
      <div class="kpi-strip" style="grid-template-columns: repeat(4, 1fr); margin-bottom: 20px;">
        <div class="kpi-tile" style="border-left: 4px solid var(--color-blue);">
          <div class="kpi-tile-header">
            <span>Sản Lượng Giao Full Hàng</span>
            <div class="kpi-tile-icon" style="background: rgba(37, 99, 235, 0.12); color: var(--color-blue);">
              <i data-lucide="package" style="width: 16px; height: 16px;"></i>
            </div>
          </div>
          <div class="kpi-tile-value" id="kpi-fd-vol-full">304,308 <small>đơn</small></div>
          <div class="kpi-tile-meta">
            <span class="badge-tag badge-tag-blue">Toàn Mạng W36</span>
            <span style="color: var(--text-muted);">84 Bưu Cục Quản Lý</span>
          </div>
        </div>

        <div class="kpi-tile kpi-red" style="border-left: 4px solid #ef4444;">
          <div class="kpi-tile-header">
            <span>%FD Return Full Hàng</span>
            <div class="kpi-tile-icon" style="background: rgba(239, 68, 68, 0.12); color: #ef4444;">
              <i data-lucide="alert-triangle" style="width: 16px; height: 16px;"></i>
            </div>
          </div>
          <div class="kpi-tile-value" id="kpi-fd-rate-full" style="color: #ef4444;">7.54%</div>
          <div class="kpi-tile-meta">
            <span class="badge-tag badge-tag-red">22,954 đơn return</span>
            <span style="color: var(--text-muted);">Mục tiêu ≤ 6.0%</span>
          </div>
        </div>

        <div class="kpi-tile kpi-amber" style="border-left: 4px solid #ea580c;">
          <div class="kpi-tile-header">
            <span>Sản Lượng TikTok Shop</span>
            <div class="kpi-tile-icon" style="background: rgba(234, 88, 12, 0.12); color: #ea580c;">
              <i data-lucide="flame" style="width: 16px; height: 16px;"></i>
            </div>
          </div>
          <div class="kpi-tile-value" id="kpi-fd-vol-tts">64,220 <small>đơn</small></div>
          <div class="kpi-tile-meta">
            <span class="badge-tag badge-tag-amber">21.1% Sản Lượng</span>
            <span style="color: var(--text-muted);">Phân khúc TTS</span>
          </div>
        </div>

        <div class="kpi-tile kpi-purple" style="border-left: 4px solid #8b5cf6;">
          <div class="kpi-tile-header">
            <span>%FD Return TikTok Shop</span>
            <div class="kpi-tile-icon" style="background: rgba(139, 92, 246, 0.12); color: #8b5cf6;">
              <i data-lucide="repeat" style="width: 16px; height: 16px;"></i>
            </div>
          </div>
          <div class="kpi-tile-value" id="kpi-fd-rate-tts" style="color: #8b5cf6;">6.80%</div>
          <div class="kpi-tile-meta">
            <span class="badge-tag badge-tag-purple">4,365 đơn return</span>
            <span style="color: var(--text-muted);">Hoàn trả TTS</span>
          </div>
        </div>
      </div>'''

assert old_kpi_block in html, "old_kpi_block not found in index.html!"
html = html.replace(old_kpi_block, new_kpi_block)
print("Replaced KPI block with native polished .kpi-strip and .kpi-tile!")

# Update table headers in Bảng 1: Điều hành %FD 18 AM to show W35 and W36
old_table_th = '''                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>AM Phụ Trách</th>
                    <th class="num">Sản Lượng Full</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%FD Full</th>
                    <th class="num">Δ WoW</th>
                    <th class="num">Sản Lượng TTS</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">%FD TTS</th>
                    <th class="num">Δ TTS</th>
                    <th class="num">Tỷ Trọng Return</th>
                    <th class="center">Đánh Giá</th>
                  </tr>'''

new_table_th = '''                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>AM Phụ Trách</th>
                    <th class="num">Vol Full</th>
                    <th class="num">Full W35</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">Full W36</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="num">Vol TTS</th>
                    <th class="num">TTS W35</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight:800; color:#ea580c;">TTS W36</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="num">Tỷ Trọng Return</th>
                    <th class="center">Đánh Giá</th>
                  </tr>'''

assert old_table_th in html, "old_table_th not found in index.html!"
html = html.replace(old_table_th, new_table_th)
print("Updated Bảng 1 headers with explicit Full W35 vs Full W36 and TTS W35 vs TTS W36!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update app.js
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update Bảng 1 row rendering in app.js
old_tbody_map = '''        return `
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
        `;'''

new_tbody_map = '''        return `
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
        `;'''

assert old_tbody_map in js, "old_tbody_map not found in app.js!"
js = js.replace(old_tbody_map, new_tbody_map)
print("Updated Bảng 1 row rendering with Full W35, W36 and TTS W35, W36!")

# Update renderFdChart to show W35 bar vs W36 bar + Area Vol + Line Diff
old_chart_func = '''    charts.fdBar = new Chart(ctx, {
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
      },'''

new_chart_func = '''    const prevData = sorted.map(d => Number(((mode === 'tts' ? d.rate_tts_prev : d.rate_full_prev) * 100).toFixed(2)));

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
      },'''

assert old_chart_func in js, "old_chart_func not found in app.js!"
js = js.replace(old_chart_func, new_chart_func)
print("Updated Chart with both W35 and W36 bars, Area Volume, and Line Diff!")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("All updates applied successfully!")
