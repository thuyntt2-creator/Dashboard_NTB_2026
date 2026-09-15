# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1400, 'height': 1200})
    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
    
    # 1. Capture ODR card
    card = page.locator('.kpi-tile').nth(4)
    card.screenshot(path='scratch/odr_card_fixed.png')
    print("ODR card inner text:")
    print(card.inner_text())
    
    # 2. Capture Overview tiles
    page.locator('#overview-kpi-tiles').screenshot(path='scratch/overview_tiles_fixed.png')
    
    # 3. Switch to Tab 6 and capture
    page.locator('.tab-item[data-tab="tab-odr"]').click()
    page.wait_for_timeout(1000)
    page.screenshot(path='scratch/tab_odr_fixed.png')
    
    browser.close()

print("All screenshots successfully captured!")
