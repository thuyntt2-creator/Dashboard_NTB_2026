import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# 1. Update TAB 5: % GÁN
tab5_old = html[html.find('<!-- TAB 5: % GÁN VẬN HÀNH'):html.find('<!-- TAB 6: %ODR')]
tab5_new = """<!-- ==================================================================== -->
    <!-- TAB 5: % GÁN VẬN HÀNH (GÁN CA 1, GÁN CA 2 & GÁN TỔNG) -->
    <!-- ==================================================================== -->
    <div id="tab-gan" class="tab-view">
      <div class="exec-banner" style="border-left-color: var(--color-purple);">
        <div class="exec-banner-content">
          <div class="exec-banner-icon" style="background: rgba(168, 85, 247, 0.2); color: var(--color-purple);">
            <i data-lucide="user-check" style="width: 24px; height: 24px;"></i>
          </div>
          <div class="exec-banner-text">
            <h3>TỶ LỆ GÁN VẬN HÀNH TOÀN MẠNG THEO CA 1, CA 2 & GÁN TỔNG (TARGET ≥ 90.0%)</h3>
            <p>
              • <strong>Toàn Vùng NTB:</strong> % Gán Tổng đạt <strong>82.6%</strong>; % Gán Ca 1+Tồn đạt <strong>87.3%</strong>; % Gán Ca 2 đạt <strong>65.2%</strong>.<br>
              • <strong>Top AM Gán Tốt:</strong> <strong>Thái Thị Thanh Thư (97.8%)</strong>, <strong>Nguyễn Duy Long (94.5%)</strong>, <strong>Nguyễn Ngọc Khánh (94.2%)</strong>.<br>
              • <strong>Cần Thúc Đẩy Gán:</strong> <strong>Trương Quang Linh (9.7%)</strong>, <strong>Lê Minh Lợi (38.2%)</strong>, <strong>Trầm Hữu Tiến (71.9%)</strong>.
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-purple" style="font-size: 12px; padding: 6px 12px;">
            Target Gán Tổng ≥ 90.0%
          </span>
        </div>
      </div>

      <!-- Chart Gán Phối Hợp 3 Cột -->
      <div class="report-card">
        <div class="report-card-header">
          <div class="report-card-title">
            <i data-lucide="bar-chart-3" style="color: var(--color-purple);"></i>
            SO SÁNH TỶ LỆ GÁN: % GÁN CA 1+TỒN vs % GÁN CA 2 vs % GÁN TỔNG THEO 18 AM (W35)
          </div>
          <span class="badge-tag badge-tag-purple">Target Chuẩn ≥ 90.0%</span>
        </div>
        <div class="report-card-body">
          <div class="chart-box chart-box-tall">
            <canvas id="chart-gan-am-bar"></canvas>
          </div>
        </div>
      </div>

      <!-- 2 Bảng Đối Xứng: Gán Ca 1 vs Gán Ca 2 & Gán Tổng -->
      <div class="grid-row-2">
        <!-- Bảng 1: Gán Ca 1+Tồn -->
        <div class="report-card">
          <div class="report-card-header">
            <div class="report-card-title">
              <i data-lucide="sun" style="color: var(--ghn-orange);"></i>
              BẢNG 1: TỶ LỆ % GÁN CA 1 + TỒN (SORT CAO XUỐNG THẤP)
            </div>
            <span class="badge-tag badge-tag-amber">Ca 1+Tồn</span>
          </div>
          <div class="report-card-body">
            <div class="bi-table-wrap">
              <table class="bi-table" id="table-gan-ca1-detailed">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>AM Phụ Trách</th>
                    <th class="num">Sản Lượng</th>
                    <th class="num">W34</th>
                    <th class="num" style="background: var(--color-amber-bg); font-weight:800;">Ca 1+Tồn W35</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="center">Đánh Giá SLA</th>
                  </tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Bảng 2: Gán Ca 2 & Gán Tổng -->
        <div class="report-card">
          <div class="report-card-header">
            <div class="report-card-title">
              <i data-lucide="moon" style="color: var(--color-purple);"></i>
              BẢNG 2: TỶ LỆ % GÁN CA 2 & GÁN TỔNG (SORT % GÁN TỔNG)
            </div>
            <span class="badge-tag badge-tag-purple">Ca 2 & Gán Tổng</span>
          </div>
          <div class="report-card-body">
            <div class="bi-table-wrap">
              <table class="bi-table" id="table-gan-ca2-detailed">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>AM Phụ Trách</th>
                    <th class="num">Sản Lượng</th>
                    <th class="num">Gán Ca 2</th>
                    <th class="num">Tổng W34</th>
                    <th class="num" style="background: var(--color-purple-bg); font-weight:800; color:#7e22ce;">Gán Tổng W35</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="center">Đánh Giá SLA</th>
                  </tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
    """

