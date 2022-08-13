# TeleDataParser

[![Python 3.7](https://img.shields.io/badge/Python-3.7-yellow.svg)](http://www.python.org/download/) 



解析 Telegram 导出的 Json 数据文件，并提取某个用户的回复语料，便于AI学习 


Parse the json data file of telegram and extract the reply corpus of a certain user, which is convenient for AI learning

## Run

- 1

在项目目录运行 `pip3 install -r requirements.txt`


- 2

导出群组对话历史，查询用户的 `from_id` ，并配置 `config.ini` 即可运行 `python3 main.py` 生成数据


**参考格式样本**

```json
{
 "name": "Unknown | Private",
 "type": "private_supergroup",
 "id": 11451418180,
 "messages": [
  {
   "id": 1,
   "type": "message",
   "date": "2022-01-28T01:35:46",
   "date_unixtime": "1643333746",
   "edited": "2022-05-15T14:16:08",
   "edited_unixtime": "1652624168",
   "from": "萨日朗",
   "from_id": "user2333",
   "text": "为了你我要变成狼人模样"
  }]
   }
```


## Todo

- [x] 初步的功能实现
- [x] 多源遍历提取
- [x] 实现数据处理可视化
- [ ] 多目标指定


## 性能测试

```
─────────────── 完成了一个目标数据的转换,用时:1.3424687385559082 ───────────────
有回复的总处理数:16204,输出于:xxxx
写入了:11269,跳过了:4620,被删除消息条:315
```
