# -*- coding: utf-8 -*-
# @Time    : 8/13/22 12:34 PM
# @FileName: Tool.py
# @Software: PyCharm
# @Github    ：sudoskys

import json
import time
import os
from rich.progress import track
from rich.console import Console


class TeleParser(object):
    def __init__(self, json_path, out_path, min_limit=5, max_limit=512):
        """
        json_path:data Dir
        len_limit:写入的回复和问题不能超过多少，超过就跳过
        :return: banned method
        """
        self.out_path = os.getcwd() + "/" + out_path
        self.input_path = os.getcwd() + "/" + json_path
        if not os.path.exists(self.input_path):
            os.makedirs(self.input_path)
        if not os.path.exists(self.out_path):
            os.makedirs(self.out_path)
        self.tg_import = [self.input_path + "/" + pos_json for pos_json in os.listdir(self.input_path) if
                          pos_json.endswith('.json')]
        if len(self.tg_import) == 0:
            raise RuntimeError('No Data in Input Dir! Which Path is:' + self.input_path)
        self.min_limit = min_limit
        self.console = Console(color_system='256', style=None)
        self.len_limit = max_limit

    @staticmethod
    def extract_chinese(txt):
        import re
        pattern = re.compile("[\u4e00-\u9fa5]")
        return "".join(pattern.findall(txt))

    @staticmethod
    def data_convert(tg, key="id"):
        """
        tg:从tg的json文件转换出的字典数据
        :return: 以id为键的新字典，取代从0排序的数据，用于回复查找
        """
        new_json = {}
        for json_item in track(tg, description='转换数据...'):
            if not json_item.get(key) is None:
                new_json[json_item.get(key)] = json_item
        return new_json

    @staticmethod
    def test_obj(aas):
        """
        aas:需要验证和去换行符的数据，清洗
        :return: 数据或False
        """
        if isinstance(aas, str) and aas:
            return aas.strip()
        else:
            return False

    def get_speech(self, lable, target_id, showDate=True):
        """
        lable:名字标签
        target_id:目标ID,带user的那个
        :return: wr lines total, skip num, deleted item num, all_items_num
        """
        user = lable + "_" + target_id
        dir_path = self.out_path + "/Speech/" + user + "/"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        out = dir_path + user + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + "_out.txt"
        self.console.print("开始提取" + lable + "的回复，MIN:" + str(self.min_limit) + ",MAX:" + str(self.len_limit),
                           style='blue')
        count = 0
        uncount = 0
        deletecount = 0
        total = 0
        wr = open(out, 'w')
        e1 = time.time()
        for data_path in self.tg_import:
            with open(data_path, 'r') as files:
                item_count = 0
                # tg_data = ast.literal_eval(json.dumps(files.read()))
                import re
                pattern = re.compile(r'\s([^"]+)(webm|webp|tgs)')
                data = re.sub(pattern, '0', files.read())
                tg_data = json.loads(data)
                mge = tg_data.get("messages")
                # print(json.dumps(tg_data, indent=4))
                cv_json = TeleParser.data_convert(mge)
                # --------
                for id_item in track(cv_json.values(), description='提取数据...'):
                    # replay = id_item.get("reply_to_message_id")
                    if id_item.get("from_id") == target_id:
                        total += 1
                        # asker = cv_json.get(replay)
                        if id_item:
                            ask = TeleParser.test_obj(id_item.get("text"))
                            if showDate:
                                ask_time = TeleParser.test_obj(id_item.get("date")) + "\n"
                            else:
                                ask_time = ""
                            if ask:
                                # time.sleep(0.1)
                                ask = ask.replace("\n", ",")
                                ask_len = len(TeleParser.extract_chinese(ask))
                                if int(self.len_limit) > ask_len > int(self.min_limit):
                                    info = (ask_time + ask + "\n\n")
                                    count += 1
                                    item_count += 1
                                    # print(info)
                                    wr.write(info)
                                else:
                                    uncount += 1
                            else:
                                uncount += 1
                        else:
                            deletecount += 1

                self.console.rule(
                    "[bold blue]完成了" + os.path.split(data_path)[1] + "目标数据的转换" + ',成功输出了:' + str(item_count))
        e2 = time.time()
        self.console.rule('[bold blue]提取用时:' + str(e2 - e1))
        wr.flush()
        wr.close()
        self.console.print("有回复的总处理数:" + str(total) + ",输出于:" + out, style='blue')
        self.console.print("写入了:" + str(count) + ",跳过了:" + str(uncount), style='blue')
        return count, uncount, deletecount, total
        # console.rule("[bold blue]完成提取")

    def get_all_reply(self, showDate=True):
        """
        :param showDate: is show date
        :return:
        """
        dir_path = self.out_path + "/Group/"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        # out = dir_path + user + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + "_out.txt"
        self.console.print("开始提取数据目录中的所有成员的回复链条，MIN:" + str(self.min_limit) + ",MAX:" + str(self.len_limit),
                           style='blue')
        total = 0
        deletecount = 0
        count = 0
        uncount = 0
        item_count = 0
        for data_path in self.tg_import:
            with open(data_path, 'r') as files:
                import re
                pattern = re.compile(r'\s([^"]+)(webm|webp|tgs)')
                data = re.sub(pattern, '0', files.read())
                tg_data = json.loads(data)
                GroupId = tg_data.get("id")
                OutPath = dir_path + str(GroupId) + "_out.txt"
                mge = tg_data.get("messages")
                wr = open(OutPath, 'w')
                e1 = time.time()
                userDict = TeleParser.data_convert(mge, key="from_id")
                # print(json.dumps(userDict, indent=4))
                cv_json = TeleParser.data_convert(mge)
                for user_id in track(userDict.keys(), description='提取数据...'):
                    for id_item in cv_json.values():
                        replay = id_item.get("reply_to_message_id")
                        if replay and id_item.get("from_id") == user_id:
                            total += 1
                            asker = cv_json.get(replay)
                            # 判断消息是不是存在
                            if asker:
                                ask = TeleParser.test_obj(asker.get("text"))
                                ans = TeleParser.test_obj(id_item.get("text"))
                                if showDate:
                                    ask_time = TeleParser.test_obj(id_item.get("date")) + "\n"
                                else:
                                    ask_time = ""
                                if ans and ask:
                                    # time.sleep(0.1)
                                    ask = ask.replace("\n", ",")
                                    ans = ans.replace("\n", ",")
                                    ask_len = len(TeleParser.extract_chinese(ask))
                                    ans_len = len(TeleParser.extract_chinese(ans))
                                    if self.len_limit > ask_len > self.min_limit and self.len_limit > ans_len > self.min_limit:
                                        info = (ask_time + ask + "\n" + ans + "\n\n")
                                        count += 1
                                        item_count += 1
                                        # print(info)
                                        wr.write(info)
                                    else:
                                        uncount += 1
                                else:
                                    uncount += 1
                            else:
                                deletecount += 1

                self.console.rule(
                        "[bold blue]完成了" + os.path.split(data_path)[1] + "目标数据的转换" + ',成功输出了:' + str(item_count))
                e2 = time.time()
                self.console.rule('[bold blue]提取用时:' + str(e2 - e1))
                wr.flush()
                wr.close()
                self.console.print("有回复的总处理数:" + str(total) + ",输出于:" + OutPath, style='blue')
                self.console.print("写入了:" + str(count) + ",跳过了:" + str(uncount) + ",被删除消息条:" + str(deletecount),
                                       style='blue')
                return count, uncount, deletecount, total

    def get_reply(self, lable, target_id, showDate=True):
        """
        lable:名字标签
        target_id:目标ID,带user的那个
        :return: wr lines total, skip num, deleted item num, all_items_num
        """
        user = lable + "_" + target_id
        dir_path = self.out_path + "/Reply/" + user + "/"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        out = dir_path + user + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + "_out.txt"
        self.console.print("开始提取" + lable + "的回复，MIN:" + str(self.min_limit) + ",MAX:" + str(self.len_limit),
                           style='blue')
        count = 0
        uncount = 0
        deletecount = 0
        total = 0
        wr = open(out, 'w')
        e1 = time.time()
        for data_path in self.tg_import:
            with open(data_path, 'r') as files:
                item_count = 0
                # tg_data = ast.literal_eval(json.dumps(files.read()))
                import re
                pattern = re.compile(r'\s([^"]+)(webm|webp|tgs)')
                data = re.sub(pattern, '0', files.read())
                tg_data = json.loads(data)
                mge = tg_data.get("messages")
                # print(json.dumps(tg_data, indent=4))
                cv_json = TeleParser.data_convert(mge)
                # --------
                for id_item in track(cv_json.values(), description='提取数据...'):
                    replay = id_item.get("reply_to_message_id")
                    if replay and id_item.get("from_id") == target_id:
                        total += 1
                        asker = cv_json.get(replay)
                        # 判断消息是不是存在
                        if asker:
                            ask = TeleParser.test_obj(asker.get("text"))
                            ans = TeleParser.test_obj(id_item.get("text"))
                            if showDate:
                                ask_time = TeleParser.test_obj(id_item.get("date")) + "\n"
                            else:
                                ask_time = ""
                            if ans and ask:
                                # time.sleep(0.1)
                                ask = ask.replace("\n", ",")
                                ans = ans.replace("\n", ",")
                                ask_len = len(TeleParser.extract_chinese(ask))
                                ans_len = len(TeleParser.extract_chinese(ans))
                                if self.len_limit > ask_len > self.min_limit and self.len_limit > ans_len > self.min_limit:
                                    info = (ask_time + ask + "\n" + ans + "\n\n")
                                    count += 1
                                    item_count += 1
                                    # print(info)
                                    wr.write(info)
                                else:
                                    uncount += 1
                            else:
                                uncount += 1
                        else:
                            deletecount += 1

                self.console.rule(
                    "[bold blue]完成了" + os.path.split(data_path)[1] + "目标数据的转换" + ',成功输出了:' + str(item_count))
        e2 = time.time()
        self.console.rule('[bold blue]提取用时:' + str(e2 - e1))
        wr.flush()
        wr.close()
        self.console.print("有回复的总处理数:" + str(total) + ",输出于:" + out, style='blue')
        self.console.print("写入了:" + str(count) + ",跳过了:" + str(uncount) + ",被删除消息条:" + str(deletecount), style='blue')
        return count, uncount, deletecount, total
        # console.rule("[bold blue]完成提取")
