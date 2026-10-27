# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    page.on('console', lambda msg: print(f"[{msg.type}] {msg.text} ({msg.location})"))
    page.on('pageerror', lambda err: print(f"[PAGE_ERROR] {repr(err)}\n{getattr(err, 'stack', '')}"))
    
    page.goto('http://127.0.0.1:3000/hop')
    page.wait_for_timeout(3000)
    browser.close()
