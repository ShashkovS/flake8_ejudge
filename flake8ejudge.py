#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import re

FLAKE = 'flake8'
MAX_LEN = 160
IGNORE = 'W293,W292,W291,W391,F405,E722,E741,E743'
TIMEOUT = 5

# ejudge вызывает валидатор с единственным параметром — именем файла, которому необходима проверка.
# src_name = sys.argv[1]

src_name = r'X:\_все py\allpy\000811_139_SV_20508_4.py'

errors_found = False
# Если имя файла не заканчивается на .py, то игнорируем
if not src_name.lower().endswith('.py'):
    sys.exit()
# Проверяем, что это действительно файл и у нас есть к нему доступ
if not os.path.isfile(src_name):
    sys.exit()
# Дополняем стандартные параметры значениями из env
# Заменяем все "-" на "_" и убираем ведущие "--", если они были
evs = {key: val.replace("-", '_').lstrip('_') for key, val in os.environ.items()}
flake_parms = [
    '--show-source',
    '--jobs=1',
    '--isolated',
    '--format=flake8ejudgeformatter'
]
if 'flake8_ignore' in evs:
    flake_parms.append('--ignore=' + evs['flake8_ignore'])
else:
    flake_parms.append('--ignore=' + IGNORE)

if 'max_line_length' in evs:
    flake_parms.append('--max-line-length=' + evs['max_line_length'])
else:
    flake_parms.append('--max-line-length=' + str(MAX_LEN))

# Запускаем flake
pr = subprocess.Popen([FLAKE] + flake_parms + [src_name],
                      stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)  # Запускаем процесс
stdout_data_b, stderr_data_b = pr.communicate(timeout=TIMEOUT)  # Передаём данные в StdIN
if stderr_data_b:
    sys.stderr.write('flake8 error:\n' + stderr_data_b.decode('utf-8', 'ignore'))
    sys.exit(1)
if stdout_data_b:
    stdout_data = stdout_data_b.decode('utf-8', 'ignore')
    errors_found = True
    sys.stderr.write(stdout_data)


# Читаем исходники
try:
    with open(src_name, 'r', encoding="utf-8", errors='ignore') as f:
        source = f.read()
except:
    sys.stderr.write('Can not parse source with encoding utf-8')
    sys.exit(1)

# Теперь вычитываем дополнительные настройки
for i in range(1, 30):
    pattern, in_or_not, msg = 'chk_pattern_' + str(i), 'chk_in_or_not_' + str(i), 'chk_err_msg_' + str(i)
    check = [evs.get(x, '') for x in (pattern, in_or_not, msg)]
    if not all(check):
        continue
    pattern, in_or_not, msg = check

    check_found = bool(re.search(pattern, source))
    if (check_found and in_or_not != 'in') or (not check_found and in_or_not != 'not'):
        sys.stderr.write(msg)
        sys.stderr.write('\n')
        errors_found = True

# Выходим с ошибкой или без в зависимости от.
if errors_found:
    sys.exit(1)
