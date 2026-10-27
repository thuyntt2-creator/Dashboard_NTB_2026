# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
    page.wait_for_timeout(2000)
    page.screenshot(path='scratch/hop_fixed_screenshot.png')
    
    # Check if charts are rendered by querying canvas dimensions / context
    canvases = page.locator('canvas').all()
    print(f"Total canvas elements: {len(canvases)}")
    
    # Check chart-vol-trend
    vol_chart = page.locator('#chart-vol-trend')
    print("chart-vol-trend visible:", vol_chart.is_visible())
    
    browser.close()
print("Done!")
