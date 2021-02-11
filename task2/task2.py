import re
import json
from argparse import ArgumentParser
from geometry import Point

data = '{sphere: {center: [0, 0, 0], radius: 10.67}, line: {[1, 0.5, 15], [43, -14.6, 0.04]}}'


def nums_parse(pattern, data):
    """parse line of comma-separated numbers"""
    nums = re.search(pattern, data).groups()[0]
    return list(map(float, nums.split(',')))


def data_parse(data):
    """parse dataline, is very format-sensitive"""
    case = {}
    case['center'] = nums_parse(r'center:\s*\[([^\]]*)', data)
    case['radius'] = nums_parse(r'radius:\s*([\d.]*)', data)[0]
    case['line_a'] = nums_parse(r'line:\s*\{\[([^\]]*)', data)
    case['line_b'] = nums_parse(r'\],\s*\[([^\]]*)', data)

    return case


def sqeq(a, b, c):
    """Solve quadratic equation

    :param a: int or float
    :param b: int or float
    :param c: int or float

    :returns: roots, even if they are complex
    """
    D = b**2 - 4*a*c
    # print('D:', D)
    if abs(D) < 1e-9:
        D = 0
    x1 = (-b + D**.5) / 2 / a
    x2 = (-b - D**.5) / 2 / a
    return x1, x2


def get_distance(point, line_a, line_b):
    """unused and untested function, returns distance between line and point"""
    linevec = line_a - line_b
    return (point - line_a).vector_mul(linevec).abs() / linevec.abs()


def get_intersect(center, radius, line_a, line_b):
    """get points of intersection sphere and line

    :param center: iterable of (x, y, z), center of sphere
    :param radius: float, radius of sphere
    :param line_a: iterable of (x, y, z), anchor point of line
    :param line_b: iterable of (x, y, z), anchor point of line

    :returns: list of points
    """
    # что же делать?
    # print('get_intersect', center, radius, line_a, line_b)
    center = Point(*center)
    line_a = Point(*line_a)
    line_b = Point(*line_b)

    # distance = get_distance(center, line_a, line_b)
    # print('distance:', distance)

    # if (distance - radius) / radius < 1e-14:
    #     pass
    # linear function r = k*t + b
    # l_k = line_a - line_b
    l_k = line_b - line_a
    l_b = line_a

    l_b_sh = l_b - center  # where center of coordinate system is shifted, so center of sphere is in 0,0,0
    # print('line:', l_k, l_b, l_b_sh)

    # coeffs for quadratic equation
    sq_a = l_k.scalar_mul(l_k)
    sq_b = l_k.scalar_mul(l_b_sh) * 2
    sq_c = l_b_sh.scalar_mul(l_b_sh) - radius**2

    # print('quadreq coeffs:', sq_a, sq_b, sq_c)
    # solution of quadratic equation
    tt = sqeq(sq_a, sq_b, sq_c)
    # print('quadreq roots:', tt)
    if isinstance(tt[0], complex):
        tt = ()
    elif tt[0] == tt[1]:
        tt = (tt[0],)

    result =  [l_k * t + l_b for t in tt]
    if len(result) == 2:
        if result[0].distance(result[1]) < 1e-5:
            return ((result[0] + result[1])/2,)
    return result


def main():
    ap = ArgumentParser("task2.pu", description="intersection points of line and sphere")

    ap.add_argument("data_filename")
    ap.add_argument("answer_filename")
    # ap.add_argument("-r", "--render", action='store_true')

    args = ap.parse_args()

    with open(args.data_filename) as file:
        case = data_parse(file.read())

    intersects = get_intersect(**case)
    with open(args.answer_filename, 'w') as file:
        if not intersects:
            print('Коллизий не найдено', file=file)
        else:
            for intersect in intersects:
                print(intersect.tolist(), file=file)


if __name__ == '__main__':
    main()
