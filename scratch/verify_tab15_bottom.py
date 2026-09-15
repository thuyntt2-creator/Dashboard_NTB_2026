import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1600, 'height': 1200})
        page = await context.new_page()
        
        await page.goto("http://127.0.0.1:3000/hop", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        await page.locator('button[data-tab="tab-bc-canhbao"]').click()
        await page.wait_for_timeout(1000)
        
        # Scroll table into view and capture
        await page.evaluate("window.scrollBy(0, 400)")
        await page.wait_for_timeout(500)
        
        await page.screenshot(path="scratch/verify_tab15_bottom_rows.png")
        await browser.close()

asyncio.run(run())
