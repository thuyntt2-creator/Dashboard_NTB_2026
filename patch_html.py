import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Sidebar item
sidebar_item = """                <li class="menu-item" id="nav-tab-ca-report" onclick="switchTab('tab-ca-report', this)">
                    <i class="fa-solid fa-boxes-stacked"></i> Báo cáo Sản lượng Ca
                </li>"""
html = html.replace('<li class="menu-item" id="nav-tab-fd"', sidebar_item + '\n                <li class="menu-item" id="nav-tab-fd"')

# 2. Add Tab Pane
tab_pane = """
            <!-- TAB: BÁO CÁO SẢN LƯỢNG CA -->
            <div id="tab-ca-report" class="content-panel">
                <div class="panel-header">
                    <h2><i class="fa-solid fa-boxes-stacked"></i> Báo cáo Sản lượng theo Ca</h2>
                </div>
                <div style="background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 24px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <h3 style="margin: 0; font-size: 16px; color: #1e293b;">View theo AM</h3>
                        <button class="btn btn-primary" onclick="loadCaReportData()"><i class="fa-solid fa-rotate-right"></i> Tải lại dữ liệu</button>
                    </div>
                    <div class="table-container">
                        <table class="data-table" id="table-ca-report-am">
                            <thead>
                                <tr>
                                    <th>AM</th>
                                    <th style="text-align:right">Hàng Mới Ca 1 (Volume)</th>
                                    <th style="text-align:right">Hàng Mới Ca 1 (GTC)</th>
                                    <th style="text-align:right">Hàng Mới Ca 2 (Volume)</th>
                                    <th style="text-align:right">Hàng Mới Ca 2 (GTC)</th>
                                    <th style="text-align:right">Hàng Tồn (Volume)</th>
                                    <th style="text-align:right">Hàng Tồn (GTC)</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr><td colspan="7" class="text-center">Đang tải dữ liệu...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div style="background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                    <div style="margin-bottom: 15px;">
                        <h3 style="margin: 0; font-size: 16px; color: #1e293b;">View theo Bưu Cục</h3>
                    </div>
                    <div class="table-container">
                        <table class="data-table" id="table-ca-report-bc">
                            <thead>
                                <tr>
                                    <th>AM</th>
                                    <th>Bưu Cục</th>
                                    <th style="text-align:right">Hàng Mới Ca 1 (Volume)</th>
                                    <th style="text-align:right">Hàng Mới Ca 1 (GTC)</th>
                                    <th style="text-align:right">Hàng Mới Ca 2 (Volume)</th>
                                    <th style="text-align:right">Hàng Mới Ca 2 (GTC)</th>
                                    <th style="text-align:right">Hàng Tồn (Volume)</th>
                                    <th style="text-align:right">Hàng Tồn (GTC)</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr><td colspan="8" class="text-center">Đang tải dữ liệu...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
"""
if 'id="tab-ca-report"' not in html:
    html = html.replace('<!-- TAB: CHỈ SỐ FD -->', tab_pane + '\n            <!-- TAB: CHỈ SỐ FD -->')

# 3. Add to JS arrays
html = html.replace("'tab-fd',", "'tab-ca-report',\n                'tab-fd',")
html = html.replace("{ id: 'tab-fd', name: 'Chỉ số FD' },", "{ id: 'tab-ca-report', name: 'Báo cáo Sản lượng Ca' },\n                { id: 'tab-fd', name: 'Chỉ số FD' },")
html = html.replace("'tab-fd': 'Chỉ số FD',", "'tab-ca-report': 'Báo cáo Ca',\n                        'tab-fd': 'Chỉ số FD',")

