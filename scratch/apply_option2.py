# -*- coding: utf-8 -*-
import os
import re

FILE_PATH = os.path.join(os.path.dirname(__file__), "send_realtime_and_target_gtalk.py")

with open(FILE_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update build_combined_report_html signature if not already
code = re.sub(
    r'def build_combined_report_html\s*\([^)]*\):',
    'def build_combined_report_html(am_name, bc_name, staff, target_info, report_date_str, update_time_str, show_target=True):',
    code
)

# 2. Add pct_real calculation right after pct_now
if 'pct_real = round(total_tc / total_gan * 100, 2)' not in code:
    code = code.replace(
        'pct_now = round(gtc_now / vol_today * 100, 2) if vol_today > 0 else 0.0',
        'pct_now = round(gtc_now / vol_today * 100, 2) if vol_today > 0 else 0.0\n    pct_real = round(total_tc / total_gan * 100, 2) if total_gan > 0 else 0.0'
    )

# 3. Add dynamic blocks before `html = f"""<!DOCTYPE html>`
old_badge_calc = 'overall_pct_badge_cls = "badge-solid-emerald" if pct_now >= 85 else ("badge-solid-gold" if pct_now >= 80 else "badge-solid-rose")'
new_badge_calc = '''    display_pct = pct_now if show_target else pct_real
    overall_pct_badge_cls = "badge-solid-emerald" if display_pct >= 85 else ("badge-solid-gold" if display_pct >= 80 else "badge-solid-rose")

    if show_target:
        tag_badge_html = f"""<div class="tags-row">
                        <div class="title-tag">
                            <span class="live-dot"></span>
                            ⚡ NĂNG SUẤT REAL-TIME & TARGET (CA 1 + TỒN)
                        </div>
                        {elevated_badge}
                    </div>"""
        sub_date_html = f'<div style="font-size: 11px; margin-top: 2px; color: #fef3c7;">So sánh N-1: {date_n1} ({pct_gtc_n1}%)</div>'
        kpi_grid_html = f"""<!-- 5 KPI TỔNG QUAN -->
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-label">% GTC N-1 (CA 1 + TỒN)</div>
                    <div class="kpi-val">{pct_gtc_n1}%</div>
                    <div class="kpi-sub">Ca 1 + Tồn hôm trước</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">HÀNG VỀ (CA 1 + TỒN)</div>
                    <div class="kpi-val">{vol_today:,}</div>
                    <div class="kpi-sub">Chốt đầu ngày 09h00</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">ĐÃ GIAO HIỆN TẠI</div>
                    <div class="kpi-val accent">{gtc_now:,}</div>
                    <div class="kpi-sub">Số đơn đã hoàn tất</div>
                </div>
                <div class="kpi-card highlight">
                    <div class="kpi-label">% GTC HIỆN TẠI (CA 1 + TỒN)</div>
                    <div class="kpi-val accent">{pct_now:.2f}%</div>
                    <div class="kpi-sub">Tính trên hàng đầu ngày</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">ĐÁNH GIÁ NHÂN SỰ</div>
                    <div class="kpi-val" style="font-size: 17px; line-height: 1.3; margin-top: 2px; color: #fef08a;">
                        {eval_summary}
                    </div>
                    <div class="kpi-sub">Tổng LTC: {total_ltc:,} đơn</div>
                </div>
            </div>"""
        section_target_html = f"""<!-- SECTION 1: TARGET GTC THEO CÁC MỐC -->
        <div class="section-target">
            <div class="section-title">
                <span>🎯 TIẾN ĐỘ TARGET GTC (CA 1 + TỒN) THEO CÁC MỐC</span>
                <span style="font-size: 11px; font-weight: 600; text-transform: none; color: #b45309;">(Cơ số tính: Hàng Ca 1 + Hàng Tồn chốt đầu ngày)</span>
            </div>
            <div class="target-cards-grid">
                {target_cards_html}
            </div>
        </div>"""
        footer_sub = "Hệ thống báo cáo tự động kết hợp Năng Suất Nhân Sự Real-Time & Theo Dõi Target GTC"
    else:
        tag_badge_html = """<div class="tags-row">
                        <div class="title-tag">
                            <span class="live-dot"></span>
                            ⚡ BÁO CÁO NĂNG SUẤT NVPTT REAL-TIME
                        </div>
                    </div>"""
        sub_date_html = f'<div style="font-size: 11px; margin-top: 2px; color: #fef3c7;">Ngày báo cáo: {report_date_str}</div>'
        kpi_grid_html = f"""<!-- 5 KPI NĂNG SUẤT -->
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-label">TỔNG ĐƠN GÁN GIAO</div>
                    <div class="kpi-val">{total_gan:,}</div>
                    <div class="kpi-sub">Gán hôm nay</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">GIAO THÀNH CÔNG</div>
                    <div class="kpi-val accent">{total_tc:,}</div>
                    <div class="kpi-sub">Đã hoàn tất</div>
                </div>
                <div class="kpi-card highlight">
                    <div class="kpi-label">% GTC BƯU CỤC</div>
                    <div class="kpi-val accent">{pct_real:.2f}%</div>
                    <div class="kpi-sub">Tiến độ phát hàng</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">LẤY THÀNH CÔNG (LTC)</div>
                    <div class="kpi-val">{total_ltc:,}</div>
                    <div class="kpi-sub">Đơn lấy hoàn tất</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">ĐÁNH GIÁ NHÂN SỰ</div>
                    <div class="kpi-val" style="font-size: 17px; line-height: 1.3; margin-top: 2px; color: #fef08a;">
                        {eval_summary}
                    </div>
                    <div class="kpi-sub">Hiệu quả ca làm việc</div>
                </div>
            </div>"""
        section_target_html = ""
        footer_sub = "Hệ thống báo cáo tự động Năng Suất Nhân Sự Real-Time"'''

code = code.replace(old_badge_calc, new_badge_calc)

# 4. Replace tags-row, date-badge, kpi-grid, and section-target in HTML
old_header_box = '''                    <div class="tags-row">
                        <div class="title-tag">
                            <span class="live-dot"></span>
                            ⚡ NĂNG SUẤT REAL-TIME & TARGET (CA 1 + TỒN)
                        </div>
                        {elevated_badge}
                    </div>'''
code = code.replace(old_header_box, '{tag_badge_html}')

old_date_sub = '<div style="font-size: 11px; margin-top: 2px; color: #fef3c7;">So sánh N-1: {date_n1} ({pct_gtc_n1}%)</div>'
code = code.replace(old_date_sub, '{sub_date_html}')

# Replace KPI grid block
old_kpi_grid = '''            <!-- 5 KPI TỔNG QUAN -->
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-label">% GTC N-1 (CA 1 + TỒN)</div>
                    <div class="kpi-val">{pct_gtc_n1}%</div>
                    <div class="kpi-sub">Ca 1 + Tồn hôm trước</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">HÀNG VỀ (CA 1 + TỒN)</div>
                    <div class="kpi-val">{vol_today:,}</div>
                    <div class="kpi-sub">Chốt đầu ngày 09h00</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">ĐÃ GIAO HIỆN TẠI</div>
                    <div class="kpi-val accent">{gtc_now:,}</div>
                    <div class="kpi-sub">Số đơn đã hoàn tất</div>
                </div>
                <div class="kpi-card highlight">
                    <div class="kpi-label">% GTC HIỆN TẠI (CA 1 + TỒN)</div>
                    <div class="kpi-val accent">{pct_now:.2f}%</div>
                    <div class="kpi-sub">Tính trên hàng đầu ngày</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">ĐÁNH GIÁ NHÂN SỰ</div>
                    <div class="kpi-val" style="font-size: 17px; line-height: 1.3; margin-top: 2px; color: #fef08a;">
                        {eval_summary}
                    </div>
                    <div class="kpi-sub">Tổng LTC: {total_ltc:,} đơn</div>
                </div>
            </div>'''
code = code.replace(old_kpi_grid, '{kpi_grid_html}')

# Replace section-target block
old_section_target = '''        <!-- SECTION 1: TARGET GTC THEO CÁC MỐC -->
        <div class="section-target">
            <div class="section-title">
                <span>🎯 TIẾN ĐỘ TARGET GTC (CA 1 + TỒN) THEO CÁC MỐC</span>
                <span style="font-size: 11px; font-weight: 600; text-transform: none; color: #b45309;">(Cơ số tính: Hàng Ca 1 + Hàng Tồn chốt đầu ngày)</span>
            </div>
            <div class="target-cards-grid">
                {target_cards_html}
            </div>
        </div>'''
code = code.replace(old_section_target, '{section_target_html}')

# Replace summary row display_pct and footer
code = code.replace('{pct_now:.2f}%</span>', '{display_pct:.2f}%</span>')
code = code.replace('<span>Hệ thống báo cáo tự động kết hợp Năng Suất Nhân Sự Real-Time & Theo Dõi Target GTC</span>', '<span>{footer_sub}</span>')

# 5. Update render_combined_image
old_render = '''def render_combined_image(am_name, bc_name, staff, target_info, report_date_str, update_time_str, out_path):
    """Render ảnh kết hợp bằng Playwright."""
    from playwright.sync_api import sync_playwright
    html_content = build_combined_report_html(am_name, bc_name, staff, target_info, report_date_str, update_time_str)'''

new_render = '''def render_combined_image(am_name, bc_name, staff, target_info, report_date_str, update_time_str, out_path, show_target=True):
    """Render ảnh kết hợp bằng Playwright."""
    from playwright.sync_api import sync_playwright
    html_content = build_combined_report_html(am_name, bc_name, staff, target_info, report_date_str, update_time_str, show_target=show_target)'''

code = code.replace(old_render, new_render)

# 6. Update build_combined_caption
old_caption = '''def build_combined_caption(am_name, bc_name, staff, target_info, update_time_str):
    tinh = target_info.get('tinh', '')
    date_n1 = target_info.get('date_n1', 'N-1')
    pct_gtc_n1 = target_info.get('pct_gtc_n1', 0.0)
    vol_today = target_info.get('vol_today', sum(s['gan'] for s in staff))
    gtc_now = target_info.get('gtc_now', sum(s['tc'] for s in staff))
    pct_now = round(gtc_now / vol_today * 100, 2) if vol_today > 0 else 0.0

    milestones = get_dynamic_milestones(pct_now)
    milestone_lines = []
    for pct in milestones:
        t_vol = int(round(vol_today * (pct / 100.0)))
        gap = t_vol - gtc_now
        if gap <= 0:
            milestone_lines.append(f"• Mốc <b>{pct}%</b>: ✅ Đã đạt (Vượt {abs(gap):,} đơn)")
        else:
            milestone_lines.append(f"• Mốc <b>{pct}%</b>: 🔴 <b>Thiếu {gap:,} đơn</b>")

    milestone_str = "\\n".join(milestone_lines)

    tot_ok = sum(1 for s in staff if "ok" in str(s["danh_gia"]).lower())
    tot_dat = sum(1 for s in staff if "đạt" in str(s["danh_gia"]).lower() or "dat" in str(s["danh_gia"]).lower())
    tot_thap = sum(1 for s in staff if "thấp" in str(s["danh_gia"]).lower() or "thap" in str(s["danh_gia"]).lower())
    total_ltc = sum(s["ltc"] for s in staff)

    eval_txt = f"{tot_ok} OK"
    if tot_dat > 0:
        eval_txt += f" · {tot_dat} Đạt"
    if tot_thap > 0:
        eval_txt += f" · {tot_thap} Thấp"

    tinh_str = f" ({tinh})" if tinh else ""

    caption = (
        f"⚡ <b>BÁO CÁO NĂNG SUẤT & TARGET GTC (CA 1 + TỒN)</b>\\n"
        f"🏢 Bưu cục: <b>{bc_name}</b>{tinh_str}\\n"
        f"👤 AM: <b>{am_name}</b> | 🕒 Cập nhật: <b>{update_time_str}</b>\\n\\n"
        f"📊 <b>TIẾN ĐỘ GTC (CA 1 + TỒN):</b>\\n"
        f"• % GTC Hôm qua ({date_n1}): <b>{pct_gtc_n1}% (Ca 1 + Tồn)</b>\\n"
        f"• Hàng đầu ngày (Ca 1 + Tồn): <b>{vol_today:,} đơn</b> | Đã giao: <b>{gtc_now:,} đơn ({pct_now:.2f}%)</b>\\n\\n"
        f"🎯 <b>SỐ ĐƠN CÒN THIẾU THEO TARGET (CA 1 + TỒN):</b>\\n"
        f"{milestone_str}"
    )
    return caption'''

new_caption = '''def build_combined_caption(am_name, bc_name, staff, target_info, update_time_str, show_target=True):
    tinh = target_info.get('tinh', '')
    tinh_str = f" ({tinh})" if tinh else ""
    total_gan = sum(s["gan"] for s in staff)
    total_tc = sum(s["tc"] for s in staff)
    total_ltc = sum(s["ltc"] for s in staff)
    pct_real = round(total_tc / total_gan * 100, 2) if total_gan > 0 else 0.0

    tot_ok = sum(1 for s in staff if "ok" in str(s["danh_gia"]).lower())
    tot_dat = sum(1 for s in staff if "đạt" in str(s["danh_gia"]).lower() or "dat" in str(s["danh_gia"]).lower())
    tot_thap = sum(1 for s in staff if "thấp" in str(s["danh_gia"]).lower() or "thap" in str(s["danh_gia"]).lower())

    eval_txt = f"{tot_ok} OK"
    if tot_dat > 0:
        eval_txt += f" · {tot_dat} Đạt"
    if tot_thap > 0:
        eval_txt += f" · {tot_thap} Thấp"

    if show_target:
        date_n1 = target_info.get('date_n1', 'N-1')
        pct_gtc_n1 = target_info.get('pct_gtc_n1', 0.0)
        vol_today = target_info.get('vol_today', total_gan)
        gtc_now = target_info.get('gtc_now', total_tc)
        pct_now = round(gtc_now / vol_today * 100, 2) if vol_today > 0 else 0.0

        milestones = get_dynamic_milestones(pct_now)
        milestone_lines = []
        for pct in milestones:
            t_vol = int(round(vol_today * (pct / 100.0)))
            gap = t_vol - gtc_now
            if gap <= 0:
                milestone_lines.append(f"• Mốc <b>{pct}%</b>: ✅ Đã đạt (Vượt {abs(gap):,} đơn)")
            else:
                milestone_lines.append(f"• Mốc <b>{pct}%</b>: 🔴 <b>Thiếu {gap:,} đơn</b>")

        milestone_str = "\\n".join(milestone_lines)

        caption = (
            f"⚡ <b>BÁO CÁO NĂNG SUẤT & TARGET GTC (CA 1 + TỒN)</b>\\n"
            f"🏢 Bưu cục: <b>{bc_name}</b>{tinh_str}\\n"
            f"👤 AM: <b>{am_name}</b> | 🕒 Cập nhật: <b>{update_time_str}</b>\\n\\n"
            f"📊 <b>TIẾN ĐỘ GTC (CA 1 + TỒN):</b>\\n"
            f"• % GTC Hôm qua ({date_n1}): <b>{pct_gtc_n1}% (Ca 1 + Tồn)</b>\\n"
            f"• Hàng đầu ngày (Ca 1 + Tồn): <b>{vol_today:,} đơn</b> | Đã giao: <b>{gtc_now:,} đơn ({pct_now:.2f}%)</b>\\n\\n"
            f"🎯 <b>SỐ ĐƠN CÒN THIẾU THEO TARGET (CA 1 + TỒN):</b>\\n"
            f"{milestone_str}"
        )
    else:
        caption = (
            f"⚡ <b>BÁO CÁO NĂNG SUẤT NVPTT REAL-TIME</b>\\n"
            f"🏢 Bưu cục: <b>{bc_name}</b>{tinh_str}\\n"
            f"👤 AM: <b>{am_name}</b> | 🕒 Cập nhật: <b>{update_time_str}</b>\\n\\n"
            f"📦 <b>TỔNG QUAN NĂNG SUẤT BƯU CỤC:</b>\\n"
            f"• <b>Gán giao:</b> <b>{total_gan:,} đơn</b> | <b>Giao TC:</b> <b>{total_tc:,} đơn ({pct_real:.2f}%)</b>\\n"
            f"• <b>Lấy TC (LTC):</b> <b>{total_ltc:,} đơn</b>\\n"
            f"• <b>Đánh giá nhân sự:</b> <b>{eval_txt}</b>\\n\\n"
            f"<i>(Bảng chi tiết số liệu từng CBĐP đính kèm bên dưới)</i>"
        )
    return caption'''

code = code.replace(old_caption, new_caption)

# 7. Add CLI argument and update main loop
code = code.replace(
    'parser.add_argument("--out-dir", type=str, default="", help="Thư mục xuất ảnh")',
    'parser.add_argument("--out-dir", type=str, default="", help="Thư mục xuất ảnh")\n    parser.add_argument("--only-nangsuat", action="store_true", help="Chỉ gửi báo cáo năng suất NVPTT, không kèm Target GTC")'
)

code = code.replace(
    'print(f"🚀 BẮT ĐẦU CHẠY BÁO CÁO NĂNG SUẤT & TARGET GTC KẾT HỢP ({update_time_str})", flush=True)',
    '''show_target = not args.only_nangsuat
    mode_str = "BÁO CÁO NĂNG SUẤT & TARGET GTC KẾT HỢP" if show_target else "BÁO CÁO NĂNG SUẤT NVPTT (KHÔNG TARGET)"
    print(f"🚀 BẮT ĐẦU CHẠY {mode_str} ({update_time_str})", flush=True)'''
)

code = code.replace(
    'render_combined_image(am_name, bc_name, staff, t_info, report_date_str, update_time_str, out_path)',
    'render_combined_image(am_name, bc_name, staff, t_info, report_date_str, update_time_str, out_path, show_target=show_target)'
)

code = code.replace(
    'caption = build_combined_caption(am_name, bc_name, staff, t_info, update_time_str)',
    'caption = build_combined_caption(am_name, bc_name, staff, t_info, update_time_str, show_target=show_target)'
)

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(code)

print("Applied Option 2 successfully to scratch/send_realtime_and_target_gtalk.py!")
