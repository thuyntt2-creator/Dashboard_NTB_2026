# -*- coding: utf-8 -*-
"""
KỊCH BẢN THUYẾT TRÌNH GIAO BAN TUẦN W40 - NAM TRUNG BỘ
CHUẨN PHONG CÁCH 'SẾP CỦA AM' (GIÁM ĐỐC VẬN HÀNH VÙNG CHỦ TRÌ)
KHỚP 100% SỐ LIỆU VÀ CẤU TRÚC 16 TAB DASHBOARD (INDEX.HTML / DATA.JSON)
"""
import sys, os, json, shutil
sys.stdout.reconfigure(encoding='utf-8')

import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

# Load data
with open('data.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# Helper styling for docx
def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_border(cell, **kwargs):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key, val in edge_data.items():
                element.set(qn('w:{}'.format(key)), str(val))

TOPICS = [
    # ----------------------------------------------------
    # TAB 1: TỔNG QUAN
    # ----------------------------------------------------
    {
        "id": "tab-overview",
        "title": "🗣️ LỜI MỞ ĐẦU & TỔNG QUAN ĐIỀU HÀNH VÙNG TUẦN W40 (BẬT TAB 1 DASHBOARD):",
        "content": """📍 1. BẢNG 10 CHỈ SỐ NHANH TRÊN MÀN HÌNH DASHBOARD (W40 vs W39):
• 1. Sản Lượng Full Hàng: 311.503 đơn (-19.810 đơn / -5,98% so với W39 331.313 đơn).
• 2. Sản Lượng TikTok Shop: 72.253 đơn (-1.190 đơn / -1,62%), chiếm tỷ trọng 23,2% sản lượng toàn vùng.
• 3. %GTC Full Hàng: 60,87% (+4,19%p so với W39 56,68%) ➔ Bứt phá ngoạn mục, chính thức vượt mốc trần 60%!
• 4. %GTC TikTok Shop: 63,38% (+5,84%p so với W39 57,54%) ➔ Lập đỉnh cao nhất từ trước đến nay, vượt Full hàng +2,51%p.
• 5. %ODR (Giao Đúng Hẹn): 93,12% (+2,28%p so với W39 90,84%) ➔ Vượt chuẩn cam kết SLA ≥ 92,0% (TTS đạt 94,18%).
• 6. %LTC (Lấy Hàng Thành Công): 91,35% (+1,22%p so với W39 90,13%; riêng TTS duy trì xuất sắc 94,97%).
• 7. %Rớt Luân Chuyển KTC: 1,69% (W39: 1,52%, tăng nhẹ +0,17%p; 219 đơn rớt / 12.934 đơn cần luân chuyển).
• 8. %FD (Tỷ Lệ Hoàn Trả): 7,77% (W39: 7,54%, tăng nhẹ +0,23%p; riêng TTS kiểm soát rất tốt ở mức 6,10%).
• 9. Tổng Cần Truy Thu: 187,1 Tr ₫ (2.424 bản ghi, giảm -125,0 Tr ₫ / -40,1% so với 312,1 Tr ₫ tuần W39).
• 10. Tỷ Lệ Tiền Mặt COD: 40,4% (so với 40,1% W39; tỷ lệ nộp COD chuyển khoản QR đạt 59,6% toàn vùng).

🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 1 DASHBOARD TỔNG QUAN):
"Dạ em chào Ban Giám Đốc, chào các anh chị AM và các phòng ban.
Mở đầu buổi họp giao ban tuần W40 (chu kỳ dữ liệu từ 28/09 đến 04/10/2026), kính mời Ban Giám Đốc và các anh chị cùng nhìn lên màn hình Dashboard Tổng quan giúp em.
Tuần 40 này, toàn vùng Nam Trung Bộ của chúng ta có một bước chuyển mình rất ấn tượng về chất lượng dịch vụ Last-mile:
Đầu tiên là điểm sáng rực rỡ nhất: Tỷ lệ Giao thành công (%GTC Full) tuần này đã chính thức phá mốc 60%, chạm mức 60,87%, tăng tới hơn 4,19%p so với tuần trước. Đặc biệt ở kênh TikTok Shop, %GTC đã tăng lên 63,38%, tăng gần 6%p! Đây là kết quả của việc các anh chị AM đã siết rất chặt ca giao chiều và giải tỏa đơn tồn đầu ngày.
Điểm sáng thứ hai là chỉ số Giao đúng hẹn %ODR: Sau nhiều tuần ngấp nghé 90-91%, tuần này toàn vùng đã vượt ngưỡng cam kết SLA 92%, vươn lên 93,12% (hàng TikTok đạt tới 94,18%). Khâu lấy hàng First-mile cũng duy trì rất đều tay trên 91,3%, riêng TikTok Shop đạt gần 95%.
Về quản trị dòng tiền, tỷ lệ nộp COD bằng chuyển khoản QR tuần này duy trì ở mức cao 59,6%, hạn chế tối đa rủi ro thất thoát quỹ.
Tuy nhiên, ở tuần vừa rồi có một số điểm lowlight sau cần nhìn nhận thẳng thắn:
Thứ nhất: Sản lượng tuần này hạ nhiệt về 311.503 đơn, giảm khoảng 6% so với tuần W39 do tuần cuối tháng thị trường có sự chững lại.
Thứ hai: Khâu vận tải KTC vẫn đang gánh 76 chuyến xe chạy non tải dưới 30% thùng, kéo tỷ lệ lấp đầy KTC đứng yên ở mức 51,0%, gây lãng phí lớn chi phí nhiên liệu đường trục.
Thứ ba: Mặc dù tổng số tiền cần truy thu giảm 40% về 187,1 triệu đồng, nhưng số tiền phát sinh ban đầu lại tăng vọt lên 433,1 triệu đồng, nổi cộm lên vụ việc chiếm dụng tiền hàng 48,7 triệu đồng tại bưu cục Bắc Cam Ranh thuộc cụm AM Nguyễn Thanh Long và 419 ticket truy thu dồn ứ tại địa bàn AM Lê Văn Trường.
Bây giờ, em xin phép bấm chuyển qua Tab 2 để đi sâu vào sản lượng từng Tỉnh và từng anh chị AM nha!\""""
    },

    # ----------------------------------------------------
    # TAB 2: SẢN LƯỢNG GIAO
    # ----------------------------------------------------
    {
        "id": "tab-volume",
        "title": "🗣️ PHÂN TÍCH SẢN LƯỢNG GIAO CHI TIẾT (BẬT TAB 2 DASHBOARD):",
        "content": """📍 1. BẢNG SẢN LƯỢNG 5 TỈNH THÀNH (W40 vs W39):
• Khánh Hòa: 95.340 đơn (-10.155 đơn / -9,63%) ➔ Tỉnh có sản lượng lớn nhất nhưng giảm mạnh nhất.
• Lâm Đồng: 89.288 đơn (-5.454 đơn / -5,76%) ➔ Địa bàn rộng lớn, đang gặp khó khăn về địa hình và thời tiết.
• Bình Thuận: 62.628 đơn (-2.278 đơn / -3,51%) ➔ Ổn định nhất toàn vùng.
• Ninh Thuận: 35.138 đơn (-413 đơn / -1,16%) ➔ Giữ nhịp rất tốt.
• Đắk Nông: 29.109 đơn (-1.510 đơn / -4,93%) ➔ Địa bàn vùng sâu vùng xa.

📍 2. PHÂN TÍCH CHI TIẾT 18 AM:
• AM sản lượng lớn nhất toàn vùng:
  1. Nguyễn Duy Long (Ninh Thuận): 61.356 đơn ➔ Tiếp tục là 'cỗ máy sản lượng' lớn nhất vùng Nam Trung Bộ!
  2. Lê Văn Trường (Lâm Đồng): 37.411 đơn (-4.568 đơn / -10,88%).
  3. Trần Thị Nhung (Đắk Nông): 36.878 đơn (-1.085 đơn / -2,86%).
  4. Thái Thị Thanh Thư (Khánh Hòa): 35.889 đơn (-9.986 đơn / -21,77%).
  5. Nguyễn Ngọc Khánh (Bình Thuận): 34.296 đơn (-769 đơn / -2,19%).

🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 2 DASHBOARD SẢN LƯỢNG):
"Dạ sang Tab 2, nhìn vào cơ cấu sản lượng toàn vùng 311 ngàn đơn:
Tỉnh Khánh Hòa vẫn là anh cả gánh 95 ngàn đơn, Lâm Đồng đứng thứ nhì với 89 ngàn đơn, kế đến là Bình Thuận 62 ngàn, Ninh Thuận 35 ngàn và Đắk Nông 29 ngàn đơn.
Về phía các AM: Anh Nguyễn Duy Long ở Ninh Thuận tiếp tục là 'cỗ máy sản lượng' khủng nhất vùng khi một mình anh điều hành tới hơn 61 ngàn đơn, chạy rất đều tay và ổn định!
Kế đến là anh Lê Văn Trường (37,4 ngàn đơn), chị Trần Thị Nhung (36,8 ngàn đơn), chị Thái Thị Thanh Thư (35,8 ngàn đơn) và anh Nguyễn Ngọc Khánh (34,2 ngàn đơn).

Tuy nhiên, có 2 điểm báo động về sản lượng cần lưu ý:
Thứ nhất là cụm của chị Thư ở Khánh Hòa: Tuần trước chị Thư tăng mạnh thì tuần này lại sụt giảm tới 7.600 đơn (-21,8%). Chị Thư cần rà soát lại xem có shop lớn nào tại Nha Trang bị đối thủ kéo đi hay do bưu cục chia lại tuyến giao.
Thứ hai là anh Trường ở Lâm Đồng: Giảm tiếp hơn 4.500 đơn. Địa bàn của anh Trường đang dính nhiều đơn tồn và ODR thấp, khi giao trễ khách hàng họ sẽ hủy đơn và shop sẽ có tâm lý giảm gửi qua GHN.
Bây giờ em xin phép chuyển sang Tab 3 để xem tỷ lệ Giao thành công (%GTC) của từng tỉnh và từng AM nhé!\""""
    },

    # ----------------------------------------------------
    # TAB 3: %GTC TỔNG
    # ----------------------------------------------------
    {
        "id": "tab-gtc-tong",
        "title": "🗣️ PHÂN TÍCH TỶ LỆ GIAO THÀNH CÔNG %GTC TỔNG (BẬT TAB 3 DASHBOARD):",
        "content": """📍 1. BẢNG %GTC 5 TỈNH THÀNH (W40 vs W39):
• Bình Thuận: 67,52% (W39: 67,49%, +0,03%p) ➔ Dẫn đầu toàn vùng, vững chắc tuyệt đối.
• Khánh Hòa: 62,23% (W39: 58,80%, bứt phá +3,43%p) ➔ Chính thức vượt mốc 60%!
• Ninh Thuận: 60,65% (W39: 59,96%, tăng +0,69%p) ➔ Vượt chuẩn an toàn.
• Đắk Nông: 54,42% (W39: 48,72%, tăng mạnh +5,70%p) ➔ Nỗ lực thoát đáy cực lớn.
• Lâm Đồng: 54,41% (W39: 47,38%, bứt phá +7,03%p) ➔ Bước nhảy vọt ngoạn mục nhất!

📍 2. PHÂN TÍCH CHI TIẾT 18 AM:
• Top 4 AM dẫn đầu GTC toàn vùng:
  1. Nguyễn Ngọc Khánh (Bình Thuận): 74,5% ➔ Quán quân GTC toàn vùng!
  2. Thái Thị Thanh Thư (Khánh Hòa): 72,0% (+9,63%p) ➔ Á quân xuất sắc.
  3. Nguyễn Duy Long (Ninh Thuận): 71,2% ➔ Vừa gánh vol lớn nhất vừa giữ GTC đỉnh.
  4. Nguyễn Đỗ Minh Nghĩa (Lâm Đồng): 70,4% ➔ Ngôi sao sáng nhất tỉnh Lâm Đồng.
• 3 AM có bước nhảy vọt thần tốc kéo cả vùng bứt phá:
  - Chị Thái Thị Thanh Thư: Tăng vọt gần +10%p (từ 62,4% lên 72,0%) trên khối lượng gần 36 ngàn đơn.
  - Anh Lê Văn Trường: Tăng phi thường +11,9%p (từ 37,1% lên 49,0%) trên khối lượng hơn 37 ngàn đơn!
  - Anh Trương Quang Linh: Tăng bứt phá mạnh nhất toàn vùng với +14,5%p (từ 25,8% lên 40,3%).
• Nhóm AM còn nằm dưới mốc 50%:
  - Lê Minh Lợi (36,5%), Phan Nguyễn Yến Nhi (38,0%), Trương Quang Linh (40,3%).

🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 3 DASHBOARD %GTC TỔNG):
"Nhìn vào 5 Tỉnh thành ở bảng trên cùng:
Bình Thuận vẫn giữ vững tỷ lệ với GTC 67,5%, cho thấy anh em khu vực tại Bình Thuận chạy tuyến rất đều và khách nhận hàng rất chuẩn.
Khánh Hòa và Ninh Thuận tuần này đã xuất sắc vượt qua mốc 60%. Đặc biệt Khánh Hòa tăng từ 58,8% lên 62,2%, đóng góp cực lớn vào tỷ lệ GTC chung của vùng.
Hai tỉnh Đắk Nông và Lâm Đồng: Dù vẫn đứng ở 2 vị trí cuối bảng với 54,4%, nhưng tuần này anh em đã có sự nỗ lực rất lớn. Lâm Đồng kéo tăng tới hơn 7,0%p, còn Đắk Nông tăng 5,7%p so với tuần trước. Về phần này có sự tuyên dương nỗ lực của các AM khu vực 2 tỉnh Đắk Nông và Lâm Đồng!

Nhìn xuống danh sách 18 AM:
Top 1 GTC full hàng tuần này thuộc về khu vực AM Nguyễn Ngọc Khánh với tỷ lệ 74,5%, kế đến là chị Thái Thị Thanh Thư (Khánh Hòa) đạt 72,0% và anh Nguyễn Đỗ Minh Nghĩa (Lâm Đồng) đạt 70,4%.
Đặc biệt, AM Duy Long tiếp tục là AM sản lượng lớn nhất toàn vùng, nhưng vẫn duy trì %GTC rất vững vàng ở mức 71,2%!
Tuần này toàn vùng tăng mạnh +4,19%p KHÔNG PHẢI nhờ nhóm ven biển (vì Bình Thuận và Ninh Thuận đã ở mức trần nên đi ngang ~67,5%), mà công lớn nhất kéo cả vùng bứt phá tuần này thuộc về 3 AM có bước nhảy vọt thần tốc:
Thứ nhất là chị Thái Thị Thanh Thư ở Khánh Hòa: Tăng vọt tới gần +10%p (từ 62,4% lên 72,0%) trên khối lượng gần 36 ngàn đơn, đưa chị Thư lên thẳng vị trí Á quân GTC toàn vùng và kéo bừng sáng cả tỉnh Khánh Hòa!
Thứ hai là anh Lê Văn Trường ở Lâm Đồng: Tăng phi thường +11,9%p (từ 37,1% lên 49,0%) trên khối lượng cực lớn hơn 37 ngàn đơn! Chính anh Trường là đầu tàu kéo Lâm Đồng tăng hơn 7%p tuần này!
Thứ ba là anh Trương Quang Linh ở Đắk Nông: Tăng bứt phá mạnh nhất toàn vùng với +14,5%p (từ 25,8% lên 40,3%). Bên cạnh đó, anh Vũ (+7,5%p), chị Nhi (+9,0%p) và chị Nhung (+3,5%p trên 37 ngàn đơn) cũng là những nhân tố nòng cốt kéo toàn bộ khu vực Tây Nguyên thoát đáy!

Tuy nhiên, ngược lại nhóm các AM vẫn còn nằm dưới mốc 50%:
Đặc biệt là anh Lê Minh Lợi (36,5%), khu vực AM mới của chị Yến Nhi (38,0%) và anh Trương Quang Linh (40,3%): Các địa bàn này tỷ lệ khách từ chối và hẹn lùi giờ còn cao, shipper chưa linh hoạt đổi ca phát.
Em đề nghị trong tuần này, các AM nhóm dưới phải ngồi lại với từng bưu cục để tối ưu lại ca phát chiều. Giờ em xin chuyển qua Tab 4 mổ xẻ Ca 1 và Ca 2 ạ!\""""
    },

    # ----------------------------------------------------
    # TAB 4: %GTC TTS CA 1 SÁNG
    # ----------------------------------------------------
    {
        "id": "tab-gtc-tts-ca1",
        "title": "🗣️ MỔ XẺ GIAO HÀNG CA 1 SÁNG: HÀNG TỒN (52.8%) VS HÀNG THUẦN (72.4%) (BẬT TAB 4 DASHBOARD):",
        "content": """📍 1. BẢNG HIỆU SUẤT CA 1 SÁNG TOÀN VÙNG:
• Hàng Thuần Ca 1 Full: 77,35% (tăng +5,12%p WoW).
• Hàng Thuần Ca 1 TikTok Shop: 81,34% (+6,17%p so với 75,16% W39) ➔ VƯỢT XA TARGET SLA 76,0%!
• 4/5 Tỉnh vượt mốc 80% TTS Ca 1: Bình Thuận 86,5%, Ninh Thuận 83,8%, Lâm Đồng 80,2%, Khánh Hòa 80,2%.
• Sự thật đằng sau con số: GTC Ca 1 thuần đạt đỉnh 81,34%, nhưng nếu tính cả hàng tồn thì rơi xuống chỉ còn 66,47% (sụt tới -14,87%p)!

📍 2. PHÂN TÍCH THEO AM:
• Top AM dẫn đầu Ca 1 TTS:
  - Nguyễn Ngọc Khánh: 88,9%
  - Nguyễn Đỗ Minh Nghĩa: 87,0%
  - Cao Thị Thanh Thủy: 87,0%
  - Nguyễn Duy Long: 85,1% (trên hơn 10 ngàn đơn)
  - Lê Văn Trường: Kéo GTC Ca 1 TTS tăng tới gần +25% lên 80,3%!
• 5 AM còn hiển thị màu đỏ dưới mốc SLA 76%:
  - Huỳnh Thúc Duân: 64,5%
  - Nguyễn Lê Nguyên Vũ: 61,4%
  - Phan Nguyễn Yến Nhi: 58,6%
  - Trương Quang Linh: 58,1%
  - Lê Minh Lợi: 46,7%

🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 4 DASHBOARD GTC CA 1 TTS):
"Đối với hàng thuần mới về sáng sớm, tỷ lệ giao thành công Full hàng toàn vùng đã tăng lên 77,35%, và đặc biệt là phân khúc TikTok Shop (TTS) tuần này đã chính thức bứt phá ngoạn mục vượt qua mốc 81% (đạt 81,34%, tăng mạnh +6,17%p so với mức 75,16% của W39)! Cả 4/5 tỉnh gồm Bình Thuận (86,5%), Ninh Thuận (83,8%), Lâm Đồng (80,2%) và Khánh Hòa (80,2%) đều đã xuất sắc vượt qua mốc 80% đối với hàng sàn Ca 1 sáng!
Soi vào AM: Anh Khánh (88,9%), anh Nghĩa (87,0%), chị Thủy (87,0%) và anh Long (85,1% trên hơn 10 ngàn đơn) đều có tỷ lệ giao ca sáng cực kỳ ấn tượng.
Đặc biệt, anh Lê Văn Trường ở Lâm Đồng đã kéo GTC Ca 1 TTS tăng tới gần +25% lên 80,3%!

Tuy nhiên, trên biểu đồ mọi người thấy vẫn còn 5 AM hiển thị màu đỏ dưới mốc 76%:
Đó là chỗ anh Duân (64,5%), anh Vũ (61,4%), chị Nhi (58,6%), anh Linh (58,1%) và anh Lợi (46,7%).
Em đề nghị tuần tới, 5 AM này phải áp dụng triệt để kỷ luật xuất bến: Bắt buộc shipper đi phát chuyến 1 trước 8h30 sáng để tận dụng tối đa khung giờ vàng nhận hàng của khách TikTok Shop.

🔍 INSIGHT BẢN CHẤT & GỐC RỄ NGUYÊN NHÂN:
GTC Ca 1 thuần đạt đỉnh 81,34% (vượt xa target SLA 76%), nhưng nếu tính cả tồn thì chỉ còn 66,47% (rơi tới -14,87%p)!
Shipper buổi sáng có thói quen 'chọn việc dễ, né việc khó': ưu tiên bốc các kiện hàng vừa hạ tải tinh tươm để đi phát cho nhanh (khách mới đặt, dễ nghe máy). Các đơn tồn lưu cữu từ hôm trước bị nhét xuống đáy sọt hoặc để lại góc bưu cục. Càng để qua ngày thì tâm lý khách hủy đơn, bom hàng, hoặc không liên lạc được càng tăng vọt.
Đây chính là lý do vì sao biểu đồ Ca 1 thuần nhìn rất 'xanh' (81,3%), nhưng tỷ lệ GTC chốt sổ cuối tuần toàn vùng lại chỉ quanh quẩn 60 - 62%.

🎯 QUYẾT SÁCH HÀNH ĐỘNG & MỆNH LỆNH TÁC CHIẾN:
• Trưởng bưu cục bắt buộc phải kiểm tra sọt hàng của shipper trước khi xuất bến lúc 08h30: 100% đơn tồn hôm trước phải được xếp lên trên cùng để phát trước 10h30.
Giờ em xin chuyển qua Tab 5 mổ xẻ Tỷ lệ gán vận hành ạ!\""""
    },

    # ----------------------------------------------------
    # TAB 5: % GÁN VẬN HÀNH
    # ----------------------------------------------------
    {
        "id": "tab-gan",
        "title": "🗣️ PHÂN TÍCH TỶ LỆ GÁN VẬN HÀNH: CA 1 + TỒN VS GÁN TỔNG (BẬT TAB 5 DASHBOARD):",
        "content": """📍 1. BẢNG 1: CHỈ TIÊU VÙNG (CA 1 + TỒN, CA 2 & GÁN TỔNG CẢ NGÀY):
• Full hàng – Ca 1 + Tồn: 92,77% (W39: 87,46%, tăng +5,32%p) ➔ VƯỢT CHUẨN SLA ≥ 90,0%!
• TTS – Ca 1 + Tồn: 94,80% (W39: 88,22%, bứt phá +6,58%p) ➔ Xuất sắc toàn diện!
• Full hàng – Ca 2: 62,87% (W39: 59,28%, chỉ tăng +3,59%p) ➔ ĐIỂM NGHẼN CỔ CHAI LỚN NHẤT VÙNG!
• TTS – Ca 2: 63,54% (W39: 58,57%, tăng +4,98%p).
• Full hàng – Tổng cả ngày: 86,32% (W39: 82,47%, tăng +3,86%p) ➔ Chưa đạt target 90,0%.
• TTS – Tổng cả ngày: 88,00% (W39: 82,83%, tăng +5,17%p).

📍 2. BẢNG 2: TỶ LỆ GÁN CA 1 + TỒN THEO 18 AM (TARGET ≥ 90.0%):
• Top 5 AM xuất sắc nhất:
  1. Nguyễn Đỗ Minh Nghĩa (Lâm Đồng): 99,1% (W39: 97,4%) | Sản lượng: 10.414 đơn
  2. Nguyễn Ngọc Khánh (Bình Thuận): 98,9% (W39: 98,4%) | Sản lượng: 34.296 đơn
  3. Lê Thanh Nhựt (Ninh Thuận): 98,9% (W39: 98,1%) | Sản lượng: 46.427 đơn
  4. Thái Thị Thanh Thư (Khánh Hòa): 98,4% (W39: 98,2%) | Sản lượng: 35.889 đơn
  5. Cao Thị Thanh Thủy (Khánh Hòa): 98,0% (W39: 98,5%) | Sản lượng: 22.756 đơn
• Nhóm bứt phá thần tốc kéo cả vùng vượt chuẩn 90%:
  - Phan Nguyễn Yến Nhi: Tăng phi thường +22,3%p (từ 60,2% lên 82,5%).
  - Trương Quang Linh: Tăng bứt phá +21,6%p (từ 58,4% lên 80,0%).
  - Lê Văn Trường: Tăng thần tốc +21,5%p (từ 61,9% lên 83,4%) trên khối lượng cực lớn 37,4k đơn!
  - Nguyễn Lê Nguyên Vũ: Tăng +9,2%p (từ 68,3% lên 77,5%).
• Đáy bảng Ca 1 + Tồn (Vẫn dưới chuẩn 90%):
  - Nguyễn Lê Nguyên Vũ (77,5%), Lê Minh Lợi (78,2%), Trương Quang Linh (80,0%), Phan Nguyễn Yến Nhi (82,5%), Lê Văn Trường (83,4%).

📍 3. BẢNG 3: TỶ LỆ GÁN TỔNG CẢ NGÀY THEO 18 AM:
• Top AM gán tổng cao nhất (> 91%):
  1. Thái Thị Thanh Thư (97,5%), Nguyễn Ngọc Khánh (92,7%), Nguyễn Hoàng Phi (92,2%), Nguyễn Duy Long (91,6%).
• 5 AM ở đáy bảng Gán Tổng (kéo tụt cả vùng dưới 80%):
  1. Nguyễn Lê Nguyên Vũ: 72,8% ➔ Thấp nhất vùng!
  2. Huỳnh Thúc Duân: 75,5% (giảm -0,5%p)
  3. Lê Văn Trường: 75,9% (dù tăng nhưng vẫn kẹt ở 75%)
  4. Huỳnh Thị Kim Chi: 77,6% (giảm -1,1%p)
  5. Lê Minh Lợi: 78,2%

🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 5 DASHBOARD TỶ LỆ GÁN):
"Kính thưa Ban Giám Đốc và các anh chị AM, khi chuyển sang Tab 5 về Tỷ lệ gán vận hành, chúng ta sẽ thấy ngay gốc rễ vì sao Last-mile tuần này có chuyển biến tích cực nhưng vẫn còn những điểm nghẽn nghiêm trọng:
Đầu tiên, nhìn vào Bảng 1: Chỉ tiêu Gán Ca 1 + Tồn toàn vùng đã có một bước nhảy vọt thực sự: Full hàng tăng từ 87,5% lên 92,77%, và riêng TikTok Shop bứt phá từ 88,2% lên 94,80%! Toàn vùng đã chính thức vượt qua chuẩn cam kết 90%!
Để có được kết quả này, nhìn xuống Bảng 2, em xin tuyên dương đặc biệt 3 AM Tây Nguyên:
Chị Phan Nguyễn Yến Nhi tăng tới +22,3%p (từ 60,2% lên 82,5%).
Anh Trương Quang Linh ở Đắk Nông tăng +21,6%p (từ 58,4% lên 80,0%).
Và anh Lê Văn Trường ở Lâm Đồng tăng +21,5%p (từ 61,9% lên 83,4%) trên khối lượng cực lớn hơn 37 ngàn đơn!
Bên cạnh đó, các anh chị nhóm ven biển như anh Nghĩa (99,1%), anh Khánh (98,9%), anh Nhựt (98,9%), chị Thư (98,4%) tiếp tục giữ vững kỷ luật thép với tỷ lệ gán ca sáng gần như tuyệt đối 100%!

TUY NHIÊN, các anh chị nhìn sang Bảng 3: Tỷ lệ Gán Tổng cả ngày của toàn vùng lại chỉ đạt 86,32%, vẫn chưa chạm được mốc target 90%!
Tại sao Ca 1 + Tồn đạt tới gần 93% mà Gán Tổng cả ngày lại rớt xuống 86%?
Câu trả lời nằm ở con số Gán Ca 2: Toàn vùng chỉ đạt vỏn vẹn 62,87%!
Nhìn vào danh sách 5 AM ở đáy Bảng 3:
Anh Nguyễn Lê Nguyên Vũ chỉ đạt 72,8%! Anh Huỳnh Thúc Duân 75,5%! Anh Lê Văn Trường 75,9%! Chị Huỳnh Thị Kim Chi 77,6%! Và anh Lê Minh Lợi 78,2%!
Năm anh chị đang để tỷ lệ gán tổng của cụm mình chìm sâu dưới mốc 80%! Cứ 100 đơn về bưu cục trong ngày thì có tới hơn 20 đến 25 đơn không được gán cho shipper đi phát!

🔍 INSIGHT BẢN CHẤT & GỐC RỄ NGUYÊN NHÂN:
Nguyên nhân gốc rễ ở đây không phải do shipper thiếu máy móc hay lỗi phần mềm, mà là THÓI QUEN VẬN HÀNH CA CHIỀU TẠI BƯU CỤC:
Chuyến xe KTC buổi chiều thường cập bưu cục vào khung giờ 13h30 đến 14h30. Khi hàng hạ tải xuống bãi, Trưởng bưu cục và điều phối có tâm lý: 'Thôi để sáng mai chia một thể, chiều nay cho shipper phát nốt mấy đơn ca 1 rồi nghỉ'.
Đơn ca 2 không được gán lên hệ thống, nằm chết dí ở kho bưu cục từ 14h chiều hôm nay đến tận 8h sáng hôm sau!
Hàng nằm kho mà không gán, hệ thống ghi nhận là hàng ngâm, chỉ số ODR lập tức bị kéo sụt, và nguy cơ khách hủy đơn tăng gấp đôi!

🎯 QUYẾT SÁCH HÀNH ĐỘNG & MỆNH LỆNH TÁC CHIẾN:
1. Tôi yêu cầu 5 AM: Vũ, Duân, Trường, Chi, Lợi: Ngay chiều nay, bắt buộc 100% bưu cục phải thực hiện quy trình GÁN CA 2 trước 15h30. Xe KTC hạ tải kiện nào là quét nhập kho và gán ngay cho bưu tá kiện đó.
2. Bưu tá phải xuất bến chuyến 2 trước 16h00 để phát dứt điểm hàng trong ngày.
3. Mục tiêu tuần W41: Toàn bộ 18 AM phải đưa tỷ lệ Gán Tổng vượt mốc 90,0%, triệt tiêu hoàn toàn tình trạng om đơn ca chiều!
Bây giờ, em xin phép chuyển sang Tab 6 để xem chất lượng giao đúng hẹn %ODR nhé!\""""
    },

    # ----------------------------------------------------
    # TAB 6: %ODR ĐÚNG HẸN
    # ----------------------------------------------------
    {
        "id": "tab-odr",
        "title": "🗣️ PHÂN TÍCH CHẤT LƯỢNG GIAO ĐÚNG HẸN %ODR (BẬT TAB 6 DASHBOARD):",
        "content": """📍 1. BẢNG 1 & 2: %ODR 5 TỈNH THÀNH (TARGET ≥ 92.0%):
• Bình Thuận: 96,74% (W39: 96,27%, +0,47%p) ➔ Dẫn đầu toàn vùng.
• Ninh Thuận: 96,62% (W39: 96,43%, +0,19%p) ➔ Rất xuất sắc.
• Khánh Hòa: 95,59% (W39: 91,94%, bứt phá +3,65%p) ➔ Vượt chuẩn an toàn.
• Đắk Nông: 90,42% (W39: 88,53%, tăng +1,89%p) ➔ Đã vượt 90%, tiệm cận chuẩn.
• Lâm Đồng: 87,79% (W39: 84,69%, tăng +3,10%p) ➔ Tiến bộ lớn nhưng là tỉnh duy nhất chưa đạt 92%.
• Toàn vùng: Full hàng đạt 93,12% (+2,28%p) | TikTok Shop đạt 94,18% (+2,41%p) ➔ ĐẠT CHUẨN SLA TOÀN VÙNG!

📍 2. BẢNG 3: HIỆU SUẤT %ODR FULL HÀNG THEO 18 AM:
• Top AM xuất sắc nhất (%ODR > 96%):
  1. Cao Thị Thanh Thủy (Khánh Hòa): 97,8% ➔ Quán quân ODR toàn vùng Nam Trung Bộ!
  2. Nguyễn Ngọc Khánh (Bình Thuận): 97,4%
  3. Thái Thị Thanh Thư (Khánh Hòa): 96,9%
  4. Nguyễn Duy Long (Ninh Thuận): 96,6%
• Bottom 5 AM báo động đỏ (%ODR thấp nhất):
  1. Lê Minh Lợi (Lâm Đồng): 74,1% ➔ Thấp nhất vùng, điểm nóng BC Lang Biang.
  2. Trương Quang Linh (Đắk Nông): 74,9% ➔ Điểm nóng BC Quảng Tín.
  3. Phan Nguyễn Yến Nhi (Lâm Đồng): 76,1% ➔ Điểm nóng BC Đơn Dương.
  4. Lê Văn Trường (Lâm Đồng): 78,3% ➔ Điểm nóng BC Xuân Hương.
  5. Nguyễn Lê Nguyên Vũ (Lâm Đồng): 87,2%

📍 3. BẢNG 4: BÁO ĐỘNG ĐỎ CỰC ĐẠI — %ODR TIKTOK SHOP (SLA CAM KẾT SÀN):
• Nhóm ven biển giữ vững đỉnh cao: Nguyễn Ngọc Khánh (98,2%), Cao Thị Thanh Thủy (97,6%), Nguyễn Đỗ Minh Nghĩa (97,3%), Nguyễn Duy Long (97,2%).
• NHƯNG KHU VỰC TÂY NGUYÊN SỤP ĐỔ THÊ THẢM TRÊN KÊNH TIKTOK SHOP:
  - Lê Minh Lợi: 14,3% (ODR TTS rớt xuống đáy vực! 100 đơn giao thì 86 đơn bị trễ hẹn!)
  - Trương Quang Linh: 42,0% (Giao trễ gần 60% đơn hàng TikTok Shop!)
  - Phan Nguyễn Yến Nhi: 44,6% (Hơn một nửa đơn hàng bị sàn phạt trễ hẹn!)
  - Lê Văn Trường: 62,1% (Gần 40% đơn giao trễ hẹn sàn!)
  - Nguyễn Lê Nguyên Vũ: 80,4% (Dưới chuẩn 92%)

🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 6 DASHBOARD %ODR):
"Dạ kính thưa Ban Giám Đốc, qua Tab 6 là chỉ số sống còn ODR - Giao đúng hẹn để giữ hợp đồng với các sàn TMĐT và khách hàng VIP:
Nhìn tổng thể, toàn vùng mình đạt 93,12% (TikTok Shop đạt 94,18%), chính thức vượt qua vạch đích SLA 92%!
Ba tỉnh ven biển gồm Bình Thuận (96,7%), Ninh Thuận (96,6%) và Khánh Hòa (95,6%) làm cực kỳ xuất sắc.
Em xin tuyên dương chị Cao Thị Thanh Thủy ở Khánh Hòa: Tuần này chị Thủy đạt ODR đỉnh toàn vùng 97,8%, gần như 100 đơn đi là giao đúng hẹn trọn vẹn 98 đơn! Anh Khánh, chị Thư và anh Duy Long cũng duy trì phong độ rất cao trên 96,6%.

TUY NHIÊN, tôi yêu cầu tất cả các AM nhìn vào Bảng 4 ODR TikTok Shop giúp tôi:
Các anh chị có thấy giật mình không?
Trong khi nhóm ven biển anh Khánh, chị Thủy, anh Nghĩa đạt 97-98%, thì nhìn xuống 4 cái tên ở Tây Nguyên:
Anh Lê Minh Lợi: ODR TikTok Shop chỉ có 14,3%! Cứ 100 đơn hàng của TikTok Shop giao tới tay khách thì có tới 86 đơn bị trễ hạn cam kết!
Anh Trương Quang Linh: 42,0%!
Chị Phan Nguyễn Yến Nhi: 44,6%!
Và anh Lê Văn Trường: 62,1%!
Bốn anh chị đang biến địa bàn của mình thành 'vùng trũng SLA' nghiêm trọng nhất toàn quốc!

🔍 INSIGHT BẢN CHẤT & GỐC RỄ NGUYÊN NHÂN:
Tại sao ODR hàng TikTok Shop ở vùng cao lại sụp đổ nặng nề như vậy?
Insight hiện trường rất rõ: Đơn TikTok Shop quy định thời gian giao hàng cực kỳ ngặt nghèo (trong vòng 24h - 48h từ khi rời kho).
Nhưng shipper của anh Lợi ở bưu cục Lang Biang, anh Linh ở bưu cục Quảng Tín, chị Nhi ở bưu cục Đơn Dương chạy các tuyến đồi núi dốc xa 20-30km có thói quen: 'Gom đơn lại 2-3 ngày mới đi một chuyến cho đỡ tốn xăng'!
Kiện hàng nằm ngâm ở bưu cục từ thứ Hai, đến tận thứ Tư shipper mới mang đi phát. Đến nơi thì hệ thống sàn TikTok Shop đã ghi nhận trễ hẹn từ hôm trước!
Hậu quả là gì?
TikTok Shop họ quét hệ thống tự động: Họ đánh gậy cảnh cáo chủ shop, shop bị phạt tiền oan ức họ quay sang chửi rủa GHN và khóa cổng vận chuyển của chúng ta! Khách hàng chờ lâu bực mình từ chối nhận hàng, đẩy tỷ lệ hoàn trả tăng vọt!

🎯 QUYẾT SÁCH HÀNH ĐỘNG & MỆNH LỆNH TÁC CHIẾN:
1. Tôi yêu cầu anh Lợi, anh Linh, chị Nhi, anh Trường: Bắt buộc phải chia lại tuyến và chạy tuyến mỗi ngày, tuyệt đối cấm hành vi gom đơn qua ngày để đi một lần!
2. Bưu cục nào đơn tuyến xa ít thì Trưởng bưu cục phải trực tiếp lấy xe máy phụ shipper chạy giải tỏa các đơn cận giờ SLA trước 12h00 trưa hàng ngày.
3. Tuần W41, 4 AM này phải đưa ODR TikTok Shop vượt lên trên mốc 80%, nếu tiếp tục để rớt dưới 50% sẽ đình chỉ điều hành Last-mile để phòng Vận hành vùng vào tiếp quản!
Giờ em xin chuyển sang Tab 7 xem tỷ lệ lấy hàng %LTC First-mile ạ!\""""
    },

    # ----------------------------------------------------
    # TAB 7: %LTC LẤY THÀNH CÔNG
    # ----------------------------------------------------
    {
        "id": "tab-ltc",
        "title": "🗣️ PHÂN TÍCH CHỈ SỐ %LTC LẤY HÀNG THÀNH CÔNG (BẬT TAB 7 DASHBOARD):",
        "content": """📍 1. BẢNG %LTC 5 TỈNH THÀNH (TARGET ≥ 90.0%):
• Ninh Thuận: 97,6% (W39: 97,3%) ➔ Dẫn đầu tuyệt đối, lấy hàng chuẩn chỉ.
• Khánh Hòa: 91,6% (W39: 91,0%) ➔ Vượt chuẩn an toàn.
• Đắk Nông: 91,1% (W39: 89,8%) ➔ Bứt phá vượt chuẩn 90%.
• Lâm Đồng: 90,0% (W39: 88,9%) ➔ Chạm ngưỡng chuẩn SLA.
• Bình Thuận: 89,8% (W39: 89,5%) ➔ Tiệm cận chuẩn 90%.
• Toàn vùng: Full hàng đạt 91,35% (+1,22%p) | Riêng TikTok Shop đạt 94,97% (+1,51%p).

📍 2. PHÂN TÍCH THEO 18 AM:
• Top AM lấy hàng xuất sắc nhất (%LTC > 94%):
  1. Nguyễn Duy Long (Ninh Thuận): 97,1%
  2. Nguyễn Đỗ Minh Nghĩa (Lâm Đồng): 97,0%
  3. Cao Thị Thanh Thủy (Khánh Hòa): 95,1%
  4. Nguyễn Thị Tuyết Thơ (Lâm Đồng): 94,5%
• 4 AM báo động đỏ khâu lấy hàng:
  1. Trương Quang Linh (Đắk Nông): 53,2% ➔ Rơi tự do, tỷ lệ lấy thất bại lên tới 46,8%!
  2. Phan Nguyễn Yến Nhi (Lâm Đồng): 70,0% ➔ Lấy hụt 30% yêu cầu của shop!
  3. Lê Minh Lợi (Lâm Đồng): 73,6% ➔ Quá thấp!
  4. Nguyễn Thanh Long (Khánh Hòa): 85,2%

🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 7 DASHBOARD %LTC):
"Kính thưa Ban Giám Đốc, First-mile lấy hàng chính là cánh cửa đầu tiên để khách hàng tin tưởng GHN. Nếu chúng ta lấy hàng không xong thì đừng bao giờ mơ đến chuyện tăng trưởng sản lượng:
Tin tốt là toàn vùng tuần này đã vượt mốc 91% (đạt 91,35%), và kênh TikTok Shop đạt gần 95%.
Anh Duy Long ở Ninh Thuận (97,1%), anh Nghĩa ở Lâm Đồng (97,0%) và chị Thủy ở Khánh Hòa (95,1%) làm khâu lấy hàng rất bài bản, shipper chủ động hẹn giờ và đến đúng hẹn với các chủ shop.

NHƯNG nhìn vào đáy bảng LTC, tôi yêu cầu anh Trương Quang Linh, chị Yến Nhi và anh Lê Minh Lợi nghe rõ:
Anh Linh ở Đắk Nông LTC chỉ đạt 53,2%! Cứ 10 shop tạo yêu cầu lấy hàng thì shipper của anh Linh bỏ lỡ gần 5 shop!
Chị Nhi ở Đơn Dương chỉ đạt 70,0%, anh Lợi ở Đà Lạt chỉ đạt 73,6%!

🔍 INSIGHT BẢN CHẤT & GỐC RỄ NGUYÊN NHÂN:
Tại sao tỷ lệ lấy hàng của anh Linh lại sụt giảm thê thảm như vậy?
Gốc rễ hiện trường: Buổi chiều từ 16h đến 18h là lúc các shop đóng gói xong hàng loạt để gửi đi.
Shipper của các anh chị lười chạy tuyến xa hoặc gặp trời mưa, tự ý bấm trên app lý do ảo: 'Shop hẹn ngày mai lấy' hoặc 'Shop chưa đóng gói xong' mà không hề gọi điện hay đến tận nơi!
Chủ shop đóng hàng xong, ngồi chờ đến 18h tối không thấy bóng dáng shipper GHN đâu, gọi điện lên bưu cục không ai bắt máy. Họ lập tức hủy đơn trên sàn và gọi shipper của Viettel Post, J&T hoặc SPX sang bốc hàng đi ngay trong đêm!
Các anh chị đang tự tay đuổi khách hàng sang cho đối thủ cạnh tranh!

🎯 QUYẾT SÁCH HÀNH ĐỘNG & MỆNH LỆNH TÁC CHIẾN:
• Yêu cầu anh Linh, chị Nhi, anh Lợi: Từ ngày hôm nay, 100% đơn lấy hàng không thành công bắt buộc phải có biên bản xác nhận hoặc ghi âm cuộc gọi của chủ shop hẹn lùi ngày.
• Trưởng bưu cục phải kiểm soát danh sách yêu cầu lấy hàng trên hệ thống trước 17h00 hàng ngày, nếu shipper nào chưa lấy phải điều phối nhân sự khác đến hỗ trợ ngay lập tức. Tuần W41 bắt buộc kéo %LTC lên trên 90%!
Giờ em xin chuyển sang Tab 8 mổ xẻ Chỉ số %OPR TikTok Shop lấy hàng ngày và đêm ạ!\""""
    },

    # ----------------------------------------------------
    # TAB 8: %OPR TIKTOK SHOP
    # ----------------------------------------------------
    {
        "id": "tab-opr-tts",
        "title": "🗣️ PHÂN TÍCH CHUYÊN SÂU HIỆU SUẤT LẤY HÀNG %OPR TIKTOK SHOP (TARGET KPI ≥ 80.0%) (BẬT TAB 8 DASHBOARD):",
        "content": """📍 1. BẢNG 1: TỔNG QUAN %OPR TIKTOK SHOP TOÀN VÙNG & 5 TỈNH THÀNH (W40):
• TỔNG TOÀN VÙNG: 83,48% ➔ Đạt chuẩn SLA sàn ≥ 80,0% (10.526 đơn đạt chuẩn / 12.609 đơn phát sinh | Tổng đơn lỗi trễ hạn: 2.083 đơn).
  - Khung giờ Ngày (9h00 – 19h00): Đạt rất cao 91,63% (6.809 / 7.431 đơn đạt chuẩn | Chỉ lỗi 622 đơn).
  - Khung giờ Đêm (19h00 – 9h00 sáng hôm sau): Sụt giảm nghiêm trọng còn 71,73% (3.718 / 5.183 đơn đạt chuẩn | LỖI TỚI 1.465 ĐƠN, chiếm tới 70,3% tổng lượng đơn lỗi của cả vùng!).
• Xếp hạng %OPR TTS theo 5 Tỉnh thành:
  1. Ninh Thuận: 93,79% (Ngày 97,59%, Đêm 85,19% | Vol 1.676 đơn) ➔ Tỉnh quán quân xuất sắc nhất toàn vùng!
  2. Khánh Hòa: 89,23% (Ngày 94,10%, Đêm 84,57% | Vol 3.157 đơn) ➔ Rất vững vàng, cả ngày và đêm đều trên 84%.
  3. Bình Thuận: 83,45% (Ngày 88,05%, Đêm 77,37% | Vol 4.235 đơn) ➔ Đạt chuẩn tổng nhưng ca đêm còn non.
  4. Lâm Đồng: 75,54% (Ngày 89,58%, ĐÊM CHỈ ĐẠT 48,32% | Vol 2.968 đơn) ➔ KHÔNG ĐẠT KPI 80% ❌
  5. Đắk Nông: 62,80% (Ngày 97,20%, ĐÊM RƠI TỰ DO XUỐNG 7,24% | Vol 578 đơn) ➔ BÁO ĐỘNG ĐỎ KHÔNG ĐẠT KPI ❌

📍 2. BẢNG 2: DANH SÁCH CÁC AM LÀM XUẤT SẮC NHẤT (%OPR TTS ≥ 90.0% — TUYÊN DƯƠNG):
• 1. Nguyễn Thị Tuyết Thơ (Lâm Đồng): OPR Tổng 96,6% (Ngày 98,8%, Đêm 94,7% | Vol 529 đơn — chỉ lỗi 18 đơn) ➔ Quán quân OPR TTS toàn vùng!
• 2. Nguyễn Đỗ Minh Nghĩa (Lâm Đồng): OPR Tổng 95,7% (Ngày 96,9%, Đêm 89,3% | Vol 468 đơn — chỉ lỗi 20 đơn).
• 3. Phan Đình Duy (Khánh Hòa): OPR Tổng 95,1% (Ngày 99,0%, Đêm 85,6% | Vol 446 đơn — chỉ lỗi 22 đơn).
• 4. Nguyễn Duy Long (Ninh Thuận): OPR Tổng 93,8% trên khối lượng cực lớn 1.824 đơn (Ngày 97,3%, Đêm 85,6% — lỗi chỉ 113 đơn).
• 5. Nguyễn Thanh Long (Khánh Hòa): OPR Tổng 100,0% (Đêm 33/33 đơn đạt 100%).
• 6. Thái Thị Thanh Thư (Khánh Hòa): OPR Tổng 90,3% trên khối lượng 1.857 đơn (Ngày 92,2%, Đêm 88,4%).
• 7. Cao Thị Thanh Thủy (Khánh Hòa): OPR Tổng 89,8% trên 1.188 đơn (Ngày 95,3%, Đêm 85,5%).

📍 3. BẢNG 3: DANH SÁCH CÁC AM KHÔNG ĐẠT KPI (< 80.0%) VÀ LỖI CỤ THỂ TỪNG AM:
• 1. Lê Văn Trường (Lâm Đồng): OPR Tổng chỉ đạt 42,6% ➔ Thấp nhất vùng! Lỗi trôi sạch đơn đêm (Đêm đạt vỏn vẹn 11,1%).
• 2. Trần Thị Nhung (Đắk Nông): OPR Tổng chỉ đạt 40,5% ➔ Ngày 98,4% nhưng đêm chỉ đạt 12,2%, bỏ rơi 115 đơn đêm.
• 3. Hồng Bích Nga (Đắk Nông): OPR Tổng 76,3% ➔ Ngày chỉ đạt 80,2%, đêm 61,4%, lỗi trôi đều cả ngày lẫn đêm.
• 4. Huỳnh Thúc Duân (Đắk Nông): OPR Tổng 78,7% ➔ Ngày 96,7% nhưng ca đêm TÊ LIỆT 0,0% (trôi sạch 63 đơn đêm).
• 5. Lê Thanh Nhựt (Bình Thuận): OPR Tổng 78,6% ➔ Ngày 78,5%, đêm 78,6%, để rớt hơn 420 đơn do quá tải điều phối.
• 6. Huỳnh Thị Kim Chi / Lê Minh Lợi / Phan Nguyễn Yến Nhi: OPR Tổng 0,0% (phát sinh đơn đêm nhưng bỏ qua không lấy).

📍 4. BẢNG 4: MỔ XẺ ĐÍCH DANH AM NÀO KÉO TỶ TRỌNG LỖI NHIỀU NHẤT VÙNG (TRÊN TỔNG 2.083 ĐƠN LỖI):
• 🔴 ĐẦU SỎ SỐ 1 KÉO TỤT TOÀN VÙNG: AM LÊ VĂN TRƯỜNG (LÂM ĐỒNG):
  - Gây ra tới 494 ĐƠN LỖI, chiếm 23,7% TỔNG LƯỢNG ĐƠN LỖI CỦA CẢ VÙNG NAM TRUNG BỘ!
  - Riêng ban đêm anh Trường để lỗi tới 434 đơn trên 488 đơn đêm phát sinh (tỷ lệ lỗi đêm lên tới 88,9%!).
• 🔴 ĐẦU SỎ SỐ 2 KÉO TỤT TOÀN VÙNG: AM LÊ THANH NHỰT (BÌNH THUẬN):
  - Gây ra 424 ĐƠN LỖI, chiếm 20,4% TỔNG LƯỢNG ĐƠN LỖI TOÀN VÙNG! (Lỗi ngày 219 đơn, lỗi đêm 205 đơn).
  ➔ ĐẶC BIỆT CHÚ Ý: CHỈ RIÊNG 2 AM LÊ VĂN TRƯỜNG VÀ LÊ THANH NHỰT ĐÃ GÂY RA 918 ĐƠN LỖI, CHIẾM TỚI 44,1% (GẦN MỘT NỬA) TOÀN BỘ ĐƠN HÀNG TRỄ HẠN OPR TTS CỦA CẢ VÙNG!
• 🔴 ĐẦU SỎ SỐ 3: AM HỒNG BÍCH NGA (ĐẮK NÔNG): Gây ra 182 đơn lỗi (chiếm 8,7% tổng lỗi vùng; lỗi ngày 121 đơn, lỗi đêm 61 đơn).
• 🔴 ĐẦU SỎ SỐ 4: AM TRẦN THỊ NHUNG (ĐẮK NÔNG): Gây ra 116 đơn lỗi (chiếm 5,6% tổng lỗi vùng; trong đó lỗi đêm là 115 đơn trên 131 đơn phát sinh).
• 🔴 ĐẦU SỎ SỐ 5: AM HUỲNH THÚC DUÂN (ĐẮK NÔNG): Gây ra 72 đơn lỗi (chiếm 3,5% tổng lỗi vùng; trôi sạch 100% 63 đơn đêm, OPR đêm 0,0%).

🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 8 DASHBOARD %OPR TIKTOK SHOP):
"Kính thưa Ban Giám Đốc và các anh chị AM, chuyển sang Tab 8 là chỉ số OPR TikTok Shop - Tỷ lệ lấy hàng đúng hạn cam kết của sàn:
Trước hết về con số tổng thể: Toàn vùng Nam Trung Bộ của chúng ta tuần W40 đạt 83,48%, chính thức vượt qua ngưỡng chuẩn KPI của sàn là 80,0%.
Tổng lượng đơn phát sinh là 12.609 đơn, trong đó chúng ta lấy chuẩn giờ được 10.526 đơn, và có 2.083 đơn hàng bị vi phạm trễ hẹn.
Tỉnh Ninh Thuận của anh Duy Long tiếp tục là quán quân toàn vùng với OPR đạt tới 93,79%, kế đến là Khánh Hòa 89,23%, và Bình Thuận 83,45%.
Về phía cá nhân các AM xuất sắc: Em xin tuyên dương đặc biệt chị Nguyễn Thị Tuyết Thơ ở Lâm Đồng: Chị Thơ đạt OPR đỉnh toàn vùng 96,6% trên 529 đơn hàng, cả ban ngày (98,8%) lẫn ban đêm (94,7%) đều gần như tuyệt đối!
Anh Nguyễn Đỗ Minh Nghĩa đạt 95,7%, anh Phan Đình Duy đạt 95,1%, và đặc biệt là anh Nguyễn Duy Long gánh sản lượng cực khủng hơn 1.800 đơn mà OPR vẫn giữ vững 93,8%! Chị Thư (90,3%) và chị Thủy (89,8%) cũng hoàn thành rất tốt nhiệm vụ.

TUY NHIÊN, nhìn vào mặt tối của bức tranh, tôi yêu cầu 2 tỉnh Lâm Đồng (75,54%) và Đắk Nông (62,80%) cùng các AM liên quan nhìn thẳng vào sự thật:
Toàn vùng có 2.083 đơn hàng bị trễ hẹn với sàn TikTok Shop, thì tôi hỏi các anh chị: AI LÀ NGƯỜI KÉO TỶ TRỌNG LỖI NHIỀU NHẤT?
Anh Lê Văn Trường và anh Lê Thanh Nhựt đứng dậy!
Hai anh nhìn lên màn hình giúp tôi:
Một mình anh Lê Văn Trường ở Lâm Đồng gây ra tới 494 đơn lỗi, chiếm tới 23,7% — tức là gần một phần tư tổng số đơn lỗi của toàn vùng!
Anh Lê Thanh Nhựt ở Bình Thuận gây ra 424 đơn lỗi, chiếm 20,4% tổng số đơn lỗi!
Cộng hai anh lại là 918 đơn hàng trễ hẹn, chiếm tới 44,1% — gần một nửa số lượng lỗi của cả vùng Nam Trung Bộ nằm trọn trong tay anh Trường và anh Nhựt!
Kế đến là chị Hồng Bích Nga gây ra 182 đơn lỗi (8,7%), chị Trần Thị Nhung gây ra 116 đơn lỗi (5,6%), và anh Huỳnh Thúc Duân gây ra 72 đơn lỗi (3,5%)!

🔍 INSIGHT BẢN CHẤT & BÓC TÁCH GỐC RỄ NGUYÊN NHÂN:
Tại sao anh Trường, anh Nhựt, chị Nhung, anh Duân lại để trôi đơn khủng khiếp như vậy?
Bóc tách ra có 3 nguyên nhân cốt tử:
1. LỖI THỨ NHẤT: TÊ LIỆT HOÀN TOÀN ĐƠN CA ĐÊM (Chiếm tới hơn 70% tổng lượng đơn lỗi toàn vùng - 1.465 / 2.083 đơn):
Đặc thù sàn TikTok Shop là các shop livestream bán hàng bùng nổ từ 20h00 đến 23h30 đêm! Khách đặt hàng nườm nượp, shop in đơn sẵn chờ lấy.
Nhưng bưu cục của anh Trường (Đơn Dương, Xuân Hương), bưu cục của anh Duân (Gia Nghĩa, Nhân Cơ), bưu cục chị Nhung (Cư Jút, Tuy Đức) đúng 18h00 là nhân viên dọn dẹp, 18h30 là Trưởng bưu cục khóa cửa tắt đèn đi về!
Không có ai trực đêm, không có shipper gom chuyến tối! Đơn hàng phát sinh từ 21h đêm qua nằm ngâm chết dí trên app, đến tận 9h30 - 10h00 sáng hôm sau shipper mới tới bưu cục rồi túc tắc đi lấy.
Lúc đó thuật toán của TikTok Shop nó đã tự động quét vi phạm SLA OPR trễ hơn 12 tiếng rồi! Đó là lý do vì sao OPR ban đêm của anh Duân rớt về 0,0%, anh Vũ 9,4%, anh Trường 11,1%, chị Nhung 12,2%!
2. LỖI THỨ HAI: TRỄ CHUYẾN LẤY CA 1 SÁNG:
Shipper buổi sáng đến bưu cục có thói quen chỉ lo tranh nhau bốc hàng đi giao ca 1 cho xong chuyến, bỏ quên toàn bộ các yêu cầu lấy hàng First-mile phát sinh đầu giờ sáng! Mãi đến 11h - 12h trưa đi giao về mới tạt qua shop lấy, dẫn đến 622 đơn ca ngày bị quá hạn cam kết 10h30.
3. LỖI THỨ BA: THIẾU CƠ CHẾ PHÂN LUỒNG SHOP LIVESTREAM:
AM và Trưởng bưu cục không nắm được danh sách các shop có lịch livestream cố định trên địa bàn để bố trí người gom riêng, dẫn đến việc đối xử cào bằng shop lớn với shop gửi lẻ thông thường.

🎯 QUYẾT SÁCH HÀNH ĐỘNG & MỆNH LỆNH TÁC CHIẾN TUẦN W41:
1. Giao đích danh AM Lê Văn Trường và AM Lê Thanh Nhựt: Phải giảm ngay ít nhất 70% lượng đơn lỗi trong tuần W41, đưa OPR TTS của cụm mình vượt mốc 85%!
2. Tất cả bưu cục có shop livestream phát sinh trên 30 đơn/đêm bắt buộc bố trí 1 ca trực tối đến 21h30 hoặc hợp đồng bưu tá gom chuyến chốt lúc 21h00.
3. Xuất bến ca lấy sớm lúc 07h30 sáng, toàn bộ đơn đêm phải được quét lấy và bắn trạng thái 'Đã lấy hàng' lên sàn TikTok Shop trước 08h30 sáng!
4. Giám đốc Vận hành sẽ kiểm tra đột xuất dữ liệu OPR đêm lúc 22h00 và 8h00 sáng mỗi ngày, bưu cục nào để trôi đơn đêm sẽ xử phạt trừ thẳng KPI của Trưởng bưu cục!
Bây giờ, em xin chuyển sang Tab 9 mổ xẻ tình trạng Rớt luân chuyển KTC ạ!"""
    },

    # ----------------------------------------------------
    # TAB 9: RỚT LUÂN CHUYỂN KTC
    # ----------------------------------------------------
    {
        "id": "tab-rot-lc",
        "title": "🗣️ PHÂN TÍCH HIỆN TƯỢNG RỚT ĐƠN LUÂN CHUYỂN KTC (BẬT TAB 9 DASHBOARD):",
        "content": """📍 1. BẢNG TỔNG HỢP VÙNG & 5 TỈNH THÀNH:
• Toàn vùng: 1,69% đơn rớt (W39: 1,52%, tăng nhẹ +0,17%p; 219 đơn rớt / 12.934 đơn cần luân chuyển).
• Lâm Đồng: 3,84% rớt LC (121 đơn rớt / 3.151 đơn) ➔ Tỉnh rớt nhiều nhất, chiếm hơn 55% lượng đơn rớt toàn vùng!
• Ninh Thuận: 3,58% rớt LC (60 đơn rớt / 1.676 đơn) ➔ Tỷ lệ rớt rất cao.
• Đắk Nông: 1,12% rớt LC (19 đơn rớt).
• Khánh Hòa: 0,48% rớt LC (12 đơn rớt / 2.500 đơn) ➔ Kiểm soát tốt.
• Bình Thuận: 0,28% rớt LC (7 đơn rớt / 2.500 đơn) ➔ Rất an toàn.

📍 2. PHÂN TÍCH CHI TIẾT THEO AM & BƯU CỤC ĐIỂM NÓNG:
• Top AM có tỷ lệ rớt LC cao nhất vùng:
  1. Nguyễn Đỗ Minh Nghĩa (Lâm Đồng): 6,20% rớt LC (BC Cát Tiên rớt tới 29 đơn!)
  2. Hồng Bích Nga (Đắk Nông): 4,63% rớt LC (BC Kiến Đức rớt 5 đơn)
  3. Nguyễn Thị Tuyết Thơ (Lâm Đồng): 4,24% rớt LC (BC Ninh Gia rớt 5 đơn)
  4. Nguyễn Duy Long (Ninh Thuận): 3,29% rớt LC (gánh tới 60 đơn rớt; riêng BC Thuận Nam rớt 6 đơn)
  5. Lê Văn Trường (Lâm Đồng): 2,77% rớt LC (BC Xuân Hương rớt 2 đơn)

🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 9 DASHBOARD RỚT LUÂN CHUYỂN):
"Dạ kính thưa Ban Giám Đốc, nhìn vào Tab 9 Rớt luân chuyển KTC:
Tuần W40 toàn vùng mình có 219 đơn hàng bị rớt luân chuyển, tương ứng tỷ lệ 1,69%, tăng nhẹ so với 1,52% của tuần trước.
Con số 219 đơn nghe qua thì thấy nhỏ so với quy mô 311 ngàn đơn, nhưng khi mổ xẻ ra thì thấy một sự phân hóa cực kỳ nguy hiểm:
Hai tỉnh Bình Thuận và Khánh Hòa kiểm soát rất chặt chẽ, tỷ lệ rớt chỉ 0,28% đến 0,48%.
NHƯNG toàn bộ 219 đơn rớt này lại tập trung dồn cục ở 2 tỉnh: Lâm Đồng rớt tới 121 đơn (chiếm 3,84%) và Ninh Thuận rớt 60 đơn (chiếm 3,58%)!
Soi vào từng AM:
Anh Nguyễn Đỗ Minh Nghĩa tỷ lệ rớt lên tới 6,20%, trong đó riêng bưu cục Cát Tiên làm rớt một phát 29 đơn hàng!
Chị Hồng Bích Nga ở Đắk Nông rớt 4,63%, chị Tuyết Thơ ở Lâm Đồng rớt 4,24%, và anh Duy Long ở Ninh Thuận rớt tới 60 đơn (3,29%)!

🔍 INSIGHT BẢN CHẤT & GỐC RỄ NGUYÊN NHÂN:
Tại sao xe tải KTC ngày nào cũng chạy qua bưu cục mà đơn hàng lại bị rớt lại kho?
Có 2 nguyên nhân cốt lõi qua kiểm tra thực tế:
Thứ nhất: Thói quen ĐÓNG BAO TRỄ GIỜ XE CHẠY. Xe tải KTC theo lịch trình đến bưu cục lúc 17h30. Nhưng đến 17h30 nhân viên bưu cục mới bắt đầu gom hàng đóng bao, in manifest. Tài xế KTC bấm còi giục, đợi 15 phút không xong phải cho xe xuất bến để kịp giờ cắt bến trung tâm. Thế là số bao chưa đóng xong bị bỏ lại kho!
Thứ hai: SÓT MÃ KIỆN VÀ LẪN HÀNG. Bưu tá thu gom về để lẫn đơn luân chuyển với đơn tồn giao. Nhân viên bắn quét sót mã kiện, hàng nằm góc kho mà không ai hay biết.
Mỗi một đơn hàng rớt luân chuyển đồng nghĩa với việc hành trình của khách hàng bị cộng thêm ít nhất 24 đến 48 tiếng! Đơn hàng đang đúng hẹn lập tức biến thành trễ hẹn, làm tụt ODR của toàn vùng!

🎯 QUYẾT SÁCH HÀNH ĐỘNG & MỆNH LỆNH TÁC CHIẾN:
1. Tôi yêu cầu Trưởng bưu cục Cát Tiên, Thuận Nam, Ninh Gia, Kiến Đức: Bắt buộc phải hoàn thành đóng bao và niêm phong seal trước giờ xe KTC đến ít nhất 15 phút.
2. Tài xế KTC và Trưởng bưu cục phải thực hiện ký biên bản giao nhận quét mã 100%, tuyệt đối không bàn giao vo bằng miệng.
3. AM Nghĩa và AM Long phải kiểm tra trực tiếp bưu cục Cát Tiên và Thuận Nam, đưa tỷ lệ rớt LC tuần W41 về dưới mốc 1,0%!
Bây giờ, em xin phép chuyển sang Tab 10 phân tích tỷ lệ hoàn trả %FD nhé!\""""
    },

    # ----------------------------------------------------
    # TAB 10: %FD HOÀN TRẢ
    # ----------------------------------------------------
    {
        "id": "tab-fd",
        "title": "🗣️ PHÂN TÍCH TỶ LỆ HOÀN TRẢ %FD (RETURN RATE) (BẬT TAB 10 DASHBOARD):",
        "content": """📍 1. BẢNG TỔNG QUAN TỶ LỆ HOÀN TRẢ TOÀN VÙNG:
• Toàn vùng: 7,77% (W39: 7,54%, tăng nhẹ +0,23%p; 24.498 đơn return / 315.328 đơn phát sinh; 86 bưu cục).
• Kênh TikTok Shop kiểm soát tốt ở mức 6,10%.

📍 2. BẢNG 2: TOP BƯU CỤC BÁO ĐỘNG ĐỎ TỶ LỆ HOÀN TRẢ TRÊN 20% (GẤP GẦN 3 LẦN BÌNH QUÂN VÙNG):
• 1. (DNO) Quảng Tín: 22,95% (380 đơn hoàn / 1.656 đơn) ➔ AM Trương Quang Linh (Cứ 4 đơn đi giao thì trả về gần 1 đơn!)
• 2. (LDO) Lang Biang - Đà Lạt 1: 21,04% (444 đơn hoàn / 2.110 đơn) ➔ AM Lê Minh Lợi (Cảnh báo 108 ngày)
• 3. (LDO) Đơn Dương: 20,99% (653 đơn hoàn / 3.111 đơn) ➔ AM Phan Nguyễn Yến Nhi
• 4. (LDO) Đức Trọng 1: 20,53% (334 đơn hoàn / 1.627 đơn) ➔ AM Nguyễn Lê Nguyên Vũ
• Kế tiếp là các bưu cục có tỷ lệ hoàn trả rất cao:
  - (DNO) Kiến Đức: 16,71% (320 đơn hoàn) ➔ AM Hồng Bích Nga
  - (KHO) Cam Linh: 15,33% (579 đơn hoàn) ➔ AM Nguyễn Thanh Long

🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 10 DASHBOARD %FD HOÀN TRẢ):
"Kính thưa Ban Giám Đốc, chuyển sang Tab 10 là chỉ số %FD tỷ lệ hoàn trả:
Đây là con số gây xót xa nhất trong vận hành Last-mile: Chúng ta tốn công vận chuyển hàng từ đầu gửi về đến tận bưu cục, shipper chở hàng đi phát không được lại phải chở ngược về kho đóng bao trả lại cho người gửi! Vừa tốn chi phí vận hành 2 đầu, vừa mất trắng doanh thu, lại bị chủ shop khiếu nại!
Bình quân toàn vùng tuần này là 7,77% với hơn 24.400 đơn hoàn.
NHƯNG tôi yêu cầu tất cả các AM nhìn vào 4 cái tên bưu cục đang hiển thị đỏ chót trên màn hình:
Thứ nhất: Bưu cục Quảng Tín của anh Trương Quang Linh ở Đắk Nông: Tỷ lệ hoàn trả lên tới 22,95%!
Thứ hai: Bưu cục Lang Biang - Đà Lạt 1 của anh Lê Minh Lợi: 21,04%!
Thứ ba: Bưu cục Đơn Dương của chị Phan Nguyễn Yến Nhi: 20,99% với 653 đơn bị trả về!
Thứ tư: Bưu cục Đức Trọng 1 của anh Nguyễn Lê Nguyên Vũ: 20,53%!
Bốn bưu cục này đang có tỷ lệ hoàn trả trên 20%, cao gấp gần 3 lần mức bình quân của vùng! Cứ 5 đơn hàng giao đi thì có hơn 1 đơn bị trả về!

🔍 INSIGHT BẢN CHẤT & GỐC RỄ NGUYÊN NHÂN:
Tại sao hàng giao ở những bưu cục này lại bị trả về khủng khiếp như vậy?
Tôi trực tiếp xuống hiện trường tại Lang Biang và Quảng Tín tôi thấy rất rõ hiện tượng: 'SHIPPER BẤM HOÀN TRẢ ẢO ĐỂ NÉ TUYẾN ĐỒI NÚI':
Đặc thù địa bàn Lang Biang, Quảng Tín, Đơn Dương là đường đèo dốc khúc khuỷu, vào các buôn làng xa 15-20km, trời mưa đường đất sình lầy trơn trượt.
Shipper nhận đơn ngại đi xa, đứng ở bưu cục nhá máy cho khách 1 tiếng chuông rồi cúp máy ngay! Khách chưa kịp cầm điện thoại lên thì shipper đã nhanh tay bấm trên app lý do: 'Khách không nghe máy' hoặc 'Khách từ chối nhận hàng'!
Hoặc shipper cứ hẹn lùi ngày 3-4 lần liên tiếp, khách hàng đợi lâu quá họ mua chỗ khác, đến khi shipper đem hàng tới thì khách bực mình từ chối nhận!
Chính sự vô trách nhiệm của shipper đã biến đơn giao thành công thành đơn hoàn trả!

🎯 QUYẾT SÁCH HÀNH ĐỘNG & MỆNH LỆNH TÁC CHIẾN:
1. Giao trách nhiệm cá nhân cho anh Linh, anh Lợi, chị Nhi, anh Vũ: Bắt buộc từ ngày mai, Trưởng bưu cục hoặc nhân viên CS bưu cục phải gọi điện đối soát 100% các đơn shipper báo 'Khách từ chối nhận' trước khi bấm duyệt hoàn trên hệ thống.
2. Nếu phát hiện shipper bấm lý do ảo khi chưa liên hệ với khách: Phạt cắt thưởng chuyên cần của shipper đó và yêu cầu bưu tá mang hàng đi phát lại ngay trong ngày!
3. Mục tiêu tuần W41: Kéo tỷ lệ %FD của 4 bưu cục này từ trên 20% xuống dưới mốc 12%!
Bây giờ, em xin phép chuyển sang Tab 11 xem Báo cáo điều hành KTC & Vận tải đường trục ạ!\""""
    },

    # ----------------------------------------------------
    # TAB 11: KTC & VẬN TẢI
    # ----------------------------------------------------
    {
        "id": "tab-ktc",
        "title": "🗣️ BÁO CÁO ĐIỀU HÀNH KTC & VẬN TẢI ĐƯỜNG TRỤC (BẬT TAB 11 DASHBOARD):",
        "content": """📍 1. BẢNG HIỆU SUẤT VẬN TẢI TOÀN VÙNG:
• Tỷ lệ lấp đầy KTC toàn vùng (%TLTĐ): 51,0% (Target tối thiểu ≥ 55,0%).
• Tình trạng lãng phí tải trọng: Vẫn còn tới 76 chuyến xe chạy non tải dưới 30% thùng (đặc biệt tập trung ở tuyến nhánh Lâm Đồng, Đắk Nông và Ninh Thuận).
• Leadtime luân chuyển trung bình:
  - KTC Khánh Hòa: 8,4h (đạt chuẩn)
  - KTC Đức Trọng: 9,2h
  - KTC Đắk Nông: 11,5h ➔ Thời gian luân chuyển còn dài do địa hình chia cắt.

🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 11 DASHBOARD KTC & VẬN TẢI):
"Kính thưa Ban Giám Đốc, vận tải KTC chính là 'huyết mạch' và cũng là khoản chi phí lớn nhất của khối vận hành:
Tuần W40 này, tỷ lệ lấp đầy KTC toàn vùng đứng yên ở mức 51,0%, chưa đạt mục tiêu 55%.
Đáng chú ý nhất là con số 76 chuyến xe chạy non tải dưới 30% thùng!
Một chuyến xe tải 5 tấn hay 8 tấn chạy từ bưu cục huyện về kho trung tâm mà thùng xe rỗng hơn 70% thì mỗi cây số lăn bánh là công ty đang đốt tiền xăng dầu và khấu hao vô ích!
Insight: Các bưu cục tuyến huyện như Tân Hà, Đơn Dương, Cát Tiên, Đắk R'lấp thường nằng nặc yêu cầu xe KTC phải đến rước hàng theo giờ cố định dù chỉ gom được vài chục kiện. Điều phối KTC thì máy móc, chưa linh hoạt gộp tuyến tam giác hoặc dịch chuyển giờ cắt bến giữa các bưu cục gần nhau.

🎯 MỆNH LỆNH TÁC CHIẾN TUẦN W41:
• Phòng Vận tải KTC phải phối hợp với các AM: Cắt giảm ngay ít nhất 30 chuyến xe non tải bằng cách ghép tuyến liên huyện (ví dụ ghép tuyến Đơn Dương - Đức Trọng; ghép Tuy Đức - Kiến Đức).
• Đưa tỷ lệ lấp đầy KTC toàn vùng trong tuần W41 vượt qua mốc 55,0%!
Giờ em xin chuyển sang Tab 12 mổ xẻ Tồn Aging & Treo luân chuyển ạ!\""""
    },

    # ----------------------------------------------------
    # TAB 12: AGING & TREO LUÂN CHUYỂN
    # ----------------------------------------------------
    {
        "id": "tab-aging",
        "title": "🗣️ ĐIỀU HÀNH XỬ LÝ HÀNG AGING TỒN ĐỌNG & TREO LUÂN CHUYỂN (BẬT TAB 12 DASHBOARD):",
        "content": """📍 1. BẢNG TỔNG HỢP HÀNG TỒN AGING VÀ TREO LUÂN CHUYỂN:
• Tổng đơn tồn Aging >5 ngày toàn vùng: Hơn 2.400 đơn dồn ứ (trong đó có hàng trăm đơn tồn >15 ngày).
• Danh sách bưu cục điểm nóng dồn ứ hàng tồn >5 ngày:
  1. (DNO) Quảng Tín: 490 đơn tồn >5 ngày (AM Trương Quang Linh)
  2. (LDO) Xuân Hương - Đà Lạt: 310 đơn tồn >5 ngày (AM Lê Văn Trường)
  3. (LDO) Đức Trọng 1: 281 đơn tồn >5 ngày (AM Trầm Hữu Tiến / Nguyễn Lê Nguyên Vũ)
  4. (KHO) Cam Linh: 250 đơn tồn >5 ngày (AM Nguyễn Thanh Long)
  5. (LDO) Di Linh: 219 đơn tồn >5 ngày (AM Trầm Hữu Tiến)
• Đơn treo luân chuyển >24h: 36 đơn (tập trung tại Lâm Đồng và Đắk Nông).

🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 12 DASHBOARD AGING & TREO LC):
"Kính thưa Ban Giám Đốc, hàng Aging tồn đọng trên 5 ngày chính là những 'ổ bệnh' làm tê liệt mặt bằng bưu cục:
Hơn 2.400 đơn hàng đang nằm lưu cữu trên 5 ngày ở các bưu cục!
Điểm nóng lớn nhất:
Bưu cục Quảng Tín của anh Linh: 490 đơn tồn >5 ngày!
Bưu cục Xuân Hương của anh Trường: 310 đơn!
Bưu cục Đức Trọng 1: 281 đơn! Cam Linh: 250 đơn! Di Linh: 219 đơn!
Insight: Đơn hàng để càng lâu thì rủi ro mất mát, bể vỡ, chuột cắn, và khách hủy hàng càng cao. Bưu tá mới vào thấy đơn tồn lưu cữu không dám nhận đi phát, Trưởng bưu cục thì lười kiểm kê kho buổi sáng, cứ để hàng chất xó kho chờ khách tự khiếu nại!

🎯 MỆNH LỆNH TÁC CHIẾN TUẦN W41:
• Tôi ra tối hậu thư 48 giờ: Bắt đầu từ 8h00 sáng nay, Trưởng bưu cục 5 điểm nóng Quảng Tín, Xuân Hương, Đức Trọng 1, Cam Linh, Di Linh phải trực tiếp rà soát từng kiện hàng tồn >5 ngày.
• Phân loại dứt điểm: Đơn nào giao được phải phát ngay trước 17h00 ngày mai; đơn nào khách từ chối phải bấm hoàn trả về kho trung tâm; đơn nào thất lạc phải lập hồ sơ đền bù theo đúng quy trình.
• Hết 48 giờ mà bưu cục nào còn tồn đơn >5 ngày chưa xử lý, Ban Giám Đốc sẽ xem xét kỷ luật Trưởng bưu cục!
Bây giờ, em xin phép chuyển sang Tab 13 mổ xẻ Quản trị dòng tiền COD & Tỷ lệ nộp bằng QR Code nhé!\""""
    },

    # ----------------------------------------------------
    # TAB 13: QR CODE & TIỀN MẶT
    # ----------------------------------------------------
    {
        "id": "tab-control",
        "title": "🗣️ BÁO CÁO COD – QUẢN TRỊ DÒNG TIỀN & TỶ LỆ NỘP BẰNG QR CODE (BẬT TAB 13 DASHBOARD):",
        "content": """📍 1. BẢNG 1: TỔNG QUAN DÒNG TIỀN COD TOÀN VÙNG (W40 vs W39):
• Tổng COD thu hộ toàn vùng tuần W40: 77.502,0 Triệu VNĐ (~77,5 Tỷ đồng, giảm -3.231,6 Tr ₫ do sản lượng giảm nhẹ).
• Tiền mặt thu về: 31.276,0 Triệu VNĐ (chiếm tỷ lệ 40,4% tiền mặt).
• Chuyển khoản QR thu về: 46.226,0 Triệu VNĐ (chiếm tỷ lệ 59,6% chuyển khoản).
• Đánh giá biến động: Tỷ lệ tiền mặt tăng nhẹ +0,2%p so với mức 40,1% của tuần W39 (Xu hướng Xấu đi ⚠️).

📍 2. BẢNG 2: SO SÁNH TỶ LỆ TIỀN MẶT THEO 18 AM (TARGET TIỀN MẶT < 40%, QR > 60%):
• Quán quân thu COD bằng QR xuất sắc nhất toàn vùng:
  1. Thái Thị Thanh Thư (Khánh Hòa): Tiền mặt chỉ 4,0% ➔ Tỷ lệ chuyển khoản QR đạt tới 96,0%! (Thu hơn 9 Tỷ COD mà chỉ cầm 360 triệu tiền mặt, số hóa dòng tiền gần như tuyệt đối!).
  2. Cao Thị Thanh Thủy (Khánh Hòa): Tiền mặt 16,1% ➔ Tỷ lệ QR đạt 83,9%!
• 3 AM BÁO ĐỘNG ĐỎ VỀ NGUY CƠ THẤT THOÁT TIỀN MẶT (TỶ LỆ TIỀN MẶT TRÊN 75%):
  1. Huỳnh Thúc Duân: 81,0% Tiền mặt! (W39: 71,5%, tăng vọt +9,5%p ➔ CỰC KỲ NGUY HIỂM)
  2. Lê Thanh Nhựt: 80,4% Tiền mặt! (W39: 77,7%, tăng +2,7%p)
  3. Huỳnh Thị Kim Chi: 75,8% Tiền mặt! (W39: 68,6%, tăng vọt +7,2%p)

🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 13 DASHBOARD COD & QR CODE):
"Kính thưa Ban Giám Đốc, chuyển sang Tab 13 là Báo cáo Quản trị dòng tiền COD và thanh toán QR Code:
Tuần W40 này, toàn vùng chúng ta luân chuyển dòng tiền COD lên tới 77,5 TỶ ĐỒNG!
Trong đó, số tiền thu bằng chuyển khoản QR đạt 46,2 tỷ đồng (chiếm 59,6%), còn tiền mặt shipper ôm về là 31,3 tỷ đồng (chiếm 40,4%). So với tuần trước, tỷ lệ tiền mặt tăng nhẹ +0,2%p, tức là xu hướng đang xấu đi!

Nhìn vào bảng so sánh các AM, chúng ta thấy 2 bức tranh hoàn toàn đối lập:
Một bên làm cực kỳ xuất sắc: Em xin biểu dương chị Thái Thị Thanh Thư ở Khánh Hòa: Chị Thư thu hơn 9 tỷ tiền COD mà tỷ lệ tiền mặt chỉ vỏn vẹn 4,0%, còn lại 96% khách hàng quét mã VietQR nộp tiền thẳng về tài khoản công ty! Chị Thủy ở Khánh Hòa cũng đạt tới 84% chuyển khoản QR!
Khánh Hòa làm được như vậy chứng tỏ nếu bưu tá chịu khó hướng dẫn thì khách hàng ai cũng sẵn sàng quét QR!
NHƯNG các anh chị nhìn sang 3 AM ở nhóm báo động đỏ nghiêm trọng:
Anh Huỳnh Thúc Duân: 81,0% tiền mặt, tăng vọt gần 10%p so với tuần trước!
Anh Lê Thanh Nhựt: 80,4% tiền mặt!
Chị Huỳnh Thị Kim Chi: 75,8% tiền mặt!
Cứ 10 đồng tiền thu hộ của khách thì shipper của anh Duân, anh Nhựt, chị Chi đang ôm tới 8 đồng tiền mặt trong người!

🔍 INSIGHT BẢN CHẤT & GỐC RỄ NGUYÊN NHÂN:
Tại sao tỷ lệ tiền mặt ở cụm anh Duân, anh Nhựt, chị Chi lại cao bất thường như vậy?
Insight: Shipper có thói quen ngại chìa mã QR trên app GHN cho khách quét vì muốn cầm tiền mặt để chi tiêu cá nhân, rồi lấy tiền thu của ngày hôm sau bù đắp cho ngày hôm trước!
Nhiều bưu tá đổ lỗi rằng 'Bà con nông thôn không có tài khoản ngân hàng'. Điều đó hoàn toàn không đúng! Hiện nay bà con ở Đắk Nông hay Ninh Thuận đi chợ mua bó rau cũng quét VietQR.
Chính sự buông lỏng kiểm tra của Trưởng bưu cục đã tạo kẽ hở cho shipper giữ tiền mặt qua đêm, là nguyên nhân trực tiếp dẫn đến chiếm dụng công nợ và vỡ nợ tập thể!

🎯 QUYẾT SÁCH HÀNH ĐỘNG & MỆNH LỆNH TÁC CHIẾN:
1. Yêu cầu anh Duân, anh Nhựt, chị Chi: Bắt buộc 100% bưu tá khi đi giao hàng phải in hoặc mở mã QR động trên app GHN cho khách thanh toán.
2. Trưởng bưu cục phải thực hiện chốt sổ tiền mặt và đối soát nộp tiền vào tài khoản công ty 2 lần/ngày (lúc 12h00 trưa và 18h30 tối), tuyệt đối cấm shipper ôm tiền mặt về nhà qua đêm!
3. Tuần W41 bắt buộc 3 cụm này phải ép tỷ lệ tiền mặt xuống dưới 60%!
Giờ em xin chuyển sang Tab 14 mổ xẻ Báo cáo truy thu 2 tuần ạ!\""""
    },

    # ----------------------------------------------------
    # TAB 14: BÁO CÁO TRUY THU (2 TUẦN)
    # ----------------------------------------------------
    {
        "id": "tab-truythu",
        "title": "🗣️ PHÂN TÍCH BÁO CÁO TRUY THU 2 TUẦN (W39 VS W40) (BẬT TAB 14 DASHBOARD):",
        "content": """📍 1. BẢNG TỔNG HỢP TRUY THU VÙNG NAM TRUNG BỘ:
• Tổng số bản ghi (ticket): 2.424 bản ghi (giảm 1.652 đơn / -40,5% so với 4.076 bản ghi tuần W39).
• Số tiền phát sinh ban đầu: 433,1 Triệu VNĐ (W39: 317,3 Tr ₫, TĂNG MẠNH +115,8 Tr ₫ / +36,5%).
• Số tiền điều chỉnh giảm: -246,0 Triệu VNĐ.
• Số tiền thực tế CẦN TRUY THU: 187,1 Triệu VNĐ (W39: 312,1 Tr ₫, GIẢM -125,0 Tr ₫ / -40,1%).

📍 2. BẢNG 1: CƠ CẤU 3 LOẠI HÌNH VI PHẠM TRỌNG ĐIỂM:
• 1. Liên đới chiếm dụng: 56,8 Triệu VNĐ (4 đơn) ➔ Số tiền cực lớn trên số đơn rất nhỏ, tính chất đặc biệt nghiêm trọng!
• 2. Tick mất hàng: 41,2 Triệu VNĐ (53 đơn).
• 3. Mất / Thiếu / Tráo sản phẩm: 30,9 Triệu VNĐ (76 đơn).

📍 3. BẢNG 3: TOP AM CÓ SỐ TIỀN TRUY THU LỚN NHẤT:
• 1. Nguyễn Thanh Long: 51,2 Triệu VNĐ (72 ticket) ➔ Điểm nóng số 1 vùng!
• 2. Lê Văn Trường: 26,3 Triệu VNĐ (419 ticket tồn đọng — số lượng ticket khủng khiếp nhất!)
• 3. Trần Văn Phước: 22,9 Triệu VNĐ (288 ticket)
• 4. Huỳnh Thị Kim Chi: 21,3 Triệu VNĐ (110 ticket)

📍 4. BẢNG 4: DANH SÁCH BƯU CỤC VI PHẠM ĐẶC BIỆT NGHIÊM TRỌNG:
• (KHO) Bắc Cam Ranh: Cần thu 48,7 Triệu VNĐ (W39: 14,3 Tr ₫, TĂNG VỌT +34,4 Tr ₫ / +240,3%) ➔ AM Nguyễn Thanh Long (VỤ ÁN CHIẾM DỤNG TIỀN HÀNG COD!).
• (LDO) Tân Hà Lâm Hà: Cần thu 21,3 Triệu VNĐ (98 đơn) ➔ AM Huỳnh Thị Kim Chi.
• (DNO) Quảng Tín: Cần thu 13,0 Triệu VNĐ (72 đơn) ➔ AM Trần Văn Phước / Trương Quang Linh.
• (LDO) Đơn Dương: Cần thu 12,8 Triệu VNĐ (118 đơn) ➔ AM Lê Văn Trường.
• (DNO) Kiến Đức: Cần thu 9,1 Triệu VNĐ (196 đơn) ➔ AM Trần Văn Phước / Hồng Bích Nga.

🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 14 DASHBOARD TRUY THU):
"Kính thưa Ban Giám Đốc, bước sang Tab 14 Báo cáo Truy thu, đây là con số ảnh hưởng trực tiếp đến túi tiền và lợi nhuận của toàn vùng:
Nhìn vào tổng thể: Tuần W40 này số tiền cần truy thu thực tế đã giảm 40%, từ 312 triệu xuống còn 187,1 triệu đồng.
TUY NHIÊN, tôi cảnh báo toàn thể cuộc họp: Số tiền vi phạm phát sinh ban đầu lại TĂNG VỌT TỚI 36,5%, từ 317 triệu nhảy lên 433,1 triệu đồng!
Trong đó, nổi cộm lên nhóm vi phạm: 'Liên đới chiếm dụng' lên tới 56,8 triệu đồng!
Tôi yêu cầu anh Nguyễn Thanh Long ở Khánh Hòa đứng dậy giải trình trước Ban Giám Đốc:
Tại bưu cục Bắc Cam Ranh thuộc cụm quản lý của anh Long: Số tiền truy thu tuần trước là 14,3 triệu, tuần này đã nhảy vọt lên 48,7 TRIỆU ĐỒNG, tăng tới 240%!
Đây là vụ việc chiếm dụng tiền hàng COD có dấu hiệu vi phạm pháp luật hình sự rất rõ ràng! Nhân viên thu tiền của khách nhưng không nộp về quỹ mà chiếm đoạt. Trưởng bưu cục làm gì? AM quản lý giám sát kiểu gì mà để nhân sự ôm gần 50 triệu đồng của công ty biến mất?

Điểm nóng thứ hai là anh Lê Văn Trường ở Lâm Đồng:
Anh Trường đang để tồn đọng tới 419 TICKET TRUY THU với số tiền 26,3 triệu đồng!
Bưu cục Đơn Dương dính 12,8 triệu, bưu cục Xuân Hương dính 8,5 triệu!
419 ticket này là 419 vụ việc khiếu nại mất hàng, thiếu hàng, đền bù trôi nổi từ tuần này qua tuần khác mà anh Trường và Trưởng bưu cục không chịu xử lý đối soát dứt điểm!
Chị Huỳnh Thị Kim Chi ở Tân Hà Lâm Hà cũng đang dính 21,3 triệu đồng truy thu!

🎯 QUYẾT SÁCH HÀNH ĐỘNG & MỆNH LỆNH TÁC CHIẾN:
1. Vụ việc bưu cục Bắc Cam Ranh (48,7 triệu đồng): Giao đích danh AM Nguyễn Thanh Long trực tiếp phối hợp với bộ phận Pháp chế - Thanh tra vùng và Công an địa phương hoàn thiện hồ sơ khởi tố, thu hồi đủ 48,7 triệu đồng trước ngày 08/10!
2. Anh Lê Văn Trường và chị Huỳnh Thị Kim Chi: Trong vòng 72 giờ tới phải rà soát và đóng dứt điểm toàn bộ 419 ticket tồn đọng. Nhân viên nào làm mất hàng thì khấu trừ lương theo quy chế, bưu cục nào sai sót thì Trưởng bưu cục chịu trách nhiệm liên đới!
3. Phòng Tài chính vùng phong tỏa ngay hạn mức nợ của các bưu cục trên. Tuần W41 dứt khoát phải kéo tổng tiền cần truy thu xuống dưới 100 triệu đồng!
Bây giờ, em xin chuyển sang Tab 15 xem tình hình Kinh doanh & Khách hàng F30 ạ!\""""
    },

    # ----------------------------------------------------
    # TAB 15: KINH DOANH & KHÁCH HÀNG F30
    # ----------------------------------------------------
    {
        "id": "tab-commercial",
        "title": "🗣️ PHÂN TÍCH DOANH THU KINH DOANH & KHÁCH HÀNG MỚI F30 (BẬT TAB 15 DASHBOARD):",
        "content": """📍 1. BẢNG XẾP HẠNG DOANH THU THEO AM:
• Top AM dẫn đầu doanh thu kinh doanh:
  1. Phan Đình Duy (Khánh Hòa): Doanh thu cao nhất toàn vùng.
  2. Nguyễn Duy Long (Ninh Thuận): Đóng góp tỷ trọng lớn thứ 2.
  3. Nguyễn Ngọc Khánh (Bình Thuận): Doanh thu rất vững chắc.
• Điểm sụt giảm đáng báo động về doanh thu & khách hàng nhóm A:
  - Huỳnh Thúc Duân (Đắk Nông): Sản lượng sụt giảm nghiêm trọng (-1.608 đơn), doanh thu rơi tự do -29,1%, mất khách hàng lớn tại bưu cục Gia Nghĩa và bưu cục Nhân Cơ!
  - Thái Thị Thanh Thư (Khánh Hòa): Hụt 7.600 đơn tại Nha Trang, doanh thu giảm 11,8 Tr ₫ do shop lớn bị đối thủ cạnh tranh lôi kéo.

🎙️ LỜI THOẠI THUYẾT TRÌNH TỰ NHIÊN (KHI BẬT TAB 15 DASHBOARD KINH DOANH & F30):
"Kính thưa Ban Giám Đốc, chuyển sang Tab 15 là bức tranh Kinh doanh và phát triển khách hàng mới F30:
Vận hành và kinh doanh luôn là hai mặt của một đồng xu. Vận hành Last-mile tốt thì giữ chân được khách, vận hành kém thì khách hàng rời bỏ ngay lập tức!
Bên cạnh những điểm sáng như anh Phan Đình Duy ở Nha Trang hay anh Duy Long ở Ninh Thuận tiếp tục duy trì doanh thu hàng đầu vùng, thì có 2 điểm báo động:
Thứ nhất là khu vực của anh Huỳnh Thúc Duân ở Đắk Nông:
Doanh thu tuần W40 giảm sốc tới -29,1%, sản lượng bốc hơi hơn 1.600 đơn hàng! Hai bưu cục trọng điểm là Gia Nghĩa và Nhân Cơ để rơi rụng hàng loạt shop nhóm A!
Thứ hai là chị Thái Thị Thanh Thư ở Nha Trang: Hụt hơn 7.600 đơn sản lượng và giảm gần 12 triệu doanh thu.
Insight: Đối thủ cạnh tranh như SPX và J&T liên tục giảm giá và đưa nhân viên kinh doanh sang chèo kéo chủ shop. Khi chất lượng lấy hàng First-mile bị trễ, bưu tá không chịu quét QR, thái độ phục vụ gắt gỏng là chủ shop lập tức chuyển toàn bộ sản lượng sang hãng khác!

🎯 MỆNH LỆNH TÁC CHIẾN TUẦN W41:
• AM Duân và AM Thư phải đích thân cùng với chuyên viên Sales xuống làm việc trực tiếp với các chủ shop nhóm A bị sụt giảm đơn ngay trong tuần này.
• Cam kết khung giờ lấy hàng riêng biệt cho shop, lấy lại bằng được sản lượng đã mất trong tháng 10!
Bây giờ, em xin chuyển sang Tab 16 - Tab cuối cùng: Danh sách 13 Bưu cục bất ổn & Giao nhiệm vụ hiện trường tuần W41 ạ!\""""
    },

    # ----------------------------------------------------
    # TAB 16: 13 BƯU CỤC CẢNH BÁO BẤT ỔN & TỔNG KẾT
    # ----------------------------------------------------
    {
        "id": "tab-bc-canhbao",
        "title": "🗣️ DANH SÁCH 13 BƯU CỤC CẢNH BÁO ĐỎ & 5 NHIỆM VỤ ĐIỀU HÀNH HIỆN TRƯỜNG TUẦN W41 (BẬT TAB 16 DASHBOARD):",
        "content": """📍 1. DANH SÁCH 13 BƯU CỤC BẤT ỔN CẦN GIẢI TỎA KHẨN CẤP (W40):
• 1. (DNO) Quảng Tín: GTC 18,1% (Cảnh báo 100 ngày liên tiếp) | Backlog 1.224 đơn (tồn >5 ngày: 490 đơn) | ODR 74,9% | Truy thu 13,0 Tr ₫ (AM Trương Quang Linh / Trần Văn Phước).
• 2. (LDO) Đức Trọng 1: GTC 20,1% (Cảnh báo 84 ngày) | Backlog 1.223 đơn (tồn >5 ngày: 281 đơn) | Rớt LC 42 đơn (AM Trầm Hữu Tiến / Nguyễn Lê Nguyên Vũ).
• 3. (DNO) Kiến Đức: GTC 29,9% (Cảnh báo 80 ngày) | Backlog 1.035 đơn (AM Hồng Bích Nga).
• 4. (LDO) Xuân Hương - Đà Lạt: GTC 30,2% | Backlog 2.165 đơn (tồn >5 ngày: 310 đơn) | ODR 78,3% (AM Lê Văn Trường).
• 5. (KHO) Cam Linh: GTC 30,7% (Cảnh báo 108 ngày) | Backlog 2.433 đơn (AM Nguyễn Thanh Long).
• 6. (KHO) Tây Nha Trang: GTC 33,3% | Backlog 2.295 đơn (AM Phan Đình Duy).
• 7. (LDO) Lang Biang - Đà Lạt 1: GTC 36,5% (Cảnh báo 108 ngày) | Backlog 992 đơn | ODR 74,1% thấp nhất vùng (AM Lê Minh Lợi).
• 8. (LDO) Di Linh: GTC 40,0% | Backlog 1.970 đơn (tồn >5 ngày: 219 đơn) (AM Trầm Hữu Tiến).
• 9. (DNO) Tuy Đức: GTC 41,2% | Backlog 640 đơn (AM Trần Thị Nhung).
• 10. (LDO) Tân Hà Lâm Hà: GTC 44,5% | Backlog 798 đơn (AM Huỳnh Thị Kim Chi).
• 11. (DNO) Nhân Cơ: GTC 45,1% | Backlog 347 đơn | Doanh thu sụt giảm -29,1% (AM Huỳnh Thúc Duân).
• 12. (LDO) Đơn Dương: GTC 45,3% | Backlog 2.038 đơn | Dính truy thu 12,8 Tr ₫ (AM Lê Văn Trường / Phan Nguyễn Yến Nhi).
• 13. (LDO) Lâm Viên - Đà Lạt 2: GTC 46,2% | Backlog 860 đơn (AM Lê Văn Trường).

📍 2. ĐÁNH GIÁ CHUNG VÀ GIAO VIỆC CỤ THỂ 18 AM:
• 🟢 KHEN THƯỞNG:
  - AM Phan Đình Duy: Top 1 Doanh thu toàn vùng.
  - AM Nguyễn Duy Long: Đầu tàu sản lượng lớn nhất vùng (61,3k đơn) & Top GTC vững chắc (71,2%).
  - AM Cao Thị Thanh Thủy: Quán quân ODR toàn vùng (97,8%).
  - AM Nguyễn Ngọc Khánh: Quán quân GTC Full hàng (74,5%) & Top 1 ODR TikTok Shop (98,2%).
  - AM Thái Thị Thanh Thư: Quán quân Chuyển khoản QR (96,0%) & Á quân GTC (72,0%).
• 🔴 CẢNH BÁO ĐẶC BIỆT & GIAO NHIỆM VỤ HIỆN TRƯỜNG:
  - AM Nguyễn Thanh Long: Trực tiếp phối hợp Pháp chế thu hồi 48,7 Tr ₫ vụ việc chiếm dụng tại Bắc Cam Ranh trước ngày 08/10; dọn sạch backlog 2.433 đơn tại Cam Linh.
  - AM Huỳnh Thúc Duân: Xuống bưu cục Gia Nghĩa và Nhân Cơ cứu vãn sản lượng bốc hơi -1.608 đơn; ép tỷ lệ tiền mặt từ 81% xuống dưới 60%.
  - AM Lê Văn Trường: Trực tiếp xuống Đơn Dương và Xuân Hương xử lý dứt điểm 419 ticket truy thu (26,3 Tr ₫) và giải phóng 4.200 đơn backlog.
  - AM Lê Minh Lợi & Trương Quang Linh: Viết cam kết đưa ODR TikTok Shop từ 14% và 42% lên trên 80% trong tuần W41; dập tắt tình trạng bấm hoàn trả ảo >20%.
  - AM Trầm Hữu Tiến & Nguyễn Lê Nguyên Vũ: Giải tỏa dứt điểm tồn Aging tại Đức Trọng 1 và Di Linh trong 48 giờ.

📍 3. 5 TRỌNG TÂM HÀNH ĐỘNG TUẦN W41 TOÀN VÙNG NAM TRUNG BỘ:
• Trọng tâm 1: Duy trì kỷ luật Last-mile, giữ vững %GTC trên 60%, nâng tỷ lệ Gán Ca 2 từ 62,9% lên trên 85% để đạt Gán Tổng >90%.
• Trọng tâm 2: Quyết liệt thu hồi công nợ & truy thu: Xử lý dứt điểm 187,1 Tr ₫, phong tỏa và thu hồi vụ 48,7 Tr ₫ tại Bắc Cam Ranh.
• Trọng tâm 3: Cứu vãn ODR tại 4 điểm đáy Tây Nguyên: Nâng ODR TikTok Shop Lang Biang, Quảng Tín, Đơn Dương, Đức Trọng lên trên 80%.
• Trọng tâm 4: Tối ưu chi phí vận tải: Cắt giảm 30 chuyến xe KTC non tải <30% thùng để đưa %TLTĐ vượt mốc 55%.
• Trọng tâm 5: Chăm sóc giữ chân khách hàng nhóm A và phục hồi sản lượng kinh doanh tại Đắk Nông và Khánh Hòa.

🎙️ LỜI THOẠI KẾT LUẬN TOÀN BỘ BUỔI HỌP GIAO BAN:
"Kính thưa Ban Giám Đốc và toàn thể các anh chị em AM,
Để kết luận lại buổi họp giao ban tuần W40 hôm nay, chúng ta thấy rất rõ:
Toàn vùng Nam Trung Bộ đã chứng minh được khi toàn hệ thống đồng lòng siết kỷ luật, chúng ta hoàn toàn có thể đưa %GTC vượt 60% và ODR vượt 93%.
Tuy nhiên, những thành tích đó sẽ bị vô hiệu hóa nếu chúng ta để rò rỉ 187 triệu tiền truy thu, để xảy ra vụ việc chiếm dụng tiền hàng ở Bắc Cam Ranh, hay để mất khách hàng lớn tại Đắk Nông.
13 bưu cục cảnh báo đỏ trên màn hình chính là nơi quyết định chất lượng dịch vụ và uy tín thương hiệu của GHN tại Nam Trung Bộ trong tuần tới.
Giải tỏa xong 13 bưu cục này là toàn vùng Nam Trung Bộ sẽ đứng vững trong top đầu toàn quốc!
Em xin cảm ơn Ban Giám Đốc và các anh chị đã lắng nghe. Kính chúc toàn vùng Nam Trung Bộ tuần W41 vận hành an toàn, bứt phá doanh số và đạt chuẩn SLA toàn diện!\""""
    }
]

print(f"Loaded {len(TOPICS)} topics ready for generation.")

# ----------------------------------------------------
# 1. BUILD WORD DOCUMENT (.DOCX)
# ----------------------------------------------------
doc = docx.Document()

# Set margins to 0.75 in
for section in doc.sections:
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

# Document Header
title_p = doc.add_paragraph()
title_p.paragraph_format.space_before = Pt(0)
title_p.paragraph_format.space_after = Pt(4)
title_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_title = title_p.add_run("KỊCH BẢN THUYẾT TRÌNH BÁO CÁO GIAO BAN TUẦN W40 - 2026")
run_title.font.name = "Arial"
run_title.font.size = Pt(17)
run_title.font.bold = True
run_title.font.color.rgb = RGBColor(234, 88, 12)  # GHN Orange

sub_p = doc.add_paragraph()
sub_p.paragraph_format.space_before = Pt(0)
sub_p.paragraph_format.space_after = Pt(14)
sub_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_sub = sub_p.add_run("VÙNG NAM TRUNG BỘ | PHONG CÁCH 'SẾP CỦA AM' (GIÁM ĐỐC ĐIỀU HÀNH HIỆN TRƯỜNG CHỦ TRÌ)\nChu kỳ số liệu: 28/09/2026 – 04/10/2026 | Khớp 100% 16 Tab Dashboard")
run_sub.font.name = "Arial"
run_sub.font.size = Pt(10.5)
run_sub.font.italic = True
run_sub.font.color.rgb = RGBColor(100, 116, 139)

# Add each topic as a styled table block
for idx, topic in enumerate(TOPICS):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=160, bottom=160, left=200, right=200)
    set_cell_border(cell, 
                    left={"val": "single", "sz": "28", "color": "EA580C", "space": "0"},
                    top={"val": "single", "sz": "4", "color": "CBD5E1", "space": "0"},
                    bottom={"val": "single", "sz": "8", "color": "CBD5E1", "space": "0"},
                    right={"val": "single", "sz": "4", "color": "CBD5E1", "space": "0"})
    
    # Cell title
    cp = cell.paragraphs[0]
    cp.paragraph_format.space_before = Pt(0)
    cp.paragraph_format.space_after = Pt(6)
    r_h = cp.add_run(f"TAB {idx+1}: {topic['title']}")
    r_h.font.name = "Arial"
    r_h.font.size = Pt(12)
    r_h.font.bold = True
    r_h.font.color.rgb = RGBColor(15, 23, 42)
    
    # Cell content
    lines = topic['content'].split('\n')
    for line in lines:
        lp = cell.add_paragraph()
        lp.paragraph_format.space_before = Pt(1)
        lp.paragraph_format.space_after = Pt(2)
        lp.paragraph_format.line_spacing = 1.15
        
        # Color coding
        lr = lp.add_run(line)
        lr.font.name = "Arial"
        lr.font.size = Pt(9.5)
        
        if line.startswith("📍") or line.startswith("🎯") or line.startswith("🔍") or line.startswith("⚠️"):
            lr.font.bold = True
            lr.font.size = Pt(10)
            lr.font.color.rgb = RGBColor(15, 23, 42)
            set_cell_background(cell, "F1F5F9")
        elif line.startswith("🎙️ LỜI THOẠI") or line.startswith("\"") or line.endswith("\""):
            lr.font.italic = True
            lr.font.color.rgb = RGBColor(15, 23, 42)
        elif line.startswith("• 🟢"):
            lr.font.color.rgb = RGBColor(22, 101, 52)
            lr.font.bold = True
        elif line.startswith("• 🔴") or "BÁO ĐỘNG ĐỎ" in line or "CẢNH BÁO" in line:
            lr.font.color.rgb = RGBColor(185, 28, 28)
            lr.font.bold = True
        else:
            lr.font.color.rgb = RGBColor(51, 65, 85)
            
    # Add spacing paragraph after table
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(8)

