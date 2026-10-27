# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    errors = []
    page.on('console', lambda msg: errors.append(f"[{msg.type}] {msg.text}") if msg.type in ['error', 'warning'] else None)
    page.on('pageerror', lambda err: errors.append(f"[PAGE_ERROR] {err}"))
    
    page.goto('http://127.0.0.1:3000/hop')
    page.wait_for_timeout(1000)
    
    # Click Tab 13: QR Code & Tiền Mặt
    tab13 = page.locator('.tab-item[data-tab="tab-control"]')
    print("Found tab 13:", tab13.count())
    tab13.click()
    page.wait_for_timeout(500)
    
    # 1. Panel 1: Xu Hướng 2 Tuần
    page.screenshot(path='scratch/verify_tab13_panel1.png')
    
    # 2. Panel 2: AM So Sánh 2 Tuần
    page.locator('#btn-cod-am').click()
    page.wait_for_timeout(400)
    page.screenshot(path='scratch/verify_tab13_panel2.png')
    
    # 3. Panel 3: Chi Tiết BC 2 Tuần
    page.locator('#btn-cod-bc').click()
    page.wait_for_timeout(400)
    page.screenshot(path='scratch/verify_tab13_panel3.png')
    
    # 4. Panel 4: Hướng Xử Lý AM
    page.locator('#btn-cod-action').click()
    page.wait_for_timeout(400)
    page.screenshot(path='scratch/verify_tab13_panel4.png')
    
    print("\nErrors during tab 13 testing:", errors)
    browser.close()
print("Done testing tab 13!")
