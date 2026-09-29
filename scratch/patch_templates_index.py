import sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update NCC status cards
old_status_cards_regex = re.compile(
    r'<!-- BẢNG TIẾN ĐỘ DỮ LIỆU TỪNG NCC.*?<!-- Bộ Lọc Đa Chiều: Ngày & Kích thước -->',
    re.DOTALL
)

new_status_cards = """<!-- BẢNG TIẾN ĐỘ DỮ LIỆU TỪNG NCC (DATA FRESHNESS & BILLING CYCLE STATUS) -->
                <div class="card" style="margin: 0 0 20px 0; padding: 16px 20px; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
                        <div style="font-size: 12.5px; font-weight: 800; color: var(--text-primary); text-transform: uppercase; letter-spacing: 0.5px; display: flex; align-items: center; gap: 8px;">
                            <i class="fa-solid fa-satellite-dish" style="color: #0284c7;"></i> MỐC THỜI GIAN & TIẾN ĐỘ ĐỐI SOÁT 7 ĐỐI TÁC NCC
                        </div>
                        <div style="font-size: 11.5px; color: var(--text-secondary);">
                            <i class="fa-regular fa-calendar-check" style="color: #10b981;"></i> Chu kỳ đối soát hoàn tất: <strong>26/08 ➔ 25/09/2026</strong> (Kỳ Tháng 9)
                        </div>
                    </div>
                    
                    <!-- 4 Group Status Cards -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px;">
                        <!-- Group 1: Công Định -->
                        <div style="background: var(--bg-primary); border: 1px solid rgba(16, 185, 129, 0.3); border-left: 4px solid #10b981; border-radius: 8px; padding: 10px 14px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-weight: 800; font-size: 12.5px; color: var(--text-primary);">🚚 Công Định</span>
                                <span style="background: rgba(16, 185, 129, 0.15); color: #059669; font-size: 10.5px; font-weight: 700; padding: 2px 6px; border-radius: 4px;">Đến 25/09 ✔</span>
                            </div>
                            <div style="font-size: 11px; color: var(--text-secondary); margin-top: 4px;">
                                187 chuyến • Hoàn tất toàn bộ chu kỳ T9
                            </div>
                        </div>

                        <!-- Group 2: NAK -->
                        <div style="background: var(--bg-primary); border: 1px solid rgba(16, 185, 129, 0.3); border-left: 4px solid #10b981; border-radius: 8px; padding: 10px 14px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-weight: 800; font-size: 12.5px; color: var(--text-primary);">🚚 NAK (Đức Trọng / LĐ)</span>
                                <span style="background: rgba(16, 185, 129, 0.15); color: #059669; font-size: 10.5px; font-weight: 700; padding: 2px 6px; border-radius: 4px;">Đến 25/09 ✔</span>
                            </div>
                            <div style="font-size: 11px; color: var(--text-secondary); margin-top: 4px;">
                                490 chuyến • Đã quét đủ 100% dữ liệu
                            </div>
                        </div>

                        <!-- Group 3: Lâm Ngọc Thành, Tốt & Rẻ, Trâm Hoá -->
                        <div style="background: var(--bg-primary); border: 1px solid rgba(2, 132, 199, 0.3); border-left: 4px solid #0284c7; border-radius: 8px; padding: 10px 14px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-weight: 800; font-size: 12.5px; color: var(--text-primary);">🚚 LNT, Tốt & Rẻ, Trâm Hoá</span>
                                <span style="background: rgba(2, 132, 199, 0.15); color: #0284c7; font-size: 10.5px; font-weight: 700; padding: 2px 6px; border-radius: 4px;">Đến 25/09 ✔</span>
                            </div>
                            <div style="font-size: 11px; color: var(--text-secondary); margin-top: 4px;">
                                194 chuyến • Đắk Nông & Tây Nguyên
                            </div>
                        </div>

                        <!-- Group 4: Mạnh Cường & Mạnh Cường BCCK -->
                        <div style="background: var(--bg-primary); border: 1px solid rgba(124, 58, 237, 0.3); border-left: 4px solid #7c3aed; border-radius: 8px; padding: 10px 14px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-weight: 800; font-size: 12.5px; color: var(--text-primary);">🚚 Mạnh Cường (Tuyến & BCCK)</span>
                                <span style="background: rgba(124, 58, 237, 0.15); color: #7c3aed; font-size: 10.5px; font-weight: 700; padding: 2px 6px; border-radius: 4px;">Đến 25/09 ✔</span>
                            </div>
                            <div style="font-size: 11px; color: var(--text-secondary); margin-top: 4px;">
                                1.512 chuyến + 15 xe HĐ • Khánh Hòa, BTH
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Bộ Lọc Đa Chiều: Ngày & Kích thước -->"""

