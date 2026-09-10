import json
import re

# Load fresh khach_hang_a.json
with open('scratch/khach_hang_a.json', 'r', encoding='utf-8') as f:
    kh_data = json.load(f)

kh_json_str = json.dumps(kh_data, ensure_ascii=False)

# 1. Update templates/index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update embedded KHACH_HANG_A_DATA
# Pattern: const KHACH_HANG_A_DATA = { ... };
pattern_kh = r'const KHACH_HANG_A_DATA\s*=\s*\{.*?\};(?=\s*let currentKdAmFilter)'
if re.search(pattern_kh, html, flags=re.DOTALL):
    html = re.sub(pattern_kh, f'const KHACH_HANG_A_DATA = {kh_json_str};', html, flags=re.DOTALL)
    print("Replaced KHACH_HANG_A_DATA in templates/index.html")
else:
    print("WARNING: Could not find KHACH_HANG_A_DATA pattern!")

# Update KPI cards in templates/index.html
# 16,278 -> 18,560
html = html.replace('16,278 <span style="font-size: 16px; font-weight: 600; color: var(--text-secondary);">Tr ₫</span>',
                    '18,560 <span style="font-size: 16px; font-weight: 600; color: var(--text-secondary);">Tr ₫</span>')

# Doanh Thu Ngày N-1 (08/09) -> Doanh Thu Ngày N-1 (09/09)
html = html.replace('Doanh Thu Ngày N-1 (08/09)', 'Doanh Thu Ngày N-1 (09/09)')
html = html.replace('2,199 <span style="font-size: 16px; font-weight: 600; color: var(--text-secondary);">Tr ₫</span>',
                    '2,282 <span style="font-size: 16px; font-weight: 600; color: var(--text-secondary);">Tr ₫</span>')
html = html.replace('▲ +512 Tr', '▲ +906 Tr')
html = html.replace('+30.3% vs W-1 (1,687 Tr)', '+65.8% vs W-1 (1,376 Tr)')

# Top 1 shop: 8,166 Tr -> 9,265 Tr
html = html.replace('<span style="background: rgba(124, 58, 237, 0.12); color: #7c3aed; font-weight: 700; padding: 2px 8px; border-radius: 6px; font-size: 11px;">8,166 Tr</span>\n                            <span>50.2% DT • AM Phan Đình Duy</span>',
                    '<span style="background: rgba(124, 58, 237, 0.12); color: #7c3aed; font-weight: 700; padding: 2px 8px; border-radius: 6px; font-size: 11px;">9,265 Tr</span>\n                            <span>49.9% DT • AM Phan Đình Duy</span>')

# Tien do thang: 8 / 30 -> 9 / 30
html = html.replace('8 / 30 <span style="font-size: 16px; font-weight: 600; color: var(--text-secondary);">ngày</span>',
                    '9 / 30 <span style="font-size: 16px; font-weight: 600; color: var(--text-secondary);">ngày</span>')
html = html.replace('26.7%', '30.0%')

# Chart 2 title: XU HƯỚNG DOANH THU 8 NGÀY GẦN NHẤT (01/09 – 08/09) -> 9 NGÀY GẦN NHẤT (01/09 – 09/09)
html = html.replace('XU HƯỚNG DOANH THU 8 NGÀY GẦN NHẤT (01/09 – 08/09)', 'XU HƯỚNG DOANH THU 9 NGÀY GẦN NHẤT (01/09 – 09/09)')
html = html.replace('Cột <strong>08/09 (N-1)</strong> là ngày gần nhất', 'Cột <strong>09/09 (N-1)</strong> là ngày gần nhất')

