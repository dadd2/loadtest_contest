from task1 import itoBase, itoBase_old
import random
import itertools as it

ALPH_10 = '0123456789'
ALPH_SRC = 'qwertyuiopasdfghjklzxcvbnm0123456789'

def get_alph():
    return ''.join(random.sample(ALPH_SRC, random.randint(2, len(ALPH_SRC))))


def random_test(easy=False):
    if easy:
        alph_a = ALPH_10
    else:
        alph_a = get_alph()
    alph_b = get_alph()
    
    num_a = random.choice(alph_a[1:]) + ''.join(random.choice(alph_a) for i in range(random.randint(1, 20)))
    
    if easy:
        num_b = itoBase_old(int(num_a), alph_b)
    else:
        num_b = itoBase(num_a, alph_a, alph_b)

    # check reversing:
    if num_a != itoBase(num_b, alph_b, alph_a):
        # print(num_a, num_b, alph_a, alph_b, itoBase(num_b, alph_b, alph_a), '', sep='\n')
        return -1

    # check 10-base:
    if itoBase(num_a, alph_a, ALPH_10) != itoBase(num_b, alph_b, ALPH_10):
        return -2

    return 0


def common_test():
    number = random.randint(0, 10**30)

    variants = [
        ('0123456789', str(number)),
        ('01', bin(number)[2:]),
        ('01234567', oct(number)[2:]),
        ('0123456789abcdef', hex(number)[2:])
    ]
    for (alph_a, s_a), (alph_b, s_b) in it.product(variants, variants):
        if s_b != itoBase(s_a, alph_a, alph_b):
            return -len(alph_a)
    return 0

def common_test_easy():
    number = random.randint(0, 10**30)

    variants = [
        ('01', bin(number)[2:]),
        ('01234567', oct(number)[2:]),
        ('0123456789abcdef', hex(number)[2:])
    ]
    for (alph_b, s_b) in variants:
        if s_b != itoBase_old(number, alph_b):
            return -len(alph_a)
    return 0

def main():
    random.seed(65468754)
    results_r = {-1: 0, -2: 0, 0: 0}
    results_c = {-16: 0, -10: 0, -8: 0, -2: 0, 0: 0}


    results_r_easy = {-1: 0, -2: 0, 0: 0}
    results_c_easy = {-16: 0, -10: 0, -8: 0, -2: 0, 0: 0}
    for i in range(1000):
        results_r[random_test()] += 1
        results_c[common_test()] += 1

        results_r_easy[random_test(easy=True)] += 1
        results_c_easy[common_test_easy()] += 1
    print('random tests:', results_r)
    print('common tests:', results_c)
    print('random tests easy:', results_r_easy)
    print('common tests easy:', results_c_easy)

if __name__ == '__main__':
    main()
