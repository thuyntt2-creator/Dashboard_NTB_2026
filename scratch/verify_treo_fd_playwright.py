import asyncio
from playwright.async_api import async_playwright

async def verify_fixes():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1600, 'height': 900})
        await page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
        await page.wait_for_timeout(1000)

        # 1. Tab FD Banner
        await page.click('button[data-tab="tab-fd"]')
        await page.wait_for_timeout(500)
        fd_banner = page.locator('#tab-fd .exec-banner')
        await fd_banner.screenshot(path='scratch/verify_fd_banner_fixed.png')
        print('Captured FD Banner!')

        # 2. Tab Aging/Treo LC
        await page.click('button[data-tab="tab-aging"]')
        await page.wait_for_timeout(500)
        # Click Treo LC subtab
        await page.click('#btn-aging-treo')
        await page.wait_for_timeout(600)
        table_am = page.locator('#table-aging-am-detailed')
        await table_am.screenshot(path='scratch/verify_treo_table_fixed.png')
        print('Captured Treo Table AM!')

        await browser.close()

asyncio.run(verify_fixes())