# Make renderKdTable dynamic in templates/index.html
old_render_kd_table = """        function renderKdTable() {
            const searchKeyword = (document.getElementById('kd-search-input')?.value || '').toLowerCase().trim();
            const tbody = document.getElementById('kd-table-tbody');
            const tfoot = document.getElementById('kd-table-tfoot');
            const badge = document.getElementById('kd-table-count-badge');
            if (!tbody || !KHACH_HANG_A_DATA || !KHACH_HANG_A_DATA.shops) return;

            let filtered = KHACH_HANG_A_DATA.shops;
            if (currentKdAmFilter) {
                filtered = filtered.filter(s => s.am === currentKdAmFilter);
            }
            if (searchKeyword) {
                filtered = filtered.filter(s => s.tenkh.toLowerCase().includes(searchKeyword) || s.makh.toLowerCase().includes(searchKeyword));
            }

            if (badge) badge.innerText = `${filtered.length} / ${KHACH_HANG_A_DATA.shops.length} Shop`;

            if (filtered.length === 0) {
                tbody.innerHTML = '<tr><td colspan="18" style="text-align:center; padding: 32px; color: var(--text-secondary); font-size: 14px;"><i class="fa-solid fa-magnifying-glass" style="margin-right:6px; opacity:0.6;"></i> Không tìm thấy khách hàng nhóm A phù hợp với bộ lọc.</td></tr>';
                if (tfoot) tfoot.innerHTML = '';
                return;
            }

            tbody.innerHTML = filtered.map((s, idx) => {
                // Diff badge
                const diffBadge = s.diff_w1 > 0
                    ? `<span style="color: #059669; font-weight: 800; background: rgba(16, 185, 129, 0.1); padding: 3px 8px; border-radius: 6px; font-size: 11.5px;">▲ +${s.diff_w1} (${s.pct_w1}%)</span>`
                    : (s.diff_w1 < 0 ? `<span style="color: #dc2626; font-weight: 800; background: rgba(239, 68, 68, 0.1); padding: 3px 8px; border-radius: 6px; font-size: 11.5px;">▼ ${s.diff_w1} (${s.pct_w1}%)</span>` : `<span style="color: var(--text-secondary); font-size: 11.5px;">0%</span>`);

                // Tru hang progress
                const truHangNum = parseFloat(s.pct_tru_hang) || 0;
                const barColor = truHangNum >= 25 ? '#10b981' : '#f59e0b';
                const truHangHtml = `
                    <div style="font-weight: 800; font-size: 12px; color: ${barColor};">${s.pct_tru_hang}</div>
                    <div class="mini-prog-bar">
                        <div class="mini-prog-fill" style="width: ${Math.min(100, truHangNum * 3)}%; background: ${barColor};"></div>
                    </div>
                `;

                return `
                    <tr style="transition: background 0.15s ease;">
                        <td style="text-align: center; font-weight: 700; color: var(--text-secondary); font-size: 12px;">${idx + 1}</td>
                        <td style="font-weight: 700; color: var(--text-primary); cursor: pointer;" onclick="setKdAmpill('${s.am}')">
                            <span style="color: #0284c7; text-decoration: underline dotted;">${s.am}</span>
                        </td>
                        <td style="font-size: 12px; color: var(--text-secondary); max-width: 180px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${s.buu_cuc}">
                            ${s.buu_cuc}
                        </td>
                        <td style="font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 12.5px;">
                            <span style="background: rgba(0,0,0,0.04); padding: 2px 6px; border-radius: 4px;">${s.makh}</span>
                        </td>
                        <td style="font-weight: 800; color: #1e3a8a;">
                            ${s.tenkh}
                        </td>
                        <td style="text-align: center;">
                            <span style="background: rgba(37, 99, 235, 0.12); color: #1d4ed8; font-weight: 800; font-size: 11px; padding: 3px 8px; border-radius: 6px;">${s.nhom_n || 'A5'}</span>
                        </td>
                        <td style="text-align: center;">
                            ${truHangHtml}
                        </td>
                        <td style="text-align: right; font-weight: 800; color: #059669; font-size: 14px; background: rgba(16, 185, 129, 0.05);">
                            ${Number(s.mtd).toLocaleString('vi-VN')}
                        </td>
                        <td style="text-align: center; font-weight: 700; font-size: 12px; color: var(--text-secondary);">
                            ${s.pct_mtd_m1}
                        </td>
                        <td style="text-align: right; font-size: 12.5px;">${Number(s.daily_dt['01/09'] || 0).toLocaleString('vi-VN')}</td>
                        <td style="text-align: right; font-size: 12.5px;">${Number(s.daily_dt['02/09'] || 0).toLocaleString('vi-VN')}</td>
                        <td style="text-align: right; font-size: 12.5px;">${Number(s.daily_dt['03/09'] || 0).toLocaleString('vi-VN')}</td>
                        <td style="text-align: right; font-size: 12.5px;">${Number(s.daily_dt['04/09'] || 0).toLocaleString('vi-VN')}</td>
                        <td style="text-align: right; font-size: 12.5px;">${Number(s.daily_dt['05/09'] || 0).toLocaleString('vi-VN')}</td>
                        <td style="text-align: right; font-size: 12.5px;">${Number(s.daily_dt['06/09'] || 0).toLocaleString('vi-VN')}</td>
                        <td style="text-align: right; font-size: 12.5px;">${Number(s.daily_dt['07/09'] || 0).toLocaleString('vi-VN')}</td>
                        <td style="text-align: right; font-weight: 800; color: #2563eb; font-size: 14px; background: rgba(37, 99, 235, 0.08);">
                            ${Number(s.dt_n1).toLocaleString('vi-VN')}
                        </td>
                        <td style="text-align: right;">
                            ${diffBadge}
                        </td>
                    </tr>
                `;
            }).join('');

            // Tfoot tổng cộng
            const sumMtd = filtered.reduce((acc, s) => acc + s.mtd, 0);
            const sum01 = filtered.reduce((acc, s) => acc + (s.daily_dt['01/09'] || 0), 0);
            const sum02 = filtered.reduce((acc, s) => acc + (s.daily_dt['02/09'] || 0), 0);
            const sum03 = filtered.reduce((acc, s) => acc + (s.daily_dt['03/09'] || 0), 0);
            const sum04 = filtered.reduce((acc, s) => acc + (s.daily_dt['04/09'] || 0), 0);
            const sum05 = filtered.reduce((acc, s) => acc + (s.daily_dt['05/09'] || 0), 0);
            const sum06 = filtered.reduce((acc, s) => acc + (s.daily_dt['06/09'] || 0), 0);
            const sum07 = filtered.reduce((acc, s) => acc + (s.daily_dt['07/09'] || 0), 0);
            const sumN1 = filtered.reduce((acc, s) => acc + s.dt_n1, 0);
            const diffTotal = sumN1 - sum01;
            const diffTotalPct = sum01 > 0 ? ((diffTotal / sum01) * 100).toFixed(1) : 0;
            const diffTotalBadge = diffTotal > 0
                ? `<span style="color: #059669; font-weight: 800;">▲ +${diffTotal} (+${diffTotalPct}%)</span>`
                : (diffTotal < 0 ? `<span style="color: #dc2626; font-weight: 800;">▼ ${diffTotal} (${diffTotalPct}%)</span>` : '0%');

            if (tfoot) {
                tfoot.innerHTML = `
                    <tr>
                        <td colspan="7" style="text-align: right; padding: 12px 16px; font-weight: 800; font-size: 13px; text-transform: uppercase;">
                            TỔNG CỘNG (${filtered.length} Shop):
                        </td>
                        <td style="text-align: right; font-weight: 800; color: #059669; font-size: 15px; background: rgba(16, 185, 129, 0.1);">
                            ${sumMtd.toLocaleString('vi-VN')}
                        </td>
                        <td style="text-align: center; color: var(--text-secondary);">-</td>
                        <td style="text-align: right;">${sum01.toLocaleString('vi-VN')}</td>
                        <td style="text-align: right;">${sum02.toLocaleString('vi-VN')}</td>
                        <td style="text-align: right;">${sum03.toLocaleString('vi-VN')}</td>
                        <td style="text-align: right;">${sum04.toLocaleString('vi-VN')}</td>
                        <td style="text-align: right;">${sum05.toLocaleString('vi-VN')}</td>
                        <td style="text-align: right;">${sum06.toLocaleString('vi-VN')}</td>
                        <td style="text-align: right;">${sum07.toLocaleString('vi-VN')}</td>
                        <td style="text-align: right; font-weight: 800; color: #2563eb; font-size: 15px; background: rgba(37, 99, 235, 0.1);">
                            ${sumN1.toLocaleString('vi-VN')}
                        </td>
                        <td style="text-align: right;">
                            ${diffTotalBadge}
                        </td>
                    </tr>
                `;
            }
        }"""

