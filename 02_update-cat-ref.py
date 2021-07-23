# Update reference of category 2 names

import pandas as pd

# read drug basic data
df = pd.read_excel('data.xlsx')

# data cleaning
cols = ['01藥品代碼', '07藥品狀態(N可用D停用)', '11藥理分類1', '12藥理分類2', '29DC註記']
for i in cols:
    df[i] = df[i].str.strip()
df = df[(df['01藥品代碼'].str.len() > 0) & (df['11藥理分類1'].str.len() > 0)]
df = df[(df['11藥理分類1'] != 'PHR') & (df['11藥理分類1'].str.len() < 5)]
df['12藥理分類2'].fillna('ZOTH', inplace=True)
df['12藥理分類2'] = df['12藥理分類2'].replace('ZOTH','ZO-01-00').replace('MEDD', 'ZO-02-00')
df = df[df['07藥品狀態(N可用D停用)'] == 'N'] 
df['29DC註記'] = df['29DC註記'].fillna('')
df = df[(df['29DC註記'] == '') | (df['29DC註記'] == 3)]

cat2_list = df['12藥理分類2'].sort_values().unique().tolist()
li = []
for i in cat2_list:
    i = i.lower()
    li.append(i)
cat2_list = li

df1 = pd.DataFrame(cat2_list, columns=['code'])
ref = pd.read_excel('cat_ref.xlsx')
df2 = df1.merge(ref, on='code', how='outer')
# 可以寫個判斷式看是哪個沒有中文說明
df2.to_excel('new_cat_ref.xlsx', index=0)