#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import re
from flake8ejudgeformatter import LINE_STARTER

FLAKE = 'flake8'
MAX_LEN = 160
IGNORE = 'W293,W292,W291,W391,F405,E722,E743,E101,F403,E721'
TIMEOUT = 5
MAX_COMPLEXITY = 9
MAX_ERRORS_TO_SHOW = 10


def flake8_it(src_name: str, f_obj):
    errors_found = False
    # Если имя файла не заканчивается на .py, то игнорируем
    if not src_name.lower().endswith('.py'):
        return 0
    # Проверяем, что это действительно файл и у нас есть к нему доступ
    if not os.path.isfile(src_name):
        return 0
    # Дополняем стандартные параметры значениями из env
    # Заменяем все "-" на "_" и убираем ведущие "--", если они были
    evs = {key: val.replace("-", '_').lstrip('_').lower() for key, val in os.environ.items()}
    flake_parms = [
        '--show-source',
        '--jobs=1',
        '--isolated',
        '--format=flake8ejudgeformatter',
    ]
    if 'flake8_ignore' in evs:
        flake_parms.append('--ignore=' + evs['flake8_ignore'])
    else:
        flake_parms.append('--ignore=' + IGNORE)

    if 'max_line_length' in evs:
        flake_parms.append('--max-line-length=' + evs['max_line_length'])
    else:
        flake_parms.append('--max-line-length=' + str(MAX_LEN))

    if 'max-complexity' in evs and evs['max_line_length'].isdecimal() and int(evs['max_line_length']) < 99:
        flake_parms.append('--max-complexity=' + evs['max_line_length'])
    elif 'max-complexity' in evs and evs['max_line_length'].isdecimal() and int(evs['max_line_length']) >= 99:
        pass
    else:
        flake_parms.append('--max-complexity=' + str(MAX_COMPLEXITY))

    max_errors = evs.get('max_errors_to_show', MAX_ERRORS_TO_SHOW)

    # Запускаем flake
    to_run = [FLAKE] + flake_parms + [src_name]
    pr = subprocess.Popen(to_run,
                          stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)  # Запускаем процесс
    stdout_data_b, stderr_data_b = pr.communicate(timeout=TIMEOUT)  # Передаём данные в StdIN
    if stderr_data_b:
        f_obj.write('flake8 error:\n' + stderr_data_b.decode('utf-8', 'ignore'))
        return 1
    if stdout_data_b:
        stdout_data = '\n' + stdout_data_b.decode('utf-8', 'ignore')
        tot_errors = stdout_data.count('\n' + LINE_STARTER)
        if tot_errors > max_errors:
            ps = -1
            for __ in range(max_errors):
                ps = stdout_data.find('\n' + LINE_STARTER, ps + 1)
            stdout_data = stdout_data[:ps]
            rem = tot_errors - max_errors
            tail = 'ий' if 5 <= rem % 100 <= 20 else 'ия' if 1 < rem % 10 < 5 else 'ие'
            add = '\n' + '=' * 50 + \
                  'Там ещё {} замечан{} к стилю.'.format(rem, tail) + \
                  'Используйте автоформатирование кода: Ctrl+Alt+L в PyCharm или сервис https://black.now.sh'
            stdout_data += add
        errors_found = True
        f_obj.write(stdout_data)

    # Читаем исходники
    try:
        with open(src_name, 'r', encoding="utf-8", errors='ignore') as f:
            source = f.read()
    except:
        f_obj.write('Can not parse source with encoding utf-8')
        return 1

    # Теперь вычитываем дополнительные настройки
    for i in range(1, 30):
        pattern, in_or_not, msg = 'chk_pattern_' + str(i), 'chk_in_or_not_' + str(i), 'chk_err_msg_' + str(i)
        check = [evs.get(x, '') for x in (pattern, in_or_not, msg)]
        if not all(check):
            continue
        pattern, in_or_not, msg = check

        check_found = bool(re.search(pattern, source))
        if (check_found and in_or_not != 'in') or (not check_found and in_or_not != 'not'):
            f_obj.write(msg)
            f_obj.write('\n')
            errors_found = True

    # Выходим с ошибкой или без в зависимости от.
    if errors_found:
        return 1


def main():
    # ejudge вызывает валидатор с единственным параметром — именем файла, которому необходима проверка.
    if len(sys.argv) < 2:
        sys.stderr.write('flake8ejudge filename')
        sys.exit(1)
    src_name = sys.argv[1]
    exit_code = flake8_it(src_name, f_obj=sys.stderr)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
