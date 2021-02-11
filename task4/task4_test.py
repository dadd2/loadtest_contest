import task4
import unittest
import random


# task4.DEBUG = True
ALPH = 'qwertyuiopasdfghjklzxcvbnm'

data_mode_plus = {
    "*": True,
    "****": True,

    "*a*": True,
    "a*": True,
    "*abgui*": True,
    "abgui*": True,

    "*ui*ke*gho*": True,
    "*ui**ke***gho*": True,

    "*ui*cd": True,
    "*ui*cd*": True,
    "*ui*cd**": True,

    "a*b*g*u*i*s*k*e*o*g*h*g*h*o*o*o*c*g*c*d": True,
    "*a*b*g*u*i*s*k*e*o*g*h*g*h*o*o*o*c*g*c*d*": True,

    "*a": False,
    "d*": False,
    "": False,
    "a*z*d": False,
    "*z*": False,
    "*g*a*": False,
}
data_mode_minus = {
    "*": True,
    "****": True,

    "*a*": True,
    "a*": True,
    "*abgui*": True,
    "abgui*": True,



    "a*b*g*u*i*s*k*e*o*g*h*g*h*o*o*o*c*g*c*d": True,
    "*a*b*g*u*i*s*k*e*o*g*h*g*h*o*o*o*c*g*c*d*": True,
    "*ui*ke*gho*": False,
    "*ui**ke***gho*": False,

    "*ui*cd": False,
    "*ui*cd*": False,
    "*ui*cd**": False,

    "*a": False,
    "d*": False,
    "": False,
    "a*z*d": False,
    "*z*": False,
    "*g*a*": False,
}


def random_true_test_generate(length):
    s1 = [random.choice(ALPH) for i in range(length)]
    s2 = s1[::]
    for i in range(max(5, length//10)):
        action = random.choice(('insert', 'replace'))
        if action == 'insert':
            i = random.randint(0, len(s2))
            s2 = s2[:i] + ['*'] * random.randint(1, 3) + s2[i:]
        elif action == 'replace':
            i = random.randint(0, len(s2))
            j = random.randint(0, len(s2))
            i, j = min(i, j), max(i, j)
            j = min(j, i+20)
            s2 = s2[:i] + ['*'] * random.randint(1, 3) + s2[j:]
    return ''.join(s1), ''.join(s2)


class Task4Test(unittest.TestCase):
    def test_mode_plus(self):
        a = "abguiskeoghghooocgcd"
        for b, answer in data_mode_plus.items():
            self.assertEqual(task4.strings_collate(a, b, mode='+'), answer)

    def test_mode_minus(self):
        a = "abguiskeoghghooocgcd"
        for b, answer in data_mode_minus.items():
            self.assertEqual(task4.strings_collate(a, b, mode='-'), answer)


    def test_bulk_10_10000(self):
        for i in range(10):
            a, b = random_true_test_generate(10000)
            self.assertTrue(task4.strings_collate(a, b, mode='+'))

    def test_bulk_10_100000(self):
        # self.skipTest('too long')
        for i in range(10):
            a, b = random_true_test_generate(100000)
            self.assertTrue(task4.strings_collate(a, b, mode='+'))

    def test_bulk_1000_1000(self):
        for i in range(1000):
            a, b = random_true_test_generate(1000)
            self.assertTrue(task4.strings_collate(a, b, mode='+'))


if __name__ == '__main__':
    unittest.main()
