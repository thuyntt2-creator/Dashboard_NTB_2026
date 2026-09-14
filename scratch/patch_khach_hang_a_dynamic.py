import json
import re
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 1. Load fresh scratch/khach_hang_a.json
with open('scratch/khach_hang_a.json', 'r', encoding='utf-8') as f:
    kh_data = json.load(f)

kh_json_str = json.dumps(kh_data, ensure_ascii=False)

# 2. Read templates/index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace embedded KHACH_HANG_A_DATA
pattern_kh = r'const KHACH_HANG_A_DATA\s*=\s*\{.*?\};(?=\s*let currentKdAmFilter)'
if re.search(pattern_kh, html, flags=re.DOTALL):
    html = re.sub(pattern_kh, f'const KHACH_HANG_A_DATA = {kh_json_str};', html, flags=re.DOTALL)
    print("✅ Replaced KHACH_HANG_A_DATA with fresh 13/09 data")
else:
    print("❌ Could not find KHACH_HANG_A_DATA pattern!")

# Replace HTML Header & Cards with dynamic IDs and 13/09 values
old_kpi_section = """                                <span style="background: rgba(59, 130, 246, 0.15); color: #2563eb; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px;">
                                    <i class="fa-regular fa-clock"></i> Cập nhật: 10/09 (N-1)
                                </span>
                            </div>
                            <h2 style="font-family: 'Outfit', sans-serif; font-size: 24px; font-weight: 800; color: var(--text-primary); margin: 0 0 6px 0; letter-spacing: -0.5px;">
                                THEO DÕI DOANH THU & TIẾN ĐỘ TRỤ HẠNG KHÁCH HÀNG NHÓM A
                            </h2>
                            
                        </div>
                        
                    </div>
                </div>

                <!-- 2. 4 STAT KPI TILES (RICH ENTERPRISE METRICS) -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-bottom: 24px;">
                    <!-- Card 1 -->
                    <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 14px; padding: 20px; position: relative; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.02); border-left: 5px solid #10b981;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                            <span style="font-size: 12px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px;">Tổng Doanh Thu MTD</span>
                            <div style="width: 36px; height: 36px; border-radius: 10px; background: rgba(16, 185, 129, 0.12); display: flex; align-items: center; justify-content: center; color: #10b981;">
                                <i class="fa-solid fa-sack-dollar" style="font-size: 16px;"></i>
                            </div>
                        </div>
                        <div style="font-family: 'Outfit', sans-serif; font-size: 30px; font-weight: 800; color: #059669; line-height: 1.1; margin-bottom: 6px;">
                            20,683 <span style="font-size: 16px; font-weight: 600; color: var(--text-secondary);">Tr ₫</span>
                        </div>
                        <div style="font-size: 12px; color: var(--text-secondary); display: flex; align-items: center; gap: 6px;">
                            <span style="background: rgba(16, 185, 129, 0.15); color: #059669; font-weight: 700; padding: 2px 8px; border-radius: 6px; font-size: 11px;">👑 9 Shop</span>
                            <span>Trọng điểm Vùng NTB</span>
                        </div>
                    </div>

                    <!-- Card 2 -->
                    <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 14px; padding: 20px; position: relative; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.02); border-left: 5px solid #2563eb;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                            <span style="font-size: 12px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px;">Doanh Thu Ngày N-1 (10/09)</span>
                            <div style="width: 36px; height: 36px; border-radius: 10px; background: rgba(37, 99, 235, 0.12); display: flex; align-items: center; justify-content: center; color: #2563eb;">
                                <i class="fa-solid fa-bolt-lightning" style="font-size: 16px;"></i>
                            </div>
                        </div>
                        <div style="font-family: 'Outfit', sans-serif; font-size: 30px; font-weight: 800; color: #2563eb; line-height: 1.1; margin-bottom: 6px;">
                            2,123 <span style="font-size: 16px; font-weight: 600; color: var(--text-secondary);">Tr ₫</span>
                        </div>
                        <div style="font-size: 12px; color: var(--text-secondary); display: flex; align-items: center; gap: 6px;">
                            <span style="background: rgba(239, 68, 68, 0.15); color: #dc2626; font-weight: 700; padding: 2px 8px; border-radius: 6px; font-size: 11px;">▼ -254 Tr</span>
                            <span>-10.7% vs W-1 (2,377 Tr)</span>
                        </div>
                    </div>

                    <!-- Card 3 -->
                    <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 14px; padding: 20px; position: relative; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.02); border-left: 5px solid #7c3aed;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                            <span style="font-size: 12px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px;">Top 1 Shop Doanh Thu</span>
                            <div style="width: 36px; height: 36px; border-radius: 10px; background: rgba(124, 58, 237, 0.12); display: flex; align-items: center; justify-content: center; color: #7c3aed;">
                                <i class="fa-solid fa-medal" style="font-size: 16px;"></i>
                            </div>
                        </div>
                        <div style="font-family: 'Outfit', sans-serif; font-size: 20px; font-weight: 800; color: #6d28d9; line-height: 1.2; margin-bottom: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                            Vận Chuyển Online
                        </div>
                        <div style="font-size: 12px; color: var(--text-secondary); display: flex; align-items: center; gap: 6px;">
                            <span style="background: rgba(124, 58, 237, 0.12); color: #7c3aed; font-weight: 700; padding: 2px 8px; border-radius: 6px; font-size: 11px;">10,316 Tr</span>
                            <span>49.9% DT • AM Phan Đình Duy</span>
                        </div>
                    </div>

                    <!-- Card 4 -->
                    <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 14px; padding: 20px; position: relative; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.02); border-left: 5px solid #f59e0b;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                            <span style="font-size: 12px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px;">Tiến Độ Tháng & Trụ Hạng</span>
                            <div style="width: 36px; height: 36px; border-radius: 10px; background: rgba(245, 158, 11, 0.12); display: flex; align-items: center; justify-content: center; color: #f59e0b;">
                                <i class="fa-solid fa-chart-pie" style="font-size: 16px;"></i>
                            </div>
                        </div>
                        <div style="font-family: 'Outfit', sans-serif; font-size: 30px; font-weight: 800; color: #d97706; line-height: 1.1; margin-bottom: 6px;">
                            10 / 30 <span style="font-size: 16px; font-weight: 600; color: var(--text-secondary);">ngày</span>
                        </div>
                        <div style="font-size: 12px; color: var(--text-secondary); display: flex; align-items: center; gap: 6px;">
                            <span style="background: rgba(245, 158, 11, 0.15); color: #d97706; font-weight: 700; padding: 2px 8px; border-radius: 6px; font-size: 11px;">33.3%</span>
                            <span>100% Shop Đạt Tiến Độ Giữ Hạng</span>
                        </div>
                    </div>
                </div>

                <!-- 3. INTERACTIVE APEXCHARTS ROW -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 20px; margin-bottom: 24px;">
                    <!-- Chart 1: Doanh thu theo AM -->
                    <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 14px; padding: 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.02);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                            <div>
                                <h3 style="font-family: 'Outfit', sans-serif; font-size: 15px; font-weight: 700; color: var(--text-primary); margin: 0 0 2px 0;">
                                    <i class="fa-solid fa-chart-column" style="color: #10b981; margin-right: 6px;"></i> PHÂN BỔ DOANH THU MTD THEO AM (TRIỆU VNĐ)
                                </h3>
                                <div style="font-size: 12px; color: var(--text-secondary);">Tỷ trọng đóng góp doanh thu của 8 AM</div>
                            </div>
                            <span style="background: rgba(16, 185, 129, 0.1); color: #059669; font-weight: 700; font-size: 11px; padding: 4px 10px; border-radius: 8px;">Top 1: Phan Đình Duy (52.6%)</span>
                        </div>
                        <div id="apex-chart-kd-am" style="min-height: 280px;"></div>
                    </div>

                    <!-- Chart 2: Xu hướng doanh thu theo ngày -->
                    <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 14px; padding: 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.02);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                            <div>
                                <h3 style="font-family: 'Outfit', sans-serif; font-size: 15px; font-weight: 700; color: var(--text-primary); margin: 0 0 2px 0;">
                                    <i class="fa-solid fa-chart-line" style="color: #2563eb; margin-right: 6px;"></i> XU HƯỚNG DOANH THU 10 NGÀY GẦN NHẤT (01/09 – 10/09)
                                </h3>
                                <div style="font-size: 12px; color: var(--text-secondary);">Diễn biến doanh thu toàn bộ 9 shop nhóm A</div>
                            </div>
                            <span style="background: rgba(37, 99, 235, 0.1); color: #2563eb; font-weight: 700; font-size: 11px; padding: 4px 10px; border-radius: 8px;">Đỉnh ngày 07/09: 2,553 Tr</span>
                        </div>"""

