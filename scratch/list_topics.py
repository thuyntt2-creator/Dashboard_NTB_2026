import sys
sys.path.insert(0, 'scratch')
from make_final_script import TOPICS
for i, t in enumerate(TOPICS):
    print(f"{i}: {t['id']} - {t['title'][:60]}")
