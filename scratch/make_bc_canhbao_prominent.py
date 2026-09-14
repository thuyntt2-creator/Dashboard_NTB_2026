import re
import time

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add tab button 15. BC Cảnh Báo to nav-list
tab_button = """          <button class="tab-item" data-tab="tab-bc-canhbao" style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(249, 115, 22, 0.12) 100%); border: 1.5px solid #ef4444; color: #dc2626; font-weight: 800; box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);">
            <i data-lucide="alert-triangle" style="color: #dc2626;"></i> 15. BC Cảnh Báo (11 BC)
          </button>"""

if 'data-tab="tab-bc-canhbao"' not in html:
    html = html.replace(
        """          <button class="tab-item" data-tab="tab-commercial">
            <i data-lucide="trending-up"></i> 14. Kinh Doanh & F30
          </button>""",
        """          <button class="tab-item" data-tab="tab-commercial">
            <i data-lucide="trending-up"></i> 14. Kinh Doanh & F30
          </button>\n""" + tab_button
    )
    print("Added Tab 15 button to nav bar!")

# 2. Add full dedicated view for tab-bc-canhbao
dedicated_tab_view = """
    <!-- ==================================================================== -->
    <!-- TAB 15: BƯU CỤC TRONG NHÓM CẢNH BÁO BẤT ỔN (GOOGLE SHEETS) -->
    <!-- ==================================================================== -->
    <div id="tab-bc-canhbao" class="tab-view">
      <!-- Executive Warning Banner -->
      <div class="exec-banner" style="border-left-color: #dc2626; background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(255, 255, 255, 0.95) 100%);">
        <div class="exec-banner-content">
          <div class="exec-banner-icon" style="background: rgba(239, 68, 68, 0.2); color: #dc2626;">
            <i data-lucide="alert-triangle" style="width: 28px; height: 28px;"></i>
          </div>
          <div class="exec-banner-text">
            <h3 style="color: #991b1b;">THEO DÕI ĐIỀU HÀNH 11 BƯU CỤC CẢNH BÁO BẤT ỔN (%GTC &lt; 45% HOẶC &lt; 70% LỊCH SỬ)</h3>
            <p>
              • <strong>Nguồn Dữ Liệu:</strong> Trích xuất trực tiếp từ Google Sheets Bất Ổn Vận Hành (<a href="https://docs.google.com/spreadsheets/d/1lmQv8KwHJzDFs_RMz64ydu4SOmG3M1YAzILNFGtzFec/edit?gid=250113221#gid=250113221" target="_blank" style="color: #dc2626; font-weight: 700;">Link Sheet gốc</a>).<br>
              • <strong>Tiêu Chí Cảnh Báo:</strong> (1) %GTC 7 ngày gần nhất &lt; 45%, hoặc (2) %GTC &lt; 70% mốc kỷ lục tốt nhất lịch sử.<br>
              • <strong>Bưu Cục Cần Cứu Hộ Khẩn Cấp:</strong> <strong>(DNO) Quảng Tín</strong> (%GTC W37 chỉ 18.4%, cảnh báo 99 ngày, backlog 1.077 đơn), <strong>(LDO) Đức Trọng 1</strong> (20.0%, cảnh báo 83 ngày, backlog 1.127 đơn), <strong>(LDO) Xuân Hương - Đà Lạt</strong> (30.2% / giảm sâu -21.4% WoW, backlog 1.738 đơn), <strong>(KHO) Cam Linh</strong> (33.9%, cảnh báo 107 ngày, backlog 2.187 đơn).
            </p>
          </div>
        </div>
        <div class="exec-banner-actions">
          <a href="https://docs.google.com/spreadsheets/d/1lmQv8KwHJzDFs_RMz64ydu4SOmG3M1YAzILNFGtzFec/edit?gid=250113221#gid=250113221" target="_blank" class="btn btn-sm" style="background: #dc2626; color: #ffffff; font-weight: 800; padding: 8px 16px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; border-radius: 6px;">
            <i data-lucide="external-link" style="width: 14px; height: 14px;"></i> Mở Google Sheets
          </a>
        </div>
      </div>

      <!-- 4 Warning KPI Tiles -->
      <div class="kpi-strip" style="margin-bottom: 20px;">
        <div class="kpi-tile kpi-red">
          <div class="kpi-tile-header">Tổng Bưu Cục Cảnh Báo</div>
          <div class="kpi-tile-value" style="color: #dc2626;">11 <small>bưu cục</small></div>
          <div class="kpi-tile-meta"><span class="diff-tag diff-up-bad">10 BC &lt; 45% | 1 BC &lt; 70% kỷ lục</span></div>
        </div>
        <div class="kpi-tile kpi-red">
          <div class="kpi-tile-header">%GTC Thấp Nhất Vùng</div>
          <div class="kpi-tile-value" style="font-size: 20px; color: #dc2626;">18.4%</div>
          <div class="kpi-tile-meta"><span class="diff-tag diff-neutral">(DNO) Quảng Tín (W36: 15.2%)</span></div>
        </div>
        <div class="kpi-tile kpi-amber">
          <div class="kpi-tile-header">Nằm Cảnh Báo Lâu Nhất</div>
          <div class="kpi-tile-value" style="font-size: 20px; color: #d97706;">107 <small>ngày</small></div>
          <div class="kpi-tile-meta"><span class="diff-tag diff-up-bad">(KHO) Cam Linh &amp; Lang Biang 1</span></div>
        </div>
        <div class="kpi-tile kpi-red">
          <div class="kpi-tile-header">Tổng Backlog Điểm Nóng</div>
          <div class="kpi-tile-value" style="color: #dc2626;">13,038 <small>đơn</small></div>
          <div class="kpi-tile-meta"><span class="diff-tag diff-up-bad">1.570 đơn tồn &gt;5 ngày</span></div>
        </div>
      </div>

      <!-- Main Warning Table Card -->
      <div class="report-card" style="border: 2px solid #ef4444; box-shadow: 0 4px 16px rgba(239, 68, 68, 0.12);">
        <div class="report-card-header" style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(249, 115, 22, 0.08) 100%);">
          <div class="report-card-title" style="color: #b91c1c; font-size: 14px; font-weight: 800;">
            <i data-lucide="alert-triangle" style="color: #dc2626;"></i>
            BẢNG CHI TIẾT: 11 BƯU CỤC TRONG DIỆN CẢNH BÁO BẤT ỔN — SO SÁNH W36 vs W37 &amp; SỐ NGÀY NẰM TRONG DANH SÁCH
          </div>
          <div style="display: flex; gap: 8px; align-items: center;">
            <span class="badge-tag badge-tag-red" style="font-weight: 800; font-size: 12px;">🚨 11 Bưu Cục</span>
          </div>
        </div>
        <div class="report-card-body">
          <div class="table-toolbar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 10px;">
            <div class="table-search-box">
              <i data-lucide="search" class="table-search-icon" style="width: 14px; height: 14px;"></i>
              <input type="text" id="search-bc-canhbao-tab" class="table-search-input search-bc-input" placeholder="Tìm bưu cục, AM, tỉnh...">
            </div>
            <div style="font-size: 12px; color: var(--text-muted);">
              Cập nhật đồng bộ trực tiếp từ Google Sheets | Tuần W37
            </div>
          </div>
          <div class="bi-table-wrap">
            <table class="bi-table table-bc-canhbao-grid" id="table-bc-canhbao-tab">
              <thead>
                <tr style="background: #1e3a8a; color: #ffffff;">
                  <th class="center" style="width: 44px; color: #ffffff;">#</th>
                  <th style="color: #ffffff;">Bưu Cục Điểm Nóng</th>
                  <th style="color: #ffffff;">Tỉnh / TP</th>
                  <th style="color: #ffffff;">AM Phụ Trách</th>
                  <th class="num" style="background: #0284c7; color: #ffffff; font-weight: 700;">%GTC W36</th>
                  <th class="num" style="background: #dc2626; color: #ffffff; font-weight: 800;">%GTC W37</th>
                  <th class="num" style="background: #ea580c; color: #ffffff; font-weight: 700;">Biến Động WoW (Δ)</th>
                  <th class="num" style="background: #475569; color: #ffffff;">Mốc Tốt Nhất</th>
                  <th class="center" style="background: #d97706; color: #ffffff; font-weight: 800;">Số Ngày Cảnh Báo (3T)</th>
                  <th class="num" style="background: #334155; color: #ffffff;">Backlog Tồn</th>
                  <th class="num" style="background: #991b1b; color: #ffffff;">Tồn &gt; 5 Ngày</th>
                  <th class="center" style="background: #0d9488; color: #ffffff;">Dự Kiến Clear</th>
                  <th class="center" style="color: #ffffff;">Tiêu Chí Cảnh Báo</th>
                </tr>
              </thead>
              <tbody class="table-bc-canh-bao-body"></tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
"""

