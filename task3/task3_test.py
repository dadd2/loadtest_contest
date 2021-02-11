import unittest
import task3_generate
import task3
import random


manual_test = """

"""
class StatisticsTest(unittest.TestCase):
    def test_seimrandom(self):
        self.skipTest('unused')
        random.seed(1234)
        assert 1892932127 == random.randint(0, 10**10), "random module doesn't work as expected"

        with open('log_test.txt', 'w') as file:
            task3_generate.generate(file, 10)

        t0 = '2021-01-10T01:19:53'
        t1 = '2021-02-10T04:17:03'

        with open('log_test.txt', 'r') as file:
            data = task3.data_prepare(file, t0, t1)
            stats = task3.data_analyse(**data)
        pass


if __name__ == '__main__':
    unittest.main()