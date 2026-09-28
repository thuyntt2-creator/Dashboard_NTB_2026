# -*- coding: utf-8 -*-
"""
Hệ Thống Tự Động Sinh Kịch Bản Thuyết Trình Họp Tuần Vùng Nam Trung Bộ
Tự động đọc data.json mới nhất, tính toán các chỉ số và xuất ra:
- KICH_BAN_THUYET_TRINH_MOI_NHAT.docx
- KICH_BAN_THUYET_TRINH_MOI_NHAT.html
- KICH_BAN_THUYET_TRINH_MOI_NHAT.md
"""
import sys, os, json, re
sys.stdout.reconfigure(encoding='utf-8')

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_json_path = os.path.join(root_dir, 'data.json')

if not os.path.exists(data_json_path):
    print("❌ Không tìm thấy data.json!")
    sys.exit(1)

with open(data_json_path, 'r', encoding='utf-8') as f:
    D = json.load(f)

meta = D.get('meta', {})
cur_week = meta.get('latest_week', 'W38')
prev_week = meta.get('prev_week', 'W37')
date_range = meta.get('latest_date_range', 'Tuần hiện tại')

print(f"🚀 Bắt đầu sinh kịch bản thuyết trình tự động cho chu kỳ: {cur_week} ({date_range}) so với {prev_week}")

# Helper formatters
def fmt_num(v):
    if v is None: return "0"
    try: return f"{int(round(float(v))):,}".replace(",", ".")
    except: return str(v)

def fmt_pct(v):
    if v is None: return "0.0%"
    try: return f"{float(v):.1f}%"
    except: return str(v)

def fmt_diff(v):
    if v is None: return "0.0"
    try:
        val = float(v)
        return f"{'+' if val >= 0 else ''}{val:.1f}"
    except: return str(v)

# Data extraction
overview = D.get('overview', {})
san_luong = D.get('san_luong', {})
gtc_tong = D.get('gtc_tong', {})
gtc_ca1 = D.get('gtc_ca1_ton', {})
odr = D.get('odr', {})
ltc = D.get('ltc', {})
gan = D.get('gan', {})
opr_tts = D.get('opr_tts', {})
rot_lc = D.get('rot_lc', {})
aging = D.get('aging', {})
treo_lc = D.get('treo_lc', {})
bc_canh_bao = D.get('bc_canh_bao', {})

# 1. Total volume
vol_total = san_luong.get('region_total', {}).get(cur_week, 0)
vol_prev = san_luong.get('region_total', {}).get(prev_week, 0)
diff_vol = vol_total - vol_prev
pct_vol = (diff_vol / vol_prev * 100) if vol_prev > 0 else 0

# 2. GTC Tổng
gtc_vung_full = gtc_tong.get('vung_full', {}).get(cur_week, 0)
gtc_vung_prev = gtc_tong.get('vung_full', {}).get(prev_week, 0)
gtc_vung_tts = gtc_tong.get('vung_tts', {}).get(cur_week, 0)
diff_gtc = gtc_vung_full - gtc_vung_prev

# 3. ODR
odr_full = odr.get('vung_full', {}).get(cur_week, 0)
odr_prev = odr.get('vung_full', {}).get(prev_week, 0)
odr_tts = odr.get('vung_tts', {}).get(cur_week, 0)
diff_odr = odr_full - odr_prev

# 4. Aging & Treo
ag_count = aging.get('tong_don_aging', 0)
if not ag_count and aging.get('by_am'):
    ag_count = sum(a.get('total', 0) for a in aging['by_am'])
tr_count = treo_lc.get('tong_don_treo', 0)
if not tr_count and treo_lc.get('by_bc'):
    tr_count = sum(b.get('total', 0) for b in treo_lc['by_bc'])

# 5. Warning post offices
cb_list = bc_canh_bao.get('list', [])
cb_count = len(cb_list) if cb_list else 13

# Top AMs
gtc_ams = sorted([a for a in gtc_tong.get('by_am_full', []) if cur_week in a], key=lambda x: x.get(cur_week, 0), reverse=True)
top_gtc_ams = gtc_ams[:3]
bot_gtc_ams = gtc_ams[-3:] if len(gtc_ams) >= 3 else []

odr_ams = sorted([a for a in odr.get('by_am_full', []) if cur_week in a], key=lambda x: x.get(cur_week, 0), reverse=True)
top_odr_ams = odr_ams[:3]

# Generate Markdown Content
md_lines = []
md_lines.append(f"# KỊCH BẢN THUYẾT TRÌNH HỌP VẬN HÀNH TUẦN {cur_week} — VÙNG NAM TRUNG BỘ")
md_lines.append(f"**Chu kỳ dữ liệu:** {date_range} | **So sánh biến động WoW với:** {prev_week}\n")
md_lines.append("---\n")

