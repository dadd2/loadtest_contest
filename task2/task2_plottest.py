import task2_test
import task2
import numpy as np

from matplotlib import pyplot as plt



def test_simple():

    data = []
    for i in np.linspace(0, 0.999, 100):
        print('----------------------------------------------')
        # case, answer = task2_test.make_simple_casetest(points_no=2, randomize_ends=False)
        case, answer = task2_test.make_manual_casetest(i, randomize_ends=False)
        print(case)
        calculated_answer = task2.get_intersect(**case)
        print('=========')
        print(case)
        print('answ    :', answer)
        print('calcansw:', calculated_answer)
        x0 = min(a.x for a in answer) if answer else -1
        x1 = min(a.x for a in calculated_answer) if calculated_answer else -1
        data.append((x0, x1))

    data.sort(key=lambda p: p[0])
    D = np.array(data)
    plt.plot(D[..., 0], 'b')
    plt.plot(D[..., 1], 'r')
    plt.show()

test_simple()