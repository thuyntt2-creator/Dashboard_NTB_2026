import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# a. Update nav tabs in index.html: Add tab-fd
nav_old = '''        <button class="tab-item" data-tab="tab-rot-lc">
          <i data-lucide="truck"></i> 9. Rớt Luân Chuyển
        </button>
        <button class="tab-item" data-tab="tab-aging">
          <i data-lucide="clock"></i> 10. Aging Tồn Đọng
        </button>
        <button class="tab-item" data-tab="tab-control">
          <i data-lucide="wallet"></i> 11. COD Tiền Mặt
        </button>
        <button class="tab-item" data-tab="tab-truythu">
          <i data-lucide="file-check"></i> 12. Báo Cáo Truy Thu
        </button>
        <button class="tab-item" data-tab="tab-commercial">
          <i data-lucide="trending-up"></i> 13. Kinh Doanh & F30
        </button>'''

nav_new = '''        <button class="tab-item" data-tab="tab-rot-lc">
          <i data-lucide="truck"></i> 9. Rớt Luân Chuyển
        </button>
        <button class="tab-item" data-tab="tab-fd">
          <i data-lucide="rotate-ccw"></i> 10. %FD Hoàn Trả
        </button>
        <button class="tab-item" data-tab="tab-aging">
          <i data-lucide="clock"></i> 11. Aging Tồn Đọng
        </button>
        <button class="tab-item" data-tab="tab-control">
          <i data-lucide="wallet"></i> 12. COD Tiền Mặt
        </button>
        <button class="tab-item" data-tab="tab-truythu">
          <i data-lucide="file-check"></i> 13. Báo Cáo Truy Thu
        </button>
        <button class="tab-item" data-tab="tab-commercial">
          <i data-lucide="trending-up"></i> 14. Kinh Doanh & F30
        </button>'''

if nav_old in html:
    html = html.replace(nav_old, nav_new)
    print("Updated navigation bar with Tab 10 %FD Hoàn Trả!")

# b. Update Tab 9 table header: Add AM Phụ Trách
tab9_th_old = '''                  <th class="center" style="width: 50px;">#</th>
                  <th>Bưu Cục</th>
                  <th class="num">Vol Cần LC</th>'''

tab9_th_new = '''                  <th class="center" style="width: 50px;">#</th>
                  <th>Bưu Cục</th>
                  <th>AM Phụ Trách</th>
                  <th class="num">Vol Cần LC</th>'''

if tab9_th_old in html:
    html = html.replace(tab9_th_old, tab9_th_new)
    print("Updated Tab 9 header with AM Phụ Trách!")

