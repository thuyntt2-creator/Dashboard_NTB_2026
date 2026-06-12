import re

with open("templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

jinja_exprs = re.findall(r"\{\{.*?\}\}", content)
jinja_blocks = re.findall(r"\{%.*?%\}", content)

print("Found Jinja expressions:", len(jinja_exprs))
for expr in set(jinja_exprs):
    print("  Expression:", expr)

print("Found Jinja blocks:", len(jinja_blocks))
for block in set(jinja_blocks):
    print("  Block:", block)
