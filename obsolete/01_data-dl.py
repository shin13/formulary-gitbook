import requests
from bs4 import BeautifulSoup
import os
import re
import pandas as pd
import numpy as np


# Append nones to list if is too short
# 用none補足list的長度
class TooLongError(ValueError):
    pass


def pad(seq, target_length, padding=None):
    """Extend the sequence seq with padding (default: None) so as to make
    its length up to target_length. Return seq. If seq is already
    longer than target_length, raise TooLongError.

    >>> pad([], 5, 1)
    [1, 1, 1, 1, 1]
    >>> pad([1, 2, 3], 7)
    [1, 2, 3, None, None, None, None]
    >>> pad([1, 2, 3], 2)
    ... # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    TooLongError: sequence too long (3) for target length 2

    """
    length = len(seq)
    if length > target_length:
        raise TooLongError("sequence too long ({}) for target length {}"
                           .format(length, target_length))
    seq.extend([padding] * (target_length - length))
    return seq


# read drug basic data
df = pd.read_excel('data.xlsx')

# data cleaning
cols = ['01藥品代碼', '07藥品狀態(N可用D停用)', '11藥理分類1', '12藥理分類2', '29DC註記']
for i in cols:
    df[i] = df[i].str.strip()
df = df[(df['01藥品代碼'].str.len() > 0) & (df['11藥理分類1'].str.len() > 0)]
df = df[(df['11藥理分類1'] != 'PHR') & (df['11藥理分類1'].str.len() < 5)]
df['12藥理分類2'].fillna('ZOTH', inplace=True)
df['12藥理分類2'] = df['12藥理分類2'].replace(
    'ZOTH', 'ZO-01-00').replace('MEDD', 'ZO-02-00')
df = df[df['07藥品狀態(N可用D停用)'] == 'N']
df['29DC註記'] = df['29DC註記'].fillna('')
df = df[(df['29DC註記'] == '') | (df['29DC註記'] == 3)]

# 生成資料夾
try:
    path = 'C:\\Users\\152551\\formulary-gitbook\\toc'
    # path = '/Users/shin/formulary/toc'
    os.mkdir(path)
except:
    pass
cat2_li = df['12藥理分類2'].unique().tolist()
for cat in cat2_li:
    if cat[-3] == '-':
        try:
            path = 'C:\\Users\\152551\\formulary-gitbook\\toc\\' + \
                cat[:3].lower() + '00-00\\'
            # path = '/Users/shin/formulary/toc/' + cat[:3].lower() + '00-00/'
            os.mkdir(path)
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
        except:
            pass
    elif (cat[-2:] != "00") & (len(cat) == 8):
        try:
            path = 'C:\\Users\\152551\\formulary-gitbook\\toc\\' + \
                cat[:3].lower() + '00-00\\' + cat[:6].lower() + '00\\'
            os.mkdir(path)
        except:
            pass
        try:
            path = 'C:\\Users\\152551\\formulary-gitbook\\toc\\' + \
                cat[:3].lower() + '00-00\\' + cat[:6].lower() + \
                '00\\' + cat.lower() + '\\'
            # path = '/Users/shin/formulary/toc/' + cat[:3].lower() + '00-00/' + cat[:6].lower() + '00/'+ cat.lower() + '/'
            os.mkdir(path)
        except:
            pass
    else:
        try:
            path = 'C:\\Users\\152551\\formulary-gitbook\\toc\\' + cat.lower() + '\\'
            # path = '/Users/shin/formulary/toc/' + cat.lower()
            os.mkdir(path)
        except:
            pass

# add path to each drug (to save markdown files)
toc1 = []
toc2 = []
toc3 = []
for i in df['12藥理分類2'].tolist():
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

df['drug_name'] = df['06藥品學名'].str.lower()
li = df['drug_name'].tolist()
new_li = []
for i in li:
    i = i.replace(' + ', '-')
    i = i.replace(' & ', '-')
    i = i.replace('+', '-')
    i = i.replace('/', '-')
    i = i.replace(' ', '_')
    new_li.append(i)
df['drug_name'] = new_li
df['name_md'] = df['drug_name'] + '.md'

