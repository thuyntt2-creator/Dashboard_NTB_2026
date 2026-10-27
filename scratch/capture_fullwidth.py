from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1200})
    page.goto('http://127.0.0.1:3000/hop')
    page.click("button.tab-item[data-tab='tab-aging']")
    page.wait_for_timeout(1000)
    page.click("#btn-aging-treo")
    page.wait_for_timeout(1000)
    
    table = page.locator('#table-aging-am-detailed')
    table.scroll_into_view_if_needed()
    table.screenshot(path='scratch/table_am_fullwidth.png')
    
    table_bc = page.locator('#table-aging-bc-detailed')
    table_bc.scroll_into_view_if_needed()
    table_bc.screenshot(path='scratch/table_bc_fullwidth.png')
    
    browser.close()
print("CAPTURED BOTH TABLES FULLWIDTH!")
