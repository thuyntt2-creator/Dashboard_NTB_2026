import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace all occurrences of '"tab-fd"' with '"tab-ca-report", "tab-fd"' in permissions list
code = code.replace('"tab-fd", "tab-nhan-su"', '"tab-ca-report", "tab-fd", "tab-nhan-su"')
code = code.replace('"tab-fd"', '"tab-ca-report", "tab-fd"')
# Above might replace too many things, let's just do it dynamically in a safer way.

# Actually, the user roles just check `all_pages = ["tab-dashboard", ... "tab-fd", "tab-nhan-su", "tab-sync"]`
if '"tab-ca-report"' not in code:
    code = code.replace(
        '"tab-fd", "tab-nhan-su", "tab-sync"',
        '"tab-ca-report", "tab-fd", "tab-nhan-su", "tab-sync"'
    )
    code = code.replace(
        '"tab-volume-creation", "tab-fd"',
        '"tab-volume-creation", "tab-ca-report", "tab-fd"'
    )
    code = code.replace(
        '            "tab-fd": {"view": True, "add": False, "edit": False, "delete": False}',
        '            "tab-ca-report": {"view": True, "add": False, "edit": False, "delete": False},\n            "tab-fd": {"view": True, "add": False, "edit": False, "delete": False}'
    )

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('Patched permissions in app.py')
