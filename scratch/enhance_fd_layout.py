import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update KPI tiles with explicit W35 vs W36 values
old_kpis = '''      <!-- FD KPI Cards Strip (Native Polished Tiles) -->
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

new_kpis = '''      <!-- FD KPI Cards Strip (Native Polished Tiles) -->
      <div class="kpi-strip" style="grid-template-columns: repeat(4, 1fr); margin-bottom: 20px;">
        <div class="kpi-tile" style="border-left: 4px solid var(--color-blue);">
          <div class="kpi-tile-header">
            <span>Sản Lượng Giao Full Hàng</span>
            <div class="kpi-tile-icon" style="background: rgba(37, 99, 235, 0.12); color: var(--color-blue);">
              <i data-lucide="package" style="width: 16px; height: 16px;"></i>
            </div>
          </div>
          <div class="kpi-tile-value" id="kpi-fd-vol-full">304,308 <small>đơn W36</small></div>
          <div class="kpi-tile-meta">
            <span class="badge-tag badge-tag-blue">Toàn Mạng NTB</span>
            <span style="color: var(--text-muted); font-size: 11.5px;">W35: 318,986 đ (▼ -4.6%)</span>
          </div>
        </div>

        <div class="kpi-tile kpi-red" style="border-left: 4px solid #ef4444;">
          <div class="kpi-tile-header">
            <span>%FD Return Full Hàng (W36 vs W35)</span>
            <div class="kpi-tile-icon" style="background: rgba(239, 68, 68, 0.12); color: #ef4444;">
              <i data-lucide="alert-triangle" style="width: 16px; height: 16px;"></i>
            </div>
          </div>
          <div class="kpi-tile-value" id="kpi-fd-rate-full" style="color: #ef4444;">7.54% <small style="color: var(--text-muted); font-size: 13px; font-weight: 600;">(W35: 7.42%)</small></div>
          <div class="kpi-tile-meta">
            <span class="diff-tag diff-up-bad">▲ +0.12% WoW</span>
            <span style="color: var(--text-muted); font-size: 11.5px;">22,954 đ return (Mục tiêu ≤ 6.0%)</span>
          </div>
        </div>

        <div class="kpi-tile kpi-amber" style="border-left: 4px solid #ea580c;">
          <div class="kpi-tile-header">
            <span>Sản Lượng TikTok Shop (TTS)</span>
            <div class="kpi-tile-icon" style="background: rgba(234, 88, 12, 0.12); color: #ea580c;">
              <i data-lucide="flame" style="width: 16px; height: 16px;"></i>
            </div>
          </div>
          <div class="kpi-tile-value" id="kpi-fd-vol-tts">64,220 <small>đơn W36</small></div>
          <div class="kpi-tile-meta">
            <span class="badge-tag badge-tag-amber">21.1% Sản Lượng</span>
            <span style="color: var(--text-muted); font-size: 11.5px;">W35: 64,311 đ (▼ -0.1%)</span>
          </div>
        </div>

        <div class="kpi-tile kpi-purple" style="border-left: 4px solid #8b5cf6;">
          <div class="kpi-tile-header">
            <span>%FD Return TikTok Shop (W36 vs W35)</span>
            <div class="kpi-tile-icon" style="background: rgba(139, 92, 246, 0.12); color: #8b5cf6;">
              <i data-lucide="repeat" style="width: 16px; height: 16px;"></i>
            </div>
          </div>
          <div class="kpi-tile-value" id="kpi-fd-rate-tts" style="color: #8b5cf6;">6.80% <small style="color: var(--text-muted); font-size: 13px; font-weight: 600;">(W35: 6.72%)</small></div>
          <div class="kpi-tile-meta">
            <span class="diff-tag diff-up-bad">▲ +0.08% WoW</span>
            <span style="color: var(--text-muted); font-size: 11.5px;">4,365 đ return TTS</span>
          </div>
        </div>
      </div>'''

assert old_kpis in html, "old_kpis not found!"
html = html.replace(old_kpis, new_kpis)
print("Updated KPI tiles with explicit W35 vs W36 values!")

# 2. Change layout of Tables: Instead of grid-row-2 which squeezes 12 columns, stack them as full-width cards
old_table_layout = '''      <!-- FD Tables Grid -->
      <div class="grid-row-2">
        <!-- Bảng 1: Bảng 18 AM (Full Hàng vs TTS) -->
        <div class="report-card">'''

new_table_layout = '''      <!-- FD Tables (Stacked Full-Width for Complete High-Definition Clarity) -->
      <!-- Bảng 1: Bảng 18 AM (Full Hàng vs TTS) -->
      <div class="report-card" style="margin-bottom: 20px;">'''

assert old_table_layout in html, "old_table_layout not found!"
html = html.replace(old_table_layout, new_table_layout)

old_table_sep = '''            </div>
          </div>
        </div>

        <!-- Bảng 2: Top Bưu Cục %FD Cao Nhất -->
        <div class="report-card">'''

new_table_sep = '''            </div>
          </div>
        </div>

      <!-- Bảng 2: Top Bưu Cục %FD Cao Nhất -->
      <div class="report-card" style="margin-bottom: 20px;">'''

assert old_table_sep in html, "old_table_sep not found!"
html = html.replace(old_table_sep, new_table_sep)

# Replace closing of grid-row-2
old_closing = '''              </table>
            </div>
          </div>
        </div>
      </div>
    </div>'''

new_closing = '''              </table>
            </div>
          </div>
        </div>
    </div>'''

assert old_closing in html, "old_closing not found!"
html = html.replace(old_closing, new_closing)
print("Updated tables to full-width stacked layout!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html successfully updated!")
