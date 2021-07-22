import re

with open('SUMMARY.md', 'r') as f:
    t = f.read()
    t = re.sub(r'\n\s*\n', '\n', t)
    
with open('SUMMARY.md', 'w+') as f:
    f.write(t)

