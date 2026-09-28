import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

sys.stdout.reconfigure(encoding='utf-8')

def update_table_15(doc_path):
    doc = docx.Document(doc_path)
    if len(doc.tables) <= 15:
        print(f"File {doc_path} has fewer than 16 tables, skipping.")
        return
    
    cell = doc.tables[15].rows[0].cells[0]
    
    # Clear existing paragraphs in cell
    p_first = cell.paragraphs[0]
    p_first.text = ""
    # Remove remaining paragraphs
    for p in cell.paragraphs[1:]:
        p._p.getparent().remove(p._p)
        
    # Title
    p_first.paragraph_format.space_before = Pt(2)
    p_first.paragraph_format.space_after = Pt(4)
    r_t = p_first.add_run("🗣️ KỊCH BẢN THUYẾT TRÌNH: THEO DÕI & XỬ LÝ NHÓM BƯU CỤC CẢNH BÁO BẤT ỔN (SO SÁNH W38 VS W39):")
    r_t.bold = True
    r_t.font.name = 'Arial'
    r_t.font.size = Pt(11)
    r_t.font.color.rgb = RGBColor(194, 65, 12)
    
    speech_blocks = [
        '"Kính thưa Ban Giám Đốc, các anh chị Giám đốc Khối và toàn thể đội ngũ Quản lý Vận hành (AM) vùng Nam Trung Bộ.',
        'Sau đây, em xin phép báo cáo vào chuyên đề trọng điểm thứ 15: Theo dõi và xử lý nhóm Bưu cục cảnh báo bất ổn (%GTC < 45% hoặc giảm sâu dưới 70% mốc tốt nhất lịch sử) — đặt trên hệ quy chiếu so sánh đối chiếu giữa Tuần W38 và Tuần W39.',
        'Thưa Ban Giám Đốc, nếu nhìn vào bức tranh chung toàn vùng, %GTC của chúng ta vẫn giữ được nhịp ổn định. Tuy nhiên, khi bóc tách xuống cấp độ bưu cục cơ sở, tuần W39 ghi nhận sự dịch chuyển rủi ro rõ rệt mà Ban Điều Hành cần báo cáo thẳng thắn:',
        '• 1. TỔNG QUAN BIẾN ĐỘNG SỐ LƯỢNG (TĂNG TỪ 13 LÊN 15 BƯU CỤC): Trong tuần W38, toàn vùng ghi nhận 13 bưu cục cảnh báo. Sang tuần W39, danh sách tăng lên 15 bưu cục (+2 BCs). Trong đó có 4 bưu cục nỗ lực thoát bể thành công, 6 bưu cục mới rơi vào diện báo động, và 9 bưu cục đang kẹt dai dẳng cả 2 tuần liên tiếp.',
        '• 2. TUYÊN DƯƠNG 4 BƯU CỤC ĐÃ GIẢI TỎA & THOÁT CẢNH BÁO THÀNH CÔNG: Xuân Hương - Đà Lạt (AM Lê Văn Trường), Cam Linh (AM Phan Đình Duy), Nhân Cơ (AM Đỗ Duy Khang), và Tây Nha Trang (AM Hồng Bích Nga). Các bưu cục này đã tối ưu vượt bậc ca phát sáng để kéo %GTC vượt ngưỡng an toàn.',
        '• 3. BÁO ĐỘNG ĐỎ 6 BƯU CỤC MỚI LỌT VÀO DIỆN CẢNH BÁO W39: BC D\'Ran (Lâm Đồng - 36.86%, cảnh báo 6 ngày), BC Lang Biang 2 (Lâm Đồng - 35.80%, cảnh báo 6 ngày), BC Trường Xuân (Đắk Nông - 38.22%, cảnh báo 8 ngày), BC Đông Gia Nghĩa (Đắk Nông - 44.89%), BC Bắc Cam Ranh (Khánh Hòa - 44.68%, tích lũy 31 ngày cảnh báo), và BC Phú Quý (Bình Thuận - 50.84%, rơi sâu dưới 70% mốc đỉnh lịch sử 88.55%).',
        '• 4. ĐIỂM NÓNG MÃN TÍNH 9 BƯU CỤC KẸT DAI DẲNG CẢ 2 TUẦN LIÊN TIẾP: Nghiêm trọng nhất là BC Lâm Viên - Đà Lạt 2 từ 46.2% ở W38 rơi tự do xuống 19.55% trong W39 (nặng nhất toàn mạng, liệt ca chiều); BC Đức Trọng 1 (23.78%) và BC Đơn Dương (29.01%, giảm -16.3%p); BC Quảng Tín (26.17%, tích lũy >100 ngày cảnh báo). Cùng 5 BC: Lang Biang 1 (30.6%), Kiến Đức (32.5%), Tân Hà Lâm Hà (36.8%), Tuy Đức (38.5%) và Di Linh (40.6%).',
        '• 5. KẾ HOẠCH HÀNH ĐỘNG CẤP BÁCH TUẦN W40 (3 MỆNH LỆNH TÁC CHIẾN):',
        '   1. Áp dụng cơ chế Điều tiết hàng (Cap Volume): Tạm thời giảm 25% hạn mức chia chọn hàng về trong 3 ngày đầu tuần tại BC Lâm Viên 2 và Quảng Tín để bưu tá tập trung quét sạch tồn kho và aging >5 ngày.',
        '   2. Tái cơ cấu bưu tá ca sáng: Điều chuyển chi viện 4 bưu tá cứng từ cụm Xuân Hương và Gia Nghĩa sang phát lượt 1 trước 11h00 trưa tại Lâm Viên 2 và Đức Trọng 1.',
        '   3. Mục tiêu cam kết W40: Quyết tâm kéo tối thiểu 5 bưu cục thoát khỏi danh sách cảnh báo, giảm tổng số lượng toàn vùng từ 15 BC về dưới 10 BC trong tuần tiếp theo.',
        'Em xin kết thúc phần báo cáo bưu cục cảnh báo. Kính mời Ban Giám Đốc cho ý kiến chỉ đạo ạ!"',
        '🔍 INSIGHT BẢN CHẤT & GỐC RỄ NGUYÊN NHÂN:',
        '• Tồn đọng và rớt %GTC ở nhóm 9 bưu cục mãn tính không phải do thiếu xe hay thiếu hàng, mà chủ yếu do thắt nút cổ chai ở tỷ lệ gán Ca 2 buổi trưa (chỉ đạt 65-72%) và thiếu bưu tá có kinh nghiệm tại các địa bàn đồi núi dốc xa.',
        '⚠️ CẢNH BÁO ĐỎ & NGUY CƠ TIỀM ẨN:',
        '• Nếu không áp dụng Cap Volume và chi viện khẩn cấp, nguy cơ vỡ tải dây chuyền tại cụm Đà Lạt - Đơn Dương - Đức Trọng trong đợt sale đầu tháng 10 là rất cao.',
        '🎯 QUYẾT SÁCH HÀNH ĐỘNG & MỆNH LỆNH TÁC CHIẾN TUẦN W40:',
        '• Thiết lập đường dây nóng giám sát 15 bưu cục này 2 lần/ngày (11h30 và 17h30) trên nhóm chỉ huy Vận hành NTB để can thiệp kịp thời trước khi đơn hàng chuyển sang trạng thái quá hạn SLA.'
    ]
    
    for text in speech_blocks:
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.2
        
        if text.startswith('•') or text.startswith('   1.') or text.startswith('   2.') or text.startswith('   3.'):
            if ':' in text:
                parts = text.split(':', 1)
                r_pre = p.add_run(parts[0] + ":")
                r_pre.bold = True
                r_pre.font.name = 'Arial'
                r_pre.font.size = Pt(9.5)
                r_pre.font.color.rgb = RGBColor(15, 23, 42)
                r_post = p.add_run(parts[1])
                r_post.font.name = 'Arial'
                r_post.font.size = Pt(9.5)
                r_post.font.color.rgb = RGBColor(51, 65, 85)
            else:
                r = p.add_run(text)
                r.font.name = 'Arial'
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(30, 41, 59)
        elif text.startswith('🔍') or text.startswith('⚠️') or text.startswith('🎯'):
            r = p.add_run(text)
            r.bold = True
            r.font.name = 'Arial'
            r.font.size = Pt(10)
            r.font.color.rgb = RGBColor(194, 65, 12) if '🎯' in text or '⚠️' in text else RGBColor(15, 76, 129)
        elif text.startswith('"') or text.endswith('"'):
            r = p.add_run(text)
            r.italic = True
            r.font.name = 'Arial'
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(15, 23, 42)
        else:
            r = p.add_run(text)
            r.font.name = 'Arial'
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(30, 41, 59)
            
    doc.save(doc_path)
    print(f"Updated {doc_path} successfully!")

targets = [
    'KICH_BAN_THUYET_TRINH_MOI_NHAT.docx',
    'KICH_BAN_THUYET_TRINH_W39_INSIGHT_CHUYEN_SAU.docx',
    'KICH_BAN_THUYET_TRINH_W39_INSIGHT_CHUYEN_SAU_CHINH_SUA.docx',
    'KICH_BAN_THUYET_TRINH_W39_NAM_TRUNG_BO.docx'
]

for t in targets:
    update_table_15(t)