new_render_kd_table = """        function renderKdTable() {
            const searchKeyword = (document.getElementById('kd-search-input')?.value || '').toLowerCase().trim();
            const tbody = document.getElementById('kd-table-tbody');
            const tfoot = document.getElementById('kd-table-tfoot');
            const theadTr = document.querySelector('#kd-table-main thead tr');
            const badge = document.getElementById('kd-table-count-badge');
            if (!tbody || !KHACH_HANG_A_DATA || !KHACH_HANG_A_DATA.shops) return;

            const dates = KHACH_HANG_A_DATA.dates || [];
            const latestDate = dates.length > 0 ? dates[dates.length - 1] : '';
            const w1Date = dates.length >= 8 ? dates[dates.length - 8] : (dates[0] || '');

            if (theadTr && dates.length > 0) {
                const datesHeaderHtml = dates.map(d => {
                    if (d === latestDate) {
                        return `<th style="text-align: right; background: rgba(37, 99, 235, 0.12); color: #2563eb; font-weight: 800; font-size: 12px;">${d} (N-1)</th>`;
                    } else if (d === w1Date) {
                        return `<th style="text-align: right; color: var(--text-secondary);">${d} (W-1)</th>`;
                    } else {
                        return `<th style="text-align: right; color: var(--text-secondary);">${d}</th>`;
                    }
                }).join('');

                theadTr.innerHTML = `
                    <th style="width: 36px; text-align: center;">#</th>
                    <th>AM Phụ Trách</th>
                    <th>Bưu Cục Quản Lý</th>
                    <th>Mã Shop</th>
                    <th>Tên Shop / Khách Hàng</th>
                    <th style="text-align: center;">Hạng</th>
                    <th style="text-align: center; min-width: 130px;">% Trụ Hạng</th>
                    <th style="text-align: right; background: rgba(16, 185, 129, 0.1); color: #059669; font-weight: 800; font-size: 12px;">MTD (Tr ₫)</th>
                    <th style="text-align: center;">% vs MTD M-1</th>
                    ${datesHeaderHtml}
                    <th style="text-align: right; min-width: 120px;">Δ vs W-1</th>
                `;
            }

            let filtered = KHACH_HANG_A_DATA.shops;
            if (currentKdAmFilter) {
                filtered = filtered.filter(s => s.am === currentKdAmFilter);
            }
            if (searchKeyword) {
                filtered = filtered.filter(s => s.tenkh.toLowerCase().includes(searchKeyword) || s.makh.toLowerCase().includes(searchKeyword));
            }

            if (badge) badge.innerText = `${filtered.length} / ${KHACH_HANG_A_DATA.shops.length} Shop`;

            if (filtered.length === 0) {
                const colSpan = 10 + dates.length;
                tbody.innerHTML = `<tr><td colspan="${colSpan}" style="text-align:center; padding: 32px; color: var(--text-secondary); font-size: 14px;"><i class="fa-solid fa-magnifying-glass" style="margin-right:6px; opacity:0.6;"></i> Không tìm thấy khách hàng nhóm A phù hợp với bộ lọc.</td></tr>`;
                if (tfoot) tfoot.innerHTML = '';
                return;
            }

            tbody.innerHTML = filtered.map((s, idx) => {
                const diffBadge = s.diff_w1 > 0
                    ? `<span style="color: #059669; font-weight: 800; background: rgba(16, 185, 129, 0.1); padding: 3px 8px; border-radius: 6px; font-size: 11.5px;">▲ +${s.diff_w1} (${s.pct_w1}%)</span>`
                    : (s.diff_w1 < 0 ? `<span style="color: #dc2626; font-weight: 800; background: rgba(239, 68, 68, 0.1); padding: 3px 8px; border-radius: 6px; font-size: 11.5px;">▼ ${s.diff_w1} (${s.pct_w1}%)</span>` : `<span style="color: var(--text-secondary); font-size: 11.5px;">0%</span>`);

                const truHangNum = parseFloat(s.pct_tru_hang) || 0;
                const barColor = truHangNum >= 25 ? '#10b981' : '#f59e0b';
                const truHangHtml = `
                    <div style="font-weight: 800; font-size: 12px; color: ${barColor};">${s.pct_tru_hang}</div>
                    <div class="mini-prog-bar">
                        <div class="mini-prog-fill" style="width: ${Math.min(100, truHangNum * 3)}%; background: ${barColor};"></div>
                    </div>
                `;

                const datesTds = dates.map(d => {
                    const val = Number(s.daily_dt[d] || 0);
                    if (d === latestDate) {
                        return `<td style="text-align: right; font-weight: 800; color: #2563eb; font-size: 14px; background: rgba(37, 99, 235, 0.08);">${val.toLocaleString('vi-VN')}</td>`;
                    }
                    return `<td style="text-align: right; font-size: 12.5px;">${val.toLocaleString('vi-VN')}</td>`;
                }).join('');

                return `
                    <tr style="transition: background 0.15s ease;">
                        <td style="text-align: center; font-weight: 700; color: var(--text-secondary); font-size: 12px;">${idx + 1}</td>
                        <td style="font-weight: 700; color: var(--text-primary); cursor: pointer;" onclick="setKdAmpill('${s.am}')">
                            <span style="color: #0284c7; text-decoration: underline dotted;">${s.am}</span>
                        </td>
                        <td style="font-size: 12px; color: var(--text-secondary); max-width: 180px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${s.buu_cuc}">
                            ${s.buu_cuc}
                        </td>
                        <td style="font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 12.5px;">
                            <span style="background: rgba(0,0,0,0.04); padding: 2px 6px; border-radius: 4px;">${s.makh}</span>
                        </td>
                        <td style="font-weight: 800; color: #1e3a8a;">
                            ${s.tenkh}
                        </td>
                        <td style="text-align: center;">
                            <span style="background: rgba(37, 99, 235, 0.12); color: #1d4ed8; font-weight: 800; font-size: 11px; padding: 3px 8px; border-radius: 6px;">${s.nhom_n || 'A5'}</span>
                        </td>
                        <td style="text-align: center;">
                            ${truHangHtml}
                        </td>
                        <td style="text-align: right; font-weight: 800; color: #059669; font-size: 14px; background: rgba(16, 185, 129, 0.05);">
                            ${Number(s.mtd).toLocaleString('vi-VN')}
                        </td>
                        <td style="text-align: center; font-weight: 700; font-size: 12px; color: var(--text-secondary);">
                            ${s.pct_mtd_m1}
                        </td>
                        ${datesTds}
                        <td style="text-align: right;">
                            ${diffBadge}
                        </td>
                    </tr>
                `;
            }).join('');

            // Tfoot
            const sumMtd = filtered.reduce((acc, s) => acc + s.mtd, 0);
            const sumN1 = filtered.reduce((acc, s) => acc + (s.daily_dt[latestDate] || 0), 0);
            const sumW1 = filtered.reduce((acc, s) => acc + (s.daily_dt[w1Date] || 0), 0);
            const diffTotal = sumN1 - sumW1;
            const diffTotalPct = sumW1 > 0 ? ((diffTotal / sumW1) * 100).toFixed(1) : 0;
            const diffTotalBadge = diffTotal > 0
                ? `<span style="color: #059669; font-weight: 800;">▲ +${diffTotal.toLocaleString('vi-VN')} (+${diffTotalPct}%)</span>`
                : (diffTotal < 0 ? `<span style="color: #dc2626; font-weight: 800;">▼ ${diffTotal.toLocaleString('vi-VN')} (${diffTotalPct}%)</span>` : '0%');

            const datesFootTds = dates.map(d => {
                const sumD = filtered.reduce((acc, s) => acc + (s.daily_dt[d] || 0), 0);
                if (d === latestDate) {
                    return `<td style="text-align: right; font-weight: 800; color: #2563eb; font-size: 15px; background: rgba(37, 99, 235, 0.1);">${sumD.toLocaleString('vi-VN')}</td>`;
                }
                return `<td style="text-align: right; font-weight: 700; font-size: 12.5px;">${sumD.toLocaleString('vi-VN')}</td>`;
            }).join('');

            if (tfoot) {
                tfoot.innerHTML = `
                    <tr>
                        <td colspan="7" style="text-align: right; padding: 12px 16px; font-weight: 800; font-size: 13px; text-transform: uppercase;">
                            TỔNG CỘNG (${filtered.length} Shop):
                        </td>
                        <td style="text-align: right; font-weight: 800; color: #059669; font-size: 15px; background: rgba(16, 185, 129, 0.1);">
                            ${sumMtd.toLocaleString('vi-VN')}
                        </td>
                        <td style="text-align: center; color: var(--text-secondary);">-</td>
                        ${datesFootTds}
                        <td style="text-align: right;">
                            ${diffTotalBadge}
                        </td>
                    </tr>
                `;
            }
        }"""

