import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
old_id = "1LEmer5MUw2iC40NXOsFI4BHJ0WHLdkxn8FSKG7cZLsc"
new_id = "1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU"

# Find all python files
py_files = []
for root, dirs, files in os.walk(workspace_dir):
    # Skip scratch folder and virtualenv
    if "scratch" in root or ".venv" in root or "__pycache__" in root:
        continue
    for file in files:
        if file.endswith(".py") or file.endswith(".bat"):
            py_files.append(os.path.join(root, file))

print(f"Found {len(py_files)} files to check.")

modified_files = []
for file_path in py_files:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        if old_id in content:
            updated_content = content.replace(old_id, new_id)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            modified_files.append(file_path)
            print(f"Updated: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print(f"Successfully updated {len(modified_files)} files.")
