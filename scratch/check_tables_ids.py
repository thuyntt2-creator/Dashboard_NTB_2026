import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("GTC IDs in index.html:")
for m in re.findall(r'id=["\']([^"\']*gtc[^"\']*)["\']', text):
    print(" ", m)

print("\nODR IDs in index.html:")
for m in re.findall(r'id=["\']([^"\']*odr[^"\']*)["\']', text):
    print(" ", m)

print("\nGAN IDs in index.html:")
for m in re.findall(r'id=["\']([^"\']*gan[^"\']*)["\']', text):
    print(" ", m)

print("\nROT LC IDs in index.html:")
for m in re.findall(r'id=["\']([^"\']*rot[^"\']*)["\']', text):
    print(" ", m)