if tab5_old:
    html = html.replace(tab5_old, tab5_new)

# 2. Update TAB 6: %ODR
tab6_old = html[html.find('<!-- TAB 6: %ODR - GIAO ĐÚNG HẸN'):html.find('<!-- TAB 7: %LTC')]
tab6_new = """<!-- ==================================================================== -->
    <!-- TAB 6: %ODR - GIAO ĐÚNG HẸN SLA (TARGET ≥ 92.0%) -->
    <!-- ==================================================================== -->
    <div id="tab-odr" class="tab-view">
      <div class="exec-banner" style="border-left-color: var(--color-green);">
        <div class="exec-banner-content">
          <div class="exec-banner-icon" style="background: rgba(16, 185, 129, 0.2); color: var(--color-green);">
            <i data-lucide="clock" style="width: 24px; height: 24px;"></i>
          </div>
          <div class="exec-banner-text">
            <h3>PHÂN TÍCH HIỆU SUẤT %ODR (GIAO ĐÚNG HẸN SLA) TOÀN VÙNG (TARGET ≥ 92.0%)</h3>
            <p>
              • <strong>Toàn Vùng:</strong> Đạt <strong>92.18%</strong> (-1.47% WoW). Có <strong>15/18 AM</strong> đạt chuẩn xanh SLA ≥92.0%.<br>
              • <strong>Top AM Xuất Sắc:</strong> <strong>Nguyễn Duy Long (96.5%)</strong>, <strong>Thái Thị Thanh Thư (96.4%)</strong>, <strong>Nguyễn Hoàng Phi (96.1%)</strong>.<br>
              • <strong>Nhóm AM Cần Khắc Phục Giao Trễ:</strong> <strong>Lê Minh Lợi (58.5%)</strong>, <strong>Trầm Hữu Tiến (82.7%)</strong>, <strong>Trương Quang Linh (83.8%)</strong>.
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-green" style="font-size: 12px; padding: 6px 12px;">
            Target ODR ≥ 92.0%
          </span>
        </div>
      </div>

      <!-- ODR Bar Chart -->
      <div class="report-card">
        <div class="report-card-header">
          <div class="report-card-title">
            <i data-lucide="bar-chart-3" style="color: var(--color-green);"></i>
            TỶ LỆ %ODR (GIAO ĐÚNG HẸN) THEO 18 AM (SORT CAO XUỐNG THẤP)
          </div>
          <span class="badge-tag badge-tag-green">SLA Target ≥ 92.0%</span>
        </div>
        <div class="report-card-body">
          <div class="chart-box chart-box-tall">
            <canvas id="chart-odr-bar"></canvas>
          </div>
        </div>
      </div>

      <!-- 2 Bảng Đối Xứng: 18 AM (Trái) vs 5 Tỉnh (Phải) -->
      <div class="grid-row-2">
        <!-- Bảng 1: %ODR 18 AM -->
        <div class="report-card">
          <div class="report-card-header">
            <div class="report-card-title">
              <i data-lucide="table-properties" style="color: var(--color-green);"></i>
              BẢNG 1: %ODR THEO 18 AM (SORT BIẾN ĐỘNG Δ)
            </div>
            <span class="badge-tag badge-tag-green">18 AM</span>
          </div>
          <div class="report-card-body">
            <div class="bi-table-wrap">
              <table class="bi-table" id="table-odr-detailed">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>AM Phụ Trách</th>
                    <th class="num">Sản Lượng</th>
                    <th class="num">W32</th>
                    <th class="num">W33</th>
                    <th class="num">W34</th>
                    <th class="num" style="background: var(--color-green-bg); font-weight:800;">%ODR W35</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="center">Đánh Giá SLA</th>
                  </tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Bảng 2: %ODR 5 Tỉnh Thành -->
        <div class="report-card">
          <div class="report-card-header">
            <div class="report-card-title">
              <i data-lucide="map-pin" style="color: var(--ghn-navy);"></i>
              BẢNG 2: %ODR THEO 5 TỈNH THÀNH (W32 – W35)
            </div>
            <span class="badge-tag badge-tag-green">5 Tỉnh Thành</span>
          </div>
          <div class="report-card-body">
            <div class="bi-table-wrap">
              <table class="bi-table" id="table-odr-tinh-detailed">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Tỉnh / Thành Phố</th>
                    <th class="num">Sản Lượng</th>
                    <th class="num">W32</th>
                    <th class="num">W33</th>
                    <th class="num">W34</th>
                    <th class="num" style="background: var(--color-green-bg); font-weight:800;">%ODR W35</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="center">Đánh Giá SLA</th>
                  </tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
    """

