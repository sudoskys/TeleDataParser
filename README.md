# Telegram Machine Learning Corpus Extraction

[![Python 3.*](https://img.shields.io/badge/Python-3.*-yellow.svg)](http://www.python.org/download/)

Machine learning corpus extractor.

Parses Json data files exported by Telegram.

- Extracting specific replies.
- Extracts specific statements.
- Filter support.
- Extract all.
- Support for word limit.
- Custom field length calculation.

Extract a user's speech for AI learning, and save your loved one's chat history.

At the moment, because I'm too lazy, I've **only** done the part of extracting the plain text corpus.

## Run

- Installation

Run `pip3 install -r requirements.txt` in the project directory

- Run

Configure `config.ini` to run `python3 main.py` to generate the data

## Performance

Number of outputs

- 100 w -> 28s
- 49w -> 12s

## Config

### Constructing classes

````python
from Core.Tool import TeleParser

Parser = TeleParser("JsonInput", "DataOutput", min_limit=5, max_limit=512)
dicts = Parser.get_all(lable="GIRL", showDate=False, ending="\n", uni_data=False)
print(dicts)
# See comments for yourself
# Returns: total number of writes, number of non-conforming skips, number of deleted, total number of signed messages
````

**TeleParser Api**

**__init__**(self,
json_path: str, out_path: str, min_limit: int = 5, max_limit: int =
512, Counter: str = 'chinese', filter_mode: str = False, filter: str =
'Not_need.txt')

```
:param json_path:input_directory
:param out_path:output
:param min_limit:min_count
:param max_limit:max_count
:param Counter:counter
:param filter_mode:type, True to keep only sentences with keywords, False to keep only sentences without keywords
:param filter:path to filter phrase file
:return: dict
```

**get_all**(self, lable: str, showDate=False, ending='\n', uni_data=False, no_id: list = None) -> dict

```
:param lable: the label
:param no_id: who not to receive (e.g. messages from service bots)
:param uni_data: whether to de-duplicate
:param ending: the suffix
:param showDate: whether to show the date
:return: dict
```

**get_all_reply**(self, showDate=True, ending='\n', uni_data=False) -> dict

```
:param uni_data: whether to de-duplicate
:param ending: the suffix
:param showDate: whether to show the date
:return: dict
```

**get_reply**(self, lable, target_id, showDate=True, ending='\n', uni_data=False) -> dict

```
:param showDate: whether to show the date
:param ending: the suffix
:param uni_data: whether to de-duplicate
:param lable: the name tag
:param target_id: the target ID, the one with user
:return: dict
```

**get_speech**(self, lable, target_id, showDate=True, ending='\n', uni_data=False) -> dict

```
:param uni_data: whether to de-duplicate
:param ending: the suffix
:param showDate: whether to attach a date
:param lable: the name tag
:param target_id: the target ID, the one with user
:return: dict
```

- hint method

**write_out**(self, speech: list, path: str, Wash: bool = False)

```
:param speech: list of phrases
:param path: the name of the output file
:param Wash: whether to de-duplicate
:return:
```

#### Length Gauge

class **Tester**(builtins.object)
Static methods defined here:

```
chinese(ask)
default(ask)
```

### Config File

````ini
; Sample configuration file
[user]
user = Someone
user_id = user114514


[path]
input = JsonInput
output = DataOutput
````

**Sample reference format**

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
      "from": "Someone",
      "from_id": "user2333",
      "reply_to_message_id": 271065,
      "text": "Hi,GOOD MORNING"
    }
  ]
}
```


![counter](https://count.getloli.com/get/@sudoskys-github-TeleDataParser?theme=moebooru)

### License

```lines
Use of this item for malicious purposes is not permitted.
This project is licensed under the Apache License
```