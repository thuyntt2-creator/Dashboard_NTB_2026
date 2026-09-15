import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1600, 'height': 1200})
        page = await context.new_page()
        
        await page.goto("http://127.0.0.1:3000/hop", wait_until="networkidle")
        await page.wait_for_timeout(2000)
        
        # Check Tab 1 table-bc-canh-bao-overview
        rows_t1 = await page.locator("#table-bc-canh-bao-overview tbody tr").count()
        print(f"Tab 1 overview warning rows: {rows_t1}")
        
        # Switch to Tab 15
        await page.locator('button[data-tab="tab-bc-canhbao"]').click()
        await page.wait_for_timeout(1500)
        
        rows_t15 = await page.locator("#table-bc-canhbao-tab tbody tr").count()
        print(f"Tab 15 warning rows: {rows_t15}")
        
        # Capture screenshot of Tab 15
        await page.screenshot(path="scratch/verify_tab15_13bc.png")
        print("Screenshot saved to scratch/verify_tab15_13bc.png")
        
        await browser.close()

asyncio.run(run())