assert old_status_cards_regex.search(html) is not None, "Could not find old status cards section"
html = old_status_cards_regex.sub(new_status_cards, html)

# 2. Update Preset Buttons
old_preset_buttons = """                            <div style="display: inline-flex; background: var(--bg-primary); padding: 3px; border-radius: 8px; border: 1px solid var(--border-color); gap: 4px; flex-wrap: wrap;">
                                <button type="button" class="tc-date-btn active" id="tc-btn-preset-actual" onclick="setTcDatePreset('actual_mtd', this)" style="border: none; background: #0284c7; color: #fff; padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer; transition: all 0.2s;">⭐ Thực tế đã chạy (01/09 - 13/09)</button>
                                <button type="button" class="tc-date-btn" id="tc-btn-preset-billing" onclick="setTcDatePreset('billing_sep', this)" style="border: none; background: transparent; color: var(--text-secondary); padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s;">📅 Kỳ đối soát T9 (26/08 - 25/09)</button>
                                <button type="button" class="tc-date-btn" id="tc-btn-preset-w36" onclick="setTcDatePreset('w36', this)" style="border: none; background: transparent; color: var(--text-secondary); padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s;">Tuần W36 (31/8-6/9)</button>
                                <button type="button" class="tc-date-btn" id="tc-btn-preset-w37" onclick="setTcDatePreset('w37', this)" style="border: none; background: transparent; color: var(--text-secondary); padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s;">Tuần W37 (7/9-13/9)</button>
                                <button type="button" class="tc-date-btn" id="tc-btn-preset-all" onclick="setTcDatePreset('all', this)" style="border: none; background: transparent; color: var(--text-secondary); padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s;">Tất cả</button>
                            </div>"""

new_preset_buttons = """                            <div style="display: inline-flex; background: var(--bg-primary); padding: 3px; border-radius: 8px; border: 1px solid var(--border-color); gap: 4px; flex-wrap: wrap;">
                                <button type="button" class="tc-date-btn active" id="tc-btn-preset-billing" onclick="setTcDatePreset('billing_sep', this)" style="border: none; background: #0284c7; color: #fff; padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer; transition: all 0.2s;">📅 Kỳ đối soát T9 (26/08 - 25/09)</button>
                                <button type="button" class="tc-date-btn" id="tc-btn-preset-actual" onclick="setTcDatePreset('actual_mtd', this)" style="border: none; background: transparent; color: var(--text-secondary); padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s;">⭐ Tháng 9/2026 (01/09 - 25/09)</button>
                                <button type="button" class="tc-date-btn" id="tc-btn-preset-w38" onclick="setTcDatePreset('w38', this)" style="border: none; background: transparent; color: var(--text-secondary); padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s;">Tuần W38 (14/9 - 20/9)</button>
                                <button type="button" class="tc-date-btn" id="tc-btn-preset-w39" onclick="setTcDatePreset('w39', this)" style="border: none; background: transparent; color: var(--text-secondary); padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s;">Tuần W39 (21/9 - 25/9)</button>
                                <button type="button" class="tc-date-btn" id="tc-btn-preset-all" onclick="setTcDatePreset('all', this)" style="border: none; background: transparent; color: var(--text-secondary); padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s;">Tất cả</button>
                            </div>"""

if old_preset_buttons in html:
    html = html.replace(old_preset_buttons, new_preset_buttons)
    print("✅ Replaced preset buttons")
else:
    print("⚠️ Old preset buttons not found, check exact text")

