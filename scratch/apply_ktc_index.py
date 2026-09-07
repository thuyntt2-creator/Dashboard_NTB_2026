import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update navbar
old_nav = '''          <button class="tab-item" data-tab="tab-fd">
            <i data-lucide="rotate-ccw"></i> 10. %FD Hoàn Trả
          </button>
          <button class="tab-item" data-tab="tab-aging">
            <i data-lucide="alert-octagon"></i> 11. Aging & Treo LC
          </button>
          <button class="tab-item" data-tab="tab-control">
            <i data-lucide="wallet"></i> 12. COD Tiền Mặt
          </button>
          <button class="tab-item" data-tab="tab-truythu">
            <i data-lucide="shield-alert"></i> 13. Báo Cáo Truy Thu
          </button>
          <button class="tab-item" data-tab="tab-commercial">
            <i data-lucide="trending-up"></i> 14. Kinh Doanh & F30
          </button>'''

new_nav = '''          <button class="tab-item" data-tab="tab-fd">
            <i data-lucide="rotate-ccw"></i> 10. %FD Hoàn Trả
          </button>
          <button class="tab-item" data-tab="tab-ktc">
            <i data-lucide="truck"></i> 11. KTC & Vận Tải
          </button>
          <button class="tab-item" data-tab="tab-aging">
            <i data-lucide="alert-octagon"></i> 12. Aging & Treo LC
          </button>
          <button class="tab-item" data-tab="tab-control">
            <i data-lucide="wallet"></i> 13. COD Tiền Mặt
          </button>
          <button class="tab-item" data-tab="tab-truythu">
            <i data-lucide="shield-alert"></i> 14. Báo Cáo Truy Thu
          </button>
          <button class="tab-item" data-tab="tab-commercial">
            <i data-lucide="trending-up"></i> 15. Kinh Doanh & F30
          </button>'''

assert old_nav in html, "old_nav not found!"
html = html.replace(old_nav, new_nav)
print("Navbar updated successfully!")

# 2. Add Tab KTC container right after Tab 10 (%FD) and before Tab Aging
old_tab_pos = '''      <!-- Bảng 2: Top Bưu Cục %FD Cao Nhất -->
      <div class="report-card" style="margin-bottom: 20px;">
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
    </div>'''

