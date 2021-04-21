# -*- coding=utf8 -*-
import os

# https://github.com/fxsjy/jieba/blob/master/jieba/dict.txt
dict_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../corpus/dict.txt')

# iterate all phrases from jieba coherent dictionary
def iter_dict():
    """
    遍历dict.txt文件
    """
    with open(dict_path, 'r', ) as f:
        for line in f:
            phrase, frequency, tag = line.split()
            yield phrase.decode('utf8'), int(frequency)