# Insert dedicated_tab_view before the closing of main or after tab-commercial
if 'id="tab-bc-canhbao"' not in html:
    pos = html.find('<!-- Modal Excel Upload -->')
    if pos != -1:
        html = html[:pos] + dedicated_tab_view + "\n  " + html[pos:]
        print("Inserted dedicated tab-bc-canhbao view!")

# 3. Add Callout & Table in Tab 1 (Tổng quan)
tab1_table = """
      <!-- CẢNH BÁO BẤT ỔN: BẢNG 11 BƯU CỤC TRONG NHÓM CẢNH BÁO -->
      <div class="report-card" style="margin-top: 24px; margin-bottom: 24px; border: 2px solid #ef4444; box-shadow: 0 4px 16px rgba(239, 68, 68, 0.12);">
        <div class="report-card-header" style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(249, 115, 22, 0.08) 100%);">
          <div class="report-card-title" style="color: #b91c1c; font-size: 14px; font-weight: 800;">
            <i data-lucide="alert-triangle" style="color: #dc2626;"></i>
            🚨 BẢNG THEO DÕI BƯU CỤC TRONG NHÓM CẢNH BÁO BẤT ỔN (%GTC &lt; 45% HOẶC &lt; 70% LỊCH SỬ) — GOOGLE SHEETS
          </div>
          <div style="display: flex; gap: 8px; align-items: center;">
            <span class="badge-tag badge-tag-red" style="font-weight: 800; font-size: 12px;">🚨 11 Bưu Cục Cảnh Báo</span>
            <button onclick="window.switchTabDirect('tab-bc-canhbao')" class="btn btn-sm btn-secondary" style="font-size: 11.5px; padding: 4px 10px; cursor: pointer;">
              Xem Tab Riêng ➔
            </button>
            <a href="https://docs.google.com/spreadsheets/d/1lmQv8KwHJzDFs_RMz64ydu4SOmG3M1YAzILNFGtzFec/edit?gid=250113221#gid=250113221" target="_blank" class="btn btn-sm btn-secondary" style="font-size: 11.5px; padding: 4px 10px; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;">
              <i data-lucide="external-link" style="width: 12px; height: 12px;"></i> Google Sheets
            </a>
          </div>
        </div>
        <div class="report-card-body">
          <div class="table-toolbar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 10px;">
            <div class="table-search-box">
              <i data-lucide="search" class="table-search-icon" style="width: 14px; height: 14px;"></i>
              <input type="text" id="search-bc-canhbao-ov" class="table-search-input search-bc-input" placeholder="Tìm bưu cục, AM, tỉnh...">
            </div>
            <div style="font-size: 12px; color: var(--text-muted);">
              Logic cảnh báo: <strong>%GTC 7 ngày &lt; 45%</strong> hoặc <strong>&lt; 70% mốc tốt nhất lịch sử</strong> | Dữ liệu Tuần W37
            </div>
          </div>
          <div class="bi-table-wrap">
            <table class="bi-table table-bc-canhbao-grid" id="table-bc-canh-bao-overview">
              <thead>
                <tr style="background: #1e3a8a; color: #ffffff;">
                  <th class="center" style="width: 44px; color: #ffffff;">#</th>
                  <th style="color: #ffffff;">Bưu Cục Điểm Nóng</th>
                  <th style="color: #ffffff;">Tỉnh / TP</th>
                  <th style="color: #ffffff;">AM Phụ Trách</th>
                  <th class="num" style="background: #0284c7; color: #ffffff; font-weight: 700;">%GTC W36</th>
                  <th class="num" style="background: #dc2626; color: #ffffff; font-weight: 800;">%GTC W37</th>
                  <th class="num" style="background: #ea580c; color: #ffffff; font-weight: 700;">Biến Động WoW (Δ)</th>
                  <th class="num" style="background: #475569; color: #ffffff;">Mốc Tốt Nhất</th>
                  <th class="center" style="background: #d97706; color: #ffffff; font-weight: 800;">Số Ngày Cảnh Báo (3T)</th>
                  <th class="num" style="background: #334155; color: #ffffff;">Backlog Tồn</th>
                  <th class="num" style="background: #991b1b; color: #ffffff;">Tồn &gt; 5 Ngày</th>
                  <th class="center" style="background: #0d9488; color: #ffffff;">Dự Kiến Clear</th>
                  <th class="center" style="color: #ffffff;">Tiêu Chí Cảnh Báo</th>
                </tr>
              </thead>
              <tbody class="table-bc-canh-bao-body"></tbody>
            </table>
          </div>
        </div>
      </div>
"""

