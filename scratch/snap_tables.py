# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 1000})
    page.goto("http://127.0.0.1:3000/hop")
    page.wait_for_timeout(2000)
    
    # Click Tab 5 (ODR)
    btn_odr = page.query_selector('button[data-tab="tab-odr"]')
    if btn_odr:
        btn_odr.click()
        page.wait_for_timeout(1000)
    
    # Scroll down to tables
    page.evaluate("window.scrollBy(0, 600)")
    page.wait_for_timeout(500)
    
    page.screenshot(path="scratch/tab5_tables_comparison.png")
    print("Screenshot saved to scratch/tab5_tables_comparison.png")
    browser.close()