if tab6_old:
    html = html.replace(tab6_old, tab6_new)

# 3. Update TAB 7: %LTC
tab7_old = html[html.find('<!-- TAB 7: %LTC - LẤY THÀNH CÔNG'):html.find('<!-- TAB 8: %OPR')]
tab7_new = """<!-- ==================================================================== -->
    <!-- TAB 7: %LTC - LẤY THÀNH CÔNG (TARGET ≥ 90.0%) -->
    <!-- ==================================================================== -->
    <div id="tab-ltc" class="tab-view">
      <div class="exec-banner" style="border-left-color: var(--color-blue);">
        <div class="exec-banner-content">
          <div class="exec-banner-icon" style="background: rgba(37, 99, 235, 0.2); color: var(--color-blue);">
            <i data-lucide="archive" style="width: 24px; height: 24px;"></i>
          </div>
          <div class="exec-banner-text">
            <h3>PHÂN TÍCH CHỈ SỐ %LTC (LẤY THÀNH CÔNG) THEO 18 AM & 5 TỈNH (TARGET ≥ 90.0%)</h3>
            <p>
              • <strong>Toàn Vùng:</strong> Đạt <strong>91.14%</strong> (+0.62% WoW). Duy trì vượt chuẩn SLA ≥90.0%.<br>
              • <strong>Top AM Dẫn Đầu:</strong> <strong>Lê Thanh Nhựt (98.2%)</strong>, <strong>Cao Thị Thanh Thủy (96.8%)</strong>, <strong>Phan Đình Duy (96.4%)</strong>.<br>
              • <strong>Bứt Phá Lấy Hàng:</strong> <strong>Trương Quang Linh</strong> tăng vọt +17.6% (từ 36.2% lên 53.8%).
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-blue" style="font-size: 12px; padding: 6px 12px;">
            Target LTC ≥ 90.0%
          </span>
        </div>
      </div>

      <!-- LTC Bar Chart -->
      <div class="report-card">
        <div class="report-card-header">
          <div class="report-card-title">
            <i data-lucide="bar-chart-3" style="color: var(--color-blue);"></i>
            TỶ LỆ %LTC (LẤY THÀNH CÔNG) THEO 18 AM (SORT CAO XUỐNG THẤP)
          </div>
          <span class="badge-tag badge-tag-blue">Target SLA ≥ 90.0%</span>
        </div>
        <div class="report-card-body">
          <div class="chart-box chart-box-tall">
            <canvas id="chart-ltc-bar"></canvas>
          </div>
        </div>
      </div>

      <!-- 2 Bảng Đối Xứng: 18 AM (Trái) vs 5 Tỉnh (Phải) -->
      <div class="grid-row-2">
        <!-- Bảng 1: %LTC 18 AM -->
        <div class="report-card">
          <div class="report-card-header">
            <div class="report-card-title">
              <i data-lucide="table-properties" style="color: var(--color-blue);"></i>
              BẢNG 1: %LTC THEO 18 AM (SORT BIẾN ĐỘNG Δ)
            </div>
            <span class="badge-tag badge-tag-blue">18 AM</span>
          </div>
          <div class="report-card-body">
            <div class="bi-table-wrap">
              <table class="bi-table" id="table-ltc-detailed">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>AM Phụ Trách</th>
                    <th class="num">Sản Lượng</th>
                    <th class="num">W32</th>
                    <th class="num">W33</th>
                    <th class="num">W34</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%LTC W35</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="center">Đánh Giá SLA</th>
                  </tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Bảng 2: %LTC 5 Tỉnh Thành -->
        <div class="report-card">
          <div class="report-card-header">
            <div class="report-card-title">
              <i data-lucide="map-pin" style="color: var(--ghn-navy);"></i>
              BẢNG 2: %LTC THEO 5 TỈNH THÀNH (W32 – W35)
            </div>
            <span class="badge-tag badge-tag-blue">5 Tỉnh Thành</span>
          </div>
          <div class="report-card-body">
            <div class="bi-table-wrap">
              <table class="bi-table" id="table-ltc-tinh-detailed">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Tỉnh / Thành Phố</th>
                    <th class="num">Sản Lượng</th>
                    <th class="num">W32</th>
                    <th class="num">W33</th>
                    <th class="num">W34</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight:800;">%LTC W35</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="center">Đánh Giá SLA</th>
                  </tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
    """

