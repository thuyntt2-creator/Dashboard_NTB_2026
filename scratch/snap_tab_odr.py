# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1400, 'height': 1200})
    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
    page.locator('.tab-item[data-tab="tab-odr"]').click()
    page.wait_for_timeout(1000)
    page.screenshot(path='scratch/hop_tab_odr_actual.png')
    browser.close()
print("Snapped Tab ODR screenshot!")
