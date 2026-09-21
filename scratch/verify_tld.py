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
    
    # 1. Overview tile for TLTD
    res = page.evaluate('''() => {
      const tile = Array.from(document.querySelectorAll('.kpi-tile')).find(el => el.textContent.includes('TLTĐ') || el.textContent.includes('TLLĐ'));
      return {
        text: tile ? tile.innerText : 'NOT FOUND',
        className: tile ? tile.className : ''
      };
    }''')
    print('Overview TLTĐ Tile:\n' + res['text'])
    
    # Capture overview tiles
    tiles = page.locator('#overview-kpi-tiles')
    tiles.screenshot(path='scratch/overview_tiles_tld_verified.png')
    
    # 2. Click Tab 11 (KTC)
    page.locator('button[data-tab="tab-ktc"]').click()
    page.wait_for_timeout(1500)
    
    # Switch to Fill rate subview if needed
    btn_fr = page.locator('button[onclick*="fillrate"], button:has-text("Tỷ Lệ Lấp Đầy"), button:has-text("TLLĐ")')
    if btn_fr.count() > 0:
        btn_fr.first.click()
        page.wait_for_timeout(1000)
        
    page.screenshot(path='scratch/tab11_ktc_verified.png', full_page=True)
    
    print('Console errors:', errors)
    browser.close()
    print('Done verification!')
