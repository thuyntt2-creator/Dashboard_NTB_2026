import os
import sys
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1600, 'height': 1200})
    file_path = os.path.abspath('index.html')
    url = 'file:///' + file_path.replace('\\', '/')
    print(f'Navigating to {url}')
    page.goto(url)
    page.wait_for_timeout(1500)
    
    # Click Tab 4: %GTC TTS Ca 1
    page.click("button[data-tab='tab-gtc-tts-ca1']")
    page.wait_for_timeout(1200)

    # Click Sort Ca 1 cao -> thap or diff
    # Get all AMs in table
    table_ams = page.eval_on_selector_all('#table-gtc-tts-ca1-detailed tbody tr', '''rows => rows.map(r => ({
        rank: r.cells[0]?.innerText.trim(),
        am: r.cells[1]?.innerText.trim(),
        vol: r.cells[2]?.innerText.trim(),
        w40: r.cells[4]?.innerText.trim(),
        diff: r.cells[5]?.innerText.trim()
    }))''')
    print(f"Total AMs in Tab 4 table: {len(table_ams)}")
    for r in table_ams:
        if 'Duân' in r['am']:
            print("Found Duân in table:", r)

    # Get chart labels
    chart_labels = page.evaluate('''() => {
        const c = Chart.getChart('chart-gtc-tts-ca1-bar');
        return c ? c.data.labels : [];
    }''')
    print(f"Total AMs in Tab 4 chart: {len(chart_labels)}")
    print("Chart labels:", chart_labels)
    has_duan_chart = 'Huỳnh Thúc Duân' in chart_labels
    print("Has Duân in chart:", has_duan_chart)

    # Screenshot of chart
    chart_elem = page.query_selector('.tab-view#tab-gtc-tts-ca1 .report-card')
    if chart_elem:
        chart_elem.screenshot(path='scratch/verify_tab4_chart_with_duan.png')
        print("Screenshot of chart saved to scratch/verify_tab4_chart_with_duan.png")

    page.screenshot(path='scratch/verify_tab4_full.png', full_page=False)
    browser.close()