# 4. Add JS function
js_logic = """
        function loadCaReportData() {
            const tbodyAM = document.querySelector('#table-ca-report-am tbody');
            const tbodyBC = document.querySelector('#table-ca-report-bc tbody');
            
            if(!tbodyAM) return;
            
            tbodyAM.innerHTML = '<tr><td colspan="7" class="text-center"><i class="fa-solid fa-spinner fa-spin"></i> Đang tải dữ liệu...</td></tr>';
            tbodyBC.innerHTML = '<tr><td colspan="8" class="text-center"><i class="fa-solid fa-spinner fa-spin"></i> Đang tải dữ liệu...</td></tr>';
            
            fetch('/api/ca-report')
                .then(res => res.json())
                .then(data => {
                    if (data.error) {
                        tbodyAM.innerHTML = `<tr><td colspan="7" class="text-center" style="color:red">${data.error}</td></tr>`;
                        tbodyBC.innerHTML = `<tr><td colspan="8" class="text-center" style="color:red">${data.error}</td></tr>`;
                        return;
                    }
                    
                    const fmt = (num) => {
                        if(num === null || num === undefined) return 0;
                        return Number(num).toLocaleString('vi-VN');
                    };
                    
                    if (data.by_am && data.by_am.length > 0) {
                        let htmlAM = '';
                        data.by_am.forEach(row => {
                            htmlAM += `<tr>
                                <td><strong>${row['AM'] || ''}</strong></td>
                                <td style="text-align:right">${fmt(row['Hàng Mới Ca 1_Volume'])}</td>
                                <td style="text-align:right">${fmt(row['Hàng Mới Ca 1_Sản Lượng Giao Thành Công'])}</td>
                                <td style="text-align:right">${fmt(row['Hàng Mới Ca 2_Volume'])}</td>
                                <td style="text-align:right">${fmt(row['Hàng Mới Ca 2_Sản Lượng Giao Thành Công'])}</td>
                                <td style="text-align:right">${fmt(row['Hàng Tồn_Volume'])}</td>
                                <td style="text-align:right">${fmt(row['Hàng Tồn_Sản Lượng Giao Thành Công'])}</td>
                            </tr>`;
                        });
                        tbodyAM.innerHTML = htmlAM;
                    } else {
                        tbodyAM.innerHTML = '<tr><td colspan="7" class="text-center">Không có dữ liệu</td></tr>';
                    }
                    
                    if (data.by_bc && data.by_bc.length > 0) {
                        let htmlBC = '';
                        data.by_bc.forEach(row => {
                            htmlBC += `<tr>
                                <td>${row['AM'] || ''}</td>
                                <td><strong>${row['Bưu Cục'] || ''}</strong></td>
                                <td style="text-align:right">${fmt(row['Hàng Mới Ca 1_Volume'])}</td>
                                <td style="text-align:right">${fmt(row['Hàng Mới Ca 1_Sản Lượng Giao Thành Công'])}</td>
                                <td style="text-align:right">${fmt(row['Hàng Mới Ca 2_Volume'])}</td>
                                <td style="text-align:right">${fmt(row['Hàng Mới Ca 2_Sản Lượng Giao Thành Công'])}</td>
                                <td style="text-align:right">${fmt(row['Hàng Tồn_Volume'])}</td>
                                <td style="text-align:right">${fmt(row['Hàng Tồn_Sản Lượng Giao Thành Công'])}</td>
                            </tr>`;
                        });
                        tbodyBC.innerHTML = htmlBC;
                    } else {
                        tbodyBC.innerHTML = '<tr><td colspan="8" class="text-center">Không có dữ liệu</td></tr>';
                    }
                })
                .catch(err => {
                    console.error(err);
                    tbodyAM.innerHTML = '<tr><td colspan="7" class="text-center" style="color:red">Lỗi tải dữ liệu</td></tr>';
                    tbodyBC.innerHTML = '<tr><td colspan="8" class="text-center" style="color:red">Lỗi tải dữ liệu</td></tr>';
                });
        }
"""
if 'function loadCaReportData' not in html:
    html = html.replace('function switchTab(tabId, element) {', js_logic + '\n        function switchTab(tabId, element) {')

# Hook into switchTab to load data if it's the tab-ca-report
hook = """
            if (tabId === 'tab-ca-report') {
                loadCaReportData();
            }
"""
if "if (tabId === 'tab-ca-report')" not in html:
    html = html.replace("if (tabId === 'tab-fd') {", hook + "            if (tabId === 'tab-fd') {")

# Also need to add tab-ca-report permission to default users and roles in app.py
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Patched templates/index.html')
