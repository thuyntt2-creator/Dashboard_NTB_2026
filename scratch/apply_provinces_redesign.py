import re, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

# 1. Restore fresh from bak or read index.html
if sys.platform:
    shutil.copy('index.html.bak_provinces_redesign', 'index.html')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ==========================================
# 1. TAB VOLUME REARRANGEMENT
# ==========================================
p_start_vol = html.find('<!-- 2 BẢNG SẢN LƯỢNG THEO 5 TỈNH THÀNH: FULL HÀNG vs TIKTOK SHOP -->')
p_end_vol = html.find('</div>\n\n    <!-- ==================================================================== -->\n        <!-- ==================================================================== -->\n    <!-- TAB 3: %GTC TỔNG', p_start_vol)

assert p_start_vol != -1 and p_end_vol != -1, "Could not find volume provincial block"
vol_tinh_block = html[p_start_vol:p_end_vol].strip()

vol_tinh_block_enhanced = f"""<!-- KHỐI 1: BẢNG ĐIỀU HÀNH SẢN LƯỢNG THEO 5 TỈNH THÀNH (FULL HÀNG vs TIKTOK SHOP) -->
      <div style="font-size: 14px; font-weight: 800; color: var(--ghn-navy); margin: 20px 0 12px 0; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <i data-lucide="map-pin" style="width: 18px; height: 18px; color: var(--color-blue);"></i>
          <span>1. TỔNG QUAN SẢN LƯỢNG 5 TỈNH THÀNH (FULL HÀNG vs TIKTOK SHOP)</span>
        </div>
        <span class="badge-tag badge-tag-blue" style="font-size: 11.5px; padding: 4px 10px;">
          Khánh Hòa • Lâm Đồng • Bình Thuận • Đắk Nông • Ninh Thuận
        </span>
      </div>

{vol_tinh_block[vol_tinh_block.find('<div class="grid-row-2"'):]}"""

# Remove from bottom of tab-volume
html = html[:p_start_vol] + html[p_end_vol:]

# Target insertion point: right after tab-volume exec-banner
vol_banner_end = html.find('</div>\n      </div>\n\n      <!-- Main Chart AM Volume')
assert vol_banner_end != -1, "Could not find vol banner end"
insert_point_vol = vol_banner_end + len('</div>\n      </div>\n\n')

am_vol_header = """      <!-- KHỐI 2: PHÂN TÍCH SẢN LƯỢNG 18 AM PHỤ TRÁCH -->
      <div style="font-size: 14px; font-weight: 800; color: var(--ghn-navy); margin: 24px 0 12px 0; display: flex; align-items: center; gap: 8px;">
        <i data-lucide="users" style="width: 18px; height: 18px; color: var(--ghn-orange);"></i>
        <span>2. BÓC TÁCH CHI TIẾT SẢN LƯỢNG THEO 18 AM PHỤ TRÁCH (CỘT W37 vs W38 + LINE Δ)</span>
      </div>\n\n"""

html = html[:insert_point_vol] + vol_tinh_block_enhanced + "\n\n" + am_vol_header + html[insert_point_vol:]
print("Tab Volume reorganized successfully.")

# ==========================================
# 2. TAB GTC TONG REARRANGEMENT
# ==========================================
p_start_gtc = html.find('<!-- 2 BẢNG ĐỐI XỨNG 5 TỈNH THÀNH: FULL HÀNG vs TIKTOK SHOP -->')
p_end_gtc = html.find('<!-- ==================================================================== -->\n      <!-- BẢNG 3: BƯU CỤC TRONG NHÓM CẢNH BÁO BẤT ỔN', p_start_gtc)

assert p_start_gtc != -1 and p_end_gtc != -1, "Could not find gtc provincial block"
gtc_tinh_block = html[p_start_gtc:p_end_gtc].strip()

gtc_tinh_block_enhanced = f"""<!-- KHỐI 1: BẢNG ĐIỀU HÀNH %GTC TỔNG THEO 5 TỈNH THÀNH -->
      <div style="font-size: 14px; font-weight: 800; color: var(--ghn-navy); margin: 20px 0 12px 0; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <i data-lucide="map-pin" style="width: 18px; height: 18px; color: var(--color-blue);"></i>
          <span>1. TỔNG QUAN HIỆU SUẤT %GTC 5 TỈNH THÀNH (FULL HÀNG vs TIKTOK SHOP)</span>
        </div>
        <span class="badge-tag badge-tag-blue" style="font-size: 11.5px; padding: 4px 10px;">
          Khánh Hòa • Lâm Đồng • Bình Thuận • Đắk Nông • Ninh Thuận
        </span>
      </div>

{gtc_tinh_block[gtc_tinh_block.find('<div class="grid-row-2"'):]}"""

