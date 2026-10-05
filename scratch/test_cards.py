import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('app.js', encoding='utf-8') as f:
    js = f.read()

cards_match = re.search(r'const pairedCards = \[(.*?)\];\s*tilesEl\.innerHTML', js, re.DOTALL)
if cards_match:
    cards_str = cards_match.group(1)
    titles = re.findall(r'title:\s*`?(.*?)`?,', cards_str)
    ids = re.findall(r'id:\s*[\'"](.*?)[\'"]', cards_str)
    print(f"Total cards in pairedCards: {len(ids)}")
    for i, (cid, title) in enumerate(zip(ids, titles), 1):
        print(f"  {i}. ID: {cid:15} Title: {title}")
else:
    print("Could not find pairedCards block")
