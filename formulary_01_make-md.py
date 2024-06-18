#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
import numpy as np


# In[19]:


# read drug basic data
df1 = pd.read_excel('1.藥品基本檔.xlsx')  # 請先開EXCEL把全形逗號換成半形逗號！
df2 = pd.read_excel('2.藥物諮詢.xlsx')  # 請先開EXCEL把全形逗號換成半形逗號！
# exclude = pd.read_excel('exclude.xlsx')


# In[20]:


# keep [Rx_o]
df1['藥局內部溝通MEMO'] = df1['藥局內部溝通MEMO'].fillna('xx')
df1_concate = df1[df1['藥局內部溝通MEMO'].str.contains('Rx_o')]


# In[21]:


# exclude [Rx_x]
df1 = df1[~df1['藥局內部溝通MEMO'].str.contains('Rx_x')]


# In[22]:


# drug selection
df1 = df1[(df1['藥品狀態'] == '可用')]


# In[23]:


# exclude DC comments
exclude_list = ['廠商缺貨,可查類似藥', '停用', '廠商缺貨', '停用,可查類似藥']
df1 = df1[~df1['DC註記'].isin(exclude_list)]


# In[24]:


# # exclude drugs in exclusion list
# # 之後用 [Rx_x] 取代
# exclude_list = exclude.iloc[:,0].tolist()
# df1 = df1[~df1['藥品代碼'].isin(exclude_list)]


# In[25]:


# exclude empty & weird category 2
df1 = df1.dropna(subset=['藥理分類2'])
exclude_list2 = ['MEDD', 'ZOTH', 'PHR']
df1 = df1[~df1['藥理分類2'].isin(exclude_list2)]


# In[26]:


# concate [Rx_o] and drop duplicates
df1 = pd.concat([df1, df1_concate], ignore_index=True, sort=False)
df1 = df1.drop_duplicates(subset=['藥品代碼'])


# In[27]:


df1['DC註記'] = df1['DC註記'].replace('停用', '')
df1['DC註記'] = df1['DC註記'].replace('停用,可查類似藥', '')


# In[28]:


df1 = df1[['藥品代碼', '商品英文名稱', '商品學名', '藥理分類1', '藥理分類2', 'DC註記']]
df2 = df2[['藥品代碼', '適應症', '用法用量',
           '肝功能異常(Y/N)', '腎功能異常(Y/N)', '禁忌', '副作用', '孕期用藥建議', '哺乳期用藥建議']]
df = df1.merge(df2, on='藥品代碼', how='left')


# In[29]:


df = df.rename(columns={'藥品代碼': 'TAH Drug Code', '適應症': 'Indications', '用法用量': 'Dosing', '禁忌': 'Contraindications', '副作用': 'Adverse Effects',
                        '肝功能異常(Y/N)': 'Hepatic Impairment', '腎功能異常(Y/N)': 'Renal Impairment', '孕期用藥建議': 'Pregnancy', '哺乳期用藥建議': 'Lactation'})
df = df.replace(np.nan, 'No Data')
df['DC註記'] = df['DC註記'].replace('No Data', '')
df['DC註記'] = df['DC註記'].replace('臨採藥,請通知藥局外購', '臨採')


# In[30]:


df = df.replace('無需調整劑量', 'Dose adjustment not necessary')
df = df.replace('需調整劑量', 'Dose adjustment required')
df = df.replace('Uknown 沒有資料', 'Unknown')
df = df.replace('Unknown 沒有資料', 'Unknown')
df = df.replace('Contraindicated 哺乳期使用禁忌', 'Contraindicated')
df = df.replace('No (Limited) Human Data - Probably Compatible 無(很少)資料 - 可使用',
                'No (Limited) Human Data - Probably Compatible')
df = df.replace('No (Limited) Human Data – Potential Toxicity(Mother) 無(很少)資料 – 避免使用(母體)',
                'No (Limited) Human Data – Potential Toxicity(Mother)')
df = df.replace('No (Limited) Human Data - Potential Toxicity 無(很少)資料 - 避免使用',
                'No (Limited) Human Data - Potential Toxicity')
df = df.replace('Compatible 哺乳時可使用', 'Compatible')
df = df.replace('Hold Breast Feeding 暫停哺乳', 'Hold Breast Feeding')


