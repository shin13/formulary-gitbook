import pandas as pd
import requests

# 读取Excel文件
df = pd.read_excel('summary_data.xlsx')  # 这里替换成你的Excel文件路径

def check_link(url):
    try:
        response = requests.head(url, allow_redirects=True, verify=False)
        # 检查状态码并返回最终的重定向URL
        if response.status_code == 200:
            final_url = response.url
        else:
            final_url = 'N/A'
        return response.status_code, final_url
    except requests.exceptions.RequestException as e:
        return f"Error: {e}", 'N/A'

# 应用 check_link 函数到 UpToDate_link 列，并拆分结果
df[['Status', 'Final_URL']] = df['UpToDate_link'].apply(lambda url: pd.Series(check_link(url)))

# 输出结果
print(df)

# 如果需要将检查结果保存到新的Excel文件
df.to_excel('checked_links.xlsx', index=False)
