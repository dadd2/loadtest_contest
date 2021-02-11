import task2
import unittest
from geometry import Point
import math
import itertools as it
import random


data = '{sphere: {center: [0, 0, 0], radius: 10.67}, line: {[1, 0.5, 15], [43, -14.6, 0.04]}}'

patterns = [
    '{sphere: {center: [CENTER], radius: RADIUS}, line: {[LINE_A], [LINE_B]}}',
    '{sphere: {radius: RADIUS, center: [CENTER]}, line: {[LINE_A], [LINE_B]}}',
    '{line: {[LINE_A], [LINE_B]}, sphere: {center: [CENTER], radius: RADIUS}}',

    '{sphere:{center:[CENTER],radius:RADIUS},line:{[LINE_A],[LINE_B]}}',
    '{sphere:{radius:RADIUS,center:[CENTER]},line:{[LINE_A],[LINE_B]}}',
    '{line:{[LINE_A],[LINE_B]},sphere:{center:[CENTER],radius:RADIUS}}',

    '{sphere:  {center:  [CENTER],  radius:  RADIUS},  line:  {[LINE_A],  [LINE_B]}}',
    '{sphere:  {radius:  RADIUS,  center:  [CENTER]},  line:  {[LINE_A],  [LINE_B]}}',
    '{line:  {[LINE_A],  [LINE_B]},  sphere:  {center:  [CENTER],  radius: RADIUS}}',
]

test_cases = [
    (
        {'center': [0.0, 0.0, 0.0], 'radius': 10.67, 'line_a': [1.0, 0.5, 15.0], 'line_b': [43.0, -14.6, 0.04]},
        []
    )
]


def data_make(case, pattern=None):
    if pattern is None:
        pattern = '{sphere: {center: [CENTER], radius: RADIUS}, line: {[LINE_A], [LINE_B]}}'
    data = pattern
    data = data.replace('CENTER', ', '.join(map(str, case['center'])))
    data = data.replace('RADIUS', str(case['radius']))
    data = data.replace('LINE_A', ', '.join(map(str, case['line_a'])))
    data = data.replace('LINE_B', ', '.join(map(str, case['line_b'])))

    return data


def test_convert():

    print(task2.data_make(task2.data_parse(data)))


def make_manual_casetest(line_dist=0.5, randomize_ends=True):
    if line_dist > 1:
        answer = []
    if line_dist == 1:
        answer = [Point(0, 0, 1)]
    if line_dist < 1:
        line_dist = line_dist
        x_coord = (1 - line_dist**2) ** .5
        answer = [
            Point(-x_coord, 0, line_dist),
            Point(x_coord, 0, line_dist),
        ]
    if randomize_ends:
        x0 = random.random() * 10
        x1 = random.random() * 10
        if x0 == x1:
            x1 += 1
    else:
        x0 = -2
        x1 = 2
    case = {
        'center': Point(0,0,0),
        'radius': 1,
        'line_a': Point(x0, 0, line_dist),
        'line_b': Point(x1, 0, line_dist),
    }
    return case, answer


def make_simple_casetest_old(points_no=None):
    if points_no is None:
        points_no = random.randint(0, 2)

    if points_no == 0:
        line_dist = 1.000001 + random.random()
        answer = []
    elif points_no == 1:
        line_dist = 1
        answer = [Point(0, 0, 1)]
    else:
        line_dist = random.random() * 0.9999
        x_coord = (1 - line_dist**2) ** .2
        answer = [
            Point(-x_coord, 0, line_dist),
            Point(x_coord, 0, line_dist),
        ]

    x0 = random.random() * 10
    x1 = random.random() * 10
    if x0 == x1:
        x1 += 1

    case = {
        'center': Point(0,0,0),
        'radius': 1,
        'line_a': Point(x0, 0, line_dist),
        'line_b': Point(x1, 0, line_dist),
    }
    return case, answer


def make_simple_casetest(points_no=None, randomize_ends=True):
    if points_no is None:
        points_no = random.randint(0, 2)

    if points_no == 0:
        line_dist = 1.000001 + random.random()

    elif points_no == 1:
        line_dist = 1

    else:
        line_dist = random.random() * 0.9999

    case, answer = make_manual_casetest(line_dist, randomize_ends=randomize_ends)
    return case, answer


def rotate2d(x, y, a):
    c = math.cos(a)
    s = math.sin(a)
    return x * c - y * s, x * s + y * c


def rotate_inplace(point, ax, ay, az):
    point.x, point.y = rotate2d(point.x, point.y, az)
    point.y, point.z = rotate2d(point.y, point.z, ax)
    point.z, point.x = rotate2d(point.z, point.x, ay)


def make_general_casetest(points_no=None):
    case, answer = make_simple_casetest(points_no=points_no, randomize_ends=False)


    rot = [random.random() * 3, random.random() * 3, random.random() * 3]
    scale = random.random() * 3 + 0.01
    shift = Point(
        random.random() * 1000 - 500,
        random.random() * 1000 - 500,
        random.random() * 1000 - 500,
    )

    for point in it.chain(answer, (case['line_a'], case['line_b'], case['center'])):
        rotate_inplace(point, *rot)
        point.set_inplace(point * scale)
        point.set_inplace(point + shift)

    case['radius'] *= scale

    return case, answer


class DataParsingTest(unittest.TestCase):
    def test_reversed(self):
        case = {'center': [0.0, 0.0, 0.0], 'radius': 10.67, 'line_a': [1.0, 0.5, 15.0], 'line_b': [43.0, -14.6, 0.04]}
        data = data_make(case)
        self.assertEqual(task2.data_parse(data), case)

    def test_format_variations(self):
        case = {'center': [0.0, 0.0, 0.0], 'radius': 10.67, 'line_a': [1.0, 0.5, 15.0], 'line_b': [43.0, -14.6, 0.04]}
        for pattern in patterns:
            data = data_make(case, pattern)

            self.assertEqual(task2.data_parse(data), case)


class CollisionTest(unittest.TestCase):
    def test_simple(self):
        # self.skipTest('time has not come yet')
        for i in range(100):
            # print('----------------------------------------------')
            case, answer = make_simple_casetest(randomize_ends=False)
            calculated_answer = task2.get_intersect(**case)
            # print('=========')
            # print()
            # print(case)
            # print('answ    :', answer)
            # print('calcansw:', calculated_answer)
            # self.assertCountEqual(task2.get_intersect(**case), answer)

    def test_general(self):
        # self.skipTest('time has not come yet')
        for i in range(10000):
            case, answer = make_general_casetest()
            # print(data_make(case))
            # print('--------------')
            answer_calc = task2.get_intersect(**case)
            # print()
            # print('answ    :', answer)
            # print('calcansw:', answer_calc)

            self.assertTrue(len(answer) == len(answer_calc))
            if len(answer) == 1:
                self.assertEqual(answer_calc[0], answer[0])
            if len(answer) == 2:
                assert_1 = answer_calc == answer
                assert_2 = answer_calc == answer[::-1]
                self.assertTrue(assert_1 or assert_2)

    def test_manual(self):
        self.skipTest('you don\'t need this')
        case, answer = make_manual_casetest(line_dist=0, randomize_ends=True)
        print()
        print(case, answer)
        answer_test = task2.get_intersect(**case)
        print(answer_test)
        self.assertCountEqual(answer_test, answer)

# print(task2.data_parse(data))

if __name__ == '__main__':
    # random.seed(0)
    unittest.main()
