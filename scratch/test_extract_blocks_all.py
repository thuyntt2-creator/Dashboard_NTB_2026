import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# tab-gtc-tong provincial block
p_start_gtc = html.find('<!-- 2 BẢNG ĐỐI XỨNG 5 TỈNH THÀNH: FULL HÀNG vs TIKTOK SHOP -->')
p_end_gtc = html.find('<!-- ==================================================================== -->\n      <!-- BẢNG 3: BƯU CỤC TRONG NHÓM CẢNH BÁO BẤT ỔN', p_start_gtc)
print("gtc block start:", p_start_gtc, "end:", p_end_gtc)
gtc_block = html[p_start_gtc:p_end_gtc].strip()
print("gtc block length:", len(gtc_block))
print("gtc block preview:", gtc_block[:150], "...", gtc_block[-100:])

# tab-odr provincial block
p_start_odr = html.find('<!-- 2 BẢNG ĐỐI XỨNG 5 TỈNH THÀNH: FULL HÀNG vs TIKTOK SHOP -->', p_end_gtc)
p_end_odr = html.find('</div>\n    </div>\n    <!-- ==================================================================== -->\n    <!-- TAB 7: %LTC', p_start_odr)
print("\nodr block start:", p_start_odr, "end:", p_end_odr)
odr_block = html[p_start_odr:p_end_odr].strip()
print("odr block length:", len(odr_block))
print("odr block preview:", odr_block[:150], "...", odr_block[-100:])
