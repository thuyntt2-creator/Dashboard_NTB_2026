import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1600, "height": 1200})
        print("Navigating to http://127.0.0.1:3000/hop...")
        await page.goto("http://127.0.0.1:3000/hop", wait_until="networkidle")
        await asyncio.sleep(2)
        
        # Click on Tab 15 (Kinh Doanh & F30)
        btn = page.locator('button[data-tab="tab-commercial"]')
        await btn.click()
        await asyncio.sleep(2)
        
        # Screenshot top part of Tab 15
        await page.screenshot(path="scratch/tab15_kpi_charts.png")
        print("Saved scratch/tab15_kpi_charts.png")
        
        # Scroll down to tables
        await page.evaluate("window.scrollBy(0, 700)")
        await asyncio.sleep(1)
        await page.screenshot(path="scratch/tab15_nhoma_tables.png")
        print("Saved scratch/tab15_nhoma_tables.png")
        
        # Scroll down to bottom tables
        await page.evaluate("window.scrollBy(0, 900)")
        await asyncio.sleep(1)
        await page.screenshot(path="scratch/tab15_bottom_tables.png")
        print("Saved scratch/tab15_bottom_tables.png")
        
        await browser.close()

asyncio.run(run())
