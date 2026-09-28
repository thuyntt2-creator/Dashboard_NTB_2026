import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Header buttons for script
target_header = '<button id="btn-sync-sheets" class="bi-btn" title="Đồng bộ dữ liệu từ Google Sheets">\n            <i data-lucide="refresh-cw"></i> Đồng Bộ Sheets\n          </button>'
replacement_header = target_header + """
          <a href="/kich-ban" target="_blank" class="bi-btn" title="Xem Kịch Bản Thuyết Trình Họp" style="text-decoration:none;">
            <i data-lucide="file-text"></i> Kịch Bản Họp
          </a>
          <a href="/KICH_BAN_THUYET_TRINH_MOI_NHAT.docx" class="bi-btn" title="Tải File Kịch Bản Word (.docx)" style="text-decoration:none;">
            <i data-lucide="download"></i> Tải Word
          </a>"""

if target_header in content and '/kich-ban' not in content:
    content = content.replace(target_header, replacement_header)
    print("Header buttons added.")

# 2. tab-gan
old_gan = """          <div class="exec-banner-text">
            <h3>TỶ LỆ GÁN VẬN HÀNH TOÀN MẠNG THEO CA 1, CA 2 & GÁN TỔNG (TARGET ≥ 90.0%) (W38)</h3>
            <p>"""
new_gan = """          <div class="exec-banner-text">
            <h3 id="banner-gan-title">TỶ LỆ GÁN VẬN HÀNH TOÀN MẠNG THEO CA 1, CA 2 & GÁN TỔNG (TARGET ≥ 90.0%)</h3>
            <p id="banner-gan-summary">"""
if old_gan in content:
    content = content.replace(old_gan, new_gan)
    print("tab-gan banner IDs added.")

# 3. tab-odr
old_odr = """          <div class="exec-banner-text">
            <h3>PHÂN TÍCH HIỆU SUẤT %ODR (GIAO ĐÚNG HẸN SLA) TOÀN VÙNG (TARGET ≥ 92.0%) (W38)</h3>
            <p>"""
new_odr = """          <div class="exec-banner-text">
            <h3 id="banner-odr-title">PHÂN TÍCH HIỆU SUẤT %ODR (GIAO ĐÚNG HẸN SLA) TOÀN VÙNG (TARGET ≥ 92.0%)</h3>
            <p id="banner-odr-summary">"""
if old_odr in content:
    content = content.replace(old_odr, new_odr)
    print("tab-odr banner IDs added.")

# 4. tab-ltc
old_ltc = """          <div class="exec-banner-text">
            <h3>PHÂN TÍCH CHỈ SỐ %LTC (LẤY THÀNH CÔNG) THEO 18 AM & 5 TỈNH (TARGET ≥ 90.0%) (W38)</h3>
            <p>"""
new_ltc = """          <div class="exec-banner-text">
            <h3 id="banner-ltc-title">PHÂN TÍCH CHỈ SỐ %LTC (LẤY THÀNH CÔNG) THEO 18 AM & 5 TỈNH (TARGET ≥ 90.0%)</h3>
            <p id="banner-ltc-summary">"""
if old_ltc in content:
    content = content.replace(old_ltc, new_ltc)
    print("tab-ltc banner IDs added.")

# 5. tab-opr-tts
old_opr = """          <div class="exec-banner-text">
            <h3>PHÂN TÍCH CHỈ SỐ %OPR TIKTOK SHOP TOÀN VÙNG (TARGET KPI ≥ 80.0%) (W38)</h3>
            <p>"""
new_opr = """          <div class="exec-banner-text">
            <h3 id="banner-opr-title">PHÂN TÍCH CHỈ SỐ %OPR TIKTOK SHOP TOÀN VÙNG (TARGET KPI ≥ 80.0%)</h3>
            <p id="banner-opr-summary">"""
if old_opr in content:
    content = content.replace(old_opr, new_opr)
    print("tab-opr banner IDs added.")

# 6. tab-rot-lc
old_rot = """          <div class="exec-banner-text">
            <h3>PHÂN TÍCH TỶ TRỌNG RỚT ĐƠN LUÂN CHUYỂN THEO AM & TỈNH THÀNH (W38)</h3>
            <p>"""
new_rot = """          <div class="exec-banner-text">
            <h3 id="banner-rot-lc-title">PHÂN TÍCH TỶ TRỌNG RỚT ĐƠN LUÂN CHUYỂN THEO AM & TỈNH THÀNH</h3>
            <p id="banner-rot-lc-summary">"""
if old_rot in content:
    content = content.replace(old_rot, new_rot)
    print("tab-rot banner IDs added.")

old_rot_badge = """        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-red" style="font-size: 12px; padding: 6px 12px;">"""
new_rot_badge = """        <div class="exec-banner-actions">
          <span class="badge-tag badge-tag-red" id="banner-rot-lc-badge" style="font-size: 12px; padding: 6px 12px;">"""
if old_rot_badge in content:
    content = content.replace(old_rot_badge, new_rot_badge)
    print("tab-rot badge ID added.")

# 7. tab-fd
old_fd = """          <div class="exec-banner-text">
            <h3>BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ (W38)</h3>
            <p>"""
new_fd = """          <div class="exec-banner-text">
            <h3 id="banner-fd-title">BÁO CÁO TỶ LỆ %FD (RETURN / HOÀN TRẢ) — VÙNG NAM TRUNG BỘ</h3>
            <p id="banner-fd-summary">"""
if old_fd in content:
    content = content.replace(old_fd, new_fd)
    print("tab-fd banner IDs added.")

# 8. tab-bc-canhbao
old_cb = """            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-bottom: 8px;">
              <h3 style="color: #991b1b; font-size: 16px; font-weight: 800; margin: 0; display: flex; align-items: center; gap: 8px;">
                ĐIỀU HÀNH TRỌNG ĐIỂM: 13 BƯU CỤC TRONG DIỆN CẢNH BÁO BẤT ỔN (%GTC &lt; 45% HOẶC &lt; 70% LỊCH SỬ)
              </h3>"""
new_cb = """            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-bottom: 8px;">
              <h3 id="banner-canhbao-title" style="color: #991b1b; font-size: 16px; font-weight: 800; margin: 0; display: flex; align-items: center; gap: 8px;">
                ĐIỀU HÀNH TRỌNG ĐIỂM: 13 BƯU CỤC TRONG DIỆN CẢNH BÁO BẤT ỔN
              </h3>"""
if old_cb in content:
    content = content.replace(old_cb, new_cb)
    print("tab-bc-canhbao title ID added.")

old_cb_p = """            <p style="color: #1e293b; font-size: 13px; line-height: 1.65; margin: 0;">
              • <strong style="color: #b45309;">Tiêu chí phân loại cảnh báo:</strong>"""
new_cb_p = """            <p id="banner-canhbao-summary" style="color: #1e293b; font-size: 13px; line-height: 1.65; margin: 0;">
              • <strong style="color: #b45309;">Tiêu chí phân loại cảnh báo:</strong>"""
if old_cb_p in content:
    content = content.replace(old_cb_p, new_cb_p)
    print("tab-bc-canhbao summary ID added.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html successfully!")