ktc_tab_html = '''      <!-- Bảng 2: Top Bưu Cục %FD Cao Nhất -->
      <div class="report-card" style="margin-bottom: 20px;">
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

    <!-- ==================================================================== -->
    <!-- TAB 11: BÁO CÁO KTC & VẬN TẢI (BACKLOG, LEADTIME & TỶ LỆ LẤP ĐẦY XE) -->
    <!-- ==================================================================== -->
    <div id="tab-ktc" class="tab-view">
      <!-- Executive Banner -->
      <div class="exec-banner" style="border-left-color: #0284c7;">
        <div class="exec-banner-content">
          <div class="exec-banner-icon" style="background: rgba(2, 132, 199, 0.15); color: #0284c7;">
            <i data-lucide="truck" style="width: 24px; height: 24px;"></i>
          </div>
          <div class="exec-banner-text">
            <h2 style="margin: 0; font-size: 16px; font-weight: 800; color: var(--text-main);">
              BÁO CÁO ĐIỀU HÀNH KTC & VẬN TẢI — VÙNG NAM TRUNG BỘ (W36)
            </h2>
            <p style="margin: 4px 0 0 0; font-size: 12.5px; color: var(--text-muted); line-height: 1.5;">
              • <strong>Backlog KTC:</strong> Toàn mạng ghi nhận <strong>16,207 đơn</strong> luân chuyển, trong đó <strong>381 đơn treo trên 36h</strong> chưa đóng kiện (tập trung tại KTC Khánh Hòa do AM Nguyễn Tiến Lực quản lý).<br>
              • <strong>Leadtime KTC/KCT:</strong> Thời gian nhận xuất trung bình đạt <strong>3.31h</strong> (P50: 2.24h, P95: 7.09h); Tỷ lệ tồn >12h đạt <strong>2.1%</strong> (662 đơn), tồn >24h chỉ <strong>0.1%</strong> (46 đơn).<br>
              • <strong>Tỷ Lệ Lấp Đầy Thùng / Xe:</strong> Daily (06/09) đạt <strong>56.2%</strong> (+0.7%p vs 05/09; 82 chuyến). Tổng hợp Tuần W36 đạt <strong>48.1%</strong> (516 chuyến, 112 chuyến &lt;30% cần tối ưu ghép điểm).
            </p>
          </div>
        </div>
        <div class="exec-banner-meta">
          <span class="badge-tag badge-tag-blue" style="font-weight: 800;">5 KTC/KCT Trọng Điểm</span>
          <span class="badge-tag badge-tag-amber">Cập nhật lúc 21:24</span>
        </div>
      </div>

      <!-- KTC KPI Cards Strip -->
      <div class="kpi-strip" style="grid-template-columns: repeat(4, 1fr); margin-bottom: 20px;">
        <div class="kpi-tile" style="border-left: 4px solid var(--color-blue);">
          <div class="kpi-tile-header">
            <span>Tổng Backlog KTC (0-192h+)</span>
            <div class="kpi-tile-icon" style="background: rgba(37, 99, 235, 0.12); color: var(--color-blue);">
              <i data-lucide="package" style="width: 16px; height: 16px;"></i>
            </div>
          </div>
          <div class="kpi-tile-value">16,207 <small>đơn</small></div>
          <div class="kpi-tile-meta">
            <span class="diff-tag diff-up-bad">+15,826 đ so trước</span>
            <span style="color: var(--text-muted); font-size: 11.5px;">5 KTC / KCT</span>
          </div>
        </div>

        <div class="kpi-tile kpi-red" style="border-left: 4px solid #ef4444;">
          <div class="kpi-tile-header">
            <span>Treo >36h Chưa Đóng Kiện</span>
            <div class="kpi-tile-icon" style="background: rgba(239, 68, 68, 0.12); color: #ef4444;">
              <i data-lucide="alert-triangle" style="width: 16px; height: 16px;"></i>
            </div>
          </div>
          <div class="kpi-tile-value" style="color: #ef4444;">381 <small>đơn</small></div>
          <div class="kpi-tile-meta">
            <span class="badge-tag badge-tag-red">100% KTC Khánh Hòa</span>
            <span style="color: var(--text-muted); font-size: 11.5px;">AM Nguyễn Tiến Lực</span>
          </div>
        </div>

        <div class="kpi-tile kpi-green" style="border-left: 4px solid #10b981;">
          <div class="kpi-tile-header">
            <span>Tỷ Lệ Tồn >12h KTC/KCT</span>
            <div class="kpi-tile-icon" style="background: rgba(16, 185, 129, 0.12); color: #10b981;">
              <i data-lucide="clock" style="width: 16px; height: 16px;"></i>
            </div>
          </div>
          <div class="kpi-tile-value" style="color: #10b981;">2.1% <small style="color: var(--text-muted); font-size: 12px;">(662 đ)</small></div>
          <div class="kpi-tile-meta">
            <span class="badge-tag badge-tag-green">Tồn >24h: 0.1% (46 đ)</span>
            <span style="color: var(--text-muted); font-size: 11.5px;">LT TB: 3.31h</span>
          </div>
        </div>

        <div class="kpi-tile kpi-amber" style="border-left: 4px solid #ea580c;">
          <div class="kpi-tile-header">
            <span>TLLĐ Xe Bình Quân (W36)</span>
            <div class="kpi-tile-icon" style="background: rgba(234, 88, 12, 0.12); color: #ea580c;">
              <i data-lucide="truck" style="width: 16px; height: 16px;"></i>
            </div>
          </div>
          <div class="kpi-tile-value" style="color: #ea580c;">48.1% <small style="color: var(--text-muted); font-size: 13px; font-weight: 600;">(W35: 51.8%)</small></div>
          <div class="kpi-tile-meta">
            <span class="badge-tag badge-tag-amber">Daily 06/09: 56.2%</span>
            <span style="color: var(--text-muted); font-size: 11.5px;">112 chuyến &lt;30%</span>
          </div>
        </div>
      </div>

      <!-- Segment Switcher for 3 Sub-Views -->
      <div class="view-mode-bar" style="margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; background: var(--bg-surface); padding: 12px 16px; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 12px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">CHỌN BÁO CÁO KTC:</span>
          <div class="btn-group" id="ktc-subtab-group">
            <button class="btn btn-sm btn-primary active" id="btn-ktc-backlog" onclick="setKtcSubTab('backlog')">
              <i data-lucide="clock" style="width: 14px; height: 14px;"></i> ⏱️ 1. Backlog Theo Khung Giờ
            </button>
            <button class="btn btn-sm btn-secondary" id="btn-ktc-leadtime" onclick="setKtcSubTab('leadtime')">
              <i data-lucide="hourglass" style="width: 14px; height: 14px;"></i> ⏳ 2. Tổng Quan Leadtime KTC/KCT
            </button>
            <button class="btn btn-sm btn-secondary" id="btn-ktc-fillrate" onclick="setKtcSubTab('fillrate')">
              <i data-lucide="truck" style="width: 14px; height: 14px;"></i> 🚚 3. Tỷ Lệ Lấp Đầy Thùng/Xe (W36 & Daily)
            </button>
          </div>
        </div>
      </div>

      <!-- ======================================================= -->
      <!-- SUB-VIEW 1: BACKLOG THEO KHUNG GIỜ -->
      <!-- ======================================================= -->
      <div id="ktc-subview-backlog" class="ktc-subview">
        <!-- Bảng 1: Đơn treo >36h theo AM -->
        <div class="report-card" style="margin-bottom: 20px;">
          <div class="report-card-header">
            <div class="report-card-title">
              <i data-lucide="users" style="color: var(--ghn-navy);"></i>
              ĐƠN TREO LUÂN CHUYỂN GIAO/TRẢ TRÊN 36H (CHƯA/KHÔNG CẦN ĐÓNG KIỆN) THEO AM
            </div>
            <span class="badge-tag badge-tag-blue">Cập nhật lúc 21:24</span>
          </div>
          <div class="report-card-body">
            <div class="bi-table-wrap">
              <table class="bi-table" id="table-ktc-backlog-am">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>AM Phụ Trách</th>
                    <th class="num">0 - 6h</th>
                    <th class="num">6 - 12h</th>
                    <th class="num">12 - 24h</th>
                    <th class="num">24 - 36h</th>
                    <th class="num">36 - 72h</th>
                    <th class="num">72 - 120h</th>
                    <th class="num">120 - 192h</th>
                    <th class="num">192h+</th>
                    <th class="num" style="background: var(--color-red-bg); font-weight: 800; color: #b91c1c;">Treo >36h</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">Tổng</th>
                    <th class="num">+/- So Với Trước</th>
                  </tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Bảng 2: Backlog KTC theo Kho -->
        <div class="report-card" style="margin-bottom: 20px;">
          <div class="report-card-header">
            <div class="report-card-title">
              <i data-lucide="warehouse" style="color: #0284c7;"></i>
              BACKLOG KTC THEO KHO / BƯU CỤC
            </div>
            <span class="badge-tag badge-tag-blue">5 Điểm Kho Luân Chuyển</span>
          </div>
          <div class="report-card-body">
            <div class="bi-table-wrap">
              <table class="bi-table" id="table-ktc-backlog-kho">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Bưu Cục / Kho</th>
                    <th>AM Quản Lý</th>
                    <th class="num">0 - 6h</th>
                    <th class="num">6 - 12h</th>
                    <th class="num">12 - 24h</th>
                    <th class="num">24 - 36h</th>
                    <th class="num">36 - 72h</th>
                    <th class="num">72 - 120h</th>
                    <th class="num">120 - 192h</th>
                    <th class="num">192h+</th>
                    <th class="num" style="background: var(--color-red-bg); font-weight: 800; color: #b91c1c;">Treo >36h</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">Tổng</th>
                    <th class="num">+/- So Với Trước</th>
                  </tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Bảng 3: Đơn treo >24h theo ngày -->
        <div class="report-card" style="margin-bottom: 20px;">
          <div class="report-card-header">
            <div class="report-card-title">
              <i data-lucide="calendar" style="color: #ea580c;"></i>
              ĐƠN TREO LUÂN CHUYỂN GIAO/TRẢ >24H — MỐC 7H30 HẰNG NGÀY (31/08 – 07/09)
            </div>
            <span class="badge-tag badge-tag-amber">8 Ngày Gần Nhất</span>
          </div>
          <div class="report-card-body">
            <div class="bi-table-wrap">
              <table class="bi-table" id="table-ktc-trend-days">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>AM Phụ Trách</th>
                    <th class="center">Ngày N (07/09)</th>
                    <th class="center">Ngày N-1 (06/09)</th>
                    <th class="center">Ngày N-2 (05/09)</th>
                    <th class="center">Ngày N-3 (04/09)</th>
                    <th class="center">Ngày N-4 (03/09)</th>
                    <th class="center">Ngày N-5 (02/09)</th>
                    <th class="center">Ngày N-6 (01/09)</th>
                    <th class="center">Ngày N-7 (31/08)</th>
                  </tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- ======================================================= -->
      <!-- SUB-VIEW 2: TỔNG QUAN LEADTIME KTC/KCT -->
      <!-- ======================================================= -->
      <div id="ktc-subview-leadtime" class="ktc-subview" style="display: none;">
        <div class="report-card" style="margin-bottom: 20px;">
          <div class="report-card-header">
            <div class="report-card-title">
              <i data-lucide="gauge" style="color: #10b981;"></i>
              TỔNG QUAN LEADTIME KTC / KCT (THEO SHEET RAW)
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="font-size: 11px; font-weight: 700; color: var(--text-muted);">KỲ BÁO CÁO:</span>
              <div class="btn-group" id="leadtime-mode-group">
                <button class="btn btn-xs btn-primary active" id="btn-lt-snapshot" onclick="setLeadtimeMode('snapshot')">
                  📌 Snapshot Chuẩn (31,542 đơn)
                </button>
                <button class="btn btn-xs btn-secondary" id="btn-lt-w36" onclick="setLeadtimeMode('w36')">
                  📅 Tuần W36 (Lũy Kế 7 Ngày)
                </button>
              </div>
            </div>
          </div>
          <div class="report-card-body">
            <div class="bi-table-wrap">
              <table class="bi-table" id="table-ktc-leadtime">
                <thead>
                  <tr>
                    <th>Loại Kho</th>
                    <th>Tên Kho</th>
                    <th class="num">Tổng Đơn</th>
                    <th class="num" style="color: #ef4444;">Tồn >12h</th>
                    <th class="num" style="background: var(--color-red-bg); font-weight: 800; color: #b91c1c;">% Tồn >12h</th>
                    <th class="num" style="color: #ef4444;">Tồn >24h</th>
                    <th class="num" style="background: var(--color-red-bg); font-weight: 800; color: #b91c1c;">% Tồn >24h</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">LT TB (h)</th>
                    <th class="num">LT P50 (h)</th>
                    <th class="num">LT P95 (h)</th>
                    <th class="center">Đánh Giá SLA</th>
                  </tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- ======================================================= -->
      <!-- SUB-VIEW 3: TỶ LỆ LẤP ĐẦY THÙNG / XE (FILL RATE) -->
      <!-- ======================================================= -->
      <div id="ktc-subview-fillrate" class="ktc-subview" style="display: none;">
        <!-- Header Controls for Fill Rate -->
        <div class="report-card" style="margin-bottom: 20px;">
          <div class="report-card-header">
            <div class="report-card-title">
              <i data-lucide="bar-chart-3" style="color: #ea580c;"></i>
              <span id="fillrate-title">BÁO CÁO DAILY TỶ LỆ LẤP ĐẦY XE - VÙNG NTB (05/09/2026 vs 06/09/2026)</span>
            </div>
            <div class="btn-group" id="fillrate-mode-group">
              <button class="btn btn-sm btn-primary active" id="btn-fr-daily" onclick="setFillRateMode('daily')">
                📅 Daily (05/09 vs 06/09)
              </button>
              <button class="btn btn-sm btn-secondary" id="btn-fr-weekly" onclick="setFillRateMode('weekly')">
                📊 Tuần (W35 vs W36)
              </button>
            </div>
          </div>
          <div class="report-card-body">
            <div class="bi-table-wrap">
              <table class="bi-table" id="table-ktc-fillrate">
                <thead id="table-ktc-fillrate-thead"></thead>
                <tbody id="table-ktc-fillrate-tbody"></tbody>
              </table>
            </div>
            <div style="margin-top: 10px; font-size: 11.5px; color: var(--text-muted); font-style: italic;">
              * Số liệu trích xuất trực tiếp từ Google Sheet "TỶ LỆ LẤP ĐẦY VÙNG NTB". Các mốc chuyến lấp đầy &lt;10%, 10%–&lt;20%, 20%–&lt;30% được phân tầng chuẩn xác.
            </div>
          </div>
        </div>

        <!-- Bảng Phân Tích Nguyên Nhân Chuyến <30% TLLĐ -->
        <div class="report-card" style="margin-bottom: 20px;">
          <div class="report-card-header">
            <div class="report-card-title">
              <i data-lucide="alert-circle" style="color: #ef4444;"></i>
              ĐÚC KẾT NGUYÊN NHÂN CÁC CHUYẾN &lt; 30% TLLĐ TOÀN VÙNG NTB
            </div>
            <span class="badge-tag badge-tag-red">Phân Nhóm Theo KTC</span>
          </div>
          <div class="report-card-body">
            <div class="bi-table-wrap">
              <table class="bi-table" id="table-ktc-fillrate-causes">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Nhóm Nguyên Nhân</th>
                    <th class="num">KTC Khánh Hòa</th>
                    <th class="num">KCT Đức Trọng</th>
                    <th class="num">KCT Đắk Nông</th>
                    <th class="num">KCT Bình Thuận</th>
                    <th class="num">KCT Bảo Lộc</th>
                    <th class="num bold" style="background: var(--color-blue-bg);">Tổng Chuyến</th>
                    <th class="num bold" style="color: #ef4444;">Tỷ Trọng (%)</th>
                  </tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>'''

assert old_tab_pos in html, "old_tab_pos not found in index.html!"
html = html.replace(old_tab_pos, ktc_tab_html)
print("Tab 11 KTC added to index.html successfully!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html successfully written!")