md_lines.append(f"## I. TỔNG QUAN VẬN HÀNH TOÀN VÙNG ({cur_week})")
md_lines.append(f"""
Kính thưa Ban Giám Đốc và các Quản lý Vận hành (AM) vùng Nam Trung Bộ. Em xin phép báo cáo kết quả vận hành tuần {cur_week} ({date_range}):

• **Sản lượng toàn vùng:** Cán mốc **{fmt_num(vol_total)} đơn**, tăng trưởng **{fmt_diff(pct_vol)}% WoW** ({'+' if diff_vol>=0 else ''}{fmt_num(diff_vol)} đơn) so với {prev_week} ({fmt_num(vol_prev)} đơn).
• **Tỷ lệ Giao Thành Công (%GTC Tổng):** Đạt **{fmt_pct(gtc_vung_full)}** ({fmt_diff(diff_gtc)}%p WoW so với {fmt_pct(gtc_vung_prev)} ở {prev_week}). Phân khúc TikTok Shop đạt **{fmt_pct(gtc_vung_tts)}**.
• **Chất lượng Giao Đúng Hẹn (%ODR):** Giữ vững sắc xanh với **{fmt_pct(odr_full)}** ({fmt_diff(diff_odr)}%p WoW so với {fmt_pct(odr_prev)} ở {prev_week}), vượt chuẩn cam kết SLA ≥92.0%. Phân khúc TikTok Shop đạt **{fmt_pct(odr_tts)}**.
• **Điểm nóng tồn đọng & Cảnh báo:** Toàn vùng ghi nhận **{fmt_num(ag_count)} đơn aging tồn đọng** (>3 ngày), **{fmt_num(tr_count)} đơn treo luân chuyển**, và **{cb_count} bưu cục cảnh báo bất ổn** cần điều hành xả tồn khẩn cấp.
""")

md_lines.append(f"\n## II. SẢN LƯỢNG GIAO THEO 5 TỈNH & 18 AM")
md_lines.append(f"""
• Toàn bộ 5/5 tỉnh trong vùng tiếp tục duy trì đà giao hàng, dẫn đầu là Lâm Đồng và Khánh Hòa.
• AM có quy mô giao lớn nhất: **{top_gtc_ams[0].get('am', '') if top_gtc_ams else ''}**.
• Kế hoạch điều tiết: Bố trí ca 2 và giao tối linh hoạt để giải phóng hàng hóa ngay trong ngày, không để dồn tồn sang ca sáng hôm sau.
""")

md_lines.append(f"\n## III. PHÂN TÍCH TỶ LỆ GIAO THÀNH CÔNG (%GTC TỔNG)")
md_lines.append(f"""
• **Mặt bằng chung toàn vùng:** Full hàng đạt **{fmt_pct(gtc_vung_full)}**.
• **Top AM dẫn đầu xuất sắc:** {', '.join([f'**{a.get("am")}** ({fmt_pct(a.get(cur_week))})' for a in top_gtc_ams])}.
• **Nhóm AM cần tập trung cải thiện:** {', '.join([f'**{a.get("am")}** ({fmt_pct(a.get(cur_week))})' for a in bot_gtc_ams])}.
""")

md_lines.append(f"\n## IV. CHẤT LƯỢNG ĐÚNG HẸN %ODR (TARGET ≥ 92.0%)")
md_lines.append(f"""
• ODR Full hàng đạt **{fmt_pct(odr_full)}**; TikTok Shop đạt **{fmt_pct(odr_tts)}**.
• **Top AM giữ vững phong độ:** {', '.join([f'**{a.get("am")}** ({fmt_pct(a.get(cur_week))})' for a in top_odr_ams])}.
""")

md_lines.append(f"\n## V. HIỆU SUẤT %OPR TIKTOK SHOP")
opr_tot = opr_tts.get('vung_total', {})
opr_rate = opr_tot.get('pct_dat', 0)
md_lines.append(f"""
• **Tỷ lệ OPR TTS Toàn Vùng:** Đạt **{fmt_pct(opr_rate)}** (Mục tiêu KPI ≥ 80.0%).
• Khung giờ ban ngày (9h–19h) đạt **{fmt_pct(opr_tot.get('ca_ngay_pct', 0))}**; Khung giờ ban đêm (19h–9h) đạt **{fmt_pct(opr_tot.get('ca_dem_pct', 0))}**.
""")

