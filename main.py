# Author Shin Li
# Update Gitbook formulary
# Make new md files, new summary, and push to GitHub

import subprocess

print('網頁版處方集更新開始')
print('STEP 1 開始')
subprocess.run(['python', 'formulary_01_make-md.py'])

print('STEP 2 開始')
# generate new SUMMARY.md
subprocess.run(['python', 'gitbook-auto-summary.py', '-o',
                'C:\\Users\\152551\\formulary-gitbook'])

print('STEP 3 開始')
subprocess.run(['python', 'formulary_03_modify-summary.py'])

print('資料庫更新完成！')
print('請更新changelog.md！')