new_kpi_section = """                                <span id="kd-header-date" style="background: rgba(59, 130, 246, 0.15); color: #2563eb; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px;">
                                    <i class="fa-regular fa-clock"></i> Cập nhật: 13/09 (N-1)
                                </span>
                            </div>
                            <h2 style="font-family: 'Outfit', sans-serif; font-size: 24px; font-weight: 800; color: var(--text-primary); margin: 0 0 6px 0; letter-spacing: -0.5px;">
                                THEO DÕI DOANH THU & TIẾN ĐỘ TRỤ HẠNG KHÁCH HÀNG NHÓM A
                            </h2>
                            
                        </div>
                        
                    </div>
                </div>

                <!-- 2. 4 STAT KPI TILES (RICH ENTERPRISE METRICS) -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-bottom: 24px;">
                    <!-- Card 1 -->
                    <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 14px; padding: 20px; position: relative; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.02); border-left: 5px solid #10b981;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                            <span style="font-size: 12px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px;">Tổng Doanh Thu MTD</span>
                            <div style="width: 36px; height: 36px; border-radius: 10px; background: rgba(16, 185, 129, 0.12); display: flex; align-items: center; justify-content: center; color: #10b981;">
                                <i class="fa-solid fa-sack-dollar" style="font-size: 16px;"></i>
                            </div>
                        </div>
                        <div id="kd-kpi-mtd-val" style="font-family: 'Outfit', sans-serif; font-size: 30px; font-weight: 800; color: #059669; line-height: 1.1; margin-bottom: 6px;">
                            26,870 <span style="font-size: 16px; font-weight: 600; color: var(--text-secondary);">Tr ₫</span>
                        </div>
                        <div style="font-size: 12px; color: var(--text-secondary); display: flex; align-items: center; gap: 6px;">
                            <span id="kd-kpi-shop-count" style="background: rgba(16, 185, 129, 0.15); color: #059669; font-weight: 700; padding: 2px 8px; border-radius: 6px; font-size: 11px;">👑 9 Shop</span>
                            <span>Trọng điểm Vùng NTB</span>
                        </div>
                    </div>

                    <!-- Card 2 -->
                    <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 14px; padding: 20px; position: relative; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.02); border-left: 5px solid #2563eb;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                            <span id="kd-kpi-n1-title" style="font-size: 12px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px;">Doanh Thu Ngày N-1 (13/09)</span>
                            <div style="width: 36px; height: 36px; border-radius: 10px; background: rgba(37, 99, 235, 0.12); display: flex; align-items: center; justify-content: center; color: #2563eb;">
                                <i class="fa-solid fa-bolt-lightning" style="font-size: 16px;"></i>
                            </div>
                        </div>
                        <div id="kd-kpi-n1-val" style="font-family: 'Outfit', sans-serif; font-size: 30px; font-weight: 800; color: #2563eb; line-height: 1.1; margin-bottom: 6px;">
                            2,089 <span style="font-size: 16px; font-weight: 600; color: var(--text-secondary);">Tr ₫</span>
                        </div>
                        <div style="font-size: 12px; color: var(--text-secondary); display: flex; align-items: center; gap: 6px;">
                            <span id="kd-kpi-n1-diff-badge" style="background: rgba(239, 68, 68, 0.15); color: #dc2626; font-weight: 700; padding: 2px 8px; border-radius: 6px; font-size: 11px;">▼ -115 Tr</span>
                            <span id="kd-kpi-n1-diff-desc">-5.2% vs W-1 (2,204 Tr)</span>
                        </div>
                    </div>

                    <!-- Card 3 -->
                    <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 14px; padding: 20px; position: relative; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.02); border-left: 5px solid #7c3aed;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                            <span style="font-size: 12px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px;">Top 1 Shop Doanh Thu</span>
                            <div style="width: 36px; height: 36px; border-radius: 10px; background: rgba(124, 58, 237, 0.12); display: flex; align-items: center; justify-content: center; color: #7c3aed;">
                                <i class="fa-solid fa-medal" style="font-size: 16px;"></i>
                            </div>
                        </div>
                        <div id="kd-kpi-top1-name" style="font-family: 'Outfit', sans-serif; font-size: 20px; font-weight: 800; color: #6d28d9; line-height: 1.2; margin-bottom: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                            Vận Chuyển Online
                        </div>
                        <div style="font-size: 12px; color: var(--text-secondary); display: flex; align-items: center; gap: 6px;">
                            <span id="kd-kpi-top1-mtd" style="background: rgba(124, 58, 237, 0.12); color: #7c3aed; font-weight: 700; padding: 2px 8px; border-radius: 6px; font-size: 11px;">13,410 Tr</span>
                            <span id="kd-kpi-top1-desc">49.9% DT • AM Phan Đình Duy</span>
                        </div>
                    </div>

                    <!-- Card 4 -->
                    <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 14px; padding: 20px; position: relative; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.02); border-left: 5px solid #f59e0b;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                            <span style="font-size: 12px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px;">Tiến Độ Tháng & Trụ Hạng</span>
                            <div style="width: 36px; height: 36px; border-radius: 10px; background: rgba(245, 158, 11, 0.12); display: flex; align-items: center; justify-content: center; color: #f59e0b;">
                                <i class="fa-solid fa-chart-pie" style="font-size: 16px;"></i>
                            </div>
                        </div>
                        <div id="kd-kpi-progress-days" style="font-family: 'Outfit', sans-serif; font-size: 30px; font-weight: 800; color: #d97706; line-height: 1.1; margin-bottom: 6px;">
                            13 / 30 <span style="font-size: 16px; font-weight: 600; color: var(--text-secondary);">ngày</span>
                        </div>
                        <div style="font-size: 12px; color: var(--text-secondary); display: flex; align-items: center; gap: 6px;">
                            <span id="kd-kpi-progress-pct" style="background: rgba(245, 158, 11, 0.15); color: #d97706; font-weight: 700; padding: 2px 8px; border-radius: 6px; font-size: 11px;">43.3%</span>
                            <span>100% Shop Đạt Tiến Độ Giữ Hạng</span>
                        </div>
                    </div>
                </div>

                <!-- 3. INTERACTIVE APEXCHARTS ROW -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 20px; margin-bottom: 24px;">
                    <!-- Chart 1: Doanh thu theo AM -->
                    <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 14px; padding: 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.02);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                            <div>
                                <h3 style="font-family: 'Outfit', sans-serif; font-size: 15px; font-weight: 700; color: var(--text-primary); margin: 0 0 2px 0;">
                                    <i class="fa-solid fa-chart-column" style="color: #10b981; margin-right: 6px;"></i> PHÂN BỔ DOANH THU MTD THEO AM (TRIỆU VNĐ)
                                </h3>
                                <div style="font-size: 12px; color: var(--text-secondary);">Tỷ trọng đóng góp doanh thu của 8 AM</div>
                            </div>
                            <span id="kd-chart-top-am-badge" style="background: rgba(16, 185, 129, 0.1); color: #059669; font-weight: 700; font-size: 11px; padding: 4px 10px; border-radius: 8px;">Top 1: Phan Đình Duy (52.6%)</span>
                        </div>
                        <div id="apex-chart-kd-am" style="min-height: 280px;"></div>
                    </div>

                    <!-- Chart 2: Xu hướng doanh thu theo ngày -->
                    <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 14px; padding: 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.02);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                            <div>
                                <h3 id="kd-trend-title" style="font-family: 'Outfit', sans-serif; font-size: 15px; font-weight: 700; color: var(--text-primary); margin: 0 0 2px 0;">
                                    <i class="fa-solid fa-chart-line" style="color: #2563eb; margin-right: 6px;"></i> XU HƯỚNG DOANH THU 13 NGÀY GẦN NHẤT (01/09 – 13/09)
                                </h3>
                                <div style="font-size: 12px; color: var(--text-secondary);">Diễn biến doanh thu toàn bộ 9 shop nhóm A</div>
                            </div>
                            <span id="kd-trend-peak-badge" style="background: rgba(37, 99, 235, 0.1); color: #2563eb; font-weight: 700; font-size: 11px; padding: 4px 10px; border-radius: 8px;">Đỉnh ngày 07/09: 2,553 Tr</span>
                        </div>"""

