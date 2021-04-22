# -*- coding=utf8 -*-

"""
    制作HMM模型
"""

from __future__ import division
from math import log

from pypinyin import pinyin, NORMAL

from model import (
    Transition,
    Emission,
    Starting,
    init_hmm_tables,
    HMMSession
)

from lib.utils import iter_dict


def init_start():
    """
    初始化起始概率
    """
    print("making start probability vector")

    freq_map = {}
    total_count = 0

    for phrase, frequency in iter_dict():
        total_count += frequency

        # 统计所有词组的第一个字出现的频率
        first_word = phrase[0]
        freq_map[first_word] = freq_map.get(first_word, 0) + frequency

    for character, frequency in freq_map.iteritems():
        # convert frequency into percentage
        char_percentage = frequency / total_count

        # make discrimination between small percentage value
        char_log_value = log(char_percentage)

        Starting.add(character, char_log_value)


def init_emission():
    """
    初始化发射概率
    """
    print("making emission probability matrix")

    character_pinyin_map = {}

    for phrase, frequency in iter_dict():
        '''
        pinyin 接口输出数据
            >>> pinyin('步履蹒跚')
            [['bù'], ['lǚ'], ['mán'], ['shān']]
        '''
        pinyins = pinyin(phrase, style=NORMAL)

        for character, py in zip(phrase, pinyins):
            character_pinyin_count = len(py)

            # py is like ['lǚ'], may have several values
            # must divide the frequency to the same parts, name it as mean frequency
            mean_frequency = frequency/character_pinyin_count

            if character not in character_pinyin_map:
                character_pinyin_map[character] = {x: mean_frequency for x in py}
            else:
                pinyin_freq_map = character_pinyin_map[character]

                for x in py:
                    pinyin_freq_map[x] = pinyin_freq_map.get(x, 0) + mean_frequency

    for character, pinyin_map in character_pinyin_map.iteritems():
        # get total emission frequency for one character
        sum_frequency = sum(pinyin_map.values())

        for py, frequency in pinyin_map.iteritems():
            py_percentage = frequency/sum_frequency
            py_log_value = log(py_percentage)

            Emission.add(character, py, py_log_value)


def init_transition():
    """
    初始化转移概率

    todo 优化 太慢
    """
    print("making transition probability matrix")

    transition_map = {}

    for phrase, frequency in iter_dict():
        for i in range(len(phrase) - 1):
            prev_char = phrase[i]
            next_char = phrase[i+1]

            if prev_char in transition_map:
                current_frequency = transition_map[prev_char].get(next_char, 0)
                transition_map[prev_char][next_char] = current_frequency + frequency
            else:
                transition_map[prev_char] = {next_char: frequency}

    for previous, next_map in transition_map.iteritems():
        # get total frequency for all next chars
        sum_frequency = sum(next_map.values())

        for next_char, freq in next_map.iteritems():
            next_percentage = freq / sum_frequency
            next_log_value = log(next_percentage)

            Transition.add(previous, next_char, next_log_value)


if __name__ == '__main__':
    init_hmm_tables()
    init_start()
    init_emission()
    init_transition()

    # 创建索引
    session = HMMSession()
    session.execute('create index ix_starting_character on starting(character);')
    session.execute('create index ix_emission_character on emission(character);')
    session.execute('create index ix_emission_pinyin on emission(pinyin);')
    session.execute('create index ix_transition_previous on transition(previous);')
    session.execute('create index ix_transition_behind on transition(behind);')
    session.commit()
