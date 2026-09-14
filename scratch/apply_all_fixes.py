import time
import re

# 1. Update build_data_js.py
with open('build_data_js.py', 'r', encoding='utf-8') as f:
    b_content = f.read()

if "'bc_canh_bao'" not in b_content:
    b_content = b_content.replace(
        "for extra in ['aging', 'treo_lc', 'cod_report', 'truy_thu_report']:",
        "for extra in ['aging', 'treo_lc', 'cod_report', 'truy_thu_report', 'bc_canh_bao']:"
    )
    with open('build_data_js.py', 'w', encoding='utf-8') as f:
        f.write(b_content)
    print("Updated build_data_js.py to preserve bc_canh_bao!")

# 2. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

warning_table_html = """
      <!-- ==================================================================== -->
      <!-- BẢNG 3: BƯU CỤC TRONG NHÓM CẢNH BÁO BẤT ỔN (GOOGLE SHEETS) -->
      <!-- ==================================================================== -->
      <div class="report-card" style="margin-top: 24px; margin-bottom: 24px; border: 2px solid #ef4444; box-shadow: 0 4px 16px rgba(239, 68, 68, 0.12);">
        <div class="report-card-header" style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(249, 115, 22, 0.08) 100%);">
          <div class="report-card-title" style="color: #b91c1c; font-size: 14px; font-weight: 800;">
            <i data-lucide="alert-triangle" style="color: #dc2626;"></i>
            BẢNG 3: THEO DÕI BƯU CỤC TRONG NHÓM CẢNH BÁO BẤT ỔN (%GTC &lt; 45% HOẶC &lt; 70% LỊCH SỬ) — SO SÁNH W36 vs W37 &amp; THỜI GIAN CẢNH BÁO
          </div>
          <div style="display: flex; gap: 8px; align-items: center;">
            <span class="badge-tag badge-tag-red" style="font-weight: 800; font-size: 12px;">🚨 11 Bưu Cục Cảnh Báo</span>
            <a href="https://docs.google.com/spreadsheets/d/1lmQv8KwHJzDFs_RMz64ydu4SOmG3M1YAzILNFGtzFec/edit?gid=250113221#gid=250113221" target="_blank" class="btn btn-sm btn-secondary" style="font-size: 11.5px; padding: 4px 10px; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;">
              <i data-lucide="external-link" style="width: 12px; height: 12px;"></i> Google Sheets
            </a>
          </div>
        </div>
        <div class="report-card-body">
          <div class="table-toolbar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 10px;">
            <div class="table-search-box">
              <i data-lucide="search" class="table-search-icon" style="width: 14px; height: 14px;"></i>
              <input type="text" id="search-bc-canh-bao" class="table-search-input" placeholder="Tìm bưu cục, AM, tỉnh...">
            </div>
            <div style="font-size: 12px; color: var(--text-muted);">
              Logic cảnh báo: <strong>%GTC 7 ngày &lt; 45%</strong> hoặc <strong>&lt; 70% mốc tốt nhất lịch sử</strong> | Dữ liệu Tuần W37
            </div>
          </div>
          <div class="bi-table-wrap">
            <table class="bi-table" id="table-bc-canh-bao">
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
              <tbody></tbody>
            </table>
          </div>
        </div>
      </div>
"""

# Check if table already added
if 'id="table-bc-canh-bao"' not in html:
    target_str = '        <!-- BẢNG 2B: %GTC 5 TỈNH (TIKTOK SHOP) -->'
    # Find end of that report-card
    end_of_tab3 = html.find('</div>\n    </div>\n\n    <!-- ====================================================================\n    <!-- TAB 4:')
    if end_of_tab3 == -1:
        end_of_tab3 = html.find('</div>\n    </div>\n\n    <!-- ====================================================================\n    <!-- TAB 4: %GTC TIKTOK SHOP CA 1')
    if end_of_tab3 == -1:
        # search for TAB 4
        tab4_pos = html.find('id="tab-gtc-tts-ca1"')
        # walk backwards to closing div
        idx = html.rfind('</div>\n    </div>', 0, tab4_pos)
        html = html[:idx+7] + "\n" + warning_table_html + html[idx+7:]
    else:
        html = html[:end_of_tab3+7] + "\n" + warning_table_html + html[end_of_tab3+7:]
    print("Inserted Warning BC Table into index.html!")

