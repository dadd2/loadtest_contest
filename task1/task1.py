import sys
import argparse


questions = """

- надо ли маркировать перегрузку:
    itoBase(nb, baseSrc) --> itoBase(nb, baseSrc, baseDst)
    а то мало ли

"""


def itoBase(nb, base):
    """converts decimal number to different numerical system

    :param nb: int, number to convert
    :param base: str, digits of destination numerical system, ascending

    :returns: string
    """
    dict_dst = dict((i, c) for i, c in enumerate(base))
    p_dst = len(base)

    result_s = ''
    while nb:
        result_s = dict_dst[nb % p_dst] + result_s
        nb //= p_dst
    return result_s
itoBase_old = itoBase


def itoBase(nb, baseSrc, baseDst):
    """convert number from one numerical system to another


    :param nb: str, number to convert
    :param base: str, digits of source numerical system, ascending
    :param base: str, digits of destination numerical system, ascending

    :returns: string
    """
    p_src = len(baseSrc)
    p_dst = len(baseDst)
    dict_src = dict((c, i) for i, c in enumerate(baseSrc))
    dict_dst = dict((i, c) for i, c in enumerate(baseDst))

    number = 0
    for exp, c in enumerate(nb[::-1]):
        number += dict_src[c] * p_src ** exp

    result_s = ''
    while number:
        result_s = dict_dst[number % p_dst] + result_s
        number //= p_dst
    return result_s


def main():
    ap = argparse.ArgumentParser('task1.py', description='converts given number from one encoding to another')
    ap.add_argument('nb', help='number')
    ap.add_argument('baseDst', help='all digits of destination numeral system; ascending')
    ap.add_argument('baseSrc', nargs='?', default = '0123456789', help='all digits of source numeral system; ascending; default is decimal')

    args = ap.parse_args()

    assert set(args.nb) <= set(args.baseSrc), f'following digits absent in baseSrc: {set(args.nb) - set(args.baseSrc)}'

    print(itoBase(**vars(args)))


if __name__ == '__main__':
    main()
