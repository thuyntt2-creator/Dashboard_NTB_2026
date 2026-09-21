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

    # 1. Test Tab 13: QR Code & Tiền Mặt
    print("Clicking Tab 13 (QR Code & Tiền Mặt)...")
    page.click('button[data-tab="tab-control"]')
    page.wait_for_timeout(1000)
    page.screenshot(path='scratch/tab13_qrcode_top.png')

    # Scroll down to capture AM and BC tables
    page.evaluate("window.scrollTo(0, 800)")
    page.wait_for_timeout(500)
    page.screenshot(path='scratch/tab13_qrcode_am_bc.png')

    # Scroll down to action plan
    page.evaluate("window.scrollTo(0, 1600)")
    page.wait_for_timeout(500)
    page.screenshot(path='scratch/tab13_qrcode_action_plan.png')

    # 2. Test Tab 14: Truy Thu (2 Tuần)
    print("Clicking Tab 14 (Báo Cáo Truy Thu)...")
    page.evaluate("window.scrollTo(0, 0)")
    page.click('button[data-tab="tab-truythu"]')
    page.wait_for_timeout(1000)
    page.screenshot(path='scratch/tab14_truythu_top.png')

    # Scroll down to capture AM & BC comparison
    page.evaluate("window.scrollTo(0, 700)")
    page.wait_for_timeout(500)
    page.screenshot(path='scratch/tab14_truythu_am_table.png')

    page.evaluate("window.scrollTo(0, 1400)")
    page.wait_for_timeout(500)
    page.screenshot(path='scratch/tab14_truythu_bc_table.png')

    browser.close()

    print(f"Total Errors detected: {len(errors)}")
    for e in errors:
        print(e)
    print("Done testing!")
