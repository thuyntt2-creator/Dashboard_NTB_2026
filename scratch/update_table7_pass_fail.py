import docx, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

src = 'KICH_BAN_THUYET_TRINH_MOI_NHAT.docx'
doc = docx.Document(src)

# TABLE 7: MỤC VIII - PHÂN ĐỊNH RÕ RÀNG AM ĐẠT VÀ KHÔNG ĐẠT KPI OPR TTS (≥80.0%)
cell7 = doc.tables[7].rows[0].cells[0]
for p in cell7.paragraphs[1:]:
    p._p.getparent().remove(p._p)

cell7.paragraphs[0].text = "🗣️ HIỆU SUẤT %OPR TIKTOK SHOP — PHÂN ĐỊNH AM ĐẠT & KHÔNG ĐẠT KPI (TARGET SLA ≥ 80.0%) W39 vs W38:"

sec8 = [
    '📍 1. BẢNG TỔNG QUAN %OPR TIKTOK SHOP 5 TỈNH THÀNH (W39 vs W38):',
    '• Top 1 - Ninh Thuận: OPR Tổng đạt 91,13% (+0,78%p) | Ca ngày: 96,49% | Ca đêm: 77,46% ➔ Đạt chuẩn xanh xuất sắc!',
    '• Top 2 - Khánh Hòa: OPR Tổng đạt 83,22% (-2,09%p) | Ca ngày: 92,95% | Ca đêm: 74,01% ➔ Đạt chuẩn xanh.',
    '• Top 3 - Lâm Đồng: OPR Tổng đạt 75,39% (+5,41%p) | Ca ngày: 87,74% | Ca đêm: 47,01% ➔ KHÔNG ĐẠT KPI 80%.',
    '• Top 4 - Bình Thuận: OPR Tổng đạt 74,36% (-13,69%p) | Ca ngày: 88,70% | Ca đêm: 52,37% (-30,3%p) ➔ KHÔNG ĐẠT KPI 80%.',
    '• Top 5 - Đắk Nông: OPR Tổng đạt 50,00% | Ca ngày: 88,50% | Ca đêm: 0,57% ➔ KHÔNG ĐẠT KPI 80% (Ca đêm gần như tê liệt).',
    '➔ TOÀN VÙNG W39: OPR Tổng đạt 80,60% (vừa chạm chuẩn SLA ≥80.0%) | Ca ngày giữ phong độ cao 91,2% ➔ Ca đêm rớt sâu về 58,4% (chênh lệch gãy cánh tới 32,8%p).',
    '',
    '🎙️ LỜI THOẠI THUYẾT TRÌNH %OPR TIKTOK SHOP (CHỈ RÕ ĐÍCH DANH AM ĐẠT & KHÔNG ĐẠT KPI):',
    '\"Dạ tiếp theo em xin phép chuyển qua Tab 8 là chỉ số %OPR TikTok Shop (tỷ lệ xử lý đơn hàng sàn đúng quy trình cam kết, mục tiêu KPI của công ty yêu cầu phải đạt từ 80.0% trở lên):',
    '',
    'Nhìn vào tỷ lệ toàn vùng tuần W39, OPR Tổng của mình đạt 80.6%, tức là vừa đủ chạm ngưỡng cam kết. Tuy nhiên, khi đi sâu vào từng Quản lý Vận hành (AM), toàn mạng bị phân hóa thành 2 thái cực rất rõ rệt: 8 AM ĐẠT CHUẨN và 9 AM KHÔNG ĐẠT CHUẨN KPI:',
    '',
    '🏆 1. TUYÊN DƯƠNG 8 AM HOÀN THÀNH XUẤT SẮC KPI (OPR TỔNG ≥ 80.0%):',
    '• Dẫn đầu toàn mạng là anh Phan Đình Duy: OPR đạt tới 96.8% (tăng vọt +14.0%p WoW, ca ngày đạt 99.7% và ca đêm đạt 86.1%).',
    '• Anh Nguyễn Lê Nguyên Vũ: Đạt 92.4% (ca ngày đạt 98.8%).',
    '• Hai đầu tàu gánh tải lớn nhất mạng tiếp tục giữ chuẩn rất tốt: Anh Nguyễn Duy Long đạt 90.7% (trên khối lượng lớn 1.756 đơn, ca ngày đạt 96.1%); và chị Thái Thị Thanh Thư đạt 90.2% (trên sản lượng lớn nhất mạng hơn 2.100 đơn, ca ngày 94.5% và ca đêm vẫn giữ được hơn 87%).',
    '• Cùng 4 AM đạt chuẩn xanh: Anh Nguyễn Thanh Long đạt 87.4% (+9.6%p); chị Nguyễn Thị Tuyết Thơ có bước nhảy vọt mạnh nhất vùng (+28.9%p, kéo từ 56% lên 85.0%); chị Hồng Bích Nga đạt 82.3%; và chị Cao Thị Thanh Thủy đạt 82.1%.',
    '',
    '🚨 2. ĐIỂM DANH 9 AM KHÔNG ĐẠT KPI (OPR TỔNG < 80.0% — CHỦ YẾU DO GÃY CÁNH CA ĐÊM):',
    'Trong 9 anh chị không đạt KPI tuần này, nguyên nhân 100% là do ca đêm bị buông lỏng:',
    '',
    '• Nhóm 4 AM tiệm cận chuẩn (72% – 78%):',
    '- Anh Nguyễn Đỗ Minh Nghĩa đạt 78.1% (ca ngày rất tốt 99.3%, nhưng ca đêm bị rớt xuống 25.4%).',
    '- Anh Nguyễn Ngọc Khánh đạt 76.1% (giảm -9.0%p so với tuần trước, ca đêm rơi về 59.0%).',
    '- Chị Huỳnh Thị Kim Chi đạt 75.0% và anh Huỳnh Thúc Duân đạt 72.8% (cả 2 anh chị ca đêm đều đạt 0%).',
    '',
    '• Nhóm 5 AM báo động đỏ rớt sâu dưới 70% (kéo lùi toàn bộ chỉ số vùng):',
    '- Anh Lê Thanh Nhựt: Rớt sâu -17.0%p WoW, OPR Tổng chỉ còn 67.6% (trên khối lượng lớn hơn 1.400 đơn, ca đêm chỉ đạt 36.6%).',
    '- Anh Nguyễn Hoàng Phi: Rớt sâu -18.7%p WoW, OPR Tổng chỉ còn 59.3% (trên 851 đơn, ca đêm chỉ đạt 34.5%).',
    '- Anh Lê Văn Trường: OPR Tổng chỉ đạt 53.5% (ca đêm chỉ đạt 24.0% trên 572 đơn).',
    '- Anh Lê Minh Lợi: OPR Tổng đạt 50.0% (ca đêm 0%).',
    '- Đội sổ toàn mạng là chị Trần Thị Nhung: OPR Tổng tuần này rớt thảm hại xuống chỉ còn 25.3% (giảm -13.4%p, ca đêm chạm đáy chỉ có 0.74% — tức là ca đêm gần như không quét xử lý đơn nào!).',
    '',
    '🎯 Về nhiệm vụ tác chiến cho 9 AM chưa đạt KPI tuần W40:',
    '• Em đề nghị 9 anh chị chưa đạt KPI (đặc biệt là chị Nhung, anh Trường, anh Phi, anh Nhựt, anh Duân, anh Nghĩa): Bắt buộc phải sắp xếp lại nhân sự trực ca đêm tại bưu cục, đẩy nhanh tốc độ quét nhập và xử lý luồng đơn sàn trước 22h00 đêm, tuyệt đối không để dồn ứ đơn sang sáng hôm sau.',
    '• Mục tiêu tuần W40: Toàn bộ 18 AM phải đưa OPR Tổng vượt mốc 80.0% cam kết Sếp giao.\"'
]

for line in sec8:
    p = cell7.add_paragraph()
    p.text = line

doc.save(src)
for c in ['KICH_BAN_THUYET_TRINH_W39_INSIGHT_CHUYEN_SAU.docx', 'KICH_BAN_THUYET_TRINH_W39_NAM_TRUNG_BO.docx']:
    shutil.copyfile(src, c)

print('Updated Table 7 correctly with clear PASS/FAIL KPI classification!')
