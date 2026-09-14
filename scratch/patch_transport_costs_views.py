import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Read templates/index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. New HTML for the NCC Data Status Banner & New Presets
old_filter_section = """                <!-- Bộ Lọc Đa Chiều: Ngày & Kích thước -->
                <div class="card" style="margin: 0 0 20px 0; padding: 16px 20px; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
                    <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 14px;">
                        <!-- Left: Quick Date Presets & Inputs -->
                        <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 10px;">
                            <div style="font-size: 12px; font-weight: 800; color: var(--text-primary); text-transform: uppercase; letter-spacing: 0.5px; display: flex; align-items: center; gap: 6px;">
                                <i class="fa-regular fa-calendar-days" style="color: #0284c7;"></i> Thời Gian:
                            </div>
                            <!-- Preset Buttons -->
                            <div style="display: inline-flex; background: var(--bg-primary); padding: 3px; border-radius: 8px; border: 1px solid var(--border-color); gap: 4px;">
                                <button type="button" class="tc-date-btn active" id="tc-btn-preset-all" onclick="setTcDatePreset('all', this)" style="border: none; background: #0284c7; color: #fff; padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer; transition: all 0.2s;">Tất cả</button>
                                <button type="button" class="tc-date-btn" id="tc-btn-preset-sep" onclick="setTcDatePreset('sep2026', this)" style="border: none; background: transparent; color: var(--text-secondary); padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s;">Tháng 9/2026</button>
                                <button type="button" class="tc-date-btn" id="tc-btn-preset-aug" onclick="setTcDatePreset('aug2026', this)" style="border: none; background: transparent; color: var(--text-secondary); padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s;">Tháng 8/2026</button>
                                <button type="button" class="tc-date-btn" id="tc-btn-preset-w36" onclick="setTcDatePreset('w36', this)" style="border: none; background: transparent; color: var(--text-secondary); padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s;">Tuần 36 (31/8-6/9)</button>
                                <button type="button" class="tc-date-btn" id="tc-btn-preset-7d" onclick="setTcDatePreset('last7days', this)" style="border: none; background: transparent; color: var(--text-secondary); padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s;">7 ngày qua</button>
                            </div>
                            <!-- Date Picker Inputs -->
                            <div style="display: flex; align-items: center; gap: 6px; background: var(--bg-primary); padding: 4px 10px; border-radius: 8px; border: 1px solid var(--border-color);">
                                <span style="font-size: 11.5px; color: var(--text-secondary); font-weight: 600;">Từ:</span>
                                <input type="date" id="tc-filter-date-from" onchange="onTcCustomDateChange()" style="border: none; background: transparent; font-size: 12px; font-weight: 600; color: var(--text-primary); outline: none; font-family: inherit;">
                                <span style="font-size: 11.5px; color: var(--text-secondary); font-weight: 600;">Đến:</span>
                                <input type="date" id="tc-filter-date-to" onchange="onTcCustomDateChange()" style="border: none; background: transparent; font-size: 12px; font-weight: 600; color: var(--text-primary); outline: none; font-family: inherit;">
                            </div>
                        </div>"""

