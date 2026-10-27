import os
from playwright.sync_api import sync_playwright

test_html = """<!DOCTYPE html>
<html>
<head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/acorn/8.11.3/acorn.min.js"></script>
</head>
<body>
<script>
window.testCode = function(code) {
    try {
        acorn.parse(code, {ecmaVersion: 2020});
        return {status: 'OK'};
    } catch (e) {
        return {status: 'ERR', message: e.message, loc: e.loc};
    }
};
</script>
</body>
</html>
"""

os.makedirs("scratch", exist_ok=True)
with open("scratch/test_acorn.html", "w", encoding="utf-8") as f:
    f.write(test_html)

with open("app.js", "r", encoding="utf-8") as f:
    code = f.read()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    url = "file:///" + os.path.abspath("scratch/test_acorn.html").replace("\\", "/")
    page.goto(url)
    
    res = page.evaluate("code => window.testCode(code)", code)
    print("Original:", res)
    
    # Check what if we add closing brace:
    for extra in range(1, 5):
        test_c = code.rstrip()
        if test_c.endswith(")();"):
            test_c = test_c[:-4] + ("}\n" * extra) + ")();"
        res = page.evaluate("code => window.testCode(code)", test_c)
        print(f"With {extra} extra braces:", res)
        if res.get("status") == "OK":
            print(f"SUCCESS with {extra} extra braces!")
            break
            
    browser.close()