# def func(row):
#     if pd.isna(row.toc2) & pd.isna(row.toc3):
#         string = ['toc', row['toc1'], row['name_md']]
#         return "\\".join(string)
#     elif pd.notna(row.toc3):
#         string = ['toc', row['toc1'], row['toc2'], row['toc3'], row['name_md']]
#         return "\\".join(string)
#     else:
#         string = ['toc', row['toc1'], row['toc2'], row['name_md']]
#         return "\\".join(string)

# df['url'] = df.apply(func, axis=1)
# df['line'] = '[' + df['06藥品學名'] + '](' + df['url'] +')'


def func2(row):
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


df['url2'] = df.apply(func2, axis=1)
df = df.sort_values(by=['12藥理分類2'])

# 爬蟲、資料處理、寫成markdown file、存在指定的資料夾
cat2_li = df['12藥理分類2'].unique().tolist()

# go through Category 2
for cat2 in cat2_li:
    df_cat2 = df[df['12藥理分類2'] == cat2]
    names = df_cat2['06藥品學名'].unique().tolist()
    # go through drug names under each Category 2
    for name in names:
        df_name = df_cat2[df_cat2['06藥品學名'] == name]
        df_name = df_name.sort_values(
            by=['01藥品代碼'], ascending=True).reset_index(drop=True)
        # find drug codes with a same drug name, and go through codes with a same drug name
        code_list = df_name['01藥品代碼'].tolist()
        df_name.set_index('01藥品代碼', inplace=True)
        # because drugs with a same drug name would be written in a same file, the saving path is the same
        filepath = df_name.iloc[0]['url2']
        with open(filepath, "w", encoding='utf-8') as f:
            title1 = '# ' + name + '\n\n'
            f.write(title1)
            for code in code_list:
                url = 'http://139.168.122.240/NIS/CommonMedication/DrugConsultation?DrugID=' + code
                html = requests.get(url)
                html.encoding = 'UTF-8'
                # 以 Beautiful Soup 解析 HTML 程式碼
                soup = BeautifulSoup(html.text, 'html.parser')
                pre = soup.find('pre', class_="pre_DrugMemo")
                text = pre.text
                # define desired replacements here
                rep = {'適應症': '切割', '副作用': '切割', '禁忌': '切割',
                       '【': '', '】': '', '：': '', '\n': '', '\r': ''}
                # use these three lines to do the replacement
                rep = dict((re.escape(k), v) for k, v in rep.items())
                # Python 3 renamed dict.iteritems to dict.items so use rep.items() for latest versions
                pattern = re.compile("|".join(rep.keys()))
                text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
                strings = text.split('切割')
                pad(strings, 7, padding='NA')
                titles = [None, '適應症', '副作用', '禁忌', None, None, None]
                df1 = pd.DataFrame(list(zip(titles, strings)), columns=[0, 1])

                # 讀取NIS藥物諮詢的表格只取有2個columns的
                # （因為第一個表格是交互作用有很多欄位、第二個表格是適應症只有1個欄位，需要另外處理）
                tables = pd.read_html(url)
                tbs = []
                for tb in tables:
                    if len(tb.columns) == 2:
                        df1 = df1.append(tb, ignore_index=True)
                    else:
                        pass

                # 修整合併之後的表格
                df1 = df1.dropna(subset=[0]).reset_index(drop=True)
                df1.fillna(value='N/A', inplace=True)

                # 移除適應症、副作用、禁忌欄位文字開頭的奇怪符號
                new = []
                for i in df1.iloc[:, 1].tolist():
                    if i[0:2] == ': ':
                        i = i[2:]
                        new.append(i)
                    elif i[0] == ':':
                        i = i[1:]
                        new.append(i)
                    elif i[0] == ' ':
                        i = i[1:]
                        new.append(i)
                    else:
                        i = i
                        new.append(i)
                data = [df1.iloc[:, 0].tolist(), new]
                df1 = pd.DataFrame(data).transpose()
                df1.columns = ['藥物代碼', code]

                # 將二階標題商品名與表格內容寫入文字檔
                prodname = df_name.loc[code, '04藥品英文名稱(商品名)']
                title2 = '## ' + prodname + '\n\n'
                f.write(title2)
                content = df1.to_markdown(index=0)
                f.write(content)
                f.write('\n\n')
