import docx
import sys
sys.stdout.reconfigure(encoding='utf-8')

table13_content = """🗣️ PHÂN TÍCH BÁO CÁO TRUY THU VẬN HÀNH TOÀN VÙNG (306,9 TRIỆU ₫) — ĐỐI SOÁT CHUẨN XÁC W38 vs W39:

📍 1. BẢNG TỔNG QUAN TRUY THU TOÀN VÙNG (W38 vs W39):
• Tổng số Ticket / Đơn vi phạm: Tuần W39 ghi nhận 4.013 ticket, tăng +939 ticket (+30,5%) so với tuần W38 (3.074 ticket). 
  (Đính chính chuẩn xác: Tuần W38 thực tế có 3.074 ticket chứ không phải 135 ticket như lỗi hiển thị thiếu ngày trước đây).
• Tổng số tiền ban đầu phát sinh: Tuần W39 đạt 306.859.209 đồng (306,9 Tr ₫), GIẢM MẠNH -368,8 Tr ₫ (-54,6% WoW) so với W38 (675,6 Tr ₫).
• Tổng số tiền cần truy thu: Tuần W39 là 306,9 Tr ₫, GIẢM -31,1 Tr ₫ (-9,2% WoW) so với số tiền cần thu của W38 (337,9 Tr ₫).

📍 2. BÓC TÁCH THEO 5 TỈNH THÀNH (W38 vs W39):
• Top 1 - Lâm Đồng: Cần thu 193,87 Tr ₫ (chiếm 63,2% toàn vùng | 1.585 ticket), tăng +81,0 Tr ₫ WoW so với W38 (112,9 Tr ₫) ➔ Ổ dịch truy thu lớn nhất toàn vùng, tập trung tại Tân Hà Lâm Hà, Bảo Lâm 1 và Đơn Dương!
• Top 2 - Đắk Nông: Cần thu 50,53 Tr ₫ (chiếm 16,5% | 1.217 ticket), giảm mạnh -27,1 Tr ₫ WoW từ mức 77,6 Tr ₫ của W38.
• Top 3 - Khánh Hòa: Cần thu 37,80 Tr ₫ (chiếm 12,3% | 657 ticket), giảm mạnh -66,6 Tr ₫ WoW so với W38 (104,4 Tr ₫).
• Top 4 - Bình Thuận: Cần thu 4,65 Tr ₫ (142 ticket), giảm -2,7 Tr ₫ so với W38 (7,3 Tr ₫).
• Top 5 - Ninh Thuận: Cần thu vỏn vẹn 132.659 đồng (87 ticket) ➔ Kiểm soát chuẩn xác tuyệt đối, gần như không phát sinh truy thu!

👤 3. TOP AM BỊ TRUY THU CAO NHẤT (W39 vs W38):
🔴 NHÓM BÁO ĐỘNG ĐỎ (≥ 40 TRIỆU ₫):
  1. AM Huỳnh Thị Kim Chi: 58,28 Tr ₫ (177 ticket), tăng +9,0 Tr ₫ WoW (+18,4%). Tâm điểm là bưu cục (LDO) Tân Hà Lâm Hà bị phạt tới 46,8 Tr ₫!
  2. AM Hồng Bích Nga: 50,73 Tr ₫ (108 ticket), tăng vọt +46,6 Tr ₫ WoW (+1135%). Tâm điểm bưu cục (LDO) Bảo Lâm 1 truy thu 50,6 Tr ₫.
  3. AM Lê Văn Trường: 50,57 Tr ₫ (722 ticket), tăng +12,0 Tr ₫ WoW (+31,2%). Tâm điểm bưu cục (LDO) Đơn Dương truy thu 21,8 Tr ₫.
🟡 NHÓM CẦN KIỂM SOÁT (15 - 40 TRIỆU ₫):
  4. AM Trần Văn Phước: 27,07 Tr ₫ (712 ticket), giảm mạnh -42,1 Tr ₫ (-60,8% WoW từ 69,1 Tr ₫). Điểm nóng (DNO) Quảng Tín truy thu 15,6 Tr ₫.
  5. AM Trầm Hữu Tiến: 24,71 Tr ₫ (439 ticket), tăng +6,4 Tr ₫ WoW. Điểm nóng (LDO) Di Linh truy thu 15,8 Tr ₫.
  6. AM Huỳnh Thúc Duân: 16,45 Tr ₫ (415 ticket), tăng +11,2 Tr ₫ WoW. Điểm nóng (DNO) ĐL Nam Gia Nghĩa 2 truy thu 14,9 Tr ₫.

🔍 4. BÓC TÁCH THEO LOẠI TRUY THU TRỌNG ĐIỂM:
  1. Backlog Giao Hàng: 742 đơn vi phạm, số tiền phạt lên tới 109,2 Tr ₫ (chiếm 35,6% tổng số tiền). Tăng +71,5 Tr ₫ so với W38 (37,7 Tr ₫).
  2. Backlog Luân Chuyển Trả: 559 đơn, phạt 53,6 Tr ₫ (chiếm 17,5%), tăng +43,3 Tr ₫ so với W38.
  3. Đơn hàng hư hỏng: 254 đơn, phạt 25,5 Tr ₫.
  4. Backlog Luân Chuyển Giao: 179 đơn, phạt 24,9 Tr ₫.
  5. Chiếm dụng: 3 đơn, phạt 19,0 Tr ₫.
  6. Backlog Bắn Kiểm Trả: 352 đơn, phạt 14,9 Tr ₫.

🎯 5. CHỈ ĐẠO HÀNH ĐỘNG DỨT KHOÁT:
• Chị Chi, chị Nga, anh Trường: Trực tiếp làm việc với Vận hành Hội quán và Trưởng bưu cục Tân Hà Lâm Hà, Bảo Lâm 1, Đơn Dương. Rà soát lại từng ticket Backlog bị phạt. Trường hợp hệ thống quét phạt oan do lỗi nghẽn quét phải làm đơn khiếu nại hoàn tiền ngay; trường hợp do bưu cục om hàng không xuất tuyến, truy cứu trách nhiệm vật chất cá nhân, không để công ty chịu khoản phạt này."""

for fn in ['KICH_BAN_THUYET_TRINH_MOI_NHAT.docx', 'KICH_BAN_THUYET_TRINH_W39_INSIGHT_CHUYEN_SAU.docx']:
    try:
        doc = docx.Document(fn)
        if len(doc.tables) > 13:
            t13 = doc.tables[13]
            t13.rows[0].cells[0].text = table13_content
            doc.save(fn)
            print(f"Updated Table 13 in {fn} successfully.")
        else:
            print(f"File {fn} has less than 14 tables.")
    except Exception as e:
        print(f"Error updating {fn}: {e}")
