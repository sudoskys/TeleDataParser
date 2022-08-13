# TeleDataParser

[![Python 3.7](https://img.shields.io/badge/Python-3.7-yellow.svg)](http://www.python.org/download/) 



解析 Telegram 导出的 Json 数据文件，并提取某个用户的回复语料，便于AI学习 


Parse the json data file of telegram and extract the reply corpus of a certain user, which is convenient for AI learning

## Run

- 1

在项目目录运行 `pip3 install -r requirements.txt`


- 2

导出群组对话历史，并配置 `config.ini` 即可运行 `python3 main.py` 生成数据



## Todo

- [x] 初步的功能实现
- [x] 多源遍历提取
- [x] 实现数据处理可视化
- [ ] 多目标指定