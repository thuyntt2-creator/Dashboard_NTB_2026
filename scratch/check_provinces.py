import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

# Build a mapping of AM -> Province
am_province = {
    "Phan Đình Duy": "Khánh Hòa",
    "Nguyễn Thanh Long": "Khánh Hòa",
    "Thái Thị Thanh Thư": "Khánh Hòa",
    "Phan Nguyễn Yến Nhi": "Khánh Hòa",
    "Nguyễn Lê Nguyên Vũ": "Khánh Hòa",
    "Lê Văn Trường": "Lâm Đồng",
    "Lê Minh Lợi": "Lâm Đồng",
    "Huỳnh Thị Kim Chi": "Lâm Đồng",
    "Trầm Hữu Tiến": "Lâm Đồng",
    "Nguyễn Duy Long": "Bình Thuận",
    "Nguyễn Ngọc Khánh": "Bình Thuận",
    "Nguyễn Thị Tuyết Thơ": "Bình Thuận",
    "Lê Thanh Nhựt": "Ninh Thuận",
    "Nguyễn Đỗ Minh Nghĩa": "Ninh Thuận",
    "Huỳnh Thúc Duân": "Đắk Nông",
    "Trương Quang Linh": "Đắk Nông",
    "Trần Thị Nhung": "Đắk Nông",
    "Hồng Bích Nga": "Đắk Nông",
    "Cao Thị Thanh Thủy": "Khánh Hòa",
    "Nguyễn Hoàng Phi": "Lâm Đồng"
}

# Check sum by province in san_luong.am_full
prov_vols = {}
for a in d['san_luong']['am_full']:
    prov = am_province.get(a['am'], "Khác")
    prov_vols[prov] = prov_vols.get(prov, 0) + a['vol']

print("Calculated Province Volumes for W40:")
for p, v in prov_vols.items():
    print(f"  {p}: {v:,} đơn")