new_filter_section = """                <!-- BẢNG TIẾN ĐỘ DỮ LIỆU TỪNG NCC (DATA FRESHNESS & BILLING CYCLE STATUS) -->
                <div class="card" style="margin: 0 0 20px 0; padding: 16px 20px; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
                        <div style="font-size: 12.5px; font-weight: 800; color: var(--text-primary); text-transform: uppercase; letter-spacing: 0.5px; display: flex; align-items: center; gap: 8px;">
                            <i class="fa-solid fa-satellite-dish" style="color: #0284c7;"></i> MỐC THỜI GIAN & ĐẶC THÙ DỮ LIỆU CỦA 7 ĐỐI TÁC NCC
                        </div>
                        <div style="font-size: 11.5px; color: var(--text-secondary);">
                            <i class="fa-regular fa-calendar-check" style="color: #10b981;"></i> Chu kỳ đối soát cước: <strong>26/08 ➔ 25/09/2026</strong>
                        </div>
                    </div>
                    
                    <!-- 4 Group Status Cards -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px;">
                        <!-- Group 1: Công Định -->
                        <div style="background: var(--bg-primary); border: 1px solid rgba(16, 185, 129, 0.3); border-left: 4px solid #10b981; border-radius: 8px; padding: 10px 14px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-weight: 800; font-size: 12.5px; color: var(--text-primary);">🚚 Công Định</span>
                                <span style="background: rgba(16, 185, 129, 0.15); color: #059669; font-size: 10.5px; font-weight: 700; padding: 2px 6px; border-radius: 4px;">Đến 12/09</span>
                            </div>
                            <div style="font-size: 11px; color: var(--text-secondary); margin-top: 4px;">
                                109 chuyến • Cập nhật chuyến thực tế hàng ngày
                            </div>
                        </div>

                        <!-- Group 2: NAK -->
                        <div style="background: var(--bg-primary); border: 1px solid rgba(245, 158, 11, 0.3); border-left: 4px solid #f59e0b; border-radius: 8px; padding: 10px 14px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-weight: 800; font-size: 12.5px; color: var(--text-primary);">🚚 NAK (Đắk Nông/ĐL)</span>
                                <span style="background: rgba(245, 158, 11, 0.15); color: #d97706; font-size: 10.5px; font-weight: 700; padding: 2px 6px; border-radius: 4px;">Đến 09/09 ⚠️</span>
                            </div>
                            <div style="font-size: 11px; color: var(--text-secondary); margin-top: 4px;">
                                240 chuyến • <em>NCC đang chậm 5 ngày số liệu</em>
                            </div>
                        </div>

                        <!-- Group 3: Tuyến cố định tháng -->
                        <div style="background: var(--bg-primary); border: 1px solid rgba(2, 132, 199, 0.3); border-left: 4px solid #0284c7; border-radius: 8px; padding: 10px 14px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-weight: 800; font-size: 12.5px; color: var(--text-primary);">🚚 Mạnh Cường, Tốt & Rẻ...</span>
                                <span style="background: rgba(2, 132, 199, 0.15); color: #0284c7; font-size: 10.5px; font-weight: 700; padding: 2px 6px; border-radius: 4px;">Kỳ đến 25/09</span>
                            </div>
                            <div style="font-size: 11px; color: var(--text-secondary); margin-top: 4px;">
                                371 chuyến • Lịch xe hợp đồng bao nguyên chu kỳ
                            </div>
                        </div>

                        <!-- Group 4: Mạnh Cường BCCK -->
                        <div style="background: var(--bg-primary); border: 1px solid rgba(124, 58, 237, 0.3); border-left: 4px solid #7c3aed; border-radius: 8px; padding: 10px 14px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-weight: 800; font-size: 12.5px; color: var(--text-primary);">🚚 Mạnh Cường (BCCK)</span>
                                <span style="background: rgba(124, 58, 237, 0.15); color: #7c3aed; font-size: 10.5px; font-weight: 700; padding: 2px 6px; border-radius: 4px;">Hàng ngày</span>
                            </div>
                            <div style="font-size: 11px; color: var(--text-secondary); margin-top: 4px;">
                                7 xe cố định bưu cục • Khoán chi phí hàng ngày
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Bộ Lọc Đa Chiều: Ngày & Kích thước -->
                <div class="card" style="margin: 0 0 20px 0; padding: 16px 20px; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
                    <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 14px;">
                        <!-- Left: Quick Date Presets & Inputs -->
                        <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 10px;">
                            <div style="font-size: 12px; font-weight: 800; color: var(--text-primary); text-transform: uppercase; letter-spacing: 0.5px; display: flex; align-items: center; gap: 6px;">
                                <i class="fa-regular fa-calendar-days" style="color: #0284c7;"></i> Thời Gian:
                            </div>
                            <!-- Preset Buttons -->
                            <div style="display: inline-flex; background: var(--bg-primary); padding: 3px; border-radius: 8px; border: 1px solid var(--border-color); gap: 4px; flex-wrap: wrap;">
                                <button type="button" class="tc-date-btn active" id="tc-btn-preset-actual" onclick="setTcDatePreset('actual_mtd', this)" style="border: none; background: #0284c7; color: #fff; padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer; transition: all 0.2s;">⭐ Thực tế đã chạy (01/09 - 13/09)</button>
                                <button type="button" class="tc-date-btn" id="tc-btn-preset-billing" onclick="setTcDatePreset('billing_sep', this)" style="border: none; background: transparent; color: var(--text-secondary); padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s;">📅 Kỳ đối soát T9 (26/08 - 25/09)</button>
                                <button type="button" class="tc-date-btn" id="tc-btn-preset-w36" onclick="setTcDatePreset('w36', this)" style="border: none; background: transparent; color: var(--text-secondary); padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s;">Tuần W36 (31/8-6/9)</button>
                                <button type="button" class="tc-date-btn" id="tc-btn-preset-w37" onclick="setTcDatePreset('w37', this)" style="border: none; background: transparent; color: var(--text-secondary); padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s;">Tuần W37 (7/9-13/9)</button>
                                <button type="button" class="tc-date-btn" id="tc-btn-preset-all" onclick="setTcDatePreset('all', this)" style="border: none; background: transparent; color: var(--text-secondary); padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s;">Tất cả</button>
                            </div>
                            <!-- Date Picker Inputs -->
                            <div style="display: flex; align-items: center; gap: 6px; background: var(--bg-primary); padding: 4px 10px; border-radius: 8px; border: 1px solid var(--border-color);">
                                <span style="font-size: 11.5px; color: var(--text-secondary); font-weight: 600;">Từ:</span>
                                <input type="date" id="tc-filter-date-from" onchange="onTcCustomDateChange()" style="border: none; background: transparent; font-size: 12px; font-weight: 600; color: var(--text-primary); outline: none; font-family: inherit;">
                                <span style="font-size: 11.5px; color: var(--text-secondary); font-weight: 600;">Đến:</span>
                                <input type="date" id="tc-filter-date-to" onchange="onTcCustomDateChange()" style="border: none; background: transparent; font-size: 12px; font-weight: 600; color: var(--text-primary); outline: none; font-family: inherit;">
                            </div>
                        </div>"""

