# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    cdp = page.context.new_cdp_session(page)
    cdp.send('Debugger.enable')
    cdp.send('Runtime.enable')

    exceptions = []
    def on_ex(event):
        d = event.get('exceptionDetails', {})
        exceptions.append(d)
        print(f"ERROR: line {d.get('lineNumber')+1}, col {d.get('columnNumber')}: {d.get('text')} - {d.get('exception', {}).get('description')}")

    cdp.on('Runtime.exceptionThrown', on_ex)

    page.evaluate(f"""() => {{
        const s = document.createElement('script');
        s.textContent = {repr(app_js)};
        document.body.appendChild(s);
    }}""")

    page.wait_for_timeout(1000)
    browser.close()