# In[31]:


df['Pregnancy'] = df['Pregnancy'].str.title()


# In[32]:


df['Pregnancy'] = df['Pregnancy'].str.replace('3 Rd', '3rd')
df['Pregnancy'] = df['Pregnancy'].str.replace('2Nd', '2nd')
df['Pregnancy'] = df['Pregnancy'].str.replace('1St', '1st')
df['Pregnancy'] = df['Pregnancy'].str.replace('In', 'in')
df['Pregnancy'] = df['Pregnancy'].str.replace('And', 'and')


# In[33]:


df.to_excel('formulary.xlsx', index=0)


# In[34]:


# remove toc folder

import os
import sys
import shutil

# Get directory name
mydir = 'C:\\Users\\152551\\formulary-gitbook\\toc'

try:
    shutil.rmtree(mydir)
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))


# In[35]:


# make file directories
import os

try:
    path = 'C:\\Users\\152551\\formulary-gitbook\\toc'
    # path = '/Users/shin/formulary/toc'
    os.mkdir(path)
    mdpath = path + '\\' + 'README.md'
    with open(mdpath, 'w') as f:
        pass
except:
    pass

cat2_li = df['藥理分類2'].unique().tolist()
for cat in cat2_li:
    if cat[-3] == '-':
        try:
            path = 'C:\\Users\\152551\\formulary-gitbook\\toc\\' + \
                cat[:3].lower() + '00-00\\'
            # path = '/Users/shin/formulary/toc/' + cat[:3].lower() + '00-00/'
            os.mkdir(path)
            mdpath = path + 'README.md'
            try:
                with open(mdpath, 'w') as f:
                    pass
            except:
                pass
        except:
            pass
    else:
        pass

for cat in cat2_li:
    if cat[-2:] == "00":
        try:
            path = 'C:\\Users\\152551\\formulary-gitbook\\toc\\' + \
                cat[:3].lower() + '00-00\\' + cat.lower() + '\\'
            # path = '/Users/shin/formulary/toc/' + cat[:3].lower() + '00-00/' + cat.lower() + '/'
            os.mkdir(path)
            mdpath = path + 'README.md'
            try:
                with open(mdpath, 'w') as f:
                    pass
            except:
                pass
        except:
            pass
    elif (cat[-2:] != "00") & (len(cat) == 8):
        try:
            path = 'C:\\Users\\152551\\formulary-gitbook\\toc\\' + \
                cat[:3].lower() + '00-00\\' + cat[:6].lower() + '00\\'
            os.mkdir(path)
            mdpath = path + 'README.md'
            try:
                with open(mdpath, 'w') as f:
                    pass
            except:
                pass
        except:
            pass
        try:
            path = 'C:\\Users\\152551\\formulary-gitbook\\toc\\' + \
                cat[:3].lower() + '00-00\\' + cat[:6].lower() + \
                '00\\' + cat.lower() + '\\'
            # path = '/Users/shin/formulary/toc/' + cat[:3].lower() + '00-00/' + cat[:6].lower() + '00/'+ cat.lower() + '/'
            os.mkdir(path)
            mdpath = path + 'README.md'
            try:
                with open(mdpath, 'w') as f:
                    pass
            except:
                pass
        except:
            pass
    else:
        try:
            path = 'C:\\Users\\152551\\formulary-gitbook\\toc\\' + cat.lower() + '\\'
            # path = '/Users/shin/formulary/toc/' + cat.lower()
            os.mkdir(path)
            mdpath = path + 'README.md'
            try:
                with open(mdpath, 'w') as f:
                    pass
            except:
                pass
        except:
            pass


# In[36]:


# add path to each drug (to save markdown files)
toc1 = []
toc2 = []
toc3 = []
for i in df['藥理分類2'].tolist():
    if i[-2:] == '00':
        toc1.append(i[:2].lower() + r'-00-00')
        toc2.append(i.lower())
        toc3.append(np.nan)
    elif (i[-2:] != "00") & (len(i) == 8):
        toc1.append(i[:2].lower() + r'-00-00')
        toc2.append(i[:5].lower() + r'-00')
        toc3.append(i.lower())
    else:
        toc1.append(i.lower())
        toc2.append(np.nan)
        toc3.append(np.nan)