if old_render_kd_table in html:
    html = html.replace(old_render_kd_table, new_render_kd_table)
    print("Replaced renderKdTable with dynamic version in templates/index.html")
else:
    print("WARNING: Could not find exact old_render_kd_table, checking...")

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated templates/index.html successfully!")

# 2. Update index.html (/hop)
with open('index.html', 'r', encoding='utf-8') as f:
    idx_html = f.read()

idx_html = idx_html.replace('MTD: 16.278 Tr ₫', 'MTD: 18.560 Tr ₫')
idx_html = idx_html.replace('Cập nhật: 08/09 (N-1)', 'Cập nhật: 09/09 (N-1)')
idx_html = idx_html.replace('16,278 <small>Tr ₫</small>', '18,560 <small>Tr ₫</small>')
idx_html = idx_html.replace('Doanh Thu Ngày N-1 (08/09)', 'Doanh Thu Ngày N-1 (09/09)')
idx_html = idx_html.replace('2,199 <small>Tr ₫</small>', '2,282 <small>Tr ₫</small>')
idx_html = idx_html.replace('▲ +512 Tr vs W-1 (+30.3%)', '▲ +906 Tr vs W-1 (+65.8%)')
idx_html = idx_html.replace('8,166 Tr MTD • AM Phan Đình Duy', '9,265 Tr MTD • AM Phan Đình Duy')
idx_html = idx_html.replace('8 / 30 <small>ngày</small>', '9 / 30 <small>ngày</small>')
idx_html = idx_html.replace('26.7% Số ngày trong tháng', '30.0% Số ngày trong tháng')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx_html)
print("Updated index.html successfully!")