if tab7_old:
    html = html.replace(tab7_old, tab7_new)

# 4. Update TAB 9: RỚT LUÂN CHUYỂN
tab9_old = html[html.find('<!-- TAB 9: RỚT LUÂN CHUYỂN'):html.find('<!-- TAB 8: AGING')]
tab9_new = """<!-- ==================================================================== -->
    <!-- TAB 9: RỚT LUÂN CHUYỂN (TRANSIT LOSS & TRANSPORT) -->
    <!-- ==================================================================== -->
    <div id="tab-rot-lc" class="tab-view">
      <div class="exec-banner" style="border-left-color: var(--color-red);">
        <div class="exec-banner-content">
          <div class="exec-banner-icon" style="background: rgba(239, 68, 68, 0.2); color: var(--color-red);">
            <i data-lucide="alert-triangle" style="width: 24px; height: 24px;"></i>
          </div>
          <div class="exec-banner-text">
            <h3>GIÁM SÁT TỶ LỆ % RỚT LUÂN CHUYỂN TOÀN MẠNG (TARGET BENCHMARK ≤ 1.0%)</h3>
            <p>
              • <strong>Toàn Vùng:</strong> Tỷ lệ rớt LC giảm mạnh về <strong>1.57%</strong> (giảm -1.03% so với 2.60% của W34).<br>
              • <strong>Top AM Quản Lý Tốt:</strong> <strong>Nguyễn Lê Nguyên Vũ (0.0%)</strong>, <strong>Lê Minh Lợi (0.0%)</strong>, <strong>Nguyễn Hoàng Phi (0.1%)</strong>, <strong>Lê Thanh Nhựt (0.2%)</strong>.<br>
              • <strong>Điểm Nóng Cần Chấn Chỉnh:</strong> AM Trầm Hữu Tiến (28.6% rớt LC), AM Huỳnh Thúc Duân (8.4% rớt LC).
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-green" style="font-size: 12px; padding: 6px 12px;">
            Mục Tiêu ≤ 1.0%
          </span>
        </div>
      </div>

      <!-- Chart Rớt LC 18 AM -->
      <div class="report-card">
        <div class="report-card-header">
          <div class="report-card-title">
            <i data-lucide="bar-chart-3" style="color: var(--color-red);"></i>
            % RỚT LUÂN CHUYỂN THEO 18 AM PHỤ TRÁCH (W35 — TARGET BENCHMARK ≤ 1.0%)
          </div>
          <span class="badge-tag badge-tag-red">Target ≤ 1.0%</span>
        </div>
        <div class="report-card-body">
          <div class="chart-box chart-box-tall">
            <canvas id="chart-rot-lc-bar"></canvas>
          </div>
        </div>
      </div>

      <!-- 2 Bảng Đối Xứng: 18 AM (Trái) vs 5 Tỉnh (Phải) -->
      <div class="grid-row-2" style="margin-bottom: 20px;">
        <!-- Bảng 1: Rớt LC 18 AM -->
        <div class="report-card">
          <div class="report-card-header">
            <div class="report-card-title">
              <i data-lucide="table-properties" style="color: var(--color-red);"></i>
              BẢNG 1: % RỚT LUÂN CHUYỂN THEO 18 AM
            </div>
            <span class="badge-tag badge-tag-red">18 AM</span>
          </div>
          <div class="report-card-body">
            <div class="bi-table-wrap">
              <table class="bi-table" id="table-rot-am-detailed">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>AM Phụ Trách</th>
                    <th class="num">Vol Cần LC</th>
                    <th class="num">% Rớt W34</th>
                    <th class="num" style="background: var(--color-red-bg); font-weight:800; color:#b91c1c;">% Rớt W35</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="center">Mức Cảnh Báo</th>
                  </tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Bảng 2: Rớt LC 5 Tỉnh -->
        <div class="report-card">
          <div class="report-card-header">
            <div class="report-card-title">
              <i data-lucide="map-pin" style="color: var(--ghn-navy);"></i>
              BẢNG 2: % RỚT LUÂN CHUYỂN THEO 5 TỈNH THÀNH
            </div>
            <span class="badge-tag badge-tag-blue">5 Tỉnh Thành</span>
          </div>
          <div class="report-card-body">
            <div class="bi-table-wrap">
              <table class="bi-table" id="table-rot-tinh-detailed">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Tỉnh / Thành Phố</th>
                    <th class="num">Vol Cần LC</th>
                    <th class="num">% Rớt W34</th>
                    <th class="num" style="background: var(--color-red-bg); font-weight:800; color:#b91c1c;">% Rớt W35</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="center">Mức Cảnh Báo</th>
                  </tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Top 20 Bưu Cục Rớt LC -->
      <div class="report-card">
        <div class="report-card-header">
          <div class="report-card-title">
            <i data-lucide="alert-octagon" style="color: var(--color-red);"></i>
            DANH SÁCH TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LUÂN CHUYỂN CAO NHẤT (W35)
          </div>
          <span class="badge-tag badge-tag-red">≥5% Nghiêm Trọng | 2–5% Cảnh Báo</span>
        </div>
        <div class="report-card-body">
          <div class="table-toolbar">
            <div class="table-search-box">
              <i data-lucide="search" class="table-search-icon" style="width: 14px; height: 14px;"></i>
              <input type="text" id="search-rotlc-bc" class="table-search-input" placeholder="Tìm tên Bưu Cục...">
            </div>
          </div>
          <div class="bi-table-wrap">
            <table class="bi-table" id="table-rot-lc-top-bc">
              <thead>
                <tr>
                  <th class="center" style="width: 50px;">#</th>
                  <th>Bưu Cục</th>
                  <th class="num">Vol Cần LC</th>
                  <th class="num">Vol Rớt LC (đơn)</th>
                  <th class="num" style="background: var(--color-red-bg); font-weight:800; color:#b91c1c;">% Rớt LC (W35)</th>
                  <th class="center">Đánh Giá & Cảnh Báo</th>
                </tr>
              </thead>
              <tbody></tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    """

if tab9_old:
    html = html.replace(tab9_old, tab9_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html all tabs successfully!")