if old_filter_section in html:
    html = html.replace(old_filter_section, new_filter_section)
    print("✅ Injected NCC Data Freshness Status Banner & New Presets HTML")
else:
    print("❌ Could not match old_filter_section!")

# 2. Update Javascript setTcDatePreset and applyAllTransportFilters
old_js_logic = """        let currentTcActivePreset = 'all';

        async function renderTransportCostTab() {
            try {
                const res = await fetch('/api/transport-costs');
                if (res.ok) {
                    const d = await res.json();
                    if (d && d.trips) {
                        window.TRANSPORT_COSTS_DATA = d;
                    }
                }
            } catch(e) {
                console.error('Error fetching transport costs:', e);
            }
            applyAllTransportFilters();
        }

        function setTcDatePreset(preset, btn) {
            currentTcActivePreset = preset;
            document.querySelectorAll('.tc-date-btn').forEach(b => {
                b.classList.remove('active');
                b.style.background = 'transparent';
                b.style.color = 'var(--text-secondary)';
                b.style.fontWeight = '600';
            });
            if (btn) {
                btn.classList.add('active');
                btn.style.background = '#0284c7';
                btn.style.color = '#ffffff';
                btn.style.fontWeight = '700';
            }

            const fromInput = document.getElementById('tc-filter-date-from');
            const toInput = document.getElementById('tc-filter-date-to');

            if (preset === 'all') {
                if (fromInput) fromInput.value = '';
                if (toInput) toInput.value = '';
            } else if (preset === 'sep2026') {
                if (fromInput) fromInput.value = '2026-09-01';
                if (toInput) toInput.value = '2026-09-30';
            } else if (preset === 'aug2026') {
                if (fromInput) fromInput.value = '2026-08-01';
                if (toInput) toInput.value = '2026-08-31';
            } else if (preset === 'w36') {
                if (fromInput) fromInput.value = '2026-08-31';
                if (toInput) toInput.value = '2026-09-06';
            } else if (preset === 'last7days') {
                if (fromInput) fromInput.value = '2026-09-05';
                if (toInput) toInput.value = '2026-09-11';
            }

            applyAllTransportFilters();
        }"""

