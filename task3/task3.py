import re
import datetime
import argparse
import os
import json


DEBUG = False


questions = """

- В логфайле (объем бочки), (текущий объем воды в бочке) – пояснение или часть файла?

- кто-то читерит (https://bigxp.ru/tasks/1436, https://metachan.ru/WCCTCOOgpWg)
- можно ли юзать pandas? - нафиг-нафиг

- "какой объем воды был не налит" - имеется в виду, что по ошибке тогось?

- что с тире из инпута? Это нормально?

"""


output_ru = """
Статистика за указанный период:
-------------------------------
{count_topup_tries} - количество попыток налить воду в бочку
{percent_overall_errors}% - процент допущеных ошибок (суммарно для налития и слития)
{vol_input} л - объем воды, налитый в бочку
{vol_input_rejected} л - объем воды, не налитый в бочку
"""


def isotime_parse(s):
    """convert ISO 8601 time to float"""
    return datetime.datetime.fromisoformat(s).timestamp()


def line_parse(line, i=None):
    """parse one line of logfile

    :param line: str
    :param i: number of line in logfile, used in error message

    :returns: time, username, command, volume
    """
    if i is None:
        i = 'unknown'
    parsed = re.search(r'^([^Z]*)Z [–-] \[([^\]]*)\] [–-] wanna (top up|scoop) (\d*)l', line)
    try:
        isotime, username, command, volume = parsed.groups()
        time = isotime_parse(isotime)
        volume = int(volume)
    except:
        raise ValueError(f'line no. {i} has wrong format: "{line}"')
    return time, username, command, volume


def data_prepare(file, **kw):
    """read file's lines and parse values

    :param file: opened file

    :returns: dict of {barrel_volume: int, current_volume: int,
                       lines_generator: generator}
    """
    result = {}

    line = file.readline()
    assert line.startswith('META DATA:'), 'first line of file should be "META DATA:"'

    try:
        result['barrel_volume'] = int(file.readline())
        result['current_volume'] = int(file.readline())
    except ValueError:
        raise ValueError('metadata has wrong format')

    log_generator = (line_parse(line, i) for i, line in enumerate(file, start=4) if not re.fullmatch(r'\w*', line))
    result['lines_generator'] = (line for line in log_generator)
    return result


def data_analyse(barrel_volume, current_volume, lines_generator, t0, t1, debug=False):
    """make short stats

    :param barrel_volume: int
    :param current_volume: int
    :param lines_generator: iterable of (time, username, command, volume) items (see line_parse)
    :param t1: str, ISO 8601 time
    :param t2: str, ISO 8601 time

    :returns: statistics dict
    """

    try:
        t0 = isotime_parse(t0)
        t1 = isotime_parse(t1)
    except:
        raise ValueError('t0 or t1 has wrong format')

    cmds_dict = {
        "top up": 1,
        "scoop": -1
    }
    vals = ('count_attempts', 'count_errs', 'percent_errs', 'vol_accepted', 'vol_rejected')
    result = dict((f'{cmd}__{val}', 0) for cmd in ('top_up', 'scoop') for val in vals)
    result.update(lines_count=0, vol_before=0, vol_after=0)

    started = False
    ended = False
    for time, username, command, volume in lines_generator:
        result['lines_count'] += 1

        new_level = current_volume + volume * cmds_dict[command]
        check_possible = 0 <= new_level <= barrel_volume

        if check_possible:
            current_volume = new_level

        if started or time >= t0:
            if not started:
                result['vol_before'] = current_volume - volume * cmds_dict[command]
                started = True
            if time > t1:
                result['vol_after'] = current_volume
                ended = True
                break
            cmd_key = command.replace(' ', '_')

            if check_possible:
                result[f'{cmd_key}__vol_accepted'] += volume
            else:
                result[f'{cmd_key}__vol_rejected'] += volume
                result[f'{cmd_key}__count_errs'] += 1

            result[f'{cmd_key}__count_attempts'] += 1

        if debug:
            print(started, command, volume, check_possible, '|', current_volume)

    if not started:
        result['vol_before'] = current_volume
    if not ended:
        result['vol_after'] = current_volume

    for cmd_key in ('top_up', 'scoop'):
        if result[f'{cmd_key}__count_attempts']:
            result[f'{cmd_key}__percent_errs'] = round(
                result[f'{cmd_key}__count_errs'] / result[f'{cmd_key}__count_attempts'] * 100,
                2
            )
        else:
            result[f'{cmd_key}__percent_errs'] = 'nan'
    return result


def write_to_csv(stats, filename, file_weep=False):
    """write stats to csv file

    :param stats: dict from data_analyse(...)
    :param filename: str
    :param file_weep: erase file content if set to True
    """
    bad_keys = ['top_up__count_errs', 'scoop__count_errs', 'lines_count']
    stats_keys = sorted(key for key in stats if key not in bad_keys)
    file_exists = os.path.isfile(filename)

    mode = 'aw'[file_weep]
    with open(filename, mode) as file:
        if file_weep or not file_exists:
            file.write(', '.join(stats_keys) + '\n')
        file.write(', '.join(map(str, (stats[key] for key in stats_keys))) + '\n')


def main():
    ap = argparse.ArgumentParser("task3.py", "make statistics from barrel's log file for given time interval")

    ap.add_argument("filename", help="log file")
    ap.add_argument("t0", help="ISO 8601 time, left boundary of interval")
    ap.add_argument("t1", help="ISO 8601 time, right boundary of interval")
    ap.add_argument("output", nargs="?", default=None, help="file to write CSV; if not specified - stats will be written to stdout")
    ap.add_argument("-d", "--debug", action='store_true', help="doesn't raises exceptions if given")
    ap.add_argument('-e', '--erase', action='store_true', help="erases previous content of output file if given")
    args = ap.parse_args()

    try:
        with open(args.filename, encoding='utf-8') as file:
            data = data_prepare(file, **vars(args))
            stats = data_analyse(**data, t0=args.t0, t1=args.t1)
        stats["condition_time_start"] = args.t0
        stats["condition_time_end"] = args.t1
        if args.output is None:
            for key, value in sorted(stats.items(), key=lambda pair: pair[0]):
                print(f'{key:>25} | {value}')
        else:
            write_to_csv(stats, args.output, file_weep=args.erase)
    except Exception as msg:
        if DEBUG or args.debug:
            raise
        else:
            print(f'{msg.__class__.__name__}: {msg}')
            return


if __name__ == '__main__':
    main()
