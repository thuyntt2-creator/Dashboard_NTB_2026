import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width': 1800, 'height': 1200})
    page = context.new_page()
    
    errors = []
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    
    page.goto('http://127.0.0.1:3000/hop')
    page.wait_for_timeout(2000)
    
    # Click Tab 10 (FD)
    page.locator('button[data-tab="tab-fd"]').click()
    page.wait_for_timeout(1500)
    
    # Capture Bảng 2 table
    card_bc = page.locator('#table-fd-top-bc')
    card_bc.screenshot(path='scratch/table_fd_bc_verified.png')
    
    # Full page screenshot of Tab 10
    page.screenshot(path='scratch/tab10_fd_full.png', full_page=True)
    
    print('Console errors:', errors)
    browser.close()
    print('Done verification!')
