from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1800, 'height': 1200})
    
    errors = []
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    
    page.goto('http://127.0.0.1:3000/hop')
    page.wait_for_timeout(2000)
    
    # 1. Click Tab 2 (Sản Lượng)
    page.locator('button[data-tab="tab-volume"]').click()
    page.wait_for_timeout(1000)
    banner2 = page.locator('#tab-volume .exec-banner').first
    banner2.screenshot(path='scratch/banner_tab2.png')
    
    # 2. Click Tab 8 (%OPR TTS)
    page.locator('button[data-tab="tab-opr-tts"]').click()
    page.wait_for_timeout(1500)
    banner8 = page.locator('#tab-opr-tts .exec-banner').first
    banner8.screenshot(path='scratch/banner_tab8.png')
    page.screenshot(path='scratch/tab8_opr_full.png', full_page=True)
    
    # 3. Click Tab 9 (Rớt LC)
    page.locator('button[data-tab="tab-rot-lc"]').click()
    page.wait_for_timeout(1000)
    banner9 = page.locator('#tab-rot-lc .exec-banner').first
    banner9.screenshot(path='scratch/banner_tab9.png')
    
    print('Console errors:', errors)
    browser.close()
    print('Done verification!')
