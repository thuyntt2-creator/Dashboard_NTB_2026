import sys
import subprocess
sys.stdout.reconfigure(encoding='utf-8')

diff = subprocess.run(["git", "diff", "app.js"], capture_output=True, text=True, encoding='utf-8').stdout
print("GIT DIFF SUMMARY:")
for line in diff.split('\n'):
    if line.startswith('@@') or (line.startswith('+') and not line.startswith('+++')) or (line.startswith('-') and not line.startswith('---')):
        if any(w in line for w in ['function', '{', '}', 'if', 'else', 'tblBodyBC', ')();']):
            print(line)