# 3. Replace the 309KB static JSON and render logic
pos = html.find('window.TRANSPORT_COSTS_DATA = ')
if pos != -1:
    end_pos = html.find(';\n', pos)
    
    # Also find where setTcDatePreset and renderTransportCostTab end
    end_render_pos = html.find('function applyAllTransportFilters()', end_pos)
    
    new_js_logic = """window.TRANSPORT_COSTS_DATA = (window.DATA && window.DATA.transport_costs && window.DATA.transport_costs.trips) ? window.DATA.transport_costs : null;

        let chartTransportKtcInstance = null;
        let chartTransportNccInstance = null;
        let currentTcActivePreset = 'billing_sep';

        async function renderTransportCostTab() {
            try {
                // Fetch dữ liệu mới nhất từ API backend
                const res = await fetch('/api/transport-costs');
                if (res.ok) {
                    const d = await res.json();
                    if (d && d.trips && d.trips.length) {
                        window.TRANSPORT_COSTS_DATA = d;
                    }
                } else if (window.DATA && window.DATA.transport_costs && window.DATA.transport_costs.trips) {
                    window.TRANSPORT_COSTS_DATA = window.DATA.transport_costs;
                }
            } catch(e) {
                console.warn('Fallback to window.DATA.transport_costs:', e);
                if (window.DATA && window.DATA.transport_costs && window.DATA.transport_costs.trips) {
                    window.TRANSPORT_COSTS_DATA = window.DATA.transport_costs;
                }
            }

            // Tự động đồng bộ text ngày cập nhật trên Header banner
            if (window.TRANSPORT_COSTS_DATA && window.TRANSPORT_COSTS_DATA.region && window.TRANSPORT_COSTS_DATA.region.last_updated) {
                const elUpdated = document.getElementById('tc-last-updated-text');
                if (elUpdated) elUpdated.innerText = window.TRANSPORT_COSTS_DATA.region.last_updated;
            }

            // Kích hoạt preset Mặc định (Kỳ đối soát T9 kết thúc ngày 25/09)
            const btnBilling = document.getElementById('tc-btn-preset-billing');
            if (btnBilling) {
                setTcDatePreset('billing_sep', btnBilling);
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

            if (preset === 'billing_sep') {
                // 📅 Trọn vẹn Kỳ cước đối soát Tháng 9 (26/08 - 25/09)
                if (fromInput) fromInput.value = '2026-08-26';
                if (toInput) toInput.value = '2026-09-25';
            } else if (preset === 'actual_mtd') {
                // ⭐ Tháng 9/2026 (01/09 - 25/09)
                if (fromInput) fromInput.value = '2026-09-01';
                if (toInput) toInput.value = '2026-09-25';
            } else if (preset === 'w38') {
                // Tuần W38 (14/09 - 20/09)
                if (fromInput) fromInput.value = '2026-09-14';
                if (toInput) toInput.value = '2026-09-20';
            } else if (preset === 'w39') {
                // Tuần W39 (21/09 - 25/09)
                if (fromInput) fromInput.value = '2026-09-21';
                if (toInput) toInput.value = '2026-09-25';
            } else if (preset === 'all') {
                if (fromInput) fromInput.value = '';
                if (toInput) toInput.value = '';
            }

            applyAllTransportFilters();
        }

        function onTcCustomDateChange() {
            currentTcActivePreset = 'custom';
            document.querySelectorAll('.tc-date-btn').forEach(b => {
                b.classList.remove('active');
                b.style.background = 'transparent';
                b.style.color = 'var(--text-secondary)';
                b.style.fontWeight = '600';
            });
            applyAllTransportFilters();
        }

        function resetTransportCostFilters() {
            const btnBilling = document.getElementById('tc-btn-preset-billing');
            if (btnBilling) {
                setTcDatePreset('billing_sep', btnBilling);
            } else {
                setTcDatePreset('all', null);
            }
            const ktcSel = document.getElementById('tc-global-filter-ktc');
            if (ktcSel) ktcSel.value = 'all';
            const nccSel = document.getElementById('tc-global-filter-ncc');
            if (nccSel) nccSel.value = 'all';
            const typeSel = document.getElementById('tc-global-filter-type');
            if (typeSel) typeSel.value = 'all';
            applyAllTransportFilters();
        }

        """
    
    html = html[:pos] + new_js_logic + html[end_render_pos:]
    print("✅ Successfully replaced static 309KB JSON and modernized renderTransportCostTab logic")

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("🎉 Finished patching templates/index.html")
