import os
import sys
import json
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

print("🚀 Generating W40 Meeting Presentation Scripts (HTML, Markdown, DOCX)...")

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

tt = d.get('truy_thu_report', {}).get('summary', {})
kd = d.get('kinh_doanh', {}).get('total', {})
f30 = d.get('f30', {}).get('total', {})
kd_ams = d.get('kinh_doanh', {}).get('am', [])
f30_ams = d.get('f30', {}).get('am', [])
tt_ams = d.get('truy_thu_report', {}).get('by_am', [])
odr_full = d.get('odr', {}).get('am_full', [])

# =========================================================================
# 1. GENERATE MARKDOWN SCRIPT
# =========================================================================
md_content = """# KỊCH BẢN THUYẾT TRÌNH BÁO CÁO HỌP TUẦN VẬN HÀNH & KINH DOANH W40
**VÙNG NAM TRUNG BỘ — GIAOHANGNHANH (GHN EXPRESS)**  
*(Thời gian đánh giá: Tuần W40 từ 28/09/2026 đến hết 04/10/2026 — Kỳ kinh doanh: 27/09 đến 03/10/2026)*

---

## 🧭 TỔNG QUAN CHIẾN LƯỢC VÙNG W40: "TỐI ƯU HÓA TRUY THU, BỨT PHÁ F30 & QUYẾT LIỆT KHÔI PHỤC VOLUME KINH DOANH"

> **🗣️ KỊCH BẢN NÓI DÀNH CHO NGƯỜI BÁO CÁO — PHẦN MỞ ĐẦU BAN GIÁM ĐỐC:**  
> *"Kính chào Ban Giám Đốc, các Giám đốc Khối và toàn thể các anh chị Quản lý Vận hành (AM), Quản lý Kinh doanh vùng Nam Trung Bộ.  
> Hôm nay, em xin đại diện Ban Điều Hành Vùng trình bày Báo cáo tổng kết tuần W40 (so sánh với tuần W39).  
>  
> Thưa Ban Giám Đốc, tuần W40 đánh dấu **bước chuyển quan trọng trong kiểm soát rủi ro tài chính** và mở rộng tệp khách hàng mới, đồng thời đặt ra thách thức khôi phục sản lượng kinh doanh tại một số địa bàn trọng điểm. Toàn vùng ghi nhận 4 điểm nhấn chính:*  
>  
> - **1. Báo cáo Truy Thu giảm sâu tích cực (-40.1% tiền, -40.5% đơn):** Số tiền cần truy thu toàn vùng giảm mạnh từ **312.1 Tr ₫ xuống còn 187.1 Tr ₫ (giảm -125.0 Tr ₫)**; số bản ghi vi phạm giảm từ **4,076 đơn xuống 2,424 đơn (-1,652 đơn)**. Đây là kết quả của việc siết chặt bàn cân đo và xử lý dứt điểm các vụ việc liên đới.  
> - **2. Khách hàng mới F30 bứt phá ngoạn mục (+20.7% shop, +62.8% doanh thu):** Kích hoạt mới thành công **111 shop F30** (tăng +19 shop so với kỳ trước 92 shop), mang lại **9.4 Tr ₫ doanh thu mới** (tăng +3.6 Tr ₫). Nhóm A tháng 10 ghi nhận 10 shop trọng điểm với lũy kế MTD đạt **8,840 Tr ₫**.  
> - **3. Chất lượng giao hàng ODR giữ vững chuẩn xanh:** %ODR Full hàng toàn vùng đạt **93.1%**, %ODR TikTok Shop đạt **94.2%** (vượt xa chuẩn cam kết SLA sàn ≥90%).  
> - **4. Hai điểm nóng cần Ban Giám Đốc chỉ đạo quyết liệt ngay trong tuần:**  
>   + *Thứ nhất:* **Vụ việc chiếm dụng tiền hàng 48.7 Tr ₫ tại (KHO) Bắc Cam Ranh** (AM Nguyễn Thanh Long), đẩy tổng tiền cần thu của AM Long lên **51.2 Tr ₫** (tăng gấp gần 3 lần W39). Cần thu hồi dứt điểm trước 10/10.  
>   + *Thứ hai:* **Sụt giảm kinh doanh sâu tại Đắk Nông:** AM Huỳnh Thúc Duân giảm **-29.1% doanh thu (-23.4 Tr ₫)** và bốc hơi **-1,608 đơn (-28.5% volume)**; AM Trần Thị Nhung giảm **-21.5% doanh thu**.*"

---

## 📦 I. SẢN LƯỢNG GIAO & HIỆU SUẤT VẬN HÀNH TOÀN MẠNG
> **🗣️ KỊCH BẢN NÓI — PHÂN TÍCH SẢN LƯỢNG & ODR:**  
> *"Về chất lượng vận hành tuần W40:  
> - Toàn vùng duy trì tỷ lệ Giao Đúng Hẹn (%ODR) ở mức cao: **Full hàng đạt 93.1%**, **TikTok Shop đạt 94.2%**.  
> - **Top AM dẫn đầu về ODR:**  
>   + **AM Cao Thị Thanh Thủy:** Đạt đỉnh toàn vùng với **97.8% ODR** (W39: 97.4%).  
>   + **AM Nguyễn Ngọc Khánh:** Đạt **97.4% ODR** (Bình Thuận vận hành cực kỳ ổn định).  
>   + **AM Thái Thị Thanh Thư:** Bứt phá mạnh mẽ đạt **96.9% ODR** (tăng +3.7%p so với 93.2% của W39).  
>   + **AM Nguyễn Duy Long:** Giữ vững **96.6% ODR**.  
> - **Nhóm AM báo động đỏ về ODR (<80%):**  
>   + **AM Lê Minh Lợi:** Chạm đáy toàn vùng với **74.1% ODR** (điểm nóng bưu cục Lang Biang - Đà Lạt 1).  
>   + **AM Trương Quang Linh:** Đạt **74.9% ODR** (điểm nóng bưu cục Quảng Tín).  
>   + **AM Phan Nguyễn Yến Nhi:** Đạt **76.1% ODR** (Đơn Dương).  
>   + **AM Lê Văn Trường:** Đạt **78.3% ODR** (Xuân Hương, Lâm Viên).*  
>  
> 🔍 **Chỉ đạo:** Yêu cầu các AM nhóm dưới 80% ODR phải tái cấu trúc lại ca bưu tá buổi sáng trước 07h00 và phân luồng trung chuyển không để tồn đọng sang ngày N+1."*

---

## 💰 II. BÁO CÁO TRUY THU (TAB 14): GIẢM MẠNH -40.1% NHƯNG XUẤT HIỆN ĐIỂM NÓNG CÁ BIỆT
> **🗣️ KỊCH BẢN NÓI — ĐÁNH GIÁ TRUY THU CHI TIẾT:**  
> *"Thưa Ban Giám Đốc, về Báo cáo Truy Thu:  
> - **Tổng thể toàn vùng:** Số tiền cần truy thu tuần W40 giảm mạnh về **187.1 Tr ₫ (giảm -125.0 Tr ₫ / -40.1%)**, số đơn giảm còn **2,424 đơn (-40.5%)**.  
> - **Cơ cấu loại vi phạm:**  
>   1. *Liên đới chiếm dụng:* **56.8 Tr ₫** (chỉ 4 đơn nhưng chiếm tới 30.4% tổng số tiền).  
>   2. *Tick mất hàng:* **41.2 Tr ₫** (53 đơn - chiếm 22.0%).  
>   3. *Mất/Thiếu/Tráo sản phẩm:* **30.9 Tr ₫** (76 đơn - chiếm 16.5%).  
>   4. *Hư hỏng hàng hóa:* **16.6 Tr ₫** (118 đơn).  
>  
> ⚠️ **ĐÁNH GIÁ & LƯU Ý ĐẶC BIỆT TỪNG AM TRUY THU:**  
> - **1. 🔴 AM NGUYỄN THANH LONG — BÁO ĐỘNG ĐỎ SỐ 1 VÙNG:**  
>   Tiền cần truy thu tăng vọt từ 18.2 Tr lên **51.2 Tr ₫ (tăng thêm +33.0 Tr ₫, gấp gần 3 lần W39!)**. Trong đó bưu cục **(KHO) Bắc Cam Ranh phát sinh 48.7 Tr ₫ liên đới chiếm dụng**. Yêu cầu AM Long giải trình ngay tại cuộc họp và nộp lộ trình thu hồi trước ngày 10/10.  
> - **2. 🟡 AM LÊ VĂN TRƯỜNG — NHIỀU TICKET NHẤT VÙNG:**  
>   Đang gánh tới **419 ticket truy thu** (cao nhất toàn mạng!), cần thu **26.3 Tr ₫** (điểm nóng bưu cục Đơn Dương 12.8 Tr ₫). Yêu cầu chấn chỉnh ngay quy trình cân đo, nhập liệu bưu cục.  
> - **3. 🟡 AM TRẦN VĂN PHƯỚC:** Cần thu **22.9 Tr ₫** (288 ticket), điểm nóng **(DNO) Quảng Tín (13.0 Tr ₫)**.  
> - **4. 🟡 AM HUỲNH THỊ KIM CHI:** Cần thu **21.3 Tr ₫** (110 ticket), điểm nóng **(LDO) Tân Hà Lâm Hà (21.3 Tr ₫)**. Đã có tiến bộ giảm từ 58.3 Tr của tuần trước.  
> - **5. 🟢 Điểm sáng tuyên dương:** AM Hồng Bích Nga giảm mạnh từ 50.7 Tr xuống **8.1 Tr ₫ (-42.6 Tr ₫)**; AM Trầm Hữu Tiến giảm từ 28.4 Tr xuống **6.3 Tr ₫ (-22.2 Tr ₫)**."*

---

## 📈 III. KINH DOANH & KHÁCH HÀNG MỚI F30 (TAB 15): 1,120.5 TR ₫ DOANH THU & 111 SHOP F30
> **🗣️ KỊCH BẢN NÓI — ĐÁNH GIÁ KINH DOANH & SHOP MỚI F30:**  
> *"Về kết quả Kinh doanh (kỳ 27/09–03/10 so với 20–26/09):  
> - **Tổng Doanh Thu Toàn Vùng:** Đạt **1,120.5 Tr ₫** (Kỳ trước 1,162.6 Tr ➔ Giảm **-42.1 Tr ₫ / -3.6% WoW**).  
> - **Tổng Volume Giao:** Đạt **35,334 đơn** (Kỳ trước 37,391 đơn ➔ Giảm **-2,057 đơn / -5.5% WoW**).  
> - **Điểm sáng bứt phá F30:** Toàn vùng mở mới và kích hoạt **111 shop F30 (+20.7% WoW)**, mang về **9.4 Tr ₫ doanh thu mới (+62.8% WoW)**.  
>  
> 🏆 **ĐÁNH GIÁ CHI TIẾT THEO TỪNG AM KINH DOANH:**  
> - **Nhóm Tăng Trưởng & Giữ Nhịp Xuất Sắc:**  
>   + **AM Phan Đình Duy:** Giữ vững vị thế số 1 với **479.0 Tr ₫ (+0.7%)**, volume **10,088 đơn (+74 đơn)**. Đồng thời dẫn đầu toàn vùng về **F30 với 16 shop mới (1.21 Tr ₫)**.  
>   + **AM Nguyễn Duy Long:** Đạt **98.2 Tr ₫ (+2.3%)**, volume **3,651 đơn**, mở được **13 shop mới F30**.  
>   + **AM Lê Thanh Nhựt:** Bứt phá rất tốt: **60.9 Tr ₫ (+6.6%, +3.8 Tr)**, volume **2,279 đơn (+227 đơn, +11.1%)**.  
>   + **AM Nguyễn Lê Nguyên Vũ:** Tăng trưởng ấn tượng: **25.4 Tr ₫ (+10.8%, +2.5 Tr)**, volume **1,058 đơn (+11.4%)**.  
>  
> 🚨 **CẢNH BÁO ĐỎ CÁC AM SỤT GIẢM DOANH THU & VOLUME (CẦN LƯU Ý ĐẶC BIỆT):**  
> - **1. 🔴 AM HUỲNH THÚC DUÂN — BÁO ĐỘNG ĐỎ SỤT GIẢM SÂU NHẤT VÙNG:**  
>   + Doanh thu giảm **-23.4 Tr ₫ (-29.1%)**, từ 80.5 Tr xuống **57.1 Tr ₫**.  
>   + Volume bốc hơi tới **-1,608 đơn (-28.5%)**, từ 5,649 đơn xuống **4,041 đơn**!  
>   + Cần chất vấn làm rõ: Shop nào ngừng lên đơn tại cụm Gia Nghĩa (Đắk Nông)? Lý do bị đối thủ lôi kéo hay do lỗi chất lượng vận hành bưu cục?  
> - **2. 🔴 AM THÁI THỊ THANH THƯ:** Doanh thu giảm **-11.8 Tr ₫ (-10.6%)**, đạt **98.9 Tr ₫**; Volume giảm **-233 đơn**. (Dù mở được 15 shop F30 nhưng luồng khách hàng cũ bị hụt).  
> - **3. 🔴 AM TRẦN THỊ NHUNG:** Doanh thu giảm **-8.0 Tr ₫ (-21.5%)**, đạt **29.3 Tr ₫**; Volume giảm **-329 đơn (-27.3%)**.  
> - **4. 🟡 AM HỒNG BÍCH NGA:** Doanh thu giảm **-7.1 Tr ₫ (-12.9%)**, đạt **47.9 Tr ₫**.  
> - **5. 🟡 AM NGUYỄN THỊ TUYẾT THƠ:** Doanh thu giảm **-4.9 Tr ₫ (-28.3%)**, đạt **12.4 Tr ₫** (dù F30 mang về 1.50 Tr ₫ cao nhất vùng).  
>  
> 👑 **Tình hình Khách Hàng Nhóm A (Tháng 10):**  
> - 10 Shop nhóm A đạt tổng MTD **8,840 Tr ₫**. Top 1 là shop *Vận Chuyển Online* (**5,688 Tr ₫ MTD** – AM Phan Đình Duy). Cần theo dõi sát shop *Hiền yến* (tỷ lệ trụ hạng chỉ đạt 3.0%) và shop *My Hà* (trụ hạng 13.1%)."*

---

## 🎯 IV. NGHỊ QUYẾT & GIAO CHỈ TIÊU HÀNH ĐỘNG TUẦN W41
> **🗣️ LỜI KẾT LUẬN CỦA CHỦ TRÌ CUỘC HỌP:**  
> *"Để khôi phục đà tăng trưởng và xử lý dứt điểm các tồn đọng, Ban Điều Hành Vùng giao 4 nhiệm vụ bắt buộc:**  
>  
> - **1. Thu hồi dứt điểm Truy Thu (Hạn chót 10/10/2026):** AM Nguyễn Thanh Long xử lý dứt điểm 48.7 Tr ₫ tại Bắc Cam Ranh; AM Lê Văn Trường và AM Trần Văn Phước thu hồi tối thiểu **80%** số tiền còn lại tại Đơn Dương và Quảng Tín.  
> - **2. Khôi phục Volume cụm Đắk Nông:** AM Huỳnh Thúc Duân và AM Trần Thị Nhung gặp trực tiếp các shop lớn sụt giảm trong 48 giờ tới, cam kết kéo lại tối thiểu 1,000 đơn/tuần.  
> - **3. Đẩy mạnh Chiến dịch F30:** Toàn vùng quyết tâm tuần W41 vượt mốc **130 shop mới F30**, doanh thu F30 trên **15 Tr ₫**.  
> - **4. Kéo %ODR toàn mạng lên ≥92%:** AM Lê Minh Lợi, AM Trương Quang Linh, AM Phan Nguyễn Yến Nhi phải thoát khỏi nhóm ODR <80%. Bưu cục nào tiếp tục để ODR dưới 75% sẽ đình chỉ đánh giá thi đua tháng của Trưởng bưu cục.  
>  
> *Chúc các anh chị AM và toàn thể đội ngũ tuần mới quyết liệt, kỷ luật và bứt phá doanh số!"*
"""