if 'id="table-bc-canh-bao-overview"' not in html:
    # Insert in Tab 1 right before the end of tab-overview
    pos = html.find('</div>\n\n\n    <!-- ====================================================================\n    <!-- TAB 2: SẢN LƯỢNG GIAO')
    if pos == -1:
        pos = html.find('id="tab-volume"')
        pos = html.rfind('</div>', 0, pos)
    if pos != -1:
        html = html[:pos] + tab1_table + "\n    " + html[pos:]
        print("Inserted Warning BC Table into Tab 1 Overview!")

# 4. Add shortcut button in Tab 12 (Aging & Treo LC)
aging_shortcut = """            <button class="btn btn-sm btn-secondary" id="btn-aging-canhbao" onclick="window.switchTabDirect('tab-bc-canhbao')" style="color: #dc2626; font-weight: 800; border-color: #ef4444; background: rgba(239, 68, 68, 0.08);">
              <i data-lucide="alert-triangle" style="width: 14px; height: 14px; color: #dc2626;"></i> 🚨 11 Bưu Cục Cảnh Báo
            </button>"""

if 'id="btn-aging-canhbao"' not in html:
    html = html.replace(
        """            <button class="btn btn-sm btn-secondary" id="btn-aging-compare" onclick="setAgingSegment('compare')">
              <i data-lucide="split" style="width: 14px; height: 14px;"></i> ⚡ Đối Chiếu Song Song Cả 2
            </button>""",
        """            <button class="btn btn-sm btn-secondary" id="btn-aging-compare" onclick="setAgingSegment('compare')">
              <i data-lucide="split" style="width: 14px; height: 14px;"></i> ⚡ Đối Chiếu Song Song Cả 2
            </button>\n""" + aging_shortcut
    )
    print("Added shortcut button to Tab 12!")

# Make sure all tbody in warning tables have class="table-bc-canh-bao-body"
html = html.replace('<table class="bi-table" id="table-bc-canh-bao">\n              <thead>', '<table class="bi-table table-bc-canhbao-grid" id="table-bc-canh-bao">\n              <thead>')
html = re.sub(r'(<table[^>]*id="table-bc-canh-bao"[^>]*>[\s\S]*?)(<tbody>)', r'\1<tbody class="table-bc-canh-bao-body">', html)

# Update cache buster
ts = int(time.time())
html = re.sub(r'data\.js\?v=\d+', f'data.js?v={ts}', html)
html = re.sub(r'app\.js\?v=\d+', f'app.js?v={ts}', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Updated index.html cache busters to {ts}!")