# Save DOCX files with lock handling
target_docx = r"c:\Users\lap4all\Desktop\New folder\KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.docx"
saved_src = None

# Save to Downloads first (where KICH_BAN_W40_MOI_NHAT.docx is usually not locked)
dl_main = r"C:\Users\lap4all\Downloads\KICH_BAN_W40_MOI_NHAT.docx"
try:
    doc.save(dl_main)
    saved_src = dl_main
    print(f"Saved docx to Downloads: {dl_main}")
except Exception as e:
    print(f"Notice: Could not save to {dl_main}: {e}")

# Save to workspace target
try:
    doc.save(target_docx)
    saved_src = target_docx
    print(f"Saved workspace docx: {target_docx}")
except Exception as e:
    fallback_ws = r"c:\Users\lap4all\Desktop\New folder\KICH_BAN_THUYET_TRINH_W40_MOI.docx"
    doc.save(fallback_ws)
    if not saved_src:
        saved_src = fallback_ws
    print(f"Notice: {target_docx} is open in Word, saved to fallback: {fallback_ws}")

# Also save to CHUAN in Downloads
try:
    doc.save(r"C:\Users\lap4all\Downloads\KICH_BAN_THUYET_TRINH_W40_CHUAN.docx")
    print(r"Saved docx to C:\Users\lap4all\Downloads\KICH_BAN_THUYET_TRINH_W40_CHUAN.docx")
