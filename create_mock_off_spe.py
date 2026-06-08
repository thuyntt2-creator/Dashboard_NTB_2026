import pandas as pd

# Mock data based on the screenshot
data = [
    {
        "Tỉnh": "Đắk Nông",
        "Quận/huyện": "Huyện Đắk R'lấp",
        "Phường/xã cần tắt": "Thị trấn Kiến Đức",
        "Bưu Cục": "Bưu Cục 01 Nguyễn Tất Thành-Đắk R'lấp-Đắk Nông",
        "Kết quả (KA) update": "DUYỆT",
        "% Cap Down (KA)": 1.0,
        "Thời gian tắt (KA)": "01-06-2026",
        "Thời gian mở (KA)": "15-06-2026",
        "Note": "Tuyến Đang OFF - Mở lại ngày: 15/06/2026"
    },
    {
        "Tỉnh": "Đắk Nông",
        "Quận/huyện": "Huyện Đắk R'lấp",
        "Phường/xã cần tắt": "Xã Đạo Nghĩa",
        "Bưu Cục": "Bưu Cục 01 Nguyễn Tất Thành-Đắk R'lấp-Đắk Nông",
        "Kết quả (KA) update": "DUYỆT",
        "% Cap Down (KA)": 1.0,
        "Thời gian tắt (KA)": "01-06-2026",
        "Thời gian mở (KA)": "15-06-2026",
        "Note": "Tuyến Đang OFF - Mở lại ngày: 15/06/2026"
    },
    {
        "Tỉnh": "Đắk Nông",
        "Quận/huyện": "Huyện Đắk R'lấp",
        "Phường/xã cần tắt": "Xã Kiến Thành",
        "Bưu Cục": "Bưu Cục 01 Nguyễn Tất Thành-Đắk R'lấp-Đắk Nông",
        "Kết quả (KA) update": "DUYỆT",
        "% Cap Down (KA)": 1.0,
        "Thời gian tắt (KA)": "01-06-2026",
        "Thời gian mở (KA)": "15-06-2026",
        "Note": "Tuyến Đang OFF - Mở lại ngày: 15/06/2026"
    },
    {
        "Tỉnh": "Khánh Hòa",
        "Quận/huyện": "Thành phố Nha Trang",
        "Phường/xã cần tắt": "Phường Phước Tiến",
        "Bưu Cục": "Bưu Cục 06 Lê Hồng Phong-TP.Nha Trang-Khánh Hòa",
        "Kết quả (KA) update": None, # Waiting for approval
        "% Cap Down (KA)": None,
        "Thời gian tắt (KA)": None,
        "Thời gian mở (KA)": None,
        "Note": "Đang đợi duyệt"
    },
    {
        "Tỉnh": "Khánh Hòa",
        "Quận/huyện": "Thành phố Nha Trang",
        "Phường/xã cần tắt": "Phường Vạn Thạnh",
        "Bưu Cục": "Bưu Cục 06 Lê Hồng Phong-TP.Nha Trang-Khánh Hòa",
        "Kết quả (KA) update": None, # Waiting for approval
        "% Cap Down (KA)": None,
        "Thời gian tắt (KA)": None,
        "Thời gian mở (KA)": None,
        "Note": "Đang đợi duyệt"
    },
    {
        "Tỉnh": "Lâm Đồng",
        "Quận/huyện": "Huyện Di Linh",
        "Phường/xã cần tắt": "Thị trấn Di Linh",
        "Bưu Cục": "Bưu Cục 1322 Hùng Vương-Di Linh-Lâm Đồng",
        "Kết quả (KA) update": "DUYỆT",
        "% Cap Down (KA)": 1.0,
        "Thời gian tắt (KA)": "27-05-2026",
        "Thời gian mở (KA)": "10-06-2026",
        "Note": "Tuyến Đang OFF - Mở lại ngày: 10/06/2026"
    },
    {
        "Tỉnh": "Lâm Đồng",
        "Quận/huyện": "Huyện Di Linh",
        "Phường/xã cần tắt": "Xã Gia Bắc",
        "Bưu Cục": "Bưu Cục 1322 Hùng Vương-Di Linh-Lâm Đồng",
        "Kết quả (KA) update": "duyệt",
        "% Cap Down (KA)": 1.0,
        "Thời gian tắt (KA)": "27-05-2026",
        "Thời gian mở (KA)": "10-06-2026",
        "Note": "Tuyến Đang OFF - Mở lại ngày: 10/06/2026"
    }
]

df = pd.DataFrame(data)

# Rename columns to match the actual sheet closely (including the long column D header option)
df.columns = [
    "Tỉnh",
    "Quận/huyện",
    "Phường/xã cần tắt",
    "Bưu Cục\nVùng để trống cột bất kỳ từ cột B-> R\nNhập sai format\n=> KHÔNG REVIEW",
    "Kết quả (KA) update",
    "% Cap Down (KA)",
    "Thời gian tắt (KA)",
    "Thời gian mở (KA)",
    "Note"
]

# Write to Excel
with pd.ExcelWriter("off_tuyen_spe.xlsx") as writer:
    df.to_excel(writer, sheet_name="Đang OFF", index=False)

print("Mock off_tuyen_spe.xlsx created successfully!")
