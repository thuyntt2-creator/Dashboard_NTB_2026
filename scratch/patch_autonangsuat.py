import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
lines = open(r"C:\Users\lap4all\Documents\Auto report\autonangsuat.py", encoding="utf-8").readlines()
for i in range(1040, min(len(lines), 1087)):
    print(f"{i}: {lines[i]}", end="")
