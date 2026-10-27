# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    # Catch any error during navigation
    page.on('console', lambda msg: print(f"CONSOLE: [{msg.type}] {msg.text}"))
    
    # Let's read the scripts directly and evaluate them to find the syntax error!
    for fname in ['data.js', 'app.js', 'control_tower_visuals.js']:
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                code = f.read()
            print(f"Testing {fname} (length {len(code)} bytes)...")
            # Try parsing by injecting into page
            page.evaluate(f"() => {{ try {{ new Function({repr(code)}); console.log('{fname} SYNTAX OK'); }} catch(e) {{ console.log('{fname} SYNTAX ERROR:', e.message, e.stack); }} }}")
        except Exception as ex:
            print(f"Error testing {fname}: {ex}")

    browser.close()