# Remove from bottom of tab-gtc-tong
html = html[:p_start_gtc] + html[p_end_gtc:]

# Target insertion point: right after tab-gtc-tong exec-banner
gtc_banner_end = html.find('</div>\n      </div>\n\n      <!-- Segment Selector: Full Hàng vs TikTok Shop')
assert gtc_banner_end != -1, "Could not find gtc banner end"
insert_point_gtc = gtc_banner_end + len('</div>\n      </div>\n\n')

am_gtc_header = """      <!-- KHỐI 2: PHÂN TÍCH HIỆU SUẤT %GTC THEO 18 AM PHỤ TRÁCH -->
      <div style="font-size: 14px; font-weight: 800; color: var(--ghn-navy); margin: 24px 0 12px 0; display: flex; align-items: center; gap: 8px;">
        <i data-lucide="users" style="width: 18px; height: 18px; color: var(--ghn-orange);"></i>
        <span>2. BÓC TÁCH HIỆU SUẤT %GTC THEO 18 AM PHỤ TRÁCH (CỘT W37 vs W38 + LINE Δ)</span>
      </div>\n\n"""

html = html[:insert_point_gtc] + gtc_tinh_block_enhanced + "\n\n" + am_gtc_header + html[insert_point_gtc:]
print("Tab GTC Tong reorganized successfully.")

# ==========================================
# 3. TAB ODR REARRANGEMENT
# ==========================================
p_start_odr = html.find('<!-- 2 BẢNG ĐỐI XỨNG 5 TỈNH THÀNH: FULL HÀNG vs TIKTOK SHOP -->')
p_end_odr = html.find('</div>\n    </div>\n    <!-- ==================================================================== -->\n    <!-- TAB 7: %LTC', p_start_odr)

assert p_start_odr != -1 and p_end_odr != -1, "Could not find odr provincial block"
odr_tinh_block = html[p_start_odr:p_end_odr].strip()

odr_tinh_block_enhanced = f"""<!-- KHỐI 1: BẢNG ĐIỀU HÀNH %ODR THEO 5 TỈNH THÀNH -->
      <div style="font-size: 14px; font-weight: 800; color: var(--ghn-navy); margin: 20px 0 12px 0; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <i data-lucide="map-pin" style="width: 18px; height: 18px; color: var(--color-green);"></i>
          <span>1. TỔNG QUAN CHỈ SỐ %ODR 5 TỈNH THÀNH (FULL HÀNG vs TIKTOK SHOP)</span>
        </div>
        <span class="badge-tag badge-tag-green" style="font-size: 11.5px; padding: 4px 10px;">
          Khánh Hòa • Lâm Đồng • Bình Thuận • Đắk Nông • Ninh Thuận
        </span>
      </div>

{odr_tinh_block[odr_tinh_block.find('<div class="grid-row-2"'):]}"""

# Remove from bottom of tab-odr
html = html[:p_start_odr] + html[p_end_odr:]

# Target insertion point: right after tab-odr exec-banner
tab_odr_idx = html.find('id="tab-odr"')
odr_banner_end = html.find('</div>\n      </div>\n\n      <!-- Segment Selector: Full Hàng vs TikTok Shop', tab_odr_idx)
assert odr_banner_end != -1, "Could not find odr banner end"
insert_point_odr = odr_banner_end + len('</div>\n      </div>\n\n')

am_odr_header = """      <!-- KHỐI 2: PHÂN TÍCH CHỈ SỐ %ODR THEO 18 AM PHỤ TRÁCH -->
      <div style="font-size: 14px; font-weight: 800; color: var(--ghn-navy); margin: 24px 0 12px 0; display: flex; align-items: center; gap: 8px;">
        <i data-lucide="users" style="width: 18px; height: 18px; color: var(--ghn-orange);"></i>
        <span>2. BÓC TÁCH CHỈ SỐ %ODR THEO 18 AM PHỤ TRÁCH (CỘT W37 vs W38 + LINE Δ)</span>
      </div>\n\n"""

html = html[:insert_point_odr] + odr_tinh_block_enhanced + "\n\n" + am_odr_header + html[insert_point_odr:]
print("Tab ODR reorganized successfully.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved new index.html with redesigned layout successfully!")
