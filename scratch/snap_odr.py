# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
    card = page.locator('.kpi-tile').nth(4)
    print("ODR card HTML:")
    print(card.inner_html())
    card.screenshot(path='scratch/odr_card_actual.png')
    page.screenshot(path='scratch/hop_overview_actual.png')
    
    # Also click Tab ODR and take screenshot
    page.locator('.nav-tab[data-tab="tab-odr"]').click()
    page.wait_for_timeout(1000)
    page.screenshot(path='scratch/hop_tab_odr_actual.png')
    
    browser.close()
print("Done snapping screenshots!")
