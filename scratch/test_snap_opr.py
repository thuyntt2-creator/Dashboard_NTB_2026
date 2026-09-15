from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1200, 'height': 1000})
    file_path = os.path.abspath('KICH_BAN_THUYET_TRINH_W37_NAM_TRUNG_BO.html')
    page.goto(f'file:///{file_path}')
    h2 = page.locator('text=OPR TIKTOK SHOP').first
    h2.scroll_into_view_if_needed()
    page.screenshot(path='scratch/kich_ban_html_opr_section.png')
    browser.close()
    print('Rendered OPR Section preview!')