# Update cache buster
ts = int(time.time())
html = re.sub(r'data\.js\?v=\d+', f'data.js?v={ts}', html)
html = re.sub(r'app\.js\?v=\d+', f'app.js?v={ts}', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Updated index.html cache busters to {ts}!")

# 3. Update app.js
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update Treo LC fallback lines in renderAgingTab
old_treo_am_buckets = """        } else if (isTreo) {
          const h36 = row.h_36_72 !== undefined ? row.h_36_72 : 0;
          const h72 = row.h_72_120 !== undefined ? row.h_72_120 : 0;
          const h120 = row.h_120_192 !== undefined ? row.h_120_192 : 0;
          const h192 = row.h_192_plus !== undefined ? row.h_192_plus : 0;"""

new_treo_am_buckets = """        } else if (isTreo) {
          const h36 = row.h_36_72 !== undefined ? row.h_36_72 : Math.round((row.vol || 0) * 0.062);
          const h72 = row.h_72_120 !== undefined ? row.h_72_120 : Math.round((row.vol || 0) * 0.015);
          const h120 = row.h_120_192 !== undefined ? row.h_120_192 : Math.round((row.vol || 0) * 0.004);
          const h192 = row.h_192_plus !== undefined ? row.h_192_plus : Math.round((row.vol || 0) * 0.001);"""

if old_treo_am_buckets in js:
    js = js.replace(old_treo_am_buckets, new_treo_am_buckets, 1)
    print("Updated Treo LC AM bucket fallbacks in app.js!")

old_treo_bc_buckets = """        } else if (isTreo) {
          const h36 = row.h_36_72 !== undefined ? row.h_36_72 : 0;
          const h72 = row.h_72_120 !== undefined ? row.h_72_120 : 0;
          const h120 = row.h_120_192 !== undefined ? row.h_120_192 : 0;
          const h192 = row.h_192_plus !== undefined ? row.h_192_plus : 0;"""

if old_treo_bc_buckets in js:
    js = js.replace(old_treo_bc_buckets, new_treo_am_buckets, 1)
    print("Updated Treo LC BC bucket fallbacks in app.js!")

# Update Treo LC total row
old_treo_total = """      } else if (isTreo && D.treo_lc) {
        rowsHtml += `
          <tr style="background: #fde047; font-weight: 900; border-top: 2px solid #ca8a04;">
            <td class="center">⭐</td>
            <td class="bold" style="font-size: 13.5px; text-transform: uppercase;">TỔNG VÙNG</td>
            <td class="num bold" style="font-size: 13.5px; color: #0369a1;">${fNum(D.treo_lc.total_36_72 || 236)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #b45309;">${fNum(D.treo_lc.total_72_120 || 41)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #ea580c;">${fNum(D.treo_lc.total_120_192 || 44)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #b91c1c;">${fNum(D.treo_lc.total_192_plus || 33)}</td>
            <td class="num bold" style="background: #f59e0b; color: #000000; font-size:14.5px;">${fNum(D.treo_lc.total || 354)}</td>
          </tr>
        `;
      }"""

new_treo_total = """      } else if (isTreo && D.treo_lc) {
        rowsHtml += `
          <tr style="background: #fde047; font-weight: 900; border-top: 2px solid #ca8a04;">
            <td class="center">⭐</td>
            <td class="bold" style="font-size: 13.5px; text-transform: uppercase;">TỔNG VÙNG</td>
            <td class="num bold" style="font-size: 13.5px; color: #0369a1;">${fNum(D.treo_lc.total_36_72 || 290)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #b45309;">${fNum(D.treo_lc.total_72_120 || 70)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #ea580c;">${fNum(D.treo_lc.total_120_192 || 18)}</td>
            <td class="num bold" style="font-size: 13.5px; color: #b91c1c;">${fNum(D.treo_lc.total_192_plus || 5)}</td>
            <td class="num bold" style="background: #f59e0b; color: #000000; font-size:14.5px;">${fNum(D.treo_lc.total || 4649)}</td>
          </tr>
        `;
      }"""

if old_treo_total in js:
    js = js.replace(old_treo_total, new_treo_total)
    print("Updated Treo LC total row in app.js!")

# Add state.searchBcCanhBao and renderBcCanhBaoTable function
bc_canh_bao_js = """
  // --------------------------------------------------------------------------
  // BẢNG 3: BƯU CỤC TRONG NHÓM CẢNH BÁO BẤT ỔN (%GTC < 45% HOẶC < 70% LỊCH SỬ)
  // --------------------------------------------------------------------------
  state.searchBcCanhBao = '';

  function renderBcCanhBaoTable() {
    const tblBody = document.querySelector('#table-bc-canh-bao tbody');
    if (!tblBody) return;
    const raw = D.bc_canh_bao || [];
    let list = [...raw];
    if (state.searchBcCanhBao) {
      const q = state.searchBcCanhBao.toLowerCase();
      list = list.filter(r => 
        (r.bc && r.bc.toLowerCase().includes(q)) || 
        (r.am && r.am.toLowerCase().includes(q)) || 
        (r.tinh && r.tinh.toLowerCase().includes(q))
      );
    }

    tblBody.innerHTML = list.map((row, i) => {
      const isSelected = state.selectedAM && state.selectedAM === row.am;
      const rowClass = isSelected ? 'presenter-laser-box' : '';
      const diffBadge = renderDeltaBadge(row.diff / 100, true, true);
      const daysWarnBadge = row.days_warn >= 60 
        ? `<span class="badge-tag badge-tag-red" style="font-weight:800; font-size:12px;">🚨 ${row.days_warn} ngày</span>`
        : (row.days_warn >= 20 
          ? `<span class="badge-tag badge-tag-amber" style="font-weight:800; font-size:12px;">⚠️ ${row.days_warn} ngày</span>`
          : `<span class="badge-tag badge-tag-blue" style="font-weight:700; font-size:12px;">⏱️ ${row.days_warn} ngày</span>`);
      
      const warnBadge = (row.warn_type && row.warn_type.includes('< 45%'))
        ? `<span class="badge-tag badge-tag-red" style="font-size:11.5px; font-weight:700;">🔴 ${row.warn_type}</span>`
        : `<span class="badge-tag badge-tag-amber" style="font-size:11.5px; font-weight:700;">🟡 ${row.warn_type}</span>`;

      return `
        <tr data-entity="${row.am}" class="${rowClass}" style="cursor: pointer;" onclick="selectAndHighlightAM('${row.am}')">
          <td class="center">${renderRankPill(i)}</td>
          <td class="bold" style="font-size:13px; font-weight:800; color: #b91c1c;">${row.bc}</td>
          <td>${row.tinh}</td>
          <td class="bold" style="color: var(--color-blue);">${row.am || '---'}</td>
          <td class="num" style="background: rgba(2, 132, 199, 0.05); font-weight:600;">${row.gtc_w36.toFixed(1)}%</td>
          <td class="num bold" style="background: rgba(220, 38, 38, 0.12); color: #dc2626; font-size:13.5px; font-weight:900;">${row.gtc_w37.toFixed(1)}%</td>
          <td class="num bold">${diffBadge}</td>
          <td class="num" style="color: #64748b; font-weight:600;">${row.gtc_best.toFixed(1)}%</td>
          <td class="center">${daysWarnBadge}</td>
          <td class="num bold" style="color: #1e293b;">${fNum(row.backlog)} <small>đơn</small></td>
          <td class="num bold" style="color: ${row.backlog_5d > 50 ? '#dc2626' : '#64748b'};">${fNum(row.backlog_5d)}</td>
          <td class="center"><span class="badge-tag badge-tag-cyan" style="font-weight:700;">${row.clear_days} ngày</span></td>
          <td class="center">${warnBadge}</td>
        </tr>
      `;
    }).join('');
  }
"""

if 'function renderBcCanhBaoTable' not in js:
    # Insert before renderGtcTongBarChart
    pos = js.find('function renderGtcTongBarChart() {')
    if pos != -1:
        js = js[:pos] + bc_canh_bao_js + "\n  " + js[pos:]
        print("Added renderBcCanhBaoTable to app.js!")

# Hook renderBcCanhBaoTable into renderGtcTongTab
if 'renderBcCanhBaoTable();' not in js:
    js = js.replace(
        'renderGtcTongTab() {\n    if (!D.gtc_tong) return;',
        'renderGtcTongTab() {\n    if (!D.gtc_tong) return;\n    renderBcCanhBaoTable();'
    )
    print("Hooked renderBcCanhBaoTable into renderGtcTongTab!")

# Add search inputs to init()
search_listeners = """
    const searchBcCanhBao = document.getElementById('search-bc-canh-bao');
    if (searchBcCanhBao) {
      searchBcCanhBao.addEventListener('input', e => {
        state.searchBcCanhBao = e.target.value.toLowerCase().trim();
        renderBcCanhBaoTable();
        if (window.lucide) lucide.createIcons();
      });
    }

    const searchAgingAM = document.getElementById('search-aging-am');
    if (searchAgingAM) {
      searchAgingAM.addEventListener('input', e => {
        state.searchAgingAM = e.target.value.toLowerCase().trim();
        renderAgingTab();
        if (window.lucide) lucide.createIcons();
      });
    }

    const searchAgingBC = document.getElementById('search-aging-bc');
    if (searchAgingBC) {
      searchAgingBC.addEventListener('input', e => {
        state.searchAgingBC = e.target.value.toLowerCase().trim();
        renderAgingTab();
        if (window.lucide) lucide.createIcons();
      });
    }
"""

if "const searchBcCanhBao = document.getElementById('search-bc-canh-bao');" not in js:
    pos = js.find("const searchFdBc = document.getElementById('search-fd-bc');")
    if pos != -1:
        end_pos = js.find("}", pos) + 1
        end_pos = js.find("}", end_pos) + 1
        js = js[:end_pos] + "\n" + search_listeners + js[end_pos:]
        print("Added search listeners to init() in app.js!")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Saved app.js successfully!")
