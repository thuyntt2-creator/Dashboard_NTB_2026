import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 1000})

    errors = []
    page.on('pageerror', lambda err: errors.append(f"PAGE ERROR: {err}"))
    page.on('console', lambda msg: errors.append(f"CONSOLE {msg.type}: {msg.text}") if msg.type == 'error' else None)

    print("Navigating to http://127.0.0.1:3000/hop...")
    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')

    # Tab 13: QR Code & Tiền Mặt
    page.click('button[data-tab="tab-control"]')
    page.wait_for_timeout(500)

    # 1. Trend
    page.click('#btn-cod-trend')
    page.wait_for_timeout(300)
    page.screenshot(path='scratch/cod_tab1_trend.png')

    # 2. AM So Sánh
    page.click('#btn-cod-am')
    page.wait_for_timeout(300)
    page.screenshot(path='scratch/cod_tab2_am.png')

    # 3. Chi Tiết BC
    page.click('#btn-cod-bc')
    page.wait_for_timeout(300)
    page.screenshot(path='scratch/cod_tab3_bc.png')

    # 4. Hướng Xử Lý AM
    page.click('#btn-cod-action')
    page.wait_for_timeout(300)
    page.screenshot(path='scratch/cod_tab4_action.png')

    # Tab 14: Truy Thu (2 Tuần)
    page.click('button[data-tab="tab-truythu"]')
    page.wait_for_timeout(500)

    # 1. Loại vi phạm
    page.click('#btn-tt-loai')
    page.wait_for_timeout(300)
    page.screenshot(path='scratch/truythu_tab1_loai.png')

    # 2. AM Phụ Trách
    page.click('#btn-tt-amticket')
    page.wait_for_timeout(300)
    page.screenshot(path='scratch/truythu_tab2_am.png')

    # 3. Top Bưu Cục
    page.click('#btn-tt-bcgiao')
    page.wait_for_timeout(300)
    page.screenshot(path='scratch/truythu_tab3_bc.png')

    browser.close()

    print(f"Total Errors: {len(errors)}")
    for e in errors:
        print(e)
    print("Screenshots taken successfully!")
