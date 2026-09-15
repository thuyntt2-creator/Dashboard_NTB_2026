import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1600, 'height': 1200})
        page = await context.new_page()
        
        await page.goto("http://127.0.0.1:3000/hop", wait_until="networkidle")
        await page.wait_for_timeout(1500)
        
        # 1. Screenshot Tab 1 with speech script
        await page.screenshot(path="scratch/verify_tab1_speech.png")
        print("Tab 1 screenshot saved.")
        
        # 2. Screenshot Tab 15 with speech script
        await page.locator('button[data-tab="tab-bc-canhbao"]').click()
        await page.wait_for_timeout(1500)
        await page.screenshot(path="scratch/verify_tab15_speech.png")
        print("Tab 15 screenshot saved.")
        
        await browser.close()

asyncio.run(run())
