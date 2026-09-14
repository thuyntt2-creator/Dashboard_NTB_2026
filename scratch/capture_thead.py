from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:3000/hop')
    page.wait_for_timeout(1000)

    page.click('[data-tab="tab-gtc-tong"]')
    page.wait_for_timeout(500)
    page.locator('#table-gtc-tts-detailed').screenshot(path='scratch/gtc_tts_table.png')

    page.click('[data-tab="tab-odr"]')
    page.wait_for_timeout(500)
    page.locator('#table-odr-tts-detailed').screenshot(path='scratch/odr_tts_table.png')

    b.close()
    print("DONE")