df['toc1'] = toc1
df['toc2'] = toc2
df['toc3'] = toc3

df['drug_name'] = df['商品學名'].str.lower()
li = df['drug_name'].tolist()
new_li = []
for i in li:
    i = i.replace(' + ', '_and_')
    i = i.replace(' & ', '_and_')
    i = i.replace('+', '_and_')
    i = i.replace('/', '-')
    i = i.replace(' ', '_')
    new_li.append(i)
df['drug_name'] = new_li
df['name_md'] = df['drug_name'] + '.md'


# In[37]:


def combine_str(row):
    if pd.isna(row.toc2) & pd.isna(row.toc3):
        string = ['C:\\Users\\152551\\formulary-gitbook\\toc',
                  row['toc1'], row['name_md']]
#         string = ['/Users/shin/formulary/toc', row['toc1'], row['name_md']]
        return "\\".join(string)
    elif pd.notna(row.toc3):
        string = ['C:\\Users\\152551\\formulary-gitbook\\toc',
                  row['toc1'], row['toc2'], row['toc3'], row['name_md']]
#         string = ['/Users/shin/formulary/toc', row['toc1'], row['toc2'], row['toc3'], row['name_md']]
        return "\\".join(string)
    else:
        string = ['C:\\Users\\152551\\formulary-gitbook\\toc',
                  row['toc1'], row['toc2'], row['name_md']]
#         string = ['/Users/shin/formulary/toc', row['toc1'], row['toc2'], row['name_md']]
        return "\\".join(string)


df['url'] = df.apply(combine_str, axis=1)
df = df.sort_values(by=['藥理分類2'])


# In[38]:


df.to_excel('formulary2.xlsx', index=0)


# In[39]:


# write markdown files and save
cat2_li = df['藥理分類2'].unique().tolist()


# In[40]:


# go through Category 2
for cat2 in cat2_li:
    df_cat2 = df[df['藥理分類2'] == cat2]

    # go through drug names under each Category 2
    names = df_cat2['商品學名'].unique().tolist()
    for name in names:
        df_name = df_cat2[df_cat2['商品學名'] == name]
        df_name = df_name.sort_values(
            by=['TAH Drug Code'], ascending=True).reset_index(drop=True)
        # find drug codes with a same drug name, and go through codes with a same drug name
        code_list = df_name['TAH Drug Code'].tolist()
        df_name.set_index('TAH Drug Code', inplace=True)
        # because drugs with a same drug name would be written in a same file, the saving path is the same
        filepath = df_name.iloc[0]['url']
        with open(filepath, "w", encoding='utf-8') as f:
            title1 = '# ' + name + '\n\n'
            f.write(title1)

            for code in code_list:
                prodname = df_name.loc[code, '商品英文名稱']
                title2 = '## ' + prodname + '\n\n'
                f.write(title2)

                note = df_name.loc[code, 'DC註記']
                if len(note) == 2:
                    title3 = '##### ' + note + '\n\n'
                    f.write(title3)
                else:
                    pass

                df_tb = df_name.loc[code,
                                    'Indications':'Lactation'].reset_index()
                col_name = '[' + code + \
                    '](https://www.tahsda.org.tw/drugs/hissearch.php?drug_code=' + code + ')'
                df_tb.columns = ['TAH Drug Code', col_name]

                # 20240618 新增UpToDate查詢連結

                # 定義特定名字及其替代名字
                special_replacements = {
                    "acetaminophen": "acetaminophen-paracetamol",
                    "propacetamol": "acetaminophen-paracetamol"
                }

                search_name = name.replace(' ', '-').lower()

                # 檢查特殊替換規則
                if search_name in special_replacements:
                    search_name = special_replacements[search_name]

                keyword = f"{search_name}-drug-information"

                # 要新增的列資料，這邊直接用列名位置
                new_row = pd.DataFrame([{
                    df_tb.columns[0]: "More Info",
                    df_tb.columns[1]: f"[UpToDate](https://www.uptodate.com/contents/{keyword})"
                }])

                # 使用 pd.concat 來附加新 row
                df_tb = pd.concat([df_tb, new_row], ignore_index=True)

                content = df_tb.to_markdown(index=0)
                f.write(content)

                f.write('\n\n')


# In[ ]:


# In[ ]:
