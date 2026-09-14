from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
    time.sleep(1)
    
    badge = page.locator('.live-badge').inner_text()
    filter_val = page.locator('#filter-week').input_value()
    h1 = page.locator('h1').inner_text()
    range_txt = page.locator('#header-weeks-range').inner_text()
    
    # Check overview cards
    card_title = page.locator('.kpi-tile-title').first.inner_text()
    
    print('Rendered Page Info:')
    print('  Badge:', badge)
    print('  Selected Week:', filter_val)
    print('  Date Range:', range_txt)
    print('  First Card Title:', card_title)
    
    page.screenshot(path='scratch/hop_w37_rendered.png', full_page=False)
    print('Screenshot saved: scratch/hop_w37_rendered.png')
    browser.close()
