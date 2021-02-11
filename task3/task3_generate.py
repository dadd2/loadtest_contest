import random
import datetime


def line_tostring(time, username, command, volume):
    """format function for log line"""
    isotime = datetime.datetime.fromtimestamp(time).isoformat()
    return f'{isotime}Z - [{username}] - wanna {command} {volume}l'


def default_timefun():
    """generates random seconds in range [1e-7, 1001.]"""

    return random.randint(0, 1000) + random.random() + 1e-7


def generate(file, nlines, barrel_vol=300, current_vol=0, usernames=None, timefun=None, current_time=1612909193., error_prob=.1):
    """generate log and write it into file"""
    if usernames is None:
        usernames = ['knight', 'mosquitte', 'elijah', 'g_d', 'john_titor']
    if timefun is None:
        timefun = default_timefun

    file.write('META DATA:\n')
    file.write(str(barrel_vol) + '\n')
    file.write(str(current_vol) + '\n')

    cmds_dict = {
        "top up": 1,
        "scoop": -1
    }

    for i in range(nlines):
        username = random.choice(usernames)
        command = random.choice(tuple(cmds_dict))

        delta_vol = random.randint(1, barrel_vol)
        new_vol = current_vol + delta_vol * cmds_dict[command]

        file.write(line_tostring(current_time, username, command, delta_vol) + '\n')
        current_time += timefun()


def main():
    with open('log_b.txt', 'w', encoding='utf-8') as file:
        generate(file, int(100000/5.8))


if __name__ == '__main__':

    main()
