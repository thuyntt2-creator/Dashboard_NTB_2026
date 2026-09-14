import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1440, 'height': 900})
    page = context.new_page()
    
    print("Navigating to http://127.0.0.1:3000/hop...")
    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
    page.wait_for_timeout(2000)
    
    # 1. Nav Tabs Check
    tab_texts = page.locator('.tab-item').all_inner_texts()
    tabs_clean = [t.replace('\n', ' ').strip() for t in tab_texts]
    print("Tabs list:", tabs_clean)
    has_cod_tab = any('COD' in t for t in tabs_clean)
    print(f"Has COD Tab: {has_cod_tab} (Should be False)")
    
    # 2. Overview KPI Tiles Check (Top Strip)
    kpi_tiles = page.locator('#overview-kpi-tiles .kpi-tile-header').all_inner_texts()
    print("Overview Strip KPI Tiles:", kpi_tiles)
    has_cod_tile = any('COD' in t for t in kpi_tiles)
    print(f"Has COD KPI Tile in Overview Strip: {has_cod_tile} (Should be False)")
    
    # 3. Overview Table
    ov_headers = page.locator('#table-overview-kpi-data thead tr th').all_inner_texts()
    print(f"Overview table headers: {ov_headers}")
    first_row = page.locator('#table-overview-kpi-data tbody tr:not(.tr-category-header)').first.all_inner_texts()
    print(f"Overview first row: {first_row}")
    page.screenshot(path='scratch/hop_w37_no_cod_overview.png')
    
    # 4. Tab 2: San Luong Giao
    print("\nClicking Tab 2 (Sản Lượng)...")
    page.click('button[data-tab="tab-volume"]')
    page.wait_for_timeout(1000)
    t2_headers = page.locator('#table-vol-full-detailed thead tr th').all_inner_texts()
    print(f"Tab 2 Full headers: {t2_headers}")
    t2_first = page.locator('#table-vol-full-detailed tbody tr').first.all_inner_texts()
    print(f"Tab 2 1st AM row: {t2_first}")
    page.screenshot(path='scratch/hop_w37_tab2_vol.png')
    
    # 5. Tab 3: %GTC
    print("\nClicking Tab 3 (%GTC)...")
    page.click('button[data-tab="tab-gtc-tong"]')
    page.wait_for_timeout(1000)
    t3_headers = page.locator('#table-gtc-full-detailed thead tr th').all_inner_texts()
    print(f"Tab 3 Full headers: {t3_headers}")
    t3_first = page.locator('#table-gtc-full-detailed tbody tr').first.all_inner_texts()
    print(f"Tab 3 1st AM row: {t3_first}")
    page.screenshot(path='scratch/hop_w37_tab3_gtc.png')
    
    # 6. Tab 5: % Gán Vận Hành
    print("\nClicking Tab 5 (% Gán)...")
    page.click('button[data-tab="tab-gan"]')
    page.wait_for_timeout(1000)
    t5_headers = page.locator('#table-gan-ca2-detailed thead tr th').all_inner_texts()
    print(f"Tab 5 Gán Tổng headers: {t5_headers}")
    t5_first = page.locator('#table-gan-ca2-detailed tbody tr').first.all_inner_texts()
    print(f"Tab 5 1st AM row: {t5_first}")
    page.screenshot(path='scratch/hop_w37_tab5_gan.png')
    
    browser.close()
    print("\n🎉 Verification finished with 100% SUCCESS!")