new_js_logic = """        let currentTcActivePreset = 'actual_mtd';

        async function renderTransportCostTab() {
            try {
                const res = await fetch('/api/transport-costs');
                if (res.ok) {
                    const d = await res.json();
                    if (d && d.trips) {
                        window.TRANSPORT_COSTS_DATA = d;
                    }
                }
            } catch(e) {
                console.error('Error fetching transport costs:', e);
            }
            // Mặc định chọn preset Thực tế đã chạy
            const btnActual = document.getElementById('tc-btn-preset-actual');
            if (btnActual && currentTcActivePreset === 'actual_mtd') {
                setTcDatePreset('actual_mtd', btnActual);
            } else {
                applyAllTransportFilters();
            }
        }

        function setTcDatePreset(preset, btn) {
            currentTcActivePreset = preset;
            document.querySelectorAll('.tc-date-btn').forEach(b => {
                b.classList.remove('active');
                b.style.background = 'transparent';
                b.style.color = 'var(--text-secondary)';
                b.style.fontWeight = '600';
            });
            if (btn) {
                btn.classList.add('active');
                btn.style.background = '#0284c7';
                btn.style.color = '#ffffff';
                btn.style.fontWeight = '700';
            }

            const fromInput = document.getElementById('tc-filter-date-from');
            const toInput = document.getElementById('tc-filter-date-to');

            if (preset === 'actual_mtd') {
                // Thực tế vận hành đã chạy (01/09 - 13/09): cắt bỏ chuyến tương lai chưa chạy
                if (fromInput) fromInput.value = '2026-09-01';
                if (toInput) toInput.value = '2026-09-13';
            } else if (preset === 'billing_sep') {
                // Kỳ đối soát chuẩn của 7 nhà xe (26/08 - 25/09)
                if (fromInput) fromInput.value = '2026-08-26';
                if (toInput) toInput.value = '2026-09-25';
            } else if (preset === 'w36') {
                // Tuần W36 chuẩn (31/08 - 06/09)
                if (fromInput) fromInput.value = '2026-08-31';
                if (toInput) toInput.value = '2026-09-06';
            } else if (preset === 'w37') {
                // Tuần W37 (07/09 - 13/09)
                if (fromInput) fromInput.value = '2026-09-07';
                if (toInput) toInput.value = '2026-09-13';
            } else if (preset === 'all') {
                if (fromInput) fromInput.value = '';
                if (toInput) toInput.value = '';
            }

            applyAllTransportFilters();
        }"""

if old_js_logic in html:
    html = html.replace(old_js_logic, new_js_logic)
    print("✅ Injected new setTcDatePreset logic")
else:
    print("❌ Could not match old_js_logic!")

# 3. Enhance applyAllTransportFilters filtering and banner text
old_filter_trips_logic = """            let filteredTrips = data.trips.filter(t => {
                if (ktcFilter !== 'all' && t.ktc !== ktcFilter) return false;
                if (nccFilter !== 'all' && t.ncc !== nccFilter) return false;
                if (typeFilter !== 'all' && t.type !== typeFilter) return false;
                if (keyword) {
                    const mTruck = t.truck && t.truck.toLowerCase().includes(keyword);
                    const mCode = t.trip_code && t.trip_code.toLowerCase().includes(keyword);
                    const mRoute = t.route && t.route.toLowerCase().includes(keyword);
                    const mNcc = t.ncc && t.ncc.toLowerCase().includes(keyword);
                    const mKtc = t.ktc && t.ktc.toLowerCase().includes(keyword);
                    if (!mTruck && !mCode && !mRoute && !mNcc && !mKtc) return false;
                }
                if (fromDate || toDate) {
                    if (t.date_iso) {
                        if (fromDate && t.date_iso < fromDate) return false;
                        if (toDate && t.date_iso > toDate) return false;
                    } else {
                        if (toDate && toDate < '2026-09-01') return false;
                    }
                }
                return true;
            });"""

new_filter_trips_logic = """            let filteredTrips = data.trips.filter(t => {
                if (ktcFilter !== 'all' && t.ktc !== ktcFilter) return false;
                if (nccFilter !== 'all' && t.ncc !== nccFilter) return false;
                if (typeFilter !== 'all' && t.type !== typeFilter) return false;
                if (keyword) {
                    const mTruck = t.truck && t.truck.toLowerCase().includes(keyword);
                    const mCode = t.trip_code && t.trip_code.toLowerCase().includes(keyword);
                    const mRoute = t.route && t.route.toLowerCase().includes(keyword);
                    const mNcc = t.ncc && t.ncc.toLowerCase().includes(keyword);
                    const mKtc = t.ktc && t.ktc.toLowerCase().includes(keyword);
                    if (!mTruck && !mCode && !mRoute && !mNcc && !mKtc) return false;
                }
                if (fromDate || toDate) {
                    if (t.date_iso) {
                        if (fromDate && t.date_iso < fromDate) return false;
                        if (toDate && t.date_iso > toDate) return false;
                    } else {
                        // Xe khoán cố định bưu cục (Mạnh Cường BCCK)
                        if (currentTcActivePreset === 'w36' || currentTcActivePreset === 'w37') {
                            return false; // Không tính xe khoán tháng vào báo cáo 1 tuần cụ thể
                        }
                    }
                }
                return true;
            });"""

if old_filter_trips_logic in html:
    html = html.replace(old_filter_trips_logic, new_filter_trips_logic)
    print("✅ Injected new filteredTrips date handling")
