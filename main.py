# -*- coding: utf-8 -*-
# @Time    : 8/13/22 12:34 PM
# @FileName: main.py
# @Software: PyCharm
# @Github    ：sudoskys

# 已经在 .gitignore 注明了不推送 json 和默认配置文件夹的所有文件

from Core.Tool import TeleParser
from configparser import ConfigParser

mew = ConfigParser()
mew.read('config.ini')
lable = mew.get('user', 'user')
target_id = mew.get('user', 'user_id')
inputDir = mew.get('path', 'input')
outDir = mew.get('path', 'input')

if __name__ == "__main__":
    total_num, skip_num, delete_num, all_num = TeleParser(inputDir, outDir, 512).app_run(lable, target_id)