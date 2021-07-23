# 以下增加的是用來修改SUMMARY.md

import re

with open('SUMMARY.md', 'r') as f:
    contents = f.read()
    contents = contents.replace('\\', '/')
    contents = contents.replace('\./', '')

rep = dict({'[Readme]': '[首頁]', '[Index]': '[索引]',
            '[Changelog]': '[更新歷程]', '[Appendix]': '[附錄]', '[Links]': '[常用連結]'})
rep = dict((re.escape(k), v) for k, v in rep.items())
pattern = re.compile("|".join(rep.keys()))
text = pattern.sub(lambda m: rep[re.escape(m.group(0))], contents)

# Remove blank lines
text = re.sub(r'\n\s*\n', '\n', text)
with open('SUMMARY.md', 'w+') as f:
    f.write(text)

print('SUMMARY.md 自訂修改完成 :)')
