# Author Shin Li
# Update Gitbook formulary
# Make new md files, new summary, and push to GitHub

import subprocess
import os

# Ask the user if they have updated changelog.md
user_input = input('Have you updated changelog.md? (Y/N): ')

if user_input.upper() == 'Y':
    print('網頁版處方集更新開始')

    print('STEP 1 開始')
    print('STEP 1 執行中...')
    subprocess.run(['python', 'formulary_01_make-md.py'])
    print('STEP 1 完成')

    print('STEP 2 開始 Generate new SUMMARY.md')
    print('STEP 2 執行中...')
    # generate new SUMMARY.md in Windows
    # subprocess.run(['python', 'gitbook - auto - Y
    #                 summary.py', ' - o',
    #                 'C:\\Users\\152551\\formulary-gitbook'])

    # generate new SUMMARY.md in MacOS
    subprocess.run(['python', 'gitbook-auto-summary.py', '-o', '/Users/shin/Projects/formulary-gitbook'])

    # For MacOS, enter below line in terminal manually
    # python gitbook-auto-summary.py -o \/Users\/shin\/Projects\/formulary-gitbook

    print('STEP 3 完成')

    print('STEP 3 modify-summary 開始')
    print('STEP 3 執行中...')
    subprocess.run(['python', 'formulary_03_modify-summary.py'])
    print('STEP 3 完成')

    print('STEP 4 make_index 開始')
    print('STEP 4 執行中...')
    subprocess.run(['python', 'formulary_04_make_index.py'])
    print('STEP 4 完成')

    # remove toc\README.md at root directory
    try:
        os.remove('toc\\README.md')
    except OSError as e:
        print(f"Error: {e.strerror}")

    print('資料庫更新完成！')

else:
    print('請更新 changelog.md 再執行處方集更新。')