except Exception as e:
    print(f"Notice: Could not save to KICH_BAN_THUYET_TRINH_W40_CHUAN.docx: {e}")

# Try to save to kịch bản.docx if closed
try:
    doc.save(r"C:\Users\lap4all\Downloads\kịch bản.docx")
    print(r"Successfully updated C:\Users\lap4all\Downloads\kịch bản.docx")
except Exception as e:
    print(rf"Notice: C:\Users\lap4all\Downloads\kịch bản.docx is open in Word: {e}")

# ----------------------------------------------------
# 2. BUILD MARKDOWN (.MD)
# ----------------------------------------------------
md_lines = [
    "# KỊCH BẢN THUYẾT TRÌNH BÁO CÁO GIAO BAN TUẦN W40 - VÙNG NAM TRUNG BỘ",
    "**Phong Cách:** 'Sếp của AM' (Giám đốc Điều hành Vùng chủ trì cuộc họp)",
    "**Chu kỳ dữ liệu:** 28/09/2026 – 04/10/2026 | **Đồng bộ 100%:** 16 Tab Dashboard Vận Hành NTB",
    "",
    "---",
    ""
]

for idx, topic in enumerate(TOPICS):
    md_lines.append(f"## TAB {idx+1}: {topic['title']}")
    md_lines.append("")
    md_lines.append(topic['content'])
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")

