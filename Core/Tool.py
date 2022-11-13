# -*- coding: utf-8 -*-
# @Time    : 8/13/22 12:34 PM
# @FileName: Tool.py
# @Software: PyCharm
# @Github    ：sudoskys

import json
import pathlib
import time
import os
from rich.progress import track
from rich.console import Console


class TeleParser(object):
    def __init__(self, json_path: str,
                 out_path: str,
                 min_limit: int = 5,
                 max_limit: int = 512,
                 tester: str = "chinese"):
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
        self.console = Console(color_system='256', style=None)
        self.tg_import = [self.input_path + "/" + pos_json for pos_json in os.listdir(self.input_path) if
                          pos_json.endswith('.json')]
        if len(self.tg_import) == 0:
            self.console.print('No Data in Input Dir! Which Path is:' + self.input_path)
        self.min_limit = min_limit
        self.len_limit = max_limit
        if tester == "chinese":
            def chinese(ask):
                len(TeleParser.extract_chinese(ask))

            self.tester = chinese
        else:
            self.tester = len

    @staticmethod
    def extract_chinese(txt: str) -> str:
        import re
        pattern = re.compile("[\u4e00-\u9fa5]")
        return "".join(pattern.findall(txt))

    @staticmethod
    def data_convert(tg: list, key="id") -> dict:
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

    @staticmethod
    def get_json(data_path: str) -> dict:
        with open(data_path, 'r') as files:
            # tg_data = ast.literal_eval(json.dumps(files.read()))
            import re
            pattern = re.compile(r'\s([^"]+)(webm|webp|tgs)')
            data = re.sub(pattern, '0', files.read())
            tg_data = json.loads(data)
            mge = tg_data.get("messages")
            # print(json.dumps(tg_data, indent=4))
            return TeleParser.data_convert(mge)

    @staticmethod
    def getTime() -> str:
        return time.strftime('%Y%m%d%H%M%S', time.localtime())

    def write_out(self, speech: list, path: str, Wash: bool = False):
        """
        :param speech: 发言列表

        :param path: 输出文件名

        :param Wash:  是否去重

        :return:
        """
        wr = open(path, 'w')
        if Wash:
            speech = list(set(speech))
        for i in speech:
            wr.write(i)
        wr.flush()
        wr.close()

    def get_all(self, showDate=False, ending="\n", unidata=False) -> dict:
        """
        :param unidata: 是否去重
        :param ending: 后缀
        :param showDate: 是否显示日期
        :return: wr lines total, skip num, deleted item num, all_items_num
        """
        pathlib.Path("Speech").mkdir(exist_ok=True)
        Out = f"{self.out_path}/Speech/{self.getTime()}.txt"
        self.console.print(f"开始提取所有发言，MIN:{self.min_limit}，MAX:{self.len_limit}", style='blue')
        (ask_time, count, uncount, total, e1) = ("", 0, 0, 0, time.time())
        Speech_list = []
        for data_path in self.tg_import:
            item_count = 0
            cv_json = self.get_json(data_path=data_path)
            for id_item in track(cv_json.values(), description='提取数据...'):
                # replay = id_item.get("reply_to_message_id")
                if id_item:
                    total += 1
                    ask = TeleParser.test_obj(id_item.get("text"))
                    if ask:
                        if showDate:
                            ask_time = TeleParser.test_obj(id_item.get("date")) + "\n"
                        ask = ask.replace("\n", ",")
                        if self.len_limit > self.tester(ask) > self.min_limit:
                            count += 1
                            item_count += 1
                            Speech_list.append(ask_time + ask + "\n" + ending)
                        else:
                            uncount += 1
                    else:
                        uncount += 1
            self.console.rule(f"[bold blue]完成了{os.path.split(data_path)[1]}目标数据的转换,成功输出了:{item_count}")
        self.write_out(speech=Speech_list, path=Out, Wash=unidata)
        e2 = time.time()
        self.console.rule(f"[bold blue]提取用时:{(e2 - e1)}")
        self.console.print("总处理数:" + str(total) + ",输出于:" + Out, style='blue')
        self.console.print("写入了:" + str(count) + ",跳过了:" + str(uncount), style='blue')
        return {"all": total, "skip": uncount, "output": count}

    def get_speech(self, lable, target_id, showDate=True, ending="\n", unidata=False) -> dict:
        """
        :param unidata: 是否去重

        :param ending: 后缀

        :param showDate: 是否附带日期

        :param lable:名字标签

        :param target_id:目标ID,带user的那个

        :return: wr lines total, skip num, deleted item num, all_items_num
        """
        pathlib.Path("Speech").mkdir(exist_ok=True)
        user = lable + "_" + target_id
        Out = f"{self.out_path}/Speech/{user}_{self.getTime()}.txt"
        self.console.print(f"开始提取{lable}的所有回复，MIN:{self.min_limit}，MAX:{self.len_limit}", style='blue')
        (ask_time, count, uncount, total, deletecount, e1) = ("", 0, 0, 0, 0, time.time())
        Speech_list = []
        for data_path in self.tg_import:
            item_count = 0
            cv_json = self.get_json(data_path=data_path)
            for id_item in track(cv_json.values(), description='提取数据...'):
                # replay = id_item.get("reply_to_message_id")
                if id_item:
                    if id_item.get("from_id") == target_id:
                        total += 1
                        ask = TeleParser.test_obj(id_item.get("text"))
                        if ask:
                            if showDate:
                                ask_time = TeleParser.test_obj(id_item.get("date")) + "\n"
                            ask = ask.replace("\n", ",")
                            if self.len_limit > self.tester(ask) > self.min_limit:
                                count += 1
                                item_count += 1
                                Speech_list.append(ask_time + ask + "\n" + ending)
                            else:
                                uncount += 1
                        else:
                            uncount += 1
            self.console.rule(f"[bold blue]完成了{os.path.split(data_path)[1]}目标数据的转换,成功输出了:{item_count}")
        self.write_out(speech=Speech_list, path=Out, Wash=unidata)
        e2 = time.time()
        self.console.rule(f"[bold blue]提取用时:{(e2 - e1)}")
        self.console.print("有回复的总处理数:" + str(total) + ",输出于:" + Out, style='blue')
        self.console.print("写入了:" + str(count) + ",跳过了:" + str(uncount), style='blue')
        return {"all": total, "skip": uncount, "output": count}

    def get_all_reply(self, showDate=True, ending="\n", unidata=False) -> dict:
        """
        :param unidata: 是否去重

        :param ending: 后缀

        :param showDate: is show date

        :return:
        """
        dir_path = self.out_path + "/Group/"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        # out = dir_path + user + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + "_out.txt"
        self.console.print(
            "开始提取数据目录中的所有成员的回复链条，MIN:" + str(self.min_limit) + ",MAX:" + str(self.len_limit),
            style='blue')
        (ask_time, count, uncount, total, deletecount, item_count) = ("", 0, 0, 0, 0, 0)
        for data_path in self.tg_import:
            with open(data_path, 'r') as files:
                import re
                pattern = re.compile(r'\s([^"]+)(webm|webp|tgs)')
                data = re.sub(pattern, '0', files.read())
                tg_data = json.loads(data)
                GroupId = tg_data.get("id")
                OutPath = dir_path + str(GroupId) + "_out.txt"
                mge = tg_data.get("messages")
                e1 = time.time()
                Speech_list = []
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
                                    ask_len = self.tester(ask)
                                    ans_len = self.tester(ans)
                                    if all([self.len_limit > ask_len > self.min_limit,
                                            self.len_limit > ans_len > self.min_limit]):
                                        Speech_list.append(f"{ask_time}{ask}\n{ans}\n" + ending)
                                        count += 1
                                        item_count += 1
                                        # print(info)
                                    else:
                                        uncount += 1
                                else:
                                    uncount += 1
                            else:
                                deletecount += 1
                self.write_out(speech=Speech_list, path=OutPath, Wash=unidata)
                self.console.rule(
                    f"[bold blue]完成了{os.path.split(data_path)[1]}目标数据的转换,成功输出了:{item_count}")
                e2 = time.time()
                self.console.rule('[bold blue]提取用时:' + str(e2 - e1))
                self.console.print("有回复的总处理数:" + str(total) + ",输出于:" + OutPath, style='blue')
                self.console.print(
                    "写入了:" + str(count) + ",跳过了:" + str(uncount) + ",被删除消息条:" + str(deletecount),
                    style='blue')
                return {"all": total, "skip": uncount, "output": count, "delete": deletecount}

    def get_reply(self, lable, target_id, showDate=True, ending="\n", unidata=False) -> dict:
        """
        :param showDate: 是否显示日期

        :param ending: 后缀

        :param unidata: 是否去重

        :param lable: 名字标签

        :param target_id: 目标ID,带user的那个

        :return: wr lines total, skip num, deleted item num, all_items_num
        """
        user = lable + "_" + target_id
        dir_path = self.out_path + "/Reply/" + user + "/"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        out = dir_path + user + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + "_out.txt"
        self.console.print("开始提取" + lable + "的回复，MIN:" + str(self.min_limit) + ",MAX:" + str(self.len_limit),
                           style='blue')
        (ask_time, count, uncount, total, deletecount) = ("", 0, 0, 0, 0)
        Speech_list = []
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
                                ask_len = self.tester(ask)
                                ans_len = self.tester(ans)
                                if all([self.len_limit > ask_len > self.min_limit,
                                        self.len_limit > ans_len > self.min_limit]):
                                    count += 1
                                    item_count += 1
                                    # print(info)
                                    Speech_list.append(f"{ask_time}{ask}\n{ans}\n" + ending)
                                else:
                                    uncount += 1
                            else:
                                uncount += 1
                        else:
                            deletecount += 1
                self.console.rule(
                    f"[bold blue]完成了{os.path.split(data_path)[1]}目标数据的转换,成功输出了:{item_count}")
        self.write_out(path=out, speech=Speech_list, Wash=unidata)
        e2 = time.time()
        self.console.rule('[bold blue]提取用时:' + str(e2 - e1))
        self.console.print("有回复的总处理数:" + str(total) + ",输出于:" + out, style='blue')
        self.console.print("写入了:" + str(count) + ",跳过了:" + str(uncount) + ",被删除消息条:" + str(deletecount),
                           style='blue')
        return {"all": total, "skip": uncount, "output": count, "delete": deletecount}
        # console.rule("[bold blue]完成提取")