if old_kpi_section in html:
    html = html.replace(old_kpi_section, new_kpi_section)
    print("✅ Replaced static KPI cards HTML with dynamic IDs & 13/09 values")
else:
    print("❌ Could not match old_kpi_section!")

# Now add renderKdKpiCards logic to Javascript
old_render_kd = """        async function renderKinhDoanhTab() {
            try {
                const res = await fetch('/api/khach-hang-a');
                if (res.ok) {
                    const d = await res.json();
                    if (d && d.shops && d.shops.length) {
                        window.KHACH_HANG_A_DATA = d;
                    }
                }
            } catch(e) {}
            renderKdTable();
            renderKdWarning();
            initKdCharts();
        }"""

new_render_kd = """        function renderKdKpiCards(dataObj) {
            if (!dataObj || !dataObj.shops || !dataObj.shops.length) return;
            const dates = dataObj.dates || [];
            if (!dates.length) return;

            const latestDate = dates[dates.length - 1];
            const w1Date = dates.length >= 8 ? dates[dates.length - 8] : (dates[0] || '');
            const dayNum = parseInt(latestDate.split('/')[0]) || dates.length;

            // 1. Header date badge
            const headerDate = document.getElementById('kd-header-date');
            if (headerDate) {
                headerDate.innerHTML = `<i class="fa-regular fa-clock"></i> Cập nhật: ${latestDate} (N-1)`;
            }

            // 2. Total MTD
            const sumMtd = dataObj.shops.reduce((acc, s) => acc + (Number(s.mtd) || 0), 0);
            const kpiMtdVal = document.getElementById('kd-kpi-mtd-val');
            if (kpiMtdVal) {
                kpiMtdVal.innerHTML = `${Math.round(sumMtd).toLocaleString('vi-VN')} <span style="font-size: 16px; font-weight: 600; color: var(--text-secondary);">Tr ₫</span>`;
            }
            const kpiShopCount = document.getElementById('kd-kpi-shop-count');
            if (kpiShopCount) {
                kpiShopCount.innerText = `👑 ${dataObj.shops.length} Shop`;
            }

            // 3. Doanh thu ngày N-1
            const sumN1 = dataObj.shops.reduce((acc, s) => acc + (Number(s.daily_dt ? s.daily_dt[latestDate] : 0) || 0), 0);
            const sumW1 = dataObj.shops.reduce((acc, s) => acc + (Number(s.daily_dt ? s.daily_dt[w1Date] : 0) || 0), 0);
            const diffW1 = sumN1 - sumW1;
            const diffW1Pct = sumW1 > 0 ? ((diffW1 / sumW1) * 100).toFixed(1) : '0.0';

            const kpiN1Title = document.getElementById('kd-kpi-n1-title');
            if (kpiN1Title) {
                kpiN1Title.innerText = `Doanh Thu Ngày N-1 (${latestDate})`;
            }
            const kpiN1Val = document.getElementById('kd-kpi-n1-val');
            if (kpiN1Val) {
                kpiN1Val.innerHTML = `${Math.round(sumN1).toLocaleString('vi-VN')} <span style="font-size: 16px; font-weight: 600; color: var(--text-secondary);">Tr ₫</span>`;
            }
            const diffBadge = document.getElementById('kd-kpi-n1-diff-badge');
            const diffDesc = document.getElementById('kd-kpi-n1-diff-desc');
            if (diffBadge) {
                if (diffW1 > 0) {
                    diffBadge.style.background = 'rgba(16, 185, 129, 0.15)';
                    diffBadge.style.color = '#059669';
                    diffBadge.innerText = `▲ +${Math.round(diffW1).toLocaleString('vi-VN')} Tr`;
                } else if (diffW1 < 0) {
                    diffBadge.style.background = 'rgba(239, 68, 68, 0.15)';
                    diffBadge.style.color = '#dc2626';
                    diffBadge.innerText = `▼ ${Math.round(diffW1).toLocaleString('vi-VN')} Tr`;
                } else {
                    diffBadge.style.background = 'rgba(100, 116, 139, 0.15)';
                    diffBadge.style.color = 'var(--text-secondary)';
                    diffBadge.innerText = `0 Tr`;
                }
            }
            if (diffDesc) {
                diffDesc.innerText = `${diffW1 > 0 ? '+' : ''}${diffW1Pct}% vs W-1 (${Math.round(sumW1).toLocaleString('vi-VN')} Tr)`;
            }

            // 4. Top 1 Shop
            const sortedShops = [...dataObj.shops].sort((a, b) => (Number(b.mtd) || 0) - (Number(a.mtd) || 0));
            if (sortedShops.length > 0) {
                const top1 = sortedShops[0];
                const top1Mtd = Number(top1.mtd) || 0;
                const top1Pct = sumMtd > 0 ? ((top1Mtd / sumMtd) * 100).toFixed(1) : '0.0';

                const top1Name = document.getElementById('kd-kpi-top1-name');
                if (top1Name) top1Name.innerText = top1.tenkh || '';

                const top1MtdEl = document.getElementById('kd-kpi-top1-mtd');
                if (top1MtdEl) top1MtdEl.innerText = `${Math.round(top1Mtd).toLocaleString('vi-VN')} Tr`;

                const top1Desc = document.getElementById('kd-kpi-top1-desc');
                if (top1Desc) top1Desc.innerText = `${top1Pct}% DT • AM ${top1.am || ''}`;
            }

            // 5. Tiến độ tháng
            const progDays = document.getElementById('kd-kpi-progress-days');
            if (progDays) {
                progDays.innerHTML = `${dayNum} / 30 <span style="font-size: 16px; font-weight: 600; color: var(--text-secondary);">ngày</span>`;
            }
            const progPct = document.getElementById('kd-kpi-progress-pct');
            if (progPct) {
                progPct.innerText = `${((dayNum / 30) * 100).toFixed(1)}%`;
            }

            // 6. Trend title & Peak note
            const trendTitle = document.getElementById('kd-trend-title');
            if (trendTitle) {
                trendTitle.innerHTML = `<i class="fa-solid fa-chart-line" style="color: #2563eb; margin-right: 6px;"></i> XU HƯỚNG DOANH THU ${dates.length} NGÀY GẦN NHẤT (${dates[0]} – ${latestDate})`;
            }
            const trendData = dataObj.daily_trend || [];
            if (trendData.length > 0) {
                const peak = [...trendData].sort((a, b) => (Number(b.dt) || 0) - (Number(a.dt) || 0))[0];
                const peakBadge = document.getElementById('kd-trend-peak-badge');
                if (peakBadge && peak) {
                    peakBadge.innerText = `Đỉnh ngày ${peak.date}: ${Math.round(Number(peak.dt) || 0).toLocaleString('vi-VN')} Tr`;
                }
            }

            // 7. Top AM Badge
            const amData = dataObj.am_chart || [];
            if (amData.length > 0) {
                const topAm = [...amData].sort((a, b) => (Number(b.mtd) || 0) - (Number(a.mtd) || 0))[0];
                const amBadge = document.getElementById('kd-chart-top-am-badge');
                if (amBadge && topAm) {
                    amBadge.innerText = `Top 1: ${topAm.am} (${topAm.pct}%)`;
                }
            }
        }

        async function renderKinhDoanhTab() {
            try {
                const res = await fetch('/api/khach-hang-a');
                if (res.ok) {
                    const d = await res.json();
                    if (d && d.shops && d.shops.length) {
                        window.KHACH_HANG_A_DATA = d;
                    }
                }
            } catch(e) {}
            const dataObj = window.KHACH_HANG_A_DATA || (typeof KHACH_HANG_A_DATA !== 'undefined' ? KHACH_HANG_A_DATA : null);
            if (dataObj) {
                renderKdKpiCards(dataObj);
            }
            renderKdTable();
            renderKdWarning();
            initKdCharts();
        }"""

if old_render_kd in html:
    html = html.replace(old_render_kd, new_render_kd)
    print("✅ Injected renderKdKpiCards into renderKinhDoanhTab")
else:
    print("❌ Could not match old_render_kd!")

# Also ensure renderKdKpiCards is called once after DOMContentLoaded
init_call = """        // Tự động render KPI Cards khi tải trang
        if (typeof KHACH_HANG_A_DATA !== 'undefined') {
            renderKdKpiCards(KHACH_HANG_A_DATA);
        }
"""
html = html.replace('// Gắn vào sự kiện switchTab', init_call + '\n        // Gắn vào sự kiện switchTab')

# Write back
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("🎉 Successfully updated templates/index.html!")
