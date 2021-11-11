#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re
import pandas as pd


# In[2]:


os.rename('SUMMARY.md', 'SUMMARY_old.md')


# In[3]:


# Remove lines of pages, keep toc contents

# list to store file lines
lines = []

# Read file
with open('SUMMARY_old.md', 'r', encoding='big5hkscs') as f:
    # read an store all lines into list
    lines = f.readlines()

# Write file
with open('toc.md', 'w', encoding='utf8') as f:
    # iterate each line
    for number, line in enumerate(lines):
        # note list index starts from 0
        if number not in list(range(8)):
            f.write(line)


# In[4]:


start_lines = ['# Table of contents\n',
               '* [首頁](README.md)\n', '* [目錄](toc/README.md)\n']
end_lines = ['* [附錄](appendix.md)\n', '* [索引](index.md)\n',
             '* [常用連結](links.md)\n', '* [更新歷程](changelog.md)']
toc_lines = []

with open('toc.md', 'r', encoding='utf8') as f:
    # read an store all lines into list
    toc_lines = f.readlines()

with open('SUMMARY_test.md', 'w', encoding='utf8') as f:
    f.writelines(start_lines)
    f.writelines(toc_lines)
    f.writelines(end_lines)
    f.write('\n')


# In[5]:


# Replace slash characters

with open('SUMMARY_test.md', 'r', encoding='utf8') as f:
    contents = f.read()

contents = contents.replace('\\', '/')

with open('SUMMARY_test.md', 'w', encoding='utf8') as f:
    f.write(contents)


# In[6]:


cat_list = pd.read_excel('cat_ref.xlsx')
cat_list['code'] = '[' + cat_list['code'].astype(str) + ']'
cat_list['name'] = '[' + cat_list['name'].astype(str) + ']'

with open('SUMMARY_test.md', 'r+', encoding="utf-8") as f:
    contents = f.read()

rep = dict(zip(cat_list['code'], cat_list['name']))
rep = dict((re.escape(k), v) for k, v in rep.items())
pattern = re.compile("|".join(rep.keys()))
text = pattern.sub(lambda m: rep[re.escape(m.group(0))], contents)
# Remove blank lines
text = re.sub(r'\n\s*\n', '\n', text)

text = text.replace('[Alanine 8.2% And Glutamine 13.64%]',
                    '[Alanine And Glutamine]')
text = text.replace('alanine_8.2%_and_glutamine_13.64%.md',
                    'alanine_and_glutamine.md')
try:
    os.rename(r'C:\Users\152551\formulary-gitbook\toc\nu-00-00\nu-04-00\nu-04-01\alanine_8.2%_and_glutamine_13.64%.md',
              r'C:\Users\152551\formulary-gitbook\toc\nu-00-00\nu-04-00\nu-04-01\alanine_and_glutamine.md')
except:
    pass
with open('SUMMARY_test.md', 'w', encoding='utf-8') as f:
    f.write(text)


# In[7]:


bad_words = ['[Readme]']

with open('SUMMARY_test.md', 'r', encoding='utf8') as oldfile, open('SUMMARY.md', 'w', encoding='utf8') as newfile:
    for line in oldfile:
        if not any(bad_word in line for bad_word in bad_words):
            newfile.write(line)


# In[8]:


lst = ['SUMMARY_old.md', 'toc.md', 'SUMMARY_test.md']
for i in lst:
    os.remove(i)
