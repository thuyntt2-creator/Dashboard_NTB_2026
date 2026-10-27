# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    logs = []
    page.on('console', lambda msg: logs.append(f"[{msg.type}] {msg.text}"))
    page.on('pageerror', lambda err: logs.append(f"[PAGE_ERROR] {err}"))
    
    page.goto('http://127.0.0.1:3000/hop', wait_until='networkidle')
    page.wait_for_timeout(2000)
    
    print("Logs captured:")
    for l in logs:
        print(l)
        
    browser.close()
