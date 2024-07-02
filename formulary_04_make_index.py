# -*- coding: utf-8 -*-

import pandas as pd


df = pd.read_excel('formulary2.xlsx')

# 定义 URL 前缀
url_prefix = "https://shin13.gitbook.io/formulary/toc/"

# 创建新的 'url' 列，利用 apply 方法逐行生成 URL，根据 toc3 是否为 None 添加不同的 URL 结构
df['url'] = df.apply(
    lambda row: f"{url_prefix}{row['toc1']}/{row['toc2']}/{row['drug_name']}"
    if pd.isna(row['toc3']) else
    f"{url_prefix}{row['toc1']}/{row['toc2']}/{row['toc3']}/{row['drug_name']}",
    axis=1
)

# Add a new column "1st_letter" using the first letter of "商品學名"
df['1st_letter'] = df['商品學名'].str[0]

grouped = df.sort_values('商品學名').groupby('1st_letter')

with open('index1.md', 'w', encoding='utf-8') as file:
    file.write("# 索引\n\n")
    for first_letter, first_letter_df in grouped:
        file.write(f"## {first_letter}\n")
        grouped_again = first_letter_df.groupby('商品學名')
        for 學名, grouped_again_df in grouped_again:
            file.write(f"* {學名}\n")
            # print(grouped_again_df)
            grouped_again_df = grouped_again_df.sort_values('商品英文名稱')
            for _, row in grouped_again_df.iterrows():
                file.write("  " + f"* [{row['商品英文名稱']}]({row['url']})\n")
