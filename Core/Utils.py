# -*- coding: utf-8 -*-
# @Time    : 11/13/22 3:22 PM
# @FileName: Utils.py.py
# @Software: PyCharm
# @Github    ：sudoskys
import os.path


class TXT(object):
    @staticmethod
    def JoinTxT(input_name: str, output_name: str, types: str = ".txt"):
        if all([input_name, output_name]):
            filelist = [input_name + "/" + pos_json for pos_json in os.listdir(input_name) if pos_json.endswith(types)]
            with open(output_name, 'w', encoding='utf-8') as f:
                for filename in filelist:
                    for line in open(filename):
                        f.writelines(line)
                    f.write('\n')
            return output_name
        else:
            return False


if __name__ == "__main__":
    TXT.JoinTxT(input_name="../DataWash/BAD", output_name="../DataWash/Bad.txt")
