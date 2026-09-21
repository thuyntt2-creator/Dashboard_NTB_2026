import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 1000})
    
    # Capture console messages
    page.on('console', lambda msg: print(f"CONSOLE [{msg.type}]: {msg.text}"))
    page.on('pageerror', lambda err: print(f"PAGE ERROR: {err}"))

    print("Navigating to http://127.0.0.1:3000/hop...")
    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')

    # Screenshot Overview
    page.screenshot(path='scratch/verify_hop_overview.png')
    print("Saved scratch/verify_hop_overview.png")

    # 1. Click Tab 13: QR Code & Tiền Mặt (data-tab="tab-control")
    print("Clicking Tab 13 (QR Code / COD)...")
    btn_cod = page.query_selector('button[data-tab="tab-control"]')
    if btn_cod:
        btn_cod.click()
        page.wait_for_timeout(1000)
        page.screenshot(path='scratch/verify_tab_qrcode_trend.png')
        print("Saved scratch/verify_tab_qrcode_trend.png")

        # Click segment 2: AM So Sánh 2 Tuần
        page.click('#btn-cod-am')
        page.wait_for_timeout(500)
        page.screenshot(path='scratch/verify_tab_qrcode_am.png')
        print("Saved scratch/verify_tab_qrcode_am.png")

        # Click segment 4: Hướng Xử Lý AM
        page.click('#btn-cod-action')
        page.wait_for_timeout(500)
        page.screenshot(path='scratch/verify_tab_qrcode_action.png')
        print("Saved scratch/verify_tab_qrcode_action.png")
    else:
        print("ERROR: button[data-tab='tab-control'] not found!")

    # 2. Click Tab 14: Báo Cáo Truy Thu (data-tab="tab-truythu")
    print("Clicking Tab 14 (Báo Cáo Truy Thu)...")
    btn_tt = page.query_selector('button[data-tab="tab-truythu"]')
    if btn_tt:
        btn_tt.click()
        page.wait_for_timeout(1000)
        page.screenshot(path='scratch/verify_tab_truythu_loai.png')
        print("Saved scratch/verify_tab_truythu_loai.png")

        # Click segment 2: AM
        page.click('#btn-tt-amticket')
        page.wait_for_timeout(500)
        page.screenshot(path='scratch/verify_tab_truythu_am.png')
        print("Saved scratch/verify_tab_truythu_am.png")

        # Click segment 3: BC & Tỉnh
        page.click('#btn-tt-bcgiao')
        page.wait_for_timeout(500)
        page.screenshot(path='scratch/verify_tab_truythu_bc.png')
        print("Saved scratch/verify_tab_truythu_bc.png")
    else:
        print("ERROR: button[data-tab='tab-truythu'] not found!")

    browser.close()
    print("Done testing with Playwright!")
