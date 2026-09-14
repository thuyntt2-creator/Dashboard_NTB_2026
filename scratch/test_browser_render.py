import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1400, 'height': 900})
    page = context.new_page()
    
    print("Navigating to http://127.0.0.1:3000/hop...")
    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
    page.wait_for_timeout(2000)
    
    # 1. Header checks
    range_text = page.locator('#header-weeks-range').inner_text()
    filter_val = page.locator('#filter-week').input_value()
    print(f"Header range: {range_text}")
    print(f"Filter week selected: {filter_val}")
    
    # 2. Overview table header
    ov_headers = page.locator('#table-overview-kpi-data thead tr th').all_inner_texts()
    print(f"Overview table headers: {ov_headers}")
    
    # First row in Overview table
    first_ov_row = page.locator('#table-overview-kpi-data tbody tr:not(.tr-category-header)').first.all_inner_texts()
    print(f"First KPI row: {first_ov_row}")
    
    page.screenshot(path='scratch/verify_overview_tab.png', full_page=False)
    
    # 3. Tab 2: San luong
    print("\nClicking Tab 2 (Sản Lượng)...")
    page.click('button[data-tab="vol"]')
    page.wait_for_timeout(1000)
    
    t2_full_headers = page.locator('#table-vol-full-detailed thead tr th').all_inner_texts()
    print(f"Tab 2 Full headers: {t2_full_headers}")
    
    t2_full_first = page.locator('#table-vol-full-detailed tbody tr').first.all_inner_texts()
    print(f"Tab 2 Full AM 1st row: {t2_full_first}")
    
    t2_tinh_headers = page.locator('#table-vol-tinh-full thead tr th').all_inner_texts()
    print(f"Tab 2 5-tinh headers: {t2_tinh_headers}")
    
    t2_tinh_first = page.locator('#table-vol-tinh-full tbody tr').first.all_inner_texts()
    print(f"Tab 2 5-tinh 1st row: {t2_tinh_first}")
    
    page.screenshot(path='scratch/verify_tab2_vol.png', full_page=False)
    
    # 4. Tab 3: %GTC
    print("\nClicking Tab 3 (%GTC)...")
    page.click('button[data-tab="gtc"]')
    page.wait_for_timeout(1000)
    
    t3_full_headers = page.locator('#table-gtc-full-detailed thead tr th').all_inner_texts()
    print(f"Tab 3 Full headers: {t3_full_headers}")
    
    t3_full_first = page.locator('#table-gtc-full-detailed tbody tr').first.all_inner_texts()
    print(f"Tab 3 Full 1st row: {t3_full_first}")
    
    page.screenshot(path='scratch/verify_tab3_gtc.png', full_page=False)
    
    # 5. Tab 8: OPR TTS
    print("\nClicking Tab 8 (OPR TTS)...")
    page.click('button[data-tab="opr_tts"]')
    page.wait_for_timeout(1000)
    
    t8_banner = page.locator('#opr-tts-vung-total').inner_text()
    print(f"Tab 8 OPR Total Banner:\n{t8_banner[:200]}")
    
    t8_headers = page.locator('#table-opr-day-detailed thead tr th').all_inner_texts()
    print(f"Tab 8 Ca Ngay headers: {t8_headers}")
    
    page.screenshot(path='scratch/verify_tab8_opr.png', full_page=False)
    
    browser.close()
    print("\n✓ Browser verification finished successfully!")
