# -*- coding=utf8 -*-
from __future__ import division
from math import log
from pypinyin import lazy_pinyin

from lib.utils import iter_dict
from model import (
    PhraseSession,
    PhrasePinyin,
    Pinyin,
    init_phrase_tables,
)


def init_pinyin_phrase_map():
    """
    初始化字典中短语的拼音

    Note: 数字为次数
        pinyin_phrase_map = {
            "xiao fang": {
                "小芳"： 10,
                "消防"： 100
            }
        }
    """
    pinyin_phrase_map = {}
    total = 0

    for phrase, frequency in iter_dict():
        pinyin = u' '.join(lazy_pinyin(phrase))
        total += frequency

        if pinyin not in pinyin_phrase_map:
            pinyin_phrase_map[pinyin] = {phrase: frequency}
        else:
            pinyin_phrase_map[pinyin][phrase] = pinyin_phrase_map[pinyin].get(phrase, 0) + frequency

    for pinyin, phrase_map in pinyin_phrase_map.iteritems():
        total_one_pinyin = sum(phrase_map.values())

        # store pinyin probability
        Pinyin.add(pinyin, log(total_one_pinyin / total))

        for phrase, frequency in phrase_map.iteritems():
            # store the phrase probability in one pinyin
            PhrasePinyin.add(phrase, pinyin, log(frequency / total_one_pinyin))


if __name__ == '__main__':
    init_phrase_tables()
    init_pinyin_phrase_map()

    session = PhraseSession()
    session.execute('create index ix_pinyin on phrase_pinyin(pinyin)')