# c. Add Tab 10 view (#tab-fd) right before #tab-aging
tab_fd_html = '''    <!-- ==================================================================== -->
    <!-- TAB 10: BÁO CÁO %FD (RETURN / HOÀN TRẢ) - FULL HÀNG & TIKTOK SHOP -->
    <!-- ==================================================================== -->
    <div id="tab-fd" class="tab-view">
      <!-- Executive Banner -->
      <div class="exec-banner" style="border-left-color: #8b5cf6;">
        <div class="exec-banner-content">
          <div class="exec-banner-icon" style="background: rgba(139, 92, 246, 0.15); color: #8b5cf6;">
            <i data-lucide="rotate-ccw" style="width: 24px; height: 24px;"></i>
          </div>
          <div class="exec-banner-text">
            <h2 style="margin: 0; font-size: 16px; font-weight: 800; color: var(--text-main);">
              BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) – VÙNG NAM TRUNG BỘ (W36)
            </h2>
            <p style="margin: 4px 0 0; font-size: 12.5px; color: var(--text-muted); line-height: 1.5;">
              Dữ liệu chu kỳ W36 (31/08 – 06/09/2026) | So sánh biến động WoW với tuần trước (W35) | Tách riêng Full Hàng và TikTok Shop
            </p>
          </div>
        </div>
        <div class="exec-banner-meta">
          <span class="badge-tag badge-tag-purple" style="font-weight: 800;">Target Toàn Vùng ≤ 6.0%</span>
          <span class="badge-tag badge-tag-blue">84 Bưu Cục / 18 AM</span>
        </div>
      </div>

      <!-- FD KPI Cards Grid -->
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
      </div>

      <!-- FD Analytical Chart with Mode Switcher -->
      <div class="report-card" style="margin-bottom: 16px;">
        <div class="report-card-header">
          <div class="report-card-title">
            <i data-lucide="bar-chart-2" style="color: #8b5cf6;"></i>
            <span id="chart-fd-title">BIỂU ĐỒ %FD THEO 18 AM (CỘT %FD RETURN + MIỀN SẢN LƯỢNG GIAO + ĐƯỜNG BIẾN ĐỘNG Δ)</span>
          </div>
          <div class="chart-mode-group">
            <button class="chart-mode-pill active" id="btn-fd-full" onclick="setFdChartMode('full')">
              📊 %FD Full Hàng (Sort %FD ↓)
            </button>
            <button class="chart-mode-pill" id="btn-fd-tts" onclick="setFdChartMode('tts')">
              ⚡ %FD TikTok Shop (Sort %FD ↓)
            </button>
          </div>
        </div>
        <div class="report-card-body">
          <div style="height: 380px; position: relative;">
            <canvas id="chart-fd-bar"></canvas>
          </div>
        </div>
      </div>

      <!-- FD Tables Grid -->
      <div class="grid-row-2">
        <!-- Bảng 1: Bảng 18 AM (Full Hàng vs TTS) -->
        <div class="report-card">
          <div class="report-card-header">
            <div class="report-card-title">
              <i data-lucide="users" style="color: var(--ghn-navy);"></i>
              BẢNG 1: ĐIỀU HÀNH %FD 18 AM (FULL HÀNG vs TIKTOK SHOP)
            </div>
            <span class="badge-tag badge-tag-blue">18 AM Phụ Trách</span>
          </div>
          <div class="report-card-body">
            <div class="table-toolbar">
              <div class="table-search-box">
                <i data-lucide="search" class="table-search-icon" style="width: 14px; height: 14px;"></i>
                <input type="text" id="search-fd-am" class="table-search-input" placeholder="Tìm tên AM...">
              </div>
            </div>
            <div class="bi-table-wrap">
              <table class="bi-table" id="table-fd-am-detailed">
                <thead>
                  <tr>
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
                  </tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Bảng 2: Top Bưu Cục %FD Cao Nhất -->
        <div class="report-card">
          <div class="report-card-header">
            <div class="report-card-title">
              <i data-lucide="alert-octagon" style="color: #ef4444;"></i>
              BẢNG 2: TOP BƯU CỤC CÓ TỶ LỆ %FD CAO NHẤT (W36)
            </div>
            <span class="badge-tag badge-tag-red">≥10% Cảnh Báo | ≥15% Nghiêm Trọng</span>
          </div>
          <div class="report-card-body">
            <div class="table-toolbar">
              <div class="table-search-box">
                <i data-lucide="search" class="table-search-icon" style="width: 14px; height: 14px;"></i>
                <input type="text" id="search-fd-bc" class="table-search-input" placeholder="Tìm tên Bưu Cục...">
              </div>
            </div>
            <div class="bi-table-wrap">
              <table class="bi-table" id="table-fd-top-bc">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Tên Bưu Cục</th>
                    <th>AM Phụ Trách</th>
                    <th class="num">Total Đơn</th>
                    <th class="num" style="color: #ef4444;">Đơn Return</th>
                    <th class="num" style="background: var(--color-red-bg); font-weight:800; color:#b91c1c;">%FD Return</th>
                    <th class="num">Tỷ Trọng Return</th>
                    <th class="center">Mức Cảnh Báo</th>
                  </tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

'''

aging_tag = '    <!-- TAB 8: AGING TỒN ĐỌNG & TREO LUÂN CHUYỂN (BACKLOG & AGING) -->'
if aging_tag in html and 'id="tab-fd"' not in html:
    html = html.replace(aging_tag, tab_fd_html + '    ' + aging_tag)
    print("Inserted Tab 10 (%FD Hoàn Trả) before Aging tab!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html updated successfully!")
