# -*- coding: utf-8 -*-
# @Time    : 8/13/22 12:34 PM
# @FileName: main.py
# @Software: PyCharm
# @Github    ：sudoskys


from Core.Tool import TeleParser
from configparser import ConfigParser

mew = ConfigParser()
mew.read('config.ini')
lable = mew.get('user', 'user')
target_id = mew.get('user', 'user_id')
inputDir = mew.get('path', 'input')
outDir = mew.get('path', 'output')

if __name__ == "__main__":
    Run = TeleParser(json_path=inputDir, out_path=outDir, min_limit=5, max_limit=100)  # , dislike="DISLIKE.bin")
    # dicts = Run.get_reply(lable, target_id, showDate=True)
    Run.get_all(lable="AS", showDate=False, ending="", uni_data=False)
