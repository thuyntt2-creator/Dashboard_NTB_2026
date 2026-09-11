with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('Has .sidebar { :', '.sidebar {' in text)
print('Has .main-content { :', '.main-content {' in text)
print('Has <aside class="sidebar"> :', '<aside class="sidebar">' in text)
print('Has <header class="top-header"> :', '<header class="top-header">' in text)
print('Has function switchTab(tabId, el) :', 'function switchTab(tabId, el)' in text)
