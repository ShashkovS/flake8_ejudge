#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import re
from flake8_ejudge.flake8_ejudgeformatter import LINE_STARTER
from flake8.main import application
import io
import base64

FLAKE = 'flake8'
MAX_LEN = 160
IGNORE = 'W293,W292,W291,W391,F405,E722,E743,E101,F403,E721,E226'
TIMEOUT = 5
MAX_COMPLEXITY = 9
MAX_ERRORS_TO_SHOW = 10


def parse_evs(evs: dict):
    # Дополняем стандартные параметры значениями из env
    flake_parms = [
        '--show-source',
        '--jobs=1',
        '--isolated',
        '--format=flake8ejudgeformatter',
    ]
    if 'flake8_ignore' in evs:
        flake_parms.append('--ignore=' + evs['flake8_ignore'].replace(' ', '').upper())
    else:
        flake_parms.append('--ignore=' + IGNORE)

    if 'max_line_length' in evs:
        flake_parms.append('--max-line-length=' + evs['max_line_length'])
    else:
        flake_parms.append('--max-line-length=' + str(MAX_LEN))

    if 'max_complexity' in evs and evs['max_complexity'].isdecimal() and int(evs['max_complexity']) < 99:
        flake_parms.append('--max-complexity=' + evs['max_complexity'])
    elif 'max_complexity' in evs and evs['max_complexity'].isdecimal() and int(evs['max_complexity']) >= 99:
        pass
    else:
        flake_parms.append('--max-complexity=' + str(MAX_COMPLEXITY))

    max_errors = int(evs.get('max_errors_to_show', MAX_ERRORS_TO_SHOW))
    return flake_parms, max_errors


def run_flake8(src_name: str, evs: dict):
    errors_found = False
    flake_parms, max_errors = parse_evs(evs)

    # Делаем так, чтобы flake8 налогировал нам в переменную
    old_stdout = sys.stdout
    log_capture_string = io.BytesIO()
    sys.stdout = log_capture_string
    sys.stdout.buffer = log_capture_string
    # Запускаем flake
    app = application.Application()
    # app.initialize(flake_parms)
    # app.run_checks([src_name])
    app.run([src_name, *flake_parms])
    app.report_errors()
    # Вытягиваем данные
    sys.stdout = old_stdout
    stdout_data = log_capture_string.getvalue().decode('utf-8')
    log_capture_string.close()
    if stdout_data:
        stdout_data = '\n' + stdout_data
        tot_errors = stdout_data.count('\n' + LINE_STARTER)
        if tot_errors > max_errors:
            ps = -1
            for __ in range(max_errors):
                ps = stdout_data.find('\n' + LINE_STARTER, ps + 1)
            stdout_data = stdout_data[:ps]
            rem = tot_errors - max_errors
            tail = 'ий' if 5 <= rem % 100 <= 20 else 'ия' if 1 < rem % 10 < 5 else 'ие'
            add = '\n' + '=' * 50 + \
                  '\nТам ещё {} замечан{} к стилю.\n'.format(rem, tail) + \
                  'Используйте автоформатирование кода: Ctrl+Alt+L в PyCharm или сервис https://black.now.sh'
            stdout_data += add
        errors_found = True
    else:
        stdout_data = ' '
    return errors_found, stdout_data[1:]


def run_regex_checks(src_name: str, evs: dict):
    errors_found = False
    stdout_data = ''

    # Читаем исходники
    try:
        with open(src_name, 'r', encoding="utf-8", errors='ignore') as f:
            source = f.read()
    except:
        stdout_data = 'Can not parse source with encoding utf-8'
        errors_found = True
        return errors_found, stdout_data

    # Теперь вычитываем дополнительные настройки
    for i in range(1, 30):
        pattern, in_or_not, msg = 'chk_pattern_' + str(i), 'chk_in_or_not_' + str(i), 'chk_err_msg_' + str(i)
        check = [evs.get(x, '') for x in (pattern, in_or_not, msg)]
        if not all(check):
            continue
        pattern, in_or_not, msg = check
        if pattern.startswith('b32_'):
            pattern = base64.b32decode(pattern[4:].upper().encode()).decode('utf-8')

        check_found = bool(re.search(pattern, source))
        if (check_found and in_or_not != 'in') or (not check_found and in_or_not != 'not'):
            stdout_data += msg + '\n'
            errors_found = True
    return errors_found, stdout_data


def style_check(src_name: str, f_obj):
    # Если имя файла не заканчивается на .py, то игнорируем
    if not src_name.lower().endswith('.py'):
        return 0
    # Проверяем, что это действительно файл и у нас есть к нему доступ
    if not os.path.isfile(src_name):
        return 0

    # Заменяем все "-" на "_" и убираем ведущие "--", если они были
    evs = {key.replace("-", '_').lstrip('_').lower(): val for key, val in os.environ.items()}

    # Запускаем flake8
    errors_found_flake = False
    if 'regexonly' not in evs:
        errors_found_flake, stdout_data_flake = run_flake8(src_name, evs)
        f_obj.write(stdout_data_flake)
    # Запускаем проверки по регуляркам
    errors_found_regex, stdout_data_regex = run_regex_checks(src_name, evs)
    f_obj.write(stdout_data_regex)

    # Выходим с ошибкой или без в зависимости от.
    if errors_found_flake or errors_found_regex:
        return 1


def main():
    # ejudge вызывает валидатор с единственным параметром — именем файла, которому необходима проверка.
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: flake8ejudge filename\n')
        sys.exit(1)
    src_name = sys.argv[1]
    exit_code = style_check(src_name, f_obj=sys.stderr)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
