# -*- coding=utf8 -*-
"""
    viterbi算法实现
"""
from model import Emission, Transition


def viterbi(pinyin_list):
    """
    viterbi算法实现输入法

    Args:
        pinyin_list (list): 拼音列表
    """

    # query the char-prob pair
    # char must in starting table, named as start_char
    # prob = start_char prob * emit_prob
    # emit_prob is the probability that start_char emit to the start_pinyin
    start_pinyin = pinyin_list[0]

    start_char = Emission.join_starting(start_pinyin)

    V = {char: prob for char, prob in start_char}

    # let's count from the second pinyin to calc viterbi matrix
    for i in range(1, len(pinyin_list)):
        pinyin = pinyin_list[i]

        prob_map = {}

        for phrase, prob in V.iteritems():
            character = phrase[-1]

            result = Transition.join_emission(pinyin, character)
            if not result:
                continue

            state, new_prob = result

            prob_map[phrase + state] = new_prob + prob

        if prob_map:
            V = prob_map
        else:
            return V
    return V


if __name__ == '__main__':
    while 1:
        string = raw_input('input:')
        pinyin_list = string.split()
        V = viterbi(pinyin_list)

        for phrase, prob in sorted(V.items(), key=lambda d: d[1], reverse=True):
            print phrase, prob
