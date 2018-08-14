#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

DEFAULT_PY_VALIDATOR = "/home/ejudge/bin/stylecheck_python_ru"

src_name = sys.argv[1]

if not src_name.endswith('.py'):
    sys.exit()

from subprocess import call

# Сначала обычный валидатор
call([DEFAULT_PY_VALIDATOR, src_name])

try:
    with open(src_name, 'r', encoding="utf-8") as f:
        source = f.read()
except:
    sys.stderr.write('Can not parse source with encoding utf-8')
    sys.exit(1)

import re
import os
errors_found = False
for i in range(1, 30):
    pattern, in_or_not, msg = 'chk_pattern_' + str(i), 'chk_in_or_not_' + str(i), 'chk_err_msg_' + str(i)
    if pattern in os.environ and in_or_not in os.environ and msg in os.environ:
        pattern, in_or_not, msg = [os.environ[x] for x in (pattern, in_or_not, msg)]
    else:
        continue
    check = bool(re.search(pattern, source))
    if (check and in_or_not != 'in') or (not check and in_or_not != 'not'):
        sys.stderr.write(msg)
        sys.stderr.write('\n')
        errors_found = True
if errors_found:
    sys.exit(1)
