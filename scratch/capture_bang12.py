import asyncio, os
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1600, 'height': 1200})
        index_path = os.path.abspath('index.html').replace('\\', '/')
        await page.goto(f'file:///{index_path}')
        await page.wait_for_timeout(2000)
        
        # Click Tab 2
        await page.click('button[data-tab="tab-volume"]')
        await page.wait_for_timeout(1000)
        
        # Scroll down to Bảng 1 & 2
        await page.evaluate('window.scrollTo(0, 750)')
        await page.wait_for_timeout(500)
        await page.screenshot(path='verify_tab2_bang1_bang2.png')
        await browser.close()
        print('Captured Tab 2 Bảng 1 & 2')

asyncio.run(run())