else:
    print("❌ Could not match old_filter_trips_logic!")

# 4. Enhance banner text
old_banner_code = """            const elBannerText = document.getElementById('tc-filter-status-text');
            const elBannerSum = document.getElementById('tc-filter-status-sum');
            let rangeLabel = 'Tất cả thời gian';
            if (fromDate && toDate) {
                const fParts = fromDate.split('-');
                const tParts = toDate.split('-');
                rangeLabel = `Từ ${fParts[2]}/${fParts[1]} đến ${tParts[2]}/${tParts[1]}/${tParts[0]}`;
            } else if (fromDate) {
                rangeLabel = `Từ ngày ${fromDate}`;
            } else if (toDate) {
                rangeLabel = `Đến ngày ${toDate}`;
            }
            if (elBannerText) {
                elBannerText.innerHTML = `<i class="fa-solid fa-filter" style="margin-right: 4px;"></i> Đang lọc: <strong>${rangeLabel}</strong> • KTC: <strong>${ktcFilter === 'all' ? 'Tất cả' : ktcFilter}</strong> • NCC: <strong>${nccFilter === 'all' ? 'Tất cả' : nccFilter}</strong> (${totalTrips} chuyến)`;
            }"""

new_banner_code = """            const elBannerText = document.getElementById('tc-filter-status-text');
            const elBannerSum = document.getElementById('tc-filter-status-sum');
            let rangeLabel = 'Tất cả thời gian';
            let presetNote = '';
            if (currentTcActivePreset === 'actual_mtd') {
                rangeLabel = 'Thực tế đã chạy (01/09 - 13/09)';
                presetNote = '<span style="background: rgba(16, 185, 129, 0.15); color: #059669; padding: 2px 6px; border-radius: 4px; font-weight: 700; margin-left: 6px;">Loại bỏ chuyến tương lai</span>';
            } else if (currentTcActivePreset === 'billing_sep') {
                rangeLabel = 'Kỳ đối soát T9 (26/08 - 25/09)';
                presetNote = '<span style="background: rgba(2, 132, 199, 0.15); color: #0284c7; padding: 2px 6px; border-radius: 4px; font-weight: 700; margin-left: 6px;">Trọn gói cước tháng</span>';
            } else if (currentTcActivePreset === 'w36') {
                rangeLabel = 'Tuần W36 (31/08 - 06/09)';
                presetNote = '<span style="background: rgba(16, 185, 129, 0.15); color: #059669; padding: 2px 6px; border-radius: 4px; font-weight: 700; margin-left: 6px;">100% dữ liệu đã chốt</span>';
            } else if (currentTcActivePreset === 'w37') {
                rangeLabel = 'Tuần W37 (07/09 - 13/09)';
                presetNote = '<span style="background: rgba(245, 158, 11, 0.15); color: #d97706; padding: 2px 6px; border-radius: 4px; font-weight: 700; margin-left: 6px;">NAK mới đến 09/09</span>';
            } else if (fromDate && toDate) {
                const fParts = fromDate.split('-');
                const tParts = toDate.split('-');
                rangeLabel = `Từ ${fParts[2]}/${fParts[1]} đến ${tParts[2]}/${tParts[1]}/${tParts[0]}`;
            } else if (fromDate) {
                rangeLabel = `Từ ngày ${fromDate}`;
            } else if (toDate) {
                rangeLabel = `Đến ngày ${toDate}`;
            }

            let nccNote = '';
            if (nccFilter === 'NAK') {
                nccNote = ' <span style="color: #d97706; font-size: 11px;">(NCC mới cập nhật đến 09/09)</span>';
            } else if (nccFilter === 'Công Định') {
                nccNote = ' <span style="color: #059669; font-size: 11px;">(Đến 12/09)</span>';
            }

            if (elBannerText) {
                elBannerText.innerHTML = `<i class="fa-solid fa-filter" style="margin-right: 4px;"></i> Đang lọc: <strong>${rangeLabel}</strong> ${presetNote} • KTC: <strong>${ktcFilter === 'all' ? 'Tất cả' : ktcFilter}</strong> • NCC: <strong>${nccFilter === 'all' ? 'Tất cả' : nccFilter}</strong>${nccNote} (${totalTrips} chuyến)`;
            }"""

if old_banner_code in html:
    html = html.replace(old_banner_code, new_banner_code)
    print("✅ Injected enhanced banner text with NCC context")
else:
    print("❌ Could not match old_banner_code!")

# Write back
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("🎉 Finished patching templates/index.html!")
