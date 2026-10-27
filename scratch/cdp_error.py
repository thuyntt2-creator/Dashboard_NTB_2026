# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    cdp = page.context.new_cdp_session(page)
    cdp.send('Debugger.enable')
    cdp.send('Runtime.enable')
    
    def on_exception(event):
        details = event.get('exceptionDetails', {})
        print("EXCEPTION DETAILS:")
        print("Text:", details.get('text'))
        print("LineNumber:", details.get('lineNumber'))
        print("ColumnNumber:", details.get('columnNumber'))
        print("ScriptId:", details.get('scriptId'))
        print("URL:", details.get('url'))
        print("Exception:", details.get('exception'))
        print("Stack:", details.get('stackTrace'))
    
    cdp.on('Runtime.exceptionThrown', on_exception)
    
    page.goto('http://127.0.0.1:3000/hop')
    page.wait_for_timeout(2000)
    browser.close()
