# -*- coding: utf-8 -*-
import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from report_BC_canh_bao_gtalk import get_gspread_client

gc = get_gspread_client()
sh2 = gc.open_by_key('1lmQv8KwHJzDFs_RMz64ydu4SOmG3M1YAzILNFGtzFec')

ws_ntbo = None
for ws in sh2.worksheets():
    if ws.id == 957775572:
        ws_ntbo = ws
        break

print(f"Worksheet found: {ws_ntbo.title} (id: {ws_ntbo.id})")

# 1. Update D1
new_d1 = """Logic: 
- %GTC của 7 ngày gần nhất
- HN và HCM lấy full hàng mới và hàng tồn
- Các tỉnh khác lấy hàng mới ca 1 + tồn

- Toàn quốc (HCM, HN và các tỉnh khác) < 50% => Cảnh báo
- Nếu %GTC < 70% Mốc %GTC tốt nhất trong lịch sử => Cảnh báo"""
ws_ntbo.update_acell('D1', new_d1)
print("Updated D1 in NTBo.")

# 2. Update N6:N91
formulas_n = []
for r in range(6, 92):
    f = f"""=LET(
  vol, IFERROR(XLOOKUP($B{r}, raw_buu_cuc_canh_bao!$D:$D, raw_buu_cuc_canh_bao!$Q:$Q, 0), 0),
  IF(OR(K{r}="", L{r}="", M{r}=""), "",
  IF(vol < 100, "Bình thường",
  IF(M{r} < 70%, "Nằm TOP Bất ổn",
  IF(K{r} < 50%, "Nằm TOP Bất ổn",
  IF(M{r} < 74%, "Chuẩn bị nhảy nhóm",
  IF(J{r} < 50%, "GTC N-1 < 50%",
  IF(M{r} < 75%, "Cấp cảnh báo", "Bình thường")))))))
)"""
    formulas_n.append([f])

ws_ntbo.update(values=formulas_n, range_name="N6:N91", value_input_option="USER_ENTERED")
print("Successfully updated N6:N91 in NTBo!")

# 3. Update BC_canh_bao A6
ws_bc = sh2.worksheet('BC_canh_bao')
new_a6 = """=QUERY(
  IMPORTRANGE("1odUPX5mWpUYUUQOrhX_k8kXWV7drMUdQ58DRwgSQNS8","raw_buu_cuc_canh_bao_2!B2:T"),
  "SELECT * 
   WHERE Col1 = 'NTB'
   AND NOT LOWER(Col4) CONTAINS 'kd '
   AND NOT LOWER(Col4) CONTAINS 'thanh lý'
   AND NOT LOWER(Col4) CONTAINS 'kho '
   AND NOT LOWER(Col4) CONTAINS 'test'
   AND NOT LOWER(Col4) CONTAINS 'lh '
   AND NOT LOWER(Col4) CONTAINS 'key'
   AND NOT LOWER(Col4) CONTAINS 'b2b'
   AND NOT LOWER(Col4) CONTAINS 'ck '
   AND NOT LOWER(Col4) CONTAINS 'kim tân'
   AND Col4 IS NOT NULL
   AND LOWER(Col19) <> 'bình thường'
   AND Col16 >= 100
   ORDER BY Col1, Col5",
  0
)"""
ws_bc.update_acell('A6', new_a6)
print("Successfully updated BC_canh_bao A6 to point to raw_buu_cuc_canh_bao_2!")

time.sleep(3)
val_j2 = ws_ntbo.acell('J2').value
print(f"NTBo J2 (Total warning count): {val_j2}")
