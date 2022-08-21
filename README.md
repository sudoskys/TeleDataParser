# TeleDataParser

[![Python 3.7](https://img.shields.io/badge/Python-3.7-yellow.svg)](http://www.python.org/download/)

解析 Telegram 导出的 Json 数据文件，并提取某个用户的语料发言，便于AI学习 ,也可以保存你心爱之人的聊天记录

Parse the json data file of telegram and extract the corpus of a certain user, which is convenient for AI learning

## Run

- 安装

在项目目录运行 `pip3 install -r requirements.txt`

- 运行

导出群组对话历史，查询用户的 `from_id` ，并配置 `config.ini` 即可运行 `python3 main.py` 生成数据

## Config

### Python？

````python
from Core.Tool import TeleParser

total_num, skip_num, delete_num, all_num = TeleParser(inputDir, outDir, min_limit=5, max_limit=512).get_speech(lable, target_id,
                                                                                            showDate=False)
# 传入：|数据文件夹，输出文件夹|标签，目标用户的 user_id (user114514),showDate是否输出消息日期|
# 返回：总写入数，不符合要求跳过数，被删除数目，总署名消息数目
````

**TeleParser Api**

| 自身参数       | 描述       |
|------------|----------|
| json_path, | 数据文件目录   |
| out_path,  | 输出文件目录   |
| max_limit, | 语料单行限制长度 |
| min_limit, | 语料单行限制长度 |

| Api        | Api                                  | 描述                    |
|------------|--------------------------------------|-----------------------|
| get_speech | lable标签, target_id目标,showDate:是否显示日期 |获取用户的发言文本             |
| get_reply  | lable标签, target_id目标,showDate:是否显示日期 |获取用户的回复文本与被回复的文本      |
|get_all_reply| lable标签, target_id目标,showDate:是否显示日期 |获取语料文件夹内全部回复，以群组id区分  |

### Ini？

````ini
; Sample configuration file
[user]
user = Someone
user_id = user1136785287


[path]
input = JsonInput
output = DataOutput
````

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
      "reply_to_message_id": 271065,
      "text": "为了你我要变成狼人模样"
    }
  ]
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

### 注意

````
已经在 .gitignore 注明了不推送 json 和默认配置文件夹的所有文件

默认字符限制是512,如果提高限制可以自己更改 TeleParser 的构建参数
````

-----

#### Support

如果你感觉这对你有帮助，可以试着我赞助我一点～

[![s](https://img.shields.io/badge/Become-sponsor-DB94A2)](https://dun.mianbaoduo.com/@Sky0717)