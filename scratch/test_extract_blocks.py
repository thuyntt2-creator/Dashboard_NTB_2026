import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's inspect the exact start and end of the provincial block in tab-volume:
# Start: <!-- 2 BẢNG SẢN LƯỢNG THEO 5 TỈNH THÀNH: FULL HÀNG vs TIKTOK SHOP -->
# End: before </div>\n\n    <!-- ==================================================================== -->\n        <!-- ==================================================================== -->\n    <!-- TAB 3: %GTC TỔNG TOÀN MẠNG
p_start_vol = html.find('<!-- 2 BẢNG SẢN LƯỢNG THEO 5 TỈNH THÀNH: FULL HÀNG vs TIKTOK SHOP -->')
p_end_vol = html.find('</div>\n\n    <!-- ==================================================================== -->\n        <!-- ==================================================================== -->\n    <!-- TAB 3: %GTC TỔNG', p_start_vol)

print("vol block start:", p_start_vol, "end:", p_end_vol)
vol_block = html[p_start_vol:p_end_vol].strip()
print("vol block length:", len(vol_block))
print("vol block preview:", vol_block[:150], "...", vol_block[-100:])