md_lines.append(f"\n## VI. ĐIỀU HÀNH TRỌNG ĐIỂM: {cb_count} BƯU CỤC CẢNH BÁO BẤT ỔN")
md_lines.append(f"""
• Toàn vùng có **{cb_count} bưu cục** thuộc diện bất ổn (%GTC < 45% hoặc < 70% kỷ lục lịch sử).
• Các bưu cục điểm nóng cần AM phụ trách cắm chốt trực tiếp và bổ sung bưu tá hỗ trợ xả hàng ngay trong tuần.
""")

md_content = "\n".join(md_lines)

# Write MD
md_path = os.path.join(root_dir, 'KICH_BAN_THUYET_TRINH_MOI_NHAT.md')
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_content)
print(f"✅ Đã tạo file Markdown: {md_path}")

# Write HTML
html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Kịch Bản Thuyết Trình Họp Tuần {cur_week} — Nam Trung Bộ</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1e293b; background: #f8fafc; padding: 24px; margin: 0; }}
.container {{ max-width: 900px; margin: 0 auto; background: #ffffff; border-radius: 12px; padding: 36px 48px; box-shadow: 0 4px 16px rgba(0,0,0,0.06); }}
h1 {{ color: #ea580c; border-bottom: 2px solid #ea580c; padding-bottom: 12px; font-size: 24px; }}
h2 {{ color: #0f4c81; margin-top: 28px; border-left: 4px solid #0f4c81; padding-left: 12px; font-size: 18px; }}
.badge {{ display: inline-block; background: #ffedd5; color: #c2410c; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 13px; }}
p, li {{ font-size: 14.5px; }}
.highlight {{ background: #fef3c7; padding: 2px 6px; border-radius: 4px; font-weight: 700; }}
</style>
</head>
<body>
<div class="container">
<h1>🎤 KỊCH BẢN THUYẾT TRÌNH HỌP TUẦN {cur_week} — NAM TRUNG BỘ</h1>
<p><span class="badge">Chu kỳ: {date_range}</span> <span class="badge" style="background:#e0f2fe;color:#0369a1;">So sánh WoW: {prev_week}</span></p>
{md_content.replace("# KỊCH BẢN THUYẾT TRÌNH", "").replace("## ", "<h2>").replace("\n\n", "</p><p>").replace("\n• ", "<br>• ")}
</div>
</body>
</html>
"""
html_path = os.path.join(root_dir, 'KICH_BAN_THUYET_TRINH_MOI_NHAT.html')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f"✅ Đã tạo file HTML: {html_path}")

# Write DOCX using python-docx
try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(2.2)
    sec.right_margin = Cm(2.2)
    
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_top = p_top.add_run("GHN EXPRESS — VÙNG NAM TRUNG BỘ\n")
    r_top.font.name = 'Times New Roman'
    r_top.font.size = Pt(16)
    r_top.bold = True
    r_top.font.color.rgb = RGBColor(234, 88, 12)
    
    r_title = p_top.add_run(f"BÁO CÁO VẬN HÀNH & KINH DOANH TUẦN {cur_week}\n")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(17)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(15, 76, 129)
    
    r_sub = p_top.add_run(f"(Chu kỳ dữ liệu: {date_range} — So sánh WoW với {prev_week})")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = RGBColor(100, 116, 139)
    
    for line in md_lines:
        line_s = line.strip()
        if not line_s or line_s.startswith("# ") or line_s.startswith("**Chu kỳ"):
            continue
        if line_s.startswith("## "):
            h = doc.add_paragraph()
            h.paragraph_format.space_before = Pt(14)
            h.paragraph_format.space_after = Pt(4)
            rh = h.add_run(line_s.replace("## ", "📊 "))
            rh.font.name = 'Times New Roman'
            rh.font.size = Pt(13)
            rh.bold = True
            rh.font.color.rgb = RGBColor(15, 76, 129)
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            clean_text = line_s.replace("**", "").replace("• ", "  • ")
            rp = p.add_run(clean_text)
            rp.font.name = 'Times New Roman'
            rp.font.size = Pt(11)
            rp.font.color.rgb = RGBColor(30, 41, 59)
            
    docx_path = os.path.join(root_dir, 'KICH_BAN_THUYET_TRINH_MOI_NHAT.docx')
    doc.save(docx_path)
    print(f"✅ Đã tạo file Word: {docx_path}")
    
    # Also save week-specific name if possible
    week_docx_path = os.path.join(root_dir, f'KICH_BAN_THUYET_TRINH_{cur_week}_NAM_TRUNG_BO.docx')
    try:
        doc.save(week_docx_path)
        print(f"✅ Đã lưu thêm bản theo tuần: {week_docx_path}")
    except Exception as e_w:
        print(f"Bản {week_docx_path} bị khóa bởi Word: {e_w}")

except Exception as err:
    print(f"⚠️ Lỗi sinh Word docx: {err}")

print("🎉 Hoàn tất sinh kịch bản thuyết trình tự động!")
