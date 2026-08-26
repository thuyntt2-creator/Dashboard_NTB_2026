import os

search_dir = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\a570b50e-300a-41ca-96a3-6b94e5e53638"
for root, dirs, files in os.walk(search_dir):
    for f in files:
        full_path = os.path.join(root, f)
        print(f"File: {os.path.relpath(full_path, search_dir)} (size: {os.path.getsize(full_path)} bytes)")
