import sys, re
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix the syntax error
code = code.replace(
    '"tab-volume-creation", "tab-ca-report", "tab-fd":',
    '"tab-volume-creation": {"view": True, "add": True, "edit": True, "delete": False},\n            "tab-ca-report": {"view": True, "add": True, "edit": True, "delete": False},\n            "tab-fd":'
)
code = code.replace(
    '"tab-ca-report", "tab-fd":',
    '"tab-ca-report": {"view": True, "add": True, "edit": True, "delete": False},\n            "tab-fd":'
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('Fixed syntax in app.py')
