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
    print("------ start_char -------")
    print(start_char)

    V = {char: prob for char, prob in start_char}

    print("------ V -------")
    print(V)

    print("\r\n")

    # let's count from the second pinyin to calc viterbi matrix
    for i in range(1, len(pinyin_list)):
        pinyin = pinyin_list[i]

        print("------ i -------")
        print(i)

        print("------ pinyin -------")
        print(pinyin)

        prob_map = {}

        for phrase, prob in V.iteritems():
            print("------ phrase -------")
            print(phrase)

            print("------ prob -------")
            print(prob)

            prev_char = phrase[-1]

            # only get the most possible next_char, with highest probability
            result = Transition.join_emission(pinyin, prev_char)
            print("------ result -------")
            print(result)

            if not result:
                continue

            # next_prob = transfer probability(pre_char -> next_char) * emission probability(next_char -> pinyin)
            next_char, next_prob = result
            print("-------- next_char --------")
            print(next_char)

            # make new V of new char path, ie phrase.
            prob_map[phrase + next_char] = next_prob + prob

        if prob_map:
            # update V, in order to do further research
            V = prob_map
        else:
            return V

        print("\r\n")

    return V


if __name__ == '__main__':
    while 1:
        string = raw_input('input:')

        if not string:
            print("bye bye")
            break

        pinyin_list = string.split()
        V = viterbi(pinyin_list)

        for phrase, prob in sorted(V.items(), key=lambda d: d[1], reverse=True):
            print phrase, prob
