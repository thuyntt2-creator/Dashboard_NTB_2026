# -*- coding: utf-8 -*-
import os

target_file = r"c:\Users\lap4all\Desktop\New folder\templates\index.html"

with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "        function renderCaTable() {"
end_marker = "        // Hook: auto-load CA report when tab is opened"

if start_marker not in content:
    raise ValueError(f"Could not find start marker: {start_marker}")
if end_marker not in content:
    raise ValueError(f"Could not find end marker: {end_marker}")

pre_content = content[:content.index(start_marker)]
post_content = content[content.index(end_marker):]

new_function = '''        function sortIcon(colKey) {
            if (caReportSortKey === colKey) {
                return caReportSortAsc ? '<i class="fa-solid fa-sort-up" style="color:#2563eb;font-size:11px;margin-left:4px;"></i>' : '<i class="fa-solid fa-sort-down" style="color:#2563eb;font-size:11px;margin-left:4px;"></i>';
            }
            return '<i class="fa-solid fa-sort" style="color:#cbd5e1;font-size:10px;margin-left:4px;"></i>';
        }

        function renderCaTable() {
            const tbody = document.getElementById('ca-table-body');
            const thead = document.getElementById('ca-table-thead');
            if (!tbody) return;

            const groupbySelect = document.getElementById('ca-filter-groupby');
            const groupby = groupbySelect ? groupbySelect.value : 'bc';
            
            const viewModeSelect = document.getElementById('ca-filter-view-mode');
            const viewMode = viewModeSelect ? viewModeSelect.value : 'all'; // 'all' or 'gtc_only'

            const dateSelect = document.getElementById('ca-filter-date');
            const selectedDate = dateSelect ? dateSelect.value : '';

            // Handle display/updating of compare date controls
            const compareContainer = document.getElementById('ca-compare-container');
            const compareSelect = document.getElementById('ca-compare-date');
            let compareDate = '';

            if (selectedDate) {
                if (compareContainer) compareContainer.style.display = 'flex';
                if (window.lastSelectedCaDate !== selectedDate) {
                    window.lastSelectedCaDate = selectedDate;
                    updateCompareDateOptions(selectedDate, window.caReportUniqueDates || []);
                }
                compareDate = compareSelect ? compareSelect.value : '';
            } else {
                if (compareContainer) compareContainer.style.display = 'none';
                if (compareSelect) compareSelect.value = '';
                window.lastSelectedCaDate = '';
            }
            
            const amSelect = document.getElementById('ca-filter-am');
            const selectedAm = amSelect ? amSelect.value : '';

            const bcSelect = document.getElementById('ca-filter-bc');
            const selectedBc = bcSelect ? bcSelect.value : '';
            
            const query = (document.getElementById('ca-search-input') || {}).value || '';
            const q = query.toLowerCase().trim();

            // Toggle legend display according to viewMode
            const legendPills = document.getElementById('ca-legend-pills');
            const legendGtcPill = document.getElementById('ca-legend-gtc-pill');
            if (legendPills && legendGtcPill) {
                if (viewMode === 'gtc_only') {
                    legendPills.style.display = 'none';
                    legendGtcPill.style.display = 'flex';
                } else {
                    legendPills.style.display = 'flex';
                    legendGtcPill.style.display = 'none';
                }
            }

            // 1. Filter raw daily rows for current date
            let filteredRaw = caReportRawRows.filter(r => {
                if (selectedDate && r.Date !== selectedDate) return false;
                if (selectedAm && r.AM !== selectedAm) return false;
                if (selectedBc && r['Bưu Cục'] !== selectedBc) return false;
                return true;
            });

            // Filter raw daily rows for comparison date if active
            let compareRaw = [];
            if (selectedDate && compareDate) {
                compareRaw = caReportRawRows.filter(r => {
                    if (r.Date !== compareDate) return false;
                    if (selectedAm && r.AM !== selectedAm) return false;
                    if (selectedBc && r['Bưu Cục'] !== selectedBc) return false;
                    return true;
                });
            }

            // 2. Aggregate comparison date data by Group By dimension
            const compareAggregated = {};
            if (selectedDate && compareDate) {
                compareRaw.forEach(r => {
                    const key = groupby === 'am' ? (r.AM || 'Không xác định') : (r['Bưu Cục'] || 'Không xác định');
                    if (!compareAggregated[key]) {
                        compareAggregated[key] = {
                            v1: 0, g1: 0, a1: 0,
                            v2: 0, g2: 0, a2: 0,
                            v3: 0, g3: 0, a3: 0
                        };
                    }
                    compareAggregated[key].v1 += r['Hàng Mới Ca 1_Volume'] || 0;
                    compareAggregated[key].g1 += r['Hàng Mới Ca 1_Sản Lượng Giao Thành Công'] || 0;
                    compareAggregated[key].a1 += r['Hàng Mới Ca 1_Assigned_Vol'] || 0;
                    compareAggregated[key].v2 += r['Hàng Mới Ca 2_Volume'] || 0;
                    compareAggregated[key].g2 += r['Hàng Mới Ca 2_Sản Lượng Giao Thành Công'] || 0;
                    compareAggregated[key].a2 += r['Hàng Mới Ca 2_Assigned_Vol'] || 0;
                    compareAggregated[key].v3 += r['Hàng Tồn_Volume'] || 0;
                    compareAggregated[key].g3 += r['Hàng Tồn_Sản Lượng Giao Thành Công'] || 0;
                    compareAggregated[key].a3 += r['Hàng Tồn_Assigned_Vol'] || 0;
                });
            }

            // 3. Aggregate current date data by Group By dimension
            const aggregated = {};
            filteredRaw.forEach(r => {
                const key = groupby === 'am' ? (r.AM || 'Không xác định') : (r['Bưu Cục'] || 'Không xác định');
                if (!aggregated[key]) {
                    aggregated[key] = {
                        name: key,
                        am: groupby === 'am' ? '' : (r.AM || ''),
                        v1: 0, g1: 0, a1: 0,
                        v2: 0, g2: 0, a2: 0,
                        v3: 0, g3: 0, a3: 0
                    };
                }
                aggregated[key].v1 += r['Hàng Mới Ca 1_Volume'] || 0;
                aggregated[key].g1 += r['Hàng Mới Ca 1_Sản Lượng Giao Thành Công'] || 0;
                aggregated[key].a1 += r['Hàng Mới Ca 1_Assigned_Vol'] || 0;
                aggregated[key].v2 += r['Hàng Mới Ca 2_Volume'] || 0;
                aggregated[key].g2 += r['Hàng Mới Ca 2_Sản Lượng Giao Thành Công'] || 0;
                aggregated[key].a2 += r['Hàng Mới Ca 2_Assigned_Vol'] || 0;
                aggregated[key].v3 += r['Hàng Tồn_Volume'] || 0;
                aggregated[key].g3 += r['Hàng Tồn_Sản Lượng Giao Thành Công'] || 0;
                aggregated[key].a3 += r['Hàng Tồn_Assigned_Vol'] || 0;
            });

            let displayRows = Object.values(aggregated).map(r => {
                const total_v = r.v1 + r.v2 + r.v3;
                const total_g = r.g1 + r.g2 + r.g3;
                const total_a = r.a1 + r.a2 + r.a3;
                
                const p1 = r.v1 > 0 ? (r.g1 / r.v1 * 100) : null;
                const gan1 = r.v1 > 0 ? (r.a1 / r.v1 * 100) : null;
                const p2 = r.v2 > 0 ? (r.g2 / r.v2 * 100) : null;
                const gan2 = r.v2 > 0 ? (r.a2 / r.v2 * 100) : null;
                const p3 = r.v3 > 0 ? (r.g3 / r.v3 * 100) : null;
                const gan3 = r.v3 > 0 ? (r.a3 / r.v3 * 100) : null;
                const total_p = total_v > 0 ? (total_g / total_v * 100) : null;
                const total_gan = total_v > 0 ? (total_a / total_v * 100) : null;

                // Handle comparison diffs
                let diff_v1 = null, diff_g1 = null, diff_gan1 = null, diff_p1 = null;
                let diff_v2 = null, diff_g2 = null, diff_gan2 = null, diff_p2 = null;
                let diff_v3 = null, diff_g3 = null, diff_gan3 = null, diff_p3 = null;
                let diff_total_v = null, diff_total_g = null, diff_total_a = null, diff_total_gan = null, diff_total_p = null;

                if (selectedDate && compareDate) {
                    const comp = compareAggregated[r.name] || {
                        v1: 0, g1: 0, a1: 0,
                        v2: 0, g2: 0, a2: 0,
                        v3: 0, g3: 0, a3: 0
                    };
                    const comp_total_v = comp.v1 + comp.v2 + comp.v3;
                    const comp_total_g = comp.g1 + comp.g2 + comp.g3;
                    const comp_total_a = comp.a1 + comp.a2 + comp.a3;

                    const comp_p1 = comp.v1 > 0 ? (comp.g1 / comp.v1 * 100) : null;
                    const comp_gan1 = comp.v1 > 0 ? (comp.a1 / comp.v1 * 100) : null;
                    const comp_p2 = comp.v2 > 0 ? (comp.g2 / comp.v2 * 100) : null;
                    const comp_gan2 = comp.v2 > 0 ? (comp.a2 / comp.v2 * 100) : null;
                    const comp_p3 = comp.v3 > 0 ? (comp.g3 / comp.v3 * 100) : null;
                    const comp_gan3 = comp.v3 > 0 ? (comp.a3 / comp.v3 * 100) : null;
                    const comp_total_p = comp_total_v > 0 ? (comp_total_g / comp_total_v * 100) : null;
                    const comp_total_gan = comp_total_v > 0 ? (comp_total_a / comp_total_v * 100) : null;

                    diff_v1 = r.v1 - comp.v1;
                    diff_g1 = r.g1 - comp.g1;
                    diff_p1 = (p1 !== null && comp_p1 !== null) ? (p1 - comp_p1) : null;
                    diff_gan1 = (gan1 !== null && comp_gan1 !== null) ? (gan1 - comp_gan1) : null;

                    diff_v2 = r.v2 - comp.v2;
                    diff_g2 = r.g2 - comp.g2;
                    diff_p2 = (p2 !== null && comp_p2 !== null) ? (p2 - comp_p2) : null;
                    diff_gan2 = (gan2 !== null && comp_gan2 !== null) ? (gan2 - comp_gan2) : null;

                    diff_v3 = r.v3 - comp.v3;
                    diff_g3 = r.g3 - comp.g3;
                    diff_p3 = (p3 !== null && comp_p3 !== null) ? (p3 - comp_p3) : null;
                    diff_gan3 = (gan3 !== null && comp_gan3 !== null) ? (gan3 - comp_gan3) : null;

                    diff_total_v = total_v - comp_total_v;
                    diff_total_g = total_g - comp_total_g;
                    diff_total_a = total_a - comp_total_a;
                    diff_total_p = (total_p !== null && comp_total_p !== null) ? (total_p - comp_total_p) : null;
                    diff_total_gan = (total_gan !== null && comp_total_gan !== null) ? (total_gan - comp_total_gan) : null;
                }

                return {
                    name: r.name,
                    am: r.am,
                    v1: r.v1, g1: r.g1, a1: r.a1, p1: p1, gan1: gan1,
                    v2: r.v2, g2: r.g2, a2: r.a2, p2: p2, gan2: gan2,
                    v3: r.v3, g3: r.g3, a3: r.a3, p3: p3, gan3: gan3,
                    total_v: total_v,
                    total_g: total_g,
                    total_a: total_a,
                    total_p: total_p,
                    total_gan: total_gan,
                    // Diffs
                    diff_v1, diff_g1, diff_p1, diff_gan1,
                    diff_v2, diff_g2, diff_p2, diff_gan2,
                    diff_v3, diff_g3, diff_p3, diff_gan3,
                    diff_total_v, diff_total_g, diff_total_a, diff_total_p, diff_total_gan
                };
            });

            // 4. Apply search text query on aggregated rows
            if (q) {
                displayRows = displayRows.filter(r => {
                    return r.name.toLowerCase().includes(q) || (r.am && r.am.toLowerCase().includes(q));
                });
            }

            // 5. Update KPI cards based on filtered dataset and viewMode
            const totalV1 = filteredRaw.reduce((s, r) => s + (r['Hàng Mới Ca 1_Volume'] || 0), 0);
            const totalV2 = filteredRaw.reduce((s, r) => s + (r['Hàng Mới Ca 2_Volume'] || 0), 0);
            const totalV3 = filteredRaw.reduce((s, r) => s + (r['Hàng Tồn_Volume'] || 0), 0);
            const grandTotalV = displayRows.reduce((s, r) => s + r.total_v, 0);
            const grandTotalG = displayRows.reduce((s, r) => s + r.total_g, 0);
            const grandTotalA = displayRows.reduce((s, r) => s + r.total_a, 0);
            const grandTotalP = grandTotalV > 0 ? (grandTotalG / grandTotalV * 100) : 0;
            const grandTotalGan = grandTotalV > 0 ? (grandTotalA / grandTotalV * 100) : 0;

            const el = id => document.getElementById(id);
            if (viewMode === 'gtc_only') {
                if (el('ca-kpi-title1')) el('ca-kpi-title1').innerText = 'Tổng Volume';
                if (el('ca-kpi-vol1')) el('ca-kpi-vol1').innerText = grandTotalV.toLocaleString('vi-VN');

                if (el('ca-kpi-title2')) el('ca-kpi-title2').innerText = 'Tổng Gán';
                if (el('ca-kpi-vol2')) el('ca-kpi-vol2').innerHTML = `${grandTotalA.toLocaleString('vi-VN')} <span style="font-size:14px;font-weight:600;color:#64748b;">(${grandTotalGan.toFixed(1)}%)</span>`;

                if (el('ca-kpi-title3')) el('ca-kpi-title3').innerText = '🏆 Tổng GTC Bưu Cục';
                if (el('ca-kpi-vol3')) el('ca-kpi-vol3').innerHTML = `${grandTotalG.toLocaleString('vi-VN')} <span style="font-size:14px;font-weight:700;color:#10b981;">(${grandTotalP.toFixed(1)}%)</span>`;

                if (el('ca-kpi-title4')) el('ca-kpi-title4').innerText = groupby === 'am' ? 'Số AM' : 'Số Bưu cục';
                if (el('ca-kpi-bc-count')) el('ca-kpi-bc-count').innerText = displayRows.length;
            } else {
                if (el('ca-kpi-title1')) el('ca-kpi-title1').innerText = 'Tổng Vol Ca 1';
                if (el('ca-kpi-vol1')) el('ca-kpi-vol1').innerText = totalV1.toLocaleString('vi-VN');

                if (el('ca-kpi-title2')) el('ca-kpi-title2').innerText = 'Tổng Vol Ca 2';
                if (el('ca-kpi-vol2')) el('ca-kpi-vol2').innerText = totalV2.toLocaleString('vi-VN');

                if (el('ca-kpi-title3')) el('ca-kpi-title3').innerText = 'Tổng Vol Hàng Tồn';
                if (el('ca-kpi-vol3')) el('ca-kpi-vol3').innerText = totalV3.toLocaleString('vi-VN');

                if (el('ca-kpi-title4')) el('ca-kpi-title4').innerText = groupby === 'am' ? 'Số AM' : 'Số Bưu cục';
                if (el('ca-kpi-bc-count')) el('ca-kpi-bc-count').innerText = displayRows.length;
            }

            // 6. Sort
            const key = caReportSortKey;
            displayRows.sort((a, b) => {
                let av = a[key], bv = b[key];
                if (typeof av === 'string') av = av.toLowerCase();
                if (typeof bv === 'string') bv = bv.toLowerCase();
                if (av === null) av = -Infinity;
                if (bv === null) bv = -Infinity;
                return caReportSortAsc ? (av > bv ? 1 : -1) : (av < bv ? 1 : -1);
            });

            const rowCount = document.getElementById('ca-row-count');
            if (rowCount) rowCount.innerText = `${displayRows.length} ${groupby === 'am' ? 'AM' : 'bưu cục'}`;

            // 7. Render dynamic <thead>
            if (thead) {
                if (viewMode === 'gtc_only') {
                    thead.innerHTML = `
                        <tr style="background:#f8fafc; position:sticky; top:0; z-index:5;">
                            <th style="padding:12px 14px; text-align:left; font-weight:700; color:#334155; border-bottom:2px solid #cbd5e1; cursor:pointer;" onclick="sortCaTable('bc')">
                                ${groupby === 'am' ? 'AM' : 'Bưu Cục'} ${sortIcon('name')}
                            </th>
                            <th style="padding:12px 12px; text-align:right; font-weight:700; color:#334155; border-bottom:2px solid #cbd5e1; cursor:pointer;" onclick="sortCaTable('total_v')">
                                Tổng Volume ${sortIcon('total_v')}
                            </th>
                            <th style="padding:12px 12px; text-align:right; font-weight:700; color:#475569; border-bottom:2px solid #cbd5e1; cursor:pointer;" onclick="sortCaTable('total_a')">
                                Tổng Gán ${sortIcon('total_a')}
                            </th>
                            <th style="padding:12px 12px; text-align:right; font-weight:700; color:#475569; border-bottom:2px solid #cbd5e1; cursor:pointer;" onclick="sortCaTable('total_gan')">
                                % Gán ${sortIcon('total_gan')}
                            </th>
                            <th style="padding:12px 14px; text-align:right; font-weight:800; color:#065f46; border-bottom:2px solid #cbd5e1; background:#ecfdf5; cursor:pointer; font-size:13px;" onclick="sortCaTable('total_g')">
                                🏆 GTC Tổng ${sortIcon('total_g')}
                            </th>
                            <th style="padding:12px 12px; text-align:right; font-weight:700; color:#065f46; border-bottom:2px solid #cbd5e1; background:#ecfdf5; cursor:pointer;" onclick="sortCaTable('total_p')">
                                % GTC ${sortIcon('total_p')}
                            </th>
                        </tr>`;
                } else {
                    thead.innerHTML = `
                        <tr style="background:#f8fafc; position:sticky; top:0; z-index:5;">
                            <th style="padding:10px 14px; text-align:left; font-weight:700; color:#475569; border-bottom:2px solid #e2e8f0; white-space:nowrap; cursor:pointer;" onclick="sortCaTable('bc')" id="ca-th-bc">
                                ${groupby === 'am' ? 'AM' : 'Bưu Cục'} ${sortIcon('name')}
                            </th>
                            <th style="padding:10px 8px; text-align:center; font-weight:700; color:#6366f1; border-bottom:2px solid #e2e8f0; background:#f0f0ff; white-space:nowrap;" colspan="4">🌅 Hàng Mới Ca 1</th>
                            <th style="padding:10px 8px; text-align:center; font-weight:700; color:#10b981; border-bottom:2px solid #e2e8f0; background:#f0fdf4; white-space:nowrap;" colspan="4">🌆 Hàng Mới Ca 2</th>
                            <th style="padding:10px 8px; text-align:center; font-weight:700; color:#d97706; border-bottom:2px solid #e2e8f0; background:#fffbeb; white-space:nowrap;" colspan="4">📦 Hàng Tồn</th>
                            <th style="padding:10px 8px; text-align:center; font-weight:700; color:#475569; border-bottom:2px solid #e2e8f0; background:#f1f5f9; white-space:nowrap;" colspan="4">📊 Tổng cộng</th>
                        </tr>
                        <tr style="background:#f8fafc; position:sticky; top:40px; z-index:5;">
                            <th style="padding:6px 14px; text-align:left; font-weight:600; font-size:11px; color:#94a3b8; border-bottom:1px solid #e2e8f0;"></th>
                            <th style="padding:6px 8px; text-align:right; font-weight:600; font-size:11px; color:#6366f1; border-bottom:1px solid #e2e8f0; background:#f5f5ff; cursor:pointer;" onclick="sortCaTable('v1')">Vol ${sortIcon('v1')}</th>
                            <th style="padding:6px 8px; text-align:right; font-weight:600; font-size:11px; color:#6366f1; border-bottom:1px solid #e2e8f0; background:#f5f5ff; cursor:pointer;" onclick="sortCaTable('gan1')">% Gán ${sortIcon('gan1')}</th>
                            <th style="padding:6px 8px; text-align:right; font-weight:600; font-size:11px; color:#6366f1; border-bottom:1px solid #e2e8f0; background:#f5f5ff; cursor:pointer;" onclick="sortCaTable('g1')">GTC ${sortIcon('g1')}</th>
                            <th style="padding:6px 8px; text-align:right; font-weight:600; font-size:11px; color:#6366f1; border-bottom:1px solid #e2e8f0; background:#f5f5ff; cursor:pointer;" onclick="sortCaTable('p1')">%GTC ${sortIcon('p1')}</th>
                            <th style="padding:6px 8px; text-align:right; font-weight:600; font-size:11px; color:#10b981; border-bottom:1px solid #e2e8f0; background:#f0fdf4; cursor:pointer;" onclick="sortCaTable('v2')">Vol ${sortIcon('v2')}</th>
                            <th style="padding:6px 8px; text-align:right; font-weight:600; font-size:11px; color:#10b981; border-bottom:1px solid #e2e8f0; background:#f0fdf4; cursor:pointer;" onclick="sortCaTable('gan2')">% Gán ${sortIcon('gan2')}</th>
                            <th style="padding:6px 8px; text-align:right; font-weight:600; font-size:11px; color:#10b981; border-bottom:1px solid #e2e8f0; background:#f0fdf4; cursor:pointer;" onclick="sortCaTable('g2')">GTC ${sortIcon('g2')}</th>
                            <th style="padding:6px 8px; text-align:right; font-weight:600; font-size:11px; color:#10b981; border-bottom:1px solid #e2e8f0; background:#f0fdf4; cursor:pointer;" onclick="sortCaTable('p2')">%GTC ${sortIcon('p2')}</th>
                            <th style="padding:6px 8px; text-align:right; font-weight:600; font-size:11px; color:#d97706; border-bottom:1px solid #e2e8f0; background:#fef9ec; cursor:pointer;" onclick="sortCaTable('v3')">Vol ${sortIcon('v3')}</th>
                            <th style="padding:6px 8px; text-align:right; font-weight:600; font-size:11px; color:#d97706; border-bottom:1px solid #e2e8f0; background:#fef9ec; cursor:pointer;" onclick="sortCaTable('gan3')">% Gán ${sortIcon('gan3')}</th>
                            <th style="padding:6px 8px; text-align:right; font-weight:600; font-size:11px; color:#d97706; border-bottom:1px solid #e2e8f0; background:#fef9ec; cursor:pointer;" onclick="sortCaTable('g3')">GTC ${sortIcon('g3')}</th>
                            <th style="padding:6px 8px; text-align:right; font-weight:600; font-size:11px; color:#d97706; border-bottom:1px solid #e2e8f0; background:#fef9ec; cursor:pointer;" onclick="sortCaTable('p3')">%GTC ${sortIcon('p3')}</th>
                            <th style="padding:6px 8px; text-align:right; font-weight:600; font-size:11px; color:#475569; border-bottom:1px solid #e2e8f0; background:#f1f5f9; cursor:pointer;" onclick="sortCaTable('total_v')">Vol ${sortIcon('total_v')}</th>
                            <th style="padding:6px 8px; text-align:right; font-weight:600; font-size:11px; color:#475569; border-bottom:1px solid #e2e8f0; background:#f1f5f9; cursor:pointer;" onclick="sortCaTable('total_gan')">% Gán ${sortIcon('total_gan')}</th>
                            <th style="padding:6px 8px; text-align:right; font-weight:600; font-size:11px; color:#475569; border-bottom:1px solid #e2e8f0; background:#f1f5f9; cursor:pointer;" onclick="sortCaTable('total_g')">GTC ${sortIcon('total_g')}</th>
                            <th style="padding:6px 8px; text-align:right; font-weight:600; font-size:11px; color:#475569; border-bottom:1px solid #e2e8f0; background:#f1f5f9; cursor:pointer;" onclick="sortCaTable('total_p')">%GTC ${sortIcon('total_p')}</th>
                        </tr>`;
                }
            }

            if (displayRows.length === 0) {
                const colSpan = viewMode === 'gtc_only' ? 6 : 17;
                tbody.innerHTML = `<tr><td colspan="${colSpan}" style="text-align:center;padding:30px;color:#94a3b8;">Không tìm thấy dữ liệu</td></tr>`;
                return;
            }

            const cellStyle = (bg, extra = '') => `style="padding:8px 10px;text-align:right;border-bottom:1px solid #f1f5f9;background:${bg};font-variant-numeric:tabular-nums;${extra}"`;
            let html = '';

            displayRows.forEach((r, i) => {
                const rowBg = i % 2 === 0 ? '' : '#fafbfc';
                if (viewMode === 'gtc_only') {
                    html += `<tr style="background:${rowBg};">
                        <td style="padding:10px 14px;border-bottom:1px solid #f1f5f9;font-weight:600;color:#1e293b;max-width:280px;word-break:break-word;">
                            ${r.name}
                            ${r.am ? `<div style="font-size:11px;color:#94a3b8;font-weight:400;margin-top:2px;"><i class="fa-solid fa-user" style="font-size:9px;"></i> ${r.am}</div>` : ''}
                        </td>
                        <td style="padding:10px 12px;text-align:right;border-bottom:1px solid #f1f5f9;font-weight:600;color:#1e293b;font-variant-numeric:tabular-nums;">
                            ${r.total_v.toLocaleString('vi-VN')}${formatDiff(r.diff_total_v)}
                        </td>
                        <td style="padding:10px 12px;text-align:right;border-bottom:1px solid #f1f5f9;color:#475569;font-variant-numeric:tabular-nums;">
                            ${r.total_a.toLocaleString('vi-VN')}
                        </td>
                        <td style="padding:10px 12px;text-align:right;border-bottom:1px solid #f1f5f9;font-variant-numeric:tabular-nums;">
                            ${pctBadge(r.total_gan)}${formatDiff(r.diff_total_gan, true)}
                        </td>
                        <td style="padding:10px 14px;text-align:right;border-bottom:1px solid #f1f5f9;font-weight:800;color:#047857;background:#ecfdf5;font-size:14px;font-variant-numeric:tabular-nums;">
                            ${r.total_g.toLocaleString('vi-VN')}${formatDiff(r.diff_total_g)}
                        </td>
                        <td style="padding:10px 12px;text-align:right;border-bottom:1px solid #f1f5f9;background:#ecfdf5;font-variant-numeric:tabular-nums;">
                            ${pctBadge(r.total_p)}${formatDiff(r.diff_total_p, true)}
                        </td>
                    </tr>`;
                } else {
                    html += `<tr style="background:${rowBg};">
                        <td style="padding:8px 14px;border-bottom:1px solid #f1f5f9;font-weight:600;color:#1e293b;max-width:280px;word-break:break-word;">
                            ${r.name}
                            ${r.am ? `<div style="font-size:11px;color:#94a3b8;font-weight:400;margin-top:2px;"><i class="fa-solid fa-user" style="font-size:9px;"></i> ${r.am}</div>` : ''}
                        </td>
                        <td ${cellStyle('#f5f5ff')}>${r.v1.toLocaleString('vi-VN')}${formatDiff(r.diff_v1)}</td>
                        <td ${cellStyle('#f5f5ff')}>${pctBadge(r.gan1)}${formatDiff(r.diff_gan1, true)}</td>
                        <td ${cellStyle('#f5f5ff')}>${r.g1.toLocaleString('vi-VN')}${formatDiff(r.diff_g1)}</td>
                        <td ${cellStyle('#f5f5ff')}>${pctBadge(r.p1)}${formatDiff(r.diff_p1, true)}</td>
                        
                        <td ${cellStyle('#f0fdf4')}>${r.v2.toLocaleString('vi-VN')}${formatDiff(r.diff_v2)}</td>
                        <td ${cellStyle('#f0fdf4')}>${pctBadge(r.gan2)}${formatDiff(r.diff_gan2, true)}</td>
                        <td ${cellStyle('#f0fdf4')}>${r.g2.toLocaleString('vi-VN')}${formatDiff(r.diff_g2)}</td>
                        <td ${cellStyle('#f0fdf4')}>${pctBadge(r.p2)}${formatDiff(r.diff_p2, true)}</td>
                        
                        <td ${cellStyle('#fef9ec')}>${r.v3.toLocaleString('vi-VN')}${formatDiff(r.diff_v3)}</td>
                        <td ${cellStyle('#fef9ec')}>${pctBadge(r.gan3)}${formatDiff(r.diff_gan3, true)}</td>
                        <td ${cellStyle('#fef9ec')}>${r.g3.toLocaleString('vi-VN')}${formatDiff(r.diff_g3)}</td>
                        <td ${cellStyle('#fef9ec')}>${pctBadge(r.p3)}${formatDiff(r.diff_p3, true)}</td>
                        
                        <td ${cellStyle('#f1f5f9', 'font-weight:700;color:#1e293b;')}>${r.total_v.toLocaleString('vi-VN')}${formatDiff(r.diff_total_v)}</td>
                        <td ${cellStyle('#f1f5f9')}>${pctBadge(r.total_gan)}${formatDiff(r.diff_total_gan, true)}</td>
                        <td ${cellStyle('#f1f5f9', 'font-weight:700;color:#1e293b;')}>${r.total_g.toLocaleString('vi-VN')}${formatDiff(r.diff_total_g)}</td>
                        <td ${cellStyle('#f1f5f9')}>${pctBadge(r.total_p)}${formatDiff(r.diff_total_p, true)}</td>
                    </tr>`;
                }
            });

            // 8. Add aggregate Grand Total Row at the bottom of the table
            if (displayRows.length > 0) {
                const sum_v1 = displayRows.reduce((s, r) => s + r.v1, 0);
                const sum_g1 = displayRows.reduce((s, r) => s + r.g1, 0);
                const sum_a1 = displayRows.reduce((s, r) => s + r.a1, 0);
                const sum_p1 = sum_v1 > 0 ? (sum_g1 / sum_v1 * 100) : null;
                const sum_gan1 = sum_v1 > 0 ? (sum_a1 / sum_v1 * 100) : null;

                const sum_v2 = displayRows.reduce((s, r) => s + r.v2, 0);
                const sum_g2 = displayRows.reduce((s, r) => s + r.g2, 0);
                const sum_a2 = displayRows.reduce((s, r) => s + r.a2, 0);
                const sum_p2 = sum_v2 > 0 ? (sum_g2 / sum_v2 * 100) : null;
                const sum_gan2 = sum_v2 > 0 ? (sum_a2 / sum_v2 * 100) : null;

                const sum_v3 = displayRows.reduce((s, r) => s + r.v3, 0);
                const sum_g3 = displayRows.reduce((s, r) => s + r.g3, 0);
                const sum_a3 = displayRows.reduce((s, r) => s + r.a3, 0);
                const sum_p3 = sum_v3 > 0 ? (sum_g3 / sum_v3 * 100) : null;
                const sum_gan3 = sum_v3 > 0 ? (sum_a3 / sum_v3 * 100) : null;

                const sum_total_v = displayRows.reduce((s, r) => s + r.total_v, 0);
                const sum_total_g = displayRows.reduce((s, r) => s + r.total_g, 0);
                const sum_total_a = displayRows.reduce((s, r) => s + r.total_a, 0);
                const sum_total_p = sum_total_v > 0 ? (sum_total_g / sum_total_v * 100) : null;
                const sum_total_gan = sum_total_v > 0 ? (sum_total_a / sum_total_v * 100) : null;

                // Diffs for footer
                let comp_sum = null;
                if (selectedDate && compareDate) {
                    comp_sum = {
                        v1: Object.values(compareAggregated).reduce((s, r) => s + r.v1, 0),
                        g1: Object.values(compareAggregated).reduce((s, r) => s + r.g1, 0),
                        a1: Object.values(compareAggregated).reduce((s, r) => s + r.a1, 0),
                        v2: Object.values(compareAggregated).reduce((s, r) => s + r.v2, 0),
                        g2: Object.values(compareAggregated).reduce((s, r) => s + r.g2, 0),
                        a2: Object.values(compareAggregated).reduce((s, r) => s + r.a2, 0),
                        v3: Object.values(compareAggregated).reduce((s, r) => s + r.v3, 0),
                        g3: Object.values(compareAggregated).reduce((s, r) => s + r.g3, 0),
                        a3: Object.values(compareAggregated).reduce((s, r) => s + r.a3, 0)
                    };
                    comp_sum.total_v = comp_sum.v1 + comp_sum.v2 + comp_sum.v3;
                    comp_sum.total_g = comp_sum.g1 + comp_sum.total_g || (comp_sum.g1 + comp_sum.g2 + comp_sum.g3);
                    comp_sum.total_a = comp_sum.a1 + comp_sum.a2 + comp_sum.a3;

                    comp_sum.p1 = comp_sum.v1 > 0 ? (comp_sum.g1 / comp_sum.v1 * 100) : null;
                    comp_sum.gan1 = comp_sum.v1 > 0 ? (comp_sum.a1 / comp_sum.v1 * 100) : null;
                    comp_sum.p2 = comp_sum.v2 > 0 ? (comp_sum.g2 / comp_sum.v2 * 100) : null;
                    comp_sum.gan2 = comp_sum.v2 > 0 ? (comp_sum.a2 / comp_sum.v2 * 100) : null;
                    comp_sum.p3 = comp_sum.v3 > 0 ? (comp_sum.g3 / comp_sum.v3 * 100) : null;
                    comp_sum.gan3 = comp_sum.v3 > 0 ? (comp_sum.a3 / comp_sum.v3 * 100) : null;
                    comp_sum.total_p = comp_sum.total_v > 0 ? (comp_sum.total_g / comp_sum.total_v * 100) : null;
                    comp_sum.total_gan = comp_sum.total_v > 0 ? (comp_sum.total_a / comp_sum.total_v * 100) : null;
                }

                if (viewMode === 'gtc_only') {
                    html += `<tr style="background:#e2e8f0; font-weight:700; border-top:2px solid #94a3b8; border-bottom:2px solid #94a3b8;">
                        <td style="padding:12px 14px;border-top:2px solid #94a3b8;border-bottom:2px solid #94a3b8;font-weight:800;color:#0f172a;">
                            TỔNG CỘNG (${displayRows.length} ${groupby === 'am' ? 'AM' : 'Bưu cục'})
                        </td>
                        <td style="padding:12px 12px;text-align:right;border-top:2px solid #94a3b8;border-bottom:2px solid #94a3b8;font-weight:800;color:#0f172a;font-variant-numeric:tabular-nums;">
                            ${sum_total_v.toLocaleString('vi-VN')}
                            ${formatDiff(comp_sum ? sum_total_v - comp_sum.total_v : null)}
                        </td>
                        <td style="padding:12px 12px;text-align:right;border-top:2px solid #94a3b8;border-bottom:2px solid #94a3b8;font-weight:700;color:#334155;font-variant-numeric:tabular-nums;">
                            ${sum_total_a.toLocaleString('vi-VN')}
                        </td>
                        <td style="padding:12px 12px;text-align:right;border-top:2px solid #94a3b8;border-bottom:2px solid #94a3b8;font-variant-numeric:tabular-nums;">
                            ${pctBadge(sum_total_gan)}
                            ${formatDiff((sum_total_gan !== null && comp_sum && comp_sum.total_gan !== null) ? sum_total_gan - comp_sum.total_gan : null, true)}
                        </td>
                        <td style="padding:12px 14px;text-align:right;border-top:2px solid #94a3b8;border-bottom:2px solid #94a3b8;font-weight:900;color:#065f46;background:#dcfce7;font-size:15px;font-variant-numeric:tabular-nums;">
                            ${sum_total_g.toLocaleString('vi-VN')}
                            ${formatDiff(comp_sum ? sum_total_g - comp_sum.total_g : null)}
                        </td>
                        <td style="padding:12px 12px;text-align:right;border-top:2px solid #94a3b8;border-bottom:2px solid #94a3b8;background:#dcfce7;font-variant-numeric:tabular-nums;">
                            ${pctBadge(sum_total_p)}
                            ${formatDiff((sum_total_p !== null && comp_sum && comp_sum.total_p !== null) ? sum_total_p - comp_sum.total_p : null, true)}
                        </td>
                    </tr>`;
                } else {
                    const footerBg = '#f1f5f9';
                    const footerCellStyle = (bg, extra = '') => `style="padding:10px 10px;text-align:right;border-top:2px solid #cbd5e1;border-bottom:2px solid #cbd5e1;background:${bg};font-weight:700;font-variant-numeric:tabular-nums;${extra}"`;

                    html += `<tr style="background:${footerBg}; font-weight:700; border-top:2px solid #cbd5e1; border-bottom:2px solid #cbd5e1;">
                        <td style="padding:10px 14px;border-top:2px solid #cbd5e1;border-bottom:2px solid #cbd5e1;font-weight:700;color:#0f172a;">
                            TỔNG CỘNG
                        </td>
                        <td ${footerCellStyle('#f5f5ff')}>
                            ${sum_v1.toLocaleString('vi-VN')}
                            ${formatDiff(comp_sum ? sum_v1 - comp_sum.v1 : null)}
                        </td>
                        <td ${footerCellStyle('#f5f5ff')}>
                            ${pctBadge(sum_gan1)}
                            ${formatDiff((sum_gan1 !== null && comp_sum && comp_sum.gan1 !== null) ? sum_gan1 - comp_sum.gan1 : null, true)}
                        </td>
                        <td ${footerCellStyle('#f5f5ff')}>
                            ${sum_g1.toLocaleString('vi-VN')}
                            ${formatDiff(comp_sum ? sum_g1 - comp_sum.g1 : null)}
                        </td>
                        <td ${footerCellStyle('#f5f5ff')}>
                            ${pctBadge(sum_p1)}
                            ${formatDiff((sum_p1 !== null && comp_sum && comp_sum.p1 !== null) ? sum_p1 - comp_sum.p1 : null, true)}
                        </td>
                        
                        <td ${footerCellStyle('#f0fdf4')}>
                            ${sum_v2.toLocaleString('vi-VN')}
                            ${formatDiff(comp_sum ? sum_v2 - comp_sum.v2 : null)}
                        </td>
                        <td ${footerCellStyle('#f0fdf4')}>
                            ${pctBadge(sum_gan2)}
                            ${formatDiff((sum_gan2 !== null && comp_sum && comp_sum.gan2 !== null) ? sum_gan2 - comp_sum.gan2 : null, true)}
                        </td>
                        <td ${footerCellStyle('#f0fdf4')}>
                            ${sum_g2.toLocaleString('vi-VN')}
                            ${formatDiff(comp_sum ? sum_g2 - comp_sum.g2 : null)}
                        </td>
                        <td ${footerCellStyle('#f0fdf4')}>
                            ${pctBadge(sum_p2)}
                            ${formatDiff((sum_p2 !== null && comp_sum && comp_sum.p2 !== null) ? sum_p2 - comp_sum.p2 : null, true)}
                        </td>
                        
                        <td ${footerCellStyle('#fef9ec')}>
                            ${sum_v3.toLocaleString('vi-VN')}
                            ${formatDiff(comp_sum ? sum_v3 - comp_sum.v3 : null)}
                        </td>
                        <td ${footerCellStyle('#fef9ec')}>
                            ${pctBadge(sum_gan3)}
                            ${formatDiff((sum_gan3 !== null && comp_sum && comp_sum.gan3 !== null) ? sum_gan3 - comp_sum.gan3 : null, true)}
                        </td>
                        <td ${footerCellStyle('#fef9ec')}>
                            ${sum_g3.toLocaleString('vi-VN')}
                            ${formatDiff(comp_sum ? sum_g3 - comp_sum.g3 : null)}
                        </td>
                        <td ${footerCellStyle('#fef9ec')}>
                            ${pctBadge(sum_p3)}
                            ${formatDiff((sum_p3 !== null && comp_sum && comp_sum.p3 !== null) ? sum_p3 - comp_sum.p3 : null, true)}
                        </td>
                        
                        <td ${footerCellStyle('#e2e8f0', 'color:#0f172a;')}>
                            ${sum_total_v.toLocaleString('vi-VN')}
                            ${formatDiff(comp_sum ? sum_total_v - comp_sum.total_v : null)}
                        </td>
                        <td ${footerCellStyle('#e2e8f0')}>
                            ${pctBadge(sum_total_gan)}
                            ${formatDiff((sum_total_gan !== null && comp_sum && comp_sum.total_gan !== null) ? sum_total_gan - comp_sum.total_gan : null, true)}
                        </td>
                        <td ${footerCellStyle('#e2e8f0', 'color:#0f172a;')}>
                            ${sum_total_g.toLocaleString('vi-VN')}
                            ${formatDiff(comp_sum ? sum_total_g - comp_sum.total_g : null)}
                        </td>
                        <td ${footerCellStyle('#e2e8f0')}>
                            ${pctBadge(sum_total_p)}
                            ${formatDiff((sum_total_p !== null && comp_sum && comp_sum.total_p !== null) ? sum_total_p - comp_sum.total_p : null, true)}
                        </td>
                    </tr>`;
                }
            }

            tbody.innerHTML = html;
        }

        window.filterCaTable = function() { renderCaTable(); };

        window.sortCaTable = function(key) {
            const actualKey = (key === 'bc') ? 'name' : key;
            if (caReportSortKey === actualKey) {
                caReportSortAsc = !caReportSortAsc;
            } else {
                caReportSortKey = actualKey;
                caReportSortAsc = (actualKey === 'name');
            }
            renderCaTable();
        };

'''

with open(target_file, "w", encoding="utf-8") as f:
    f.write(pre_content + new_function + post_content)

print("Successfully patched renderCaTable in templates/index.html")
