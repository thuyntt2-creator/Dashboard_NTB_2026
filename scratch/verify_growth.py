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
        
        rows_3a = await page.eval_on_selector_all('#table-vol-tinh-full tbody tr', 'trs => trs.map(tr => tr.innerText.replace(/\\t/g, " | "))')
        rows_3b = await page.eval_on_selector_all('#table-vol-tinh-tts tbody tr', 'trs => trs.map(tr => tr.innerText.replace(/\\t/g, " | "))')
        
        with open('scratch/verify_growth_sort.txt', 'w', encoding='utf-8') as f:
            f.write('=== BANG 3A (XEP THEO BIEN DONG Δ) ===\n')
            for r in rows_3a:
                f.write(r + '\n')
            f.write('\n=== BANG 3B (XEP THEO BIEN DONG TTS Δ) ===\n')
            for r in rows_3b:
                f.write(r + '\n')
                
        await page.screenshot(path='verify_tab2_growth_sort.png')
        await browser.close()
        print('DONE')

asyncio.run(run())
