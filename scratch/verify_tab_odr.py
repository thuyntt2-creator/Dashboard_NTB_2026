# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 1000})
    page.goto("http://127.0.0.1:3000/hop")
    page.wait_for_timeout(2000)
    
    # Click Tab 5 (ODR)
    btn_odr = page.query_selector('button[data-tab="tab-odr"]')
    if btn_odr:
        btn_odr.click()
        page.wait_for_timeout(1500)
    
    # Screenshot of ODR comparison table
    page.screenshot(path="scratch/tab5_odr_fixed.png")
    print("Screenshot saved to scratch/tab5_odr_fixed.png")
    browser.close()
