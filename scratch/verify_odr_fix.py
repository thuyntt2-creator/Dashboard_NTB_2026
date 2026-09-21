import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width': 1800, 'height': 1200})
    page = context.new_page()
    page.goto('http://127.0.0.1:3000/hop')
    page.wait_for_timeout(2000)
    
    res = page.evaluate('''() => {
      const tile = Array.from(document.querySelectorAll('.kpi-tile')).find(el => el.textContent.includes('ODR'));
      return {
        innerText: tile ? tile.innerText : 'NOT FOUND',
        className: tile ? tile.className : ''
      };
    }''')
    print('Tile text:\n' + res['innerText'])
    print('Tile class: ' + res['className'])
    
    # Take screenshot of the overview tiles
    tiles = page.locator('#overview-kpi-tiles')
    tiles.screenshot(path='scratch/overview_tiles_w38_fixed.png')
    
    # Also take screenshot of Tab 6 (ODR tab)
    page.locator('button[data-tab="tab-odr"]').click()
    page.wait_for_timeout(1500)
    page.screenshot(path='scratch/tab6_odr_w38_fixed.png', full_page=True)
    
    browser.close()
    print('Verification done and screenshots saved!')
