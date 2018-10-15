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

    # Делаем так, чтобы flake8 налогировал нам в переменную
    old_stdout = sys.stdout
    log_capture_string = io.StringIO()
    sys.stdout = log_capture_string
    # Запускаем flake
    to_run = [FLAKE] + flake_parms + [src_name]
    app = application.Application()
    app.run(to_run)
    # Вытягиваем данные
    sys.stdout = old_stdout
    stdout_data = log_capture_string.getvalue()
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
        f_obj.write(stdout_data[1:])

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
        if pattern.startswith('b64_'):
            pattern = base64.b64decode(pattern[4:].encode()).decode('utf-8')

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
        sys.stderr.write('Usage: flake8ejudge filename\n')
        sys.exit(1)
    src_name = sys.argv[1]
    exit_code = flake8_it(src_name, f_obj=sys.stderr)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
