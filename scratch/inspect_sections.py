import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/generate_professional_w38_script.py', 'r', encoding='utf-8') as f:
    text = f.read()

sections = text.split('add_speech_section(')
print(f'Total sections: {len(sections) - 1}')
for i in range(1, len(sections)):
    s = sections[i]
    m_title = re.search(r'sec_title="(.*?)"', s)
    m_head = re.search(r'speech_heading="(.*?)"', s)
    title = m_title.group(1) if m_title else 'No Title'
    head = m_head.group(1) if m_head else 'No Heading'
    print(f'Sec {i}: {title[:70]} | {head[:50]}')
