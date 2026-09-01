import re
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# 1. Replacement for TAB 3 (%GTC Tổng)
new_tab3 = """    <!-- ==================================================================== -->
    <!-- TAB 3: %GTC TỔNG TOÀN MẠNG (W34 vs W35) -->
    <!-- ==================================================================== -->
    <div id="tab-gtc-tong" class="tab-view">
      <div class="exec-banner" style="border-left-color: var(--color-blue);">
        <div class="exec-banner-content">
          <div class="exec-banner-icon" style="background: rgba(37, 99, 235, 0.2); color: var(--color-blue);">
            <i data-lucide="check-circle-2" style="width: 24px; height: 24px;"></i>
          </div>
          <div class="exec-banner-text">
            <h3>PHÂN TÍCH HIỆU SUẤT %GTC TỔNG TOÀN MẠNG THEO 18 AM & 5 TỈNH</h3>
            <p>
              • <strong>%GTC Tổng Toàn Vùng:</strong> Full hàng đạt <strong>58.16%</strong> (-0.10% WoW); Phân khúc TTS đạt <strong>57.72%</strong> (+1.03% WoW).<br>
              • <strong>Top AM dẫn đầu:</strong> <strong>Nguyễn Ngọc Khánh (76.6%)</strong>, <strong>Thái Thị Thanh Thư (70.9%)</strong>, <strong>Nguyễn Duy Long (70.7%)</strong>.<br>
              • <strong>Bứt phá tăng trưởng WoW:</strong> <strong>Lê Minh Lợi</strong> tăng ngoạn mục +12.1% (lên 35.6%); <strong>Trương Quang Linh</strong> tăng +10.7% (lên 17.4%); <strong>Trần Thị Nhung</strong> tăng +2.6% (lên 59.9%).<br>
              • <strong>Nhóm AM cần cải thiện GTC:</strong> <strong>Trầm Hữu Tiến (34.1%)</strong>, <strong>Lê Văn Trường (44.5%)</strong>, <strong>Hồng Bích Nga (46.3%)</strong>, <strong>Nguyễn Thanh Long (46.9%)</strong>.
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-blue" style="font-size: 12px; padding: 6px 12px;">
            Target %GTC Tổng ≥ 60.0%
          </span>
        </div>
      </div>

      <!-- Segment Selector: Full Hàng vs TikTok Shop (TTS) -->
      <div class="view-mode-bar" style="margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; background: var(--bg-surface); padding: 12px 16px; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 12px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">PHÂN KHÚC HIỂN THỊ:</span>
          <div class="btn-group" id="gtc-tong-segment-group">
            <button class="btn btn-sm btn-primary active" id="btn-gtctong-full" onclick="setGtcTongSegment('full')">
              <i data-lucide="package" style="width: 14px; height: 14px;"></i> 📦 Full Hàng (Toàn Trình)
            </button>
            <button class="btn btn-sm btn-secondary" id="btn-gtctong-tts" onclick="setGtcTongSegment('tts')">
              <i data-lucide="award" style="width: 14px; height: 14px;"></i> 🛍️ TikTok Shop (TTS)
            </button>
          </div>
        </div>

        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 12px; font-weight: 700; color: var(--text-muted);">LỌC ĐỒ THỊ:</span>
          <div class="btn-group">
            <button class="btn btn-sm btn-secondary active" id="btn-gtctong-hl-all" onclick="setGtcTongHighlight('all')">Tất Cả</button>
            <button class="btn btn-sm btn-secondary" id="btn-gtctong-hl-grow" onclick="setGtcTongHighlight('grow')">🟢 Tăng Trưởng</button>
            <button class="btn btn-sm btn-secondary" id="btn-gtctong-hl-drop" onclick="setGtcTongHighlight('drop')">🔴 &lt; 50%</button>
          </div>
        </div>
      </div>

      <!-- Chart %GTC Tổng 2 Cột -->
      <div class="report-card" style="margin-bottom: 20px;">
        <div class="report-card-header">
          <div class="report-card-title">
            <i data-lucide="bar-chart-3" style="color: var(--color-blue);"></i>
            <span id="chart-gtc-tong-title">BIỂU ĐỒ SO SÁNH %GTC TỔNG W34 vs W35 THEO 18 AM (FULL HÀNG)</span>
          </div>
          <span class="badge-tag badge-tag-blue" id="badge-gtc-tong-segment">Full Hàng</span>
        </div>
        <div class="report-card-body">
          <div class="chart-box chart-box-tall">
            <canvas id="chart-gtc-tong-bar"></canvas>
          </div>
        </div>
      </div>

      <!-- 2 Bảng Đối Xứng: 18 AM (Trái) vs 5 Tỉnh (Phải) -->
      <div class="grid-row-2">
        <!-- Bảng 1: %GTC 18 AM -->
        <div class="report-card">
          <div class="report-card-header">
            <div class="report-card-title">
              <i data-lucide="table-properties" style="color: var(--color-blue);"></i>
              <span id="table-gtctong-am-title">BẢNG 1: %GTC TỔNG THEO 18 AM (FULL HÀNG)</span>
            </div>
            <span class="badge-tag badge-tag-blue">18 AM</span>
          </div>
          <div class="report-card-body">
            <div class="table-toolbar">
              <div class="table-search-box">
                <i data-lucide="search" class="table-search-icon" style="width: 14px; height: 14px;"></i>
                <input type="text" id="search-gtctong-am" class="table-search-input" placeholder="Tìm tên AM...">
              </div>
            </div>
            <div class="bi-table-wrap">
              <table class="bi-table" id="table-gtc-tong-detailed">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>AM Phụ Trách</th>
                    <th class="num">Sản Lượng</th>
                    <th class="num">W32</th>
                    <th class="num">W33</th>
                    <th class="num">W34</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">%GTC W35</th>
                    <th class="num">Biến Động (Δ)</th>
                    <th class="center">Đánh Giá SLA</th>
                  </tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Bảng 2: %GTC 5 Tỉnh Thành -->
        <div class="report-card">
          <div class="report-card-header">
            <div class="report-card-title">
              <i data-lucide="map-pin" style="color: var(--ghn-navy);"></i>
              <span id="table-gtctong-tinh-title">BẢNG 2: %GTC TỔNG THEO 5 TỈNH THÀNH (FULL HÀNG)</span>
            </div>
            <span class="badge-tag badge-tag-blue">5 Tỉnh Thành</span>
          </div>
          <div class="report-card-body">
            <div class="bi-table-wrap">
              <table class="bi-table" id="table-gtc-tinh-detailed">
                <thead>
                  <tr>
                    <th class="center" style="width: 44px;">#</th>
                    <th>Tỉnh / Thành Phố</th>
                    <th class="num">Sản Lượng</th>
                    <th class="num">W32</th>
                    <th class="num">W33</th>
                    <th class="num">W34</th>
                    <th class="num" style="background: var(--color-blue-bg); font-weight: 800;">%GTC W35</th>
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

# Replace from TAB 3 start to TAB 4 start
p_tab3 = html.find('<!-- TAB 3: %GTC TỔNG TOÀN MẠNG')
p_tab4 = html.find('<!-- ====================================================================\n    <!-- TAB 4: %GTC TIKTOK SHOP CA 1')
if p_tab4 == -1:
    p_tab4 = html.find('<!-- TAB 4: %GTC TIKTOK SHOP CA 1')
    # search back for delimiter
    p_tab4 = html.rfind('<!-- ===', 0, p_tab4)

print(f"p_tab3={p_tab3}, p_tab4={p_tab4}")
if p_tab3 != -1 and p_tab4 != -1:
    html = html[:p_tab3] + new_tab3 + '\n    ' + html[p_tab4:]

# 2. Fix broken OPR comment
html = html.replace('</div>ng Chi Tiết OPR TTS -->', '<!-- Bảng Chi Tiết OPR TTS -->')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully!")