target_md = r"c:\Users\lap4all\Desktop\New folder\KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.md"
with open(target_md, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))
print(f"Saved workspace md: {target_md}")

# ----------------------------------------------------
# 3. BUILD HTML (.HTML)
# ----------------------------------------------------
html_parts = [
    """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KỊCH BẢN GIAO BAN TUẦN W40 - SẾP CỦA AM CHỦ TRÌ</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root {
  --primary: #ea580c;
  --primary-dark: #c2410c;
  --bg: #0f172a;
  --card-bg: #1e293b;
  --card-border: #334155;
  --text: #f8fafc;
  --text-muted: #94a3b8;
  --success: #22c55e;
  --danger: #ef4444;
  --warning: #f59e0b;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; padding: 30px 20px; }
.container { max-width: 1200px; margin: 0 auto; }
header { text-align: center; margin-bottom: 35px; border-bottom: 2px solid var(--card-border); padding-bottom: 20px; }
h1 { font-size: 26px; font-weight: 800; color: var(--primary); text-transform: uppercase; letter-spacing: 0.5px; }
.subtitle { font-size: 14px; color: var(--text-muted); margin-top: 6px; }
.badge { display: inline-block; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 700; background: rgba(234,88,12,0.15); color: var(--primary); margin-top: 10px; }
.topic-card { background: var(--card-bg); border: 1px solid var(--card-border); border-left: 5px solid var(--primary); border-radius: 10px; padding: 22px; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
.topic-title { font-size: 18px; font-weight: 700; color: #fff; margin-bottom: 14px; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid var(--card-border); padding-bottom: 10px; }
.topic-body { font-size: 14px; color: #cbd5e1; white-space: pre-wrap; font-family: inherit; }
.topic-body strong { color: #fff; }
.highlight-green { color: #4ade80; font-weight: 600; }
.highlight-red { color: #f87171; font-weight: 600; }
</style>
</head>
<body>
<div class="container">
<header>
  <h1>KỊCH BẢN THUYẾT TRÌNH BÁO CÁO GIAO BAN W40 - VÙNG NAM TRUNG BỘ</h1>
  <div class="subtitle">PHONG CÁCH 'SẾP CỦA AM' (GIÁM ĐỐC VẬN HÀNH VÙNG CHỦ TRÌ) | CHU KỲ SỐ LIỆU: 28/09 – 04/10/2026</div>
  <div class="badge">ĐỒNG BỘ 100% 16 TAB DASHBOARD VẬN HÀNH</div>
</header>
"""
]

for idx, topic in enumerate(TOPICS):
    c_escaped = topic['content'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    html_parts.append(f"""
<div class="topic-card" id="{topic['id']}">
  <div class="topic-title"><span>TAB {idx+1}:</span> {topic['title']}</div>
  <div class="topic-body">{c_escaped}</div>
</div>
""")

html_parts.append("""
</div>
</body>
</html>
""")

target_html = r"c:\Users\lap4all\Desktop\New folder\KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.html"
with open(target_html, "w", encoding="utf-8") as f:
    f.write("\n".join(html_parts))
print(f"Saved workspace html: {target_html}")
print("ALL GENERATIONS COMPLETED SUCCESSFULLY!")
