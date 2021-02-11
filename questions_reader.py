
# from task1.task1 import questions as questions1
# from task2.task2 import questions as questions2
# from task3.task3 import questions as questions3
# from task4.task4 import questions as questions4

for i in range(1, 5):
    print('------------------------------------')
    print(f'file {i}')
    print('------------------------------------')
    try:
        exec(f'from task{i}.task{i} import questions as questions{i}')
        eval(f'print(questions{i})')
    except:
        print('error')
        pass