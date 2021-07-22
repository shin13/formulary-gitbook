# 以下增加的是用來修改SUMMARY.md

import re
import pandas as pd

with open('SUMMARY.md', 'rb') as f:
    contents = f.read().decode('big5hkscs')
    contents = contents.replace('\\', '/')
    contents = contents.replace('./', '')

cat_list = pd.read_excel('cat_ref.xlsx')
cat_list['code'] = '[' + cat_list['code'].astype(str) + ']'
cat_list['name'] = '[' + cat_list['name'].astype(str) + ']'

rep = dict(zip(cat_list['code'], cat_list['name']))
rep = dict((re.escape(k), v) for k, v in rep.items())
pattern = re.compile("|".join(rep.keys()))
text = pattern.sub(lambda m: rep[re.escape(m.group(0))], contents)

rep = dict({'[Readme]': '[首頁]', '[Index]': '[索引]',
            '[Changelog]': '[更新歷程]', '[Appendix]': '[附錄]', '[Links]': '[常用連結]'})
rep = dict((re.escape(k), v) for k, v in rep.items())
pattern = re.compile("|".join(rep.keys()))
text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)

with open('SUMMARY.md', 'w') as f:
    f.write(text)

print('SUMMARY.md 自訂修改完成 :) ')

