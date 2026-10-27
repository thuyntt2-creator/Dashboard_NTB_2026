import sys
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    cdp = page.context.new_cdp_session(page)
    cdp.send("Debugger.enable")
    
    def on_paused(event):
        call_frames = event.get("callFrames", [])
        if call_frames:
            f = call_frames[0]
            print(f"Debugger paused at {f.get('url')}:{f.get('lineNumber')}:{f.get('columnNumber')}")
            
    cdp.on("Debugger.paused", on_paused)
    
    def on_script_failed_to_parse(event):
        print(f"FAILED TO PARSE: {event.get('url')}:{event.get('startLine')}:{event.get('errorLine')}")
        print(f"Reason: {event.get('message')}")
        
    cdp.on("Debugger.scriptFailedToParse", on_script_failed_to_parse)
    
    page.goto('http://127.0.0.1:3000/hop')
    page.wait_for_timeout(2000)
    browser.close()
