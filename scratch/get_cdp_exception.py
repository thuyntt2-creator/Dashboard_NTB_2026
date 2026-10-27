import sys
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    cdp = page.context.new_cdp_session(page)
    cdp.send("Debugger.enable")
    cdp.send("Runtime.enable")
    
    def on_exception(event):
        details = event.get("exceptionDetails", {})
        print("EXCEPTION DETAILS:", details)
        
    cdp.on("Runtime.exceptionThrown", on_exception)
    
    page.goto('http://127.0.0.1:3000/hop')
    page.wait_for_timeout(2000)
    browser.close()
