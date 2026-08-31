import os
import platform

path1 = '/Users/lap4all/.gemini/antigravity-ide/brain/9eaa8cda-979e-44b8-a650-694ddc1c1b6b/telegram_am_mockup_1784220444476.png'
path2 = '/C:/Users/lap4all/.gemini/antigravity-ide/brain/9eaa8cda-979e-44b8-a650-694ddc1c1b6b/telegram_am_mockup_1784220444476.png'
path3 = '/C:\\Users\\lap4all\\.gemini\\antigravity-ide\\brain\\9eaa8cda-979e-44b8-a650-694ddc1c1b6b\\telegram_am_mockup_1784220444476.png'

print("path1:", os.path.abspath(path1))
print("path2:", os.path.abspath(path2))
print("path3:", os.path.abspath(path3))

artifact_dir = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\9eaa8cda-979e-44b8-a650-694ddc1c1b6b"
print("artifact_dir:", os.path.abspath(artifact_dir))

for p in [path1, path2, path3]:
    resolved = os.path.abspath(p)
    common = os.path.commonpath([resolved, artifact_dir])
    print(f"p resolved: {resolved}, common: {common}, is_inside: {common == artifact_dir}")
