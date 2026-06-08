import os
import re

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
found = []
for root, dirs, files in os.walk(workspace_dir):
    for file in files:
        if file.endswith(".py") or file.endswith(".html") or file.endswith(".js"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "thu_cung_ky" in content or "cung_ky" in content or "cung kỳ" in content:
                        print(f"Found keyword in {file_path}")
            except Exception as e:
                pass
