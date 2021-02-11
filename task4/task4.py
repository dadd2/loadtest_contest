import argparse


DEBUG = False
# DEBUG = True



lazy_help = """defines how lazy algorythm will search for coinsidence,
when dealing with '*'.
Let's compare lazy and non-lazy modes
for case s1='abgucdcg', s2='a*cg'.

if mode is lazy, algorythm will run lazy:
    1. 0th character a=a, ok
    2. then we have wildcard '*', search for letter 'c' in s1
    3. found: s1[4] = c
    4. oops, s1[5] == 'd' != 'g', returning False

if mode is not lazy:
    1. 0th character a=a, ok
    2. then we have wildcard '*', search for letter 'c' in s1
    3. found: s1[4] = 'c'
    4. oops, s1[5] == 'd' != 'g', falling back to step 2
    5. found s1[6] = 'c'
6. s1[7] = 'g', string ends here, returning True"""

def ifstr(s):
    """formatting shortcut function, used for debug"""
    if isinstance(s, str):
        return s
    return ''.join(s)


def strings_collate(s1, s2, mode='+'):
    """collate two strings; s2 supports wildcard *
    
    :param s1: string, should NOT content '*'
    :param s2: string, may content '*'
    :param mode: string, '+' or '-'
    
    Mode defines how lazy algorythm will search for coinsidence,
    when dealing with '*'.
    Let's compare '+' and '-' modes for case s1='abgucdcg', s2='a*cg'.

    if mode is '-', algorythm will run lazy:
        1. 0th character a=a, ok
        2. then we have wildcard '*', search for letter 'c' in s1
        3. found: s1[4] = c
        4. oops, s1[5] == 'd' != 'g', returning False

    if mode is '+':
        1. 0th character a=a, ok
        2. then we have wildcard '*', search for letter 'c' in s1
        3. found: s1[4] = 'c'
        4. oops, s1[5] == 'd' != 'g', falling back to step 2
        5. found s1[6] = 'c'
        6. s1[7] = 'g', string ends here, returning True

    :returns: bool
    """
    assert mode in '+-'

    if DEBUG:
        if s1 == 'break':
            raise KeyboardInterrupt('break')
        print('strings_collate', mode)
        print(ifstr(s1))
        print(ifstr(s2))
        print()

    star_mode = False
    s1 = list(s1)
    s2 = list(s2)

    while s1 and s2:
        if s2[0] == '*':
            # atfirst reduse all stars:
            while s2[0] == '*':
                s2.pop(0)
                if not s2:
                    return True
            # then work
            while s1:
                if s1[0] == s2[0]:
                    if strings_collate(s1, s2, mode=mode):
                        return True
                    elif mode == '-':
                        return False
                s1.pop(0)
        elif s1[0] == s2[0]:
            s1.pop(0)
            s2.pop(0)
        else:
            return False
    if s2:
        while s2:
            if s2.pop() != '*':
                return False
        return True
    if s1:
        return False
    return True

def main():
    ap = argparse.ArgumentParser(
        "task No. 4: strings collation",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    ap.add_argument("s1")
    ap.add_argument("s2")
    ap.add_argument("-l", "--lazy", action='store_true', help=lazy_help)

    args = ap.parse_args()
    result = strings_collate(args.s1, args.s2, '+-'[args.lazy])
    print(('KO', 'OK')[result])
if __name__ == '__main__':
    main()