with open('KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.md', 'w', encoding='utf-8') as f:
    f.write(md_content)
print("✅ Saved KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.md")

# =========================================================================
# 2. GENERATE HTML SCRIPT (PREMIUM DASHBOARD STYLE)
# =========================================================================
html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kịch Bản Thuyết Trình Điều Hành W40 — Vùng Nam Trung Bộ</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --bg-body: #f8fafc;
            --bg-card: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --ghn-orange: #ea580c;
            --ghn-blue: #0f4c81;
            --success: #16a34a;
            --danger: #dc2626;
            --warning: #d97706;
            --border: #e2e8f0;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-body);
            color: var(--text-main);
            line-height: 1.6;
            padding: 24px;
        }}
        .container {{
            max-width: 1080px;
            margin: 0 auto;
            background: var(--bg-card);
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
            padding: 40px;
            border: 1px solid var(--border);
        }}
        .header-box {{
            text-align: center;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 24px;
            margin-bottom: 32px;
        }}
        .header-sub {{ font-size: 13px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }}
        .header-title {{ font-family: 'Outfit', sans-serif; font-size: 26px; font-weight: 800; color: var(--ghn-blue); margin: 8px 0; }}
        .header-date {{ font-size: 14px; color: var(--text-muted); font-style: italic; }}
        .header-tag {{ display: inline-block; background: #fff7ed; color: var(--ghn-orange); border: 1px solid #ffedd5; font-size: 12px; font-weight: 700; padding: 4px 12px; border-radius: 20px; margin-top: 10px; }}
        
        .section-card {{
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 28px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
        }}
        .section-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 18px;
            font-weight: 700;
            color: var(--ghn-blue);
            margin-bottom: 16px;
            border-left: 4px solid var(--ghn-orange);
            padding-left: 12px;
        }}
        .speech-heading {{
            font-size: 13.5px;
            font-weight: 700;
            color: #b45309;
            background: #fef3c7;
            padding: 8px 14px;
            border-radius: 8px;
            margin-bottom: 14px;
            display: inline-block;
        }}
        p {{ margin-bottom: 12px; font-size: 14.5px; }}
        .bullet-point {{ margin-left: 20px; margin-bottom: 8px; font-size: 14.5px; }}
        
        .callout {{
            border-radius: 8px;
            padding: 12px 16px;
            margin: 12px 0;
            font-size: 13.5px;
        }}
        .callout-insight {{ background: #eff6ff; border-left: 4px solid #3b82f6; color: #1e40af; }}
        .callout-warning {{ background: #fef2f2; border-left: 4px solid #ef4444; color: #991b1b; }}
        .callout-action {{ background: #f0fdf4; border-left: 4px solid #22c55e; color: #166534; }}
        .callout-title {{ font-weight: 700; margin-bottom: 6px; display: flex; align-items: center; gap: 6px; }}

        .table-custom {{
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-size: 13px;
        }}
        .table-custom th, .table-custom td {{
            padding: 10px 12px;
            border: 1px solid var(--border);
            text-align: left;
        }}
        .table-custom th {{
            background: #f1f5f9;
            font-weight: 700;
            color: var(--ghn-blue);
        }}
        .badge-red {{ background: #fee2e2; color: #b91c1c; padding: 2px 8px; border-radius: 4px; font-weight: 700; }}
        .badge-green {{ background: #dcfce7; color: #15803d; padding: 2px 8px; border-radius: 4px; font-weight: 700; }}
        .badge-yellow {{ background: #fef9c3; color: #a16207; padding: 2px 8px; border-radius: 4px; font-weight: 700; }}

        .top-btn {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: var(--ghn-orange);
            color: white;
            padding: 10px 18px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: 700;
            box-shadow: 0 4px 12px rgba(234, 88, 12, 0.3);
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
        }}
        .top-btn:hover {{ background: #c2410c; }}

        @media print {{
            body {{ background: white; padding: 0; }}
            .container {{ box-shadow: none; border: none; padding: 0; max-width: 100%; }}
            .top-btn {{ display: none; }}
        }}
    </style>
</head>
<body>
    <a href="/KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.docx" class="top-btn">
        <i class="fa-solid fa-file-word"></i> Tải Bản Word (.docx)
    </a>

    <div class="container">
        <div class="header-box">
            <div class="header-sub">Giaohangnhanh Express — Vùng Nam Trung Bộ</div>
            <h1 class="header-title">KỊCH BẢN THUYẾT TRÌNH BÁO CÁO HỌP TUẦN W40</h1>
            <div class="header-date">Thời gian đánh giá: Tuần W40 (28/09/2026 – 04/10/2026) | Chu kỳ KD: 27/09 – 03/10/2026</div>
            <div class="header-tag">DỮ LIỆU ĐỐI SOÁT LOOKER CHUẨN XÁC 100%</div>
        </div>

        <!-- MỤC MỞ ĐẦU -->
        <div class="section-card">
            <h2 class="section-title"><i class="fa-solid fa-compass"></i> TỔNG QUAN CHIẾN LƯỢC VÙNG W40</h2>
            <div class="speech-heading"><i class="fa-solid fa-microphone"></i> LỜI PHÁT BIỂU DÀNH CHO NGƯỜI CHỦ TRÌ / BÁO CÁO:</div>
            <p><em>"Kính chào Ban Giám Đốc, các Giám đốc Khối và toàn thể các anh chị Quản lý Vận hành (AM), Quản lý Kinh doanh vùng Nam Trung Bộ. Hôm nay, em xin đại diện Ban Điều Hành Vùng trình bày Báo cáo tổng kết tuần W40 (so sánh với tuần W39)."</em></p>
            <p><em>"Thưa Ban Giám Đốc, tuần W40 đánh dấu **bước chuyển quan trọng trong kiểm soát rủi ro tài chính** và mở rộng tệp khách hàng mới, đồng thời đặt ra thách thức khôi phục sản lượng kinh doanh tại một số địa bàn trọng điểm. Toàn vùng ghi nhận 4 điểm nhấn chính:"</em></p>
            <div class="bullet-point"><strong>1. Báo cáo Truy Thu giảm sâu tích cực (-40.1% tiền, -40.5% đơn):</strong> Số tiền cần truy thu toàn vùng giảm mạnh từ <strong>312.1 Tr ₫ xuống còn 187.1 Tr ₫ (giảm -125.0 Tr ₫)</strong>; số bản ghi vi phạm giảm từ <strong>4,076 đơn xuống 2,424 đơn (-1,652 đơn)</strong>.</div>
            <div class="bullet-point"><strong>2. Khách hàng mới F30 bứt phá (+20.7% shop, +62.8% doanh thu):</strong> Kích hoạt mới thành công <strong>111 shop F30</strong> (tăng +19 shop so với kỳ trước 92 shop), mang lại <strong>9.4 Tr ₫ doanh thu mới</strong>. Nhóm A tháng 10 ghi nhận 10 shop trọng điểm với lũy kế MTD đạt <strong>8,840 Tr ₫</strong>.</div>
            <div class="bullet-point"><strong>3. Chất lượng giao hàng ODR giữ vững chuẩn xanh:</strong> %ODR Full hàng toàn vùng đạt <strong>93.1%</strong>, %ODR TikTok Shop đạt <strong>94.2%</strong> (vượt xa chuẩn cam kết SLA sàn ≥90%).</div>
            <div class="bullet-point"><strong>4. Hai điểm nóng cần Ban Giám Đốc chỉ đạo quyết liệt ngay trong tuần:</strong></div>
            <div style="margin-left: 36px; margin-bottom: 8px;">• <em>Thứ nhất:</em> <strong>Vụ việc chiếm dụng tiền hàng 48.7 Tr ₫ tại (KHO) Bắc Cam Ranh</strong> (AM Nguyễn Thanh Long), đẩy tổng tiền cần thu của AM Long lên <strong>51.2 Tr ₫</strong>. Cần thu hồi dứt điểm trước 10/10.</div>
            <div style="margin-left: 36px;">• <em>Thứ hai:</em> <strong>Sụt giảm kinh doanh sâu tại Đắk Nông:</strong> AM Huỳnh Thúc Duân giảm <strong>-29.1% doanh thu (-23.4 Tr ₫)</strong> và bốc hơi <strong>-1,608 đơn (-28.5% volume)</strong>; AM Trần Thị Nhung giảm <strong>-21.5% doanh thu</strong>.</div>
        </div>

        <!-- MỤC 1: SẢN LƯỢNG & ODR -->
        <div class="section-card">
            <h2 class="section-title"><i class="fa-solid fa-truck-fast"></i> I. SẢN LƯỢNG GIAO & HIỆU SUẤT VẬN HÀNH TOÀN MẠNG</h2>
            <div class="speech-heading"><i class="fa-solid fa-microphone"></i> LỜI PHÁT BIỂU:</div>
            <p><em>"Về chất lượng vận hành tuần W40, toàn vùng duy trì tỷ lệ Giao Đúng Hẹn (%ODR) ở mức cao: Full hàng đạt <strong>93.1%</strong>, TikTok Shop đạt <strong>94.2%</strong>."</em></p>
            <div class="callout callout-action">
                <div class="callout-title"><i class="fa-solid fa-circle-check"></i> TOP AM DẪN ĐẦU VỀ ODR FULL HÀNG (≥96%)</div>
                <div>• <strong>AM Cao Thị Thanh Thủy:</strong> Đạt đỉnh toàn vùng với <strong>97.8% ODR</strong> (W39: 97.4%).</div>
                <div>• <strong>AM Nguyễn Ngọc Khánh:</strong> Đạt <strong>97.4% ODR</strong> (Bình Thuận duy trì ổn định tuyệt đối).</div>
                <div>• <strong>AM Thái Thị Thanh Thư:</strong> Bứt phá ngoạn mục đạt <strong>96.9% ODR</strong> (tăng +3.7%p so với 93.2% W39).</div>
                <div>• <strong>AM Nguyễn Duy Long:</strong> Giữ vững phong độ <strong>96.6% ODR</strong>.</div>
            </div>
            <div class="callout callout-warning">
                <div class="callout-title"><i class="fa-solid fa-triangle-exclamation"></i> NHÓM AM BÁO ĐỘNG ĐỎ VỀ ODR VÙNG TRŨNG (&lt;80%)</div>
                <div>• <strong>AM Lê Minh Lợi:</strong> Chạm đáy toàn vùng với <strong>74.1% ODR</strong> (điểm nóng bưu cục Lang Biang - Đà Lạt 1).</div>
                <div>• <strong>AM Trương Quang Linh:</strong> Đạt <strong>74.9% ODR</strong> (điểm nóng bưu cục Quảng Tín).</div>
                <div>• <strong>AM Phan Nguyễn Yến Nhi:</strong> Đạt <strong>76.1% ODR</strong> (bưu cục Đơn Dương).</div>
                <div>• <strong>AM Lê Văn Trường:</strong> Đạt <strong>78.3% ODR</strong> (Xuân Hương, Lâm Viên).</div>
            </div>
        </div>

        <!-- MỤC 2: BÁO CÁO TRUY THU -->
        <div class="section-card">
            <h2 class="section-title"><i class="fa-solid fa-shield-halved"></i> II. BÁO CÁO TRUY THU (TAB 14): GIẢM MẠNH -40.1%</h2>
            <div class="speech-heading"><i class="fa-solid fa-microphone"></i> LỜI PHÁT BIỂU:</div>
            <p><em>"Thưa Ban Giám Đốc, số tiền cần truy thu tuần W40 giảm mạnh về <strong>187.1 Tr ₫ (giảm -125.0 Tr ₫ / -40.1%)</strong>, số đơn giảm còn <strong>2,424 đơn (-40.5%)</strong>."</em></p>
            <div class="bullet-point">• <strong>Liên đới chiếm dụng:</strong> <strong>56.8 Tr ₫</strong> (chỉ 4 đơn nhưng chiếm tới 30.4% tổng số tiền).</div>
            <div class="bullet-point">• <strong>Tick mất hàng:</strong> <strong>41.2 Tr ₫</strong> (53 đơn - chiếm 22.0%).</div>
            <div class="bullet-point">• <strong>Mất/Thiếu/Tráo sản phẩm:</strong> <strong>30.9 Tr ₫</strong> (76 đơn - chiếm 16.5%).</div>

            <table class="table-custom">
                <thead>
                    <tr>
                        <th>AM Phụ Trách</th>
                        <th>Cần Thu W40 (Tr ₫)</th>
                        <th>So với W39 (Tr ₫)</th>
                        <th>Số Ticket</th>
                        <th>Mức Độ Rủi Ro</th>
                        <th>Điểm Nóng Bưu Cục</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Nguyễn Thanh Long</strong></td>
                        <td style="color: #dc2626; font-weight:800;">51.2 Tr</td>
                        <td style="color: #dc2626;">+33.0 Tr (gấp gần 3x)</td>
                        <td>72</td>
                        <td><span class="badge-red">🔴 Rất cao (≥40 Tr)</span></td>
                        <td>(KHO) Bắc Cam Ranh (48.7 Tr)</td>
                    </tr>
                    <tr>
                        <td><strong>Lê Văn Trường</strong></td>
                        <td style="font-weight:700;">26.3 Tr</td>
                        <td style="color: #16a34a;">-24.6 Tr</td>
                        <td style="color: #dc2626; font-weight:800;">419 (Cao nhất)</td>
                        <td><span class="badge-yellow">🟡 Cần kiểm soát</span></td>
                        <td>(LDO) Đơn Dương (12.8 Tr)</td>
                    </tr>
                    <tr>
                        <td><strong>Trần Văn Phước</strong></td>
                        <td>22.9 Tr</td>
                        <td style="color: #16a34a;">-4.5 Tr</td>
                        <td>288</td>
                        <td><span class="badge-yellow">🟡 Cần kiểm soát</span></td>
                        <td>(DNO) Quảng Tín (13.0 Tr)</td>
                    </tr>
                    <tr>
                        <td><strong>Huỳnh Thị Kim Chi</strong></td>
                        <td>21.3 Tr</td>
                        <td style="color: #16a34a;">-37.0 Tr</td>
                        <td>110</td>
                        <td><span class="badge-yellow">🟡 Cần kiểm soát</span></td>
                        <td>(LDO) Tân Hà Lâm Hà (21.3 Tr)</td>
                    </tr>
                    <tr>
                        <td><strong>Phan Đình Duy</strong></td>
                        <td>8.9 Tr</td>
                        <td style="color: #16a34a;">-4.7 Tr</td>
                        <td>86</td>
                        <td><span class="badge-green">🟢 Tốt</span></td>
                        <td>(KHO) Tây Nha Trang (2.5 Tr)</td>
                    </tr>
                    <tr>
                        <td><strong>Hồng Bích Nga</strong></td>
                        <td>8.1 Tr</td>
                        <td style="color: #16a34a; font-weight:800;">-42.6 Tr (Giảm sâu)</td>
                        <td>60</td>
                        <td><span class="badge-green">🟢 Tốt</span></td>
                        <td>(LDO) Bảo Lâm 1 (6.1 Tr)</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- MỤC 3: KINH DOANH & F30 -->
        <div class="section-card">
            <h2 class="section-title"><i class="fa-solid fa-chart-line"></i> III. KINH DOANH & KHÁCH HÀNG MỚI F30 (TAB 15)</h2>
            <div class="speech-heading"><i class="fa-solid fa-microphone"></i> LỜI PHÁT BIỂU:</div>
            <p><em>"Về kết quả Kinh doanh (kỳ 27/09–03/10 so với 20–26/09): Doanh thu toàn vùng đạt <strong>1,120.5 Tr ₫ (-3.6% WoW)</strong>; Volume đạt <strong>35,334 đơn (-5.5% WoW)</strong>. Khách hàng mới F30 bứt phá đạt <strong>111 shop (+20.7%)</strong> mang lại <strong>9.4 Tr ₫ (+62.8%)</strong>."</em></p>

            <table class="table-custom">
                <thead>
                    <tr>
                        <th>AM Phụ Trách</th>
                        <th>Doanh Thu W40 (Tr ₫)</th>
                        <th>Biến Động Doanh Thu</th>
                        <th>Volume W40 (Đơn)</th>
                        <th>Biến Động Volume</th>
                        <th>F30 Shop Mới</th>
                        <th>Đánh Giá</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Phan Đình Duy</strong></td>
                        <td style="color:#16a34a; font-weight:800;">479.0 Tr</td>
                        <td style="color:#16a34a;">+3.2 Tr (+0.7%)</td>
                        <td>10,088</td>
                        <td style="color:#16a34a;">+74</td>
                        <td style="font-weight:700;">16 shop (1.21 Tr)</td>
                        <td><span class="badge-green">👑 Top 1 Vùng</span></td>
                    </tr>
                    <tr>
                        <td><strong>Thái Thị Thanh Thư</strong></td>
                        <td>98.9 Tr</td>
                        <td style="color:#dc2626;">-11.8 Tr (-10.6%)</td>
                        <td>4,608</td>
                        <td style="color:#dc2626;">-233</td>
                        <td>15 shop (0.63 Tr)</td>
                        <td><span class="badge-yellow">⚠️ Giảm DT cũ</span></td>
                    </tr>
                    <tr>
                        <td><strong>Nguyễn Duy Long</strong></td>
                        <td>98.2 Tr</td>
                        <td style="color:#16a34a;">+2.2 Tr (+2.3%)</td>
                        <td>3,651</td>
                        <td>-50</td>
                        <td>13 shop (0.68 Tr)</td>
                        <td><span class="badge-green">🟢 Tăng trưởng</span></td>
                    </tr>
                    <tr>
                        <td><strong>Lê Thanh Nhựt</strong></td>
                        <td>60.9 Tr</td>
                        <td style="color:#16a34a;">+3.8 Tr (+6.6%)</td>
                        <td>2,279</td>
                        <td style="color:#16a34a;">+227 (+11.1%)</td>
                        <td>5 shop (0.67 Tr)</td>
                        <td><span class="badge-green">🟢 Tăng trưởng</span></td>
                    </tr>
                    <tr style="background: #fff1f2;">
                        <td><strong>Huỳnh Thúc Duân</strong></td>
                        <td style="color:#dc2626; font-weight:800;">57.1 Tr</td>
                        <td style="color:#dc2626; font-weight:800;">-23.4 Tr (-29.1%)</td>
                        <td style="color:#dc2626; font-weight:800;">4,041</td>
                        <td style="color:#dc2626; font-weight:800;">-1,608 (-28.5%)</td>
                        <td>3 shop</td>
                        <td><span class="badge-red">🔴 Sụt giảm nặng nhất</span></td>
                    </tr>
                    <tr style="background: #fff1f2;">
                        <td><strong>Trần Thị Nhung</strong></td>
                        <td>29.3 Tr</td>
                        <td style="color:#dc2626;">-8.0 Tr (-21.5%)</td>
                        <td>878</td>
                        <td style="color:#dc2626;">-329 (-27.3%)</td>
                        <td>9 shop (0.64 Tr)</td>
                        <td><span class="badge-red">🔴 Sụt giảm volume</span></td>
                    </tr>
                    <tr>
                        <td><strong>Nguyễn Lê Nguyên Vũ</strong></td>
                        <td>25.4 Tr</td>
                        <td style="color:#16a34a;">+2.5 Tr (+10.8%)</td>
                        <td>1,058</td>
                        <td style="color:#16a34a;">+108 (+11.4%)</td>
                        <td>4 shop</td>
                        <td><span class="badge-green">🟢 Bứt phá</span></td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- MỤC 4: NGHỊ QUYẾT & GIAO CHỈ TIÊU -->
        <div class="section-card">
            <h2 class="section-title"><i class="fa-solid fa-bullseye"></i> IV. NGHỊ QUYẾT & GIAO CHỈ TIÊU HÀNH ĐỘNG TUẦN W41</h2>
            <div class="speech-heading"><i class="fa-solid fa-microphone"></i> LỜI KẾT LUẬN CỦA CHỦ TRÌ:</div>
            <p><em>"Để khôi phục đà tăng trưởng và xử lý dứt điểm các tồn đọng, Ban Điều Hành Vùng giao 4 nhiệm vụ bắt buộc:"</em></p>
            <div class="callout callout-action">
                <div><strong>1. Thu hồi dứt điểm Truy Thu (Hạn chót 10/10/2026):</strong> AM Nguyễn Thanh Long xử lý dứt điểm 48.7 Tr ₫ tại Bắc Cam Ranh; AM Lê Văn Trường và AM Trần Văn Phước thu hồi tối thiểu <strong>80%</strong> số tiền còn lại tại Đơn Dương và Quảng Tín.</div>
                <div style="margin-top: 8px;"><strong>2. Khôi phục Volume cụm Đắk Nông:</strong> AM Huỳnh Thúc Duân và AM Trần Thị Nhung gặp trực tiếp các shop lớn sụt giảm trong 48 giờ tới, cam kết kéo lại tối thiểu 1,000 đơn/tuần.</div>
                <div style="margin-top: 8px;"><strong>3. Đẩy mạnh Chiến dịch F30:</strong> Toàn vùng quyết tâm tuần W41 vượt mốc <strong>130 shop mới F30</strong>, doanh thu F30 trên <strong>15 Tr ₫</strong>.</div>
                <div style="margin-top: 8px;"><strong>4. Kéo %ODR toàn mạng lên ≥92%:</strong> AM Lê Minh Lợi, AM Trương Quang Linh, AM Phan Nguyễn Yến Nhi phải thoát khỏi nhóm ODR &lt;80%. Bưu cục nào tiếp tục để ODR dưới 75% sẽ đình chỉ đánh giá thi đua tháng của Trưởng bưu cục.</div>
            </div>
            <p style="text-align: center; margin-top: 16px; font-weight: 700; color: var(--ghn-orange);">Chúc các anh chị AM và toàn thể đội ngũ tuần mới quyết liệt, kỷ luật và bứt phá doanh số!</p>
        </div>
    </div>
</body>
</html>
"""

with open('KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
print("✅ Saved KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.html")

# =========================================================================
# 3. GENERATE WORD DOCX SCRIPT (.DOCX)
# =========================================================================
doc = docx.Document()

# Page Setup
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Title
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_sub = p_title.add_run("GIAOHANGNHANH EXPRESS — VÙNG NAM TRUNG BỘ\n")
run_sub.font.size = Pt(11)
run_sub.font.bold = True
run_sub.font.color.rgb = RGBColor(100, 116, 139)

run_main = p_title.add_run("KỊCH BẢN THUYẾT TRÌNH BÁO CÁO HỌP TUẦN W40\n")
run_main.font.size = Pt(18)
run_main.font.bold = True
run_main.font.color.rgb = RGBColor(15, 76, 129)

run_date = p_title.add_run("Thời gian đánh giá: Tuần W40 (28/09/2026 – 04/10/2026) | Chu kỳ KD: 27/09 – 03/10/2026\n")
run_date.font.size = Pt(10.5)
run_date.font.italic = True
run_date.font.color.rgb = RGBColor(100, 116, 139)

def add_heading_box(title, text):
    h = doc.add_heading(title, level=1)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)
    for r in h.runs:
        r.font.color.rgb = RGBColor(234, 88, 12)
        r.font.size = Pt(14)
    
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    r_spk = p.add_run("🗣️ KỊCH BẢN NÓI — LỜI PHÁT BIỂU CHỦ TRÌ / BÁO CÁO:\n")
    r_spk.font.bold = True
    r_spk.font.color.rgb = RGBColor(180, 83, 9)
    r_spk.font.size = Pt(10)
    
    r_txt = p.add_run(text)
    r_txt.font.italic = True
    r_txt.font.size = Pt(11)

add_heading_box(
    "🧭 TỔNG QUAN CHIẾN LƯỢC VÙNG W40",
    "\"Kính chào Ban Giám Đốc, các Giám đốc Khối và toàn thể các anh chị Quản lý Vận hành (AM), Quản lý Kinh doanh vùng Nam Trung Bộ. Hôm nay, em xin đại diện Ban Điều Hành Vùng trình bày Báo cáo tổng kết tuần W40 (so sánh với tuần W39).\n\n"
    "Thưa Ban Giám Đốc, tuần W40 ghi nhận 4 điểm nhấn chính:\n"
    "1. Báo cáo Truy Thu giảm sâu tích cực: Số tiền cần thu giảm -40.1% từ 312.1 Tr xuống còn 187.1 Tr ₫ (-125.0 Tr ₫); số đơn giảm -40.5% (-1,652 đơn).\n"
    "2. Khách hàng mới F30 bứt phá: Đạt 111 shop mới (+20.7%), mang lại 9.4 Tr ₫ doanh thu mới (+62.8%). Nhóm A tháng 10 đạt 8,840 Tr ₫ MTD.\n"
    "3. Chất lượng ODR toàn mạng giữ vững: %ODR Full hàng đạt 93.1%, TTS đạt 94.2%.\n"
    "4. Hai điểm nóng cần xử lý dứt điểm: Vụ việc chiếm dụng tiền hàng 48.7 Tr ₫ tại Bắc Cam Ranh (AM Nguyễn Thanh Long) và sụt giảm kinh doanh sâu tại Đắk Nông (AM Huỳnh Thúc Duân giảm -29.1% doanh thu, -28.5% volume).\""
)

add_heading_box(
    "📦 I. SẢN LƯỢNG GIAO & HIỆU SUẤT VẬN HÀNH TOÀN MẠNG",
    "\"Toàn vùng duy trì tỷ lệ Giao Đúng Hẹn (%ODR) ở mức cao: Full hàng đạt 93.1%, TikTok Shop đạt 94.2%.\n"
    "• Top AM xuất sắc ODR: AM Cao Thị Thanh Thủy (97.8%), AM Nguyễn Ngọc Khánh (97.4%), AM Thái Thị Thanh Thư (96.9%), AM Nguyễn Duy Long (96.6%).\n"
    "• Cảnh báo đỏ AM ODR thấp (<80%): AM Lê Minh Lợi (74.1%), AM Trương Quang Linh (74.9%), AM Phan Nguyễn Yến Nhi (76.1%), AM Lê Văn Trường (78.3%). Yêu cầu tái bố trí ca bưu tá trước 07h00 sáng.\""
)

add_heading_box(
    "💰 II. BÁO CÁO TRUY THU (TAB 14): GIẢM -40.1% NHƯNG XUẤT HIỆN ĐIỂM NÓNG CÁ BIỆT",
    "\"Số tiền cần truy thu tuần W40 giảm mạnh về 187.1 Tr ₫ (-125.0 Tr ₫ / -40.1%), số đơn giảm còn 2,424 đơn (-40.5%).\n"
    "Top loại vi phạm: Liên đới chiếm dụng 56.8 Tr ₫ (4 đơn), Tick mất hàng 41.2 Tr ₫ (53 đơn), Mất/Thiếu/Tráo sản phẩm 30.9 Tr ₫ (76 đơn).\n\n"
    "LƯU Ý ĐẶC BIỆT CÁC AM:\n"
    "1. 🔴 AM Nguyễn Thanh Long: BÁO ĐỘNG ĐỎ! Cần thu tăng vọt lên 51.2 Tr ₫ (tăng +33.0 Tr ₫, gấp gần 3x). Điểm nóng bưu cục Bắc Cam Ranh phát sinh 48.7 Tr ₫ liên đới chiếm dụng. Yêu cầu thu hồi dứt điểm trước 10/10.\n"
    "2. 🟡 AM Lê Văn Trường: Đang gánh 419 ticket (cao nhất vùng), cần thu 26.3 Tr ₫ (Đơn Dương 12.8 Tr ₫).\n"
    "3. 🟡 AM Trần Văn Phước: Cần thu 22.9 Tr ₫ (Quảng Tín 13.0 Tr ₫).\n"
    "4. 🟡 AM Huỳnh Thị Kim Chi: Cần thu 21.3 Tr ₫ (Tân Hà Lâm Hà 21.3 Tr ₫).\n"
    "5. 🟢 Tuyên dương AM Hồng Bích Nga: Giảm sâu từ 50.7 Tr xuống 8.1 Tr ₫ (-42.6 Tr ₫).\""
)

add_heading_box(
    "📈 III. KINH DOANH & KHÁCH HÀNG MỚI F30 (TAB 15)",
    "\"Doanh thu toàn vùng kỳ 27/09–03/10 đạt 1,120.5 Tr ₫ (-3.6%), volume đạt 35,334 đơn (-5.5%). F30 bứt phá đạt 111 shop (+20.7%), mang về 9.4 Tr ₫ (+62.8%).\n\n"
    "ĐÁNH GIÁ AM KINH DOANH:\n"
    "• Điểm sáng: AM Phan Đình Duy đạt 479.0 Tr ₫ (+0.7%), volume 10,088 đơn (+74), mở 16 shop F30; AM Nguyễn Duy Long đạt 98.2 Tr ₫ (+2.3%), mở 13 shop F30; AM Lê Thanh Nhựt đạt 60.9 Tr ₫ (+6.6%), volume +11.1%; AM Nguyễn Lê Nguyên Vũ đạt 25.4 Tr ₫ (+10.8%), volume +11.4%.\n"
    "• 🔴 Cảnh báo sụt giảm nặng: AM Huỳnh Thúc Duân giảm -29.1% doanh thu (-23.4 Tr ₫) và bốc hơi -1,608 đơn (-28.5% volume); AM Thái Thị Thanh Thư giảm -11.8 Tr ₫ (-10.6%); AM Trần Thị Nhung giảm -8.0 Tr ₫ (-21.5%), volume giảm -329 đơn (-27.3%).\n"
    "• Khách hàng nhóm A: 10 shop đạt 8,840 Tr ₫ MTD đầu tháng 10. Top 1: Vận Chuyển Online (5,688 Tr ₫ MTD – AM Phan Đình Duy).\""
)

add_heading_box(
    "🎯 IV. NGHỊ QUYẾT & GIAO CHỈ TIÊU HÀNH ĐỘNG TUẦN W41",
    "\"1. Thu hồi dứt điểm Truy Thu (Hạn 10/10/2026): AM Long xử lý dứt điểm 48.7 Tr ₫ tại Bắc Cam Ranh; AM Trường và AM Phước thu hồi tối thiểu 80% tại Đơn Dương và Quảng Tín.\n"
    "2. Khôi phục Volume Đắk Nông: AM Duân và AM Nhung làm việc trực tiếp các shop lớn trong 48h, cam kết kéo lại tối thiểu 1,000 đơn/tuần.\n"
    "3. Đẩy mạnh F30: Toàn vùng phấn đấu tuần W41 vượt 130 shop mới F30, doanh thu F30 trên 15 Tr ₫.\n"
    "4. Kéo %ODR lên ≥92%: AM Lợi, AM Linh, AM Nhi phải thoát khỏi nhóm ODR <80%.\""
)

# Save Word files
doc_path_w40 = 'KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.docx'
doc_path_latest = 'KICH_BAN_THUYET_TRINH_MOI_NHAT.docx'
doc.save(doc_path_w40)
doc.save(doc_path_latest)
print("✅ Saved KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.docx and KICH_BAN_THUYET_TRINH_MOI_NHAT.docx")
