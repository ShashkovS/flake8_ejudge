Проверка стиля и требований к используемому синтаксису в python коде для ejudge
===============================================================================

Данный модуль реализует проверку синтаксиса python кода в ejudge с русификацией комментариев.
Проверка прогнана на ~190000 файлах, сданных в тестирующую систему 179-й школы г.Москва.
Русифицированы все тексты ошибок, которые возникли при этой проверке.
Вот примеры наиболее популярных «ошибок»::

    ('E251 unexpected spaces around keyword / parameter equals', 148444)
    ('E226 missing whitespace around arithmetic operator', 22104)
    ('A001 $0 is a python builtin and is being shadowed, consider renaming the variable', 20994)
    ('E305 expected 2 blank lines after class or function definition, found $0', 20615)
    ('F403 $0 used; unable to detect undefined names', 13442)
    ("E211 whitespace before '('", 10875)


Кроме того, модуль возволяет выполнить проверку используемого синтаксиса.
Настройка выполняется в ``serve.cfg`` путём указания переменных окружения для style-checker'а.
Добавляются примерно такие настройки::

    style_checker_env = "chk_pattern_1=\.find\b|\.rfind\b"
    style_checker_env = "chk_in_or_not_1=in"
    style_checker_env = "chk_err_msg_1=Запрещается использовать методы find и rfind"

    style_checker_env = "chk_pattern_2=def my_func\(parm1: type1, parm2: type2\) -> type3:"
    style_checker_env = "chk_in_or_not_2=not"
    style_checker_env = "chk_err_msg_2=Необходима реализация функции сигнатуры `def my_func(parm1: type1, parm2: type2) -> type3:`"

    style_checker_env = "chk_pattern_3=(?m)^def\s+(\w+)\s*\(.*\n?(^(:?[ \t].*|)$\n)*[ \t].*?\1\s*\("
    style_checker_env = "chk_in_or_not_3=in"
    style_checker_env = "chk_err_msg_3=Решение необходимо оформить в виде рекурсивной функции"

Для каждой проверки требуется три переменных: ``chk_pattern_i``, ``chk_in_or_not_i`` и ``chk_err_msg_i``.
Число i должно быть от 1 до 30 без ведущих нулей. Допускаются пропуски.

В переменной ``chk_pattern_i`` должно быть указано регулярное выражение, которое будет искаться при помощи модуля ``re``
по всему коду. Используйте модификаторы ``(?m)`` для поднятия флага ``re.MULTILINE``, ``(?s)`` для поднятия флага
``re.DOTALL``, и вообще: вот документация https://docs.python.org/3/library/re.html, вот статья: https://habr.com/post/349860/.

В переменной ``chk_in_or_not_i`` должна быть указана либо константа ``in``, либо константа ``not``.
В первом случае ошибка будет, если соответствие регулярному выражению не будет найдено, во втором — наоборот.

И наконец, в переменной ``chk_err_msg_i`` необходимо указать сообщение, которое выдаст валидатор стиля на ошибку.


Эти настройки можно выполнять на уровне каждой задачи, а также на уровне языкового процессора.
При необходимости можно добавить игнорирование отдельных ошибок такой настройкой::

    style_checker_env = "flake8_ignore=W293,W292,W291,W391,F405,E722,E743,E101,F403,E721"
    style_checker_env = "max_line_length=120"  (по умолчанию стоит 160)

Кроме того, имеются следующие настройки::

    style_checker_env = "max-complexity=10"  (максимальная цикломатическая сложность, 99, чтобы отключить проверку)
    style_checker_env = "max_errors_to_show=10"  (максимальная количество замечаний в отчёте)


Установка
---------

Для установки пакета необходимо из под юзера ``ejudge`` выполнить команду

``pip3 install git+https://github.com/ShashkovS/flake8_ejudge --user --install-option="--install-scripts=~/bin"``

После этого нужно добавить в ``serve.cfg`` в часть с описанием языкового процессора команду запуска::

    [language]
    id = **
    short_name = "python3"
    long_name = "Python3 3.6.5"
    arch = "linux-shared"
    src_sfx = ".py"
    style_checker_cmd = "/home/ejudge/bin/flake8ejudge"        <- Вот здесь самое важное
    style_checker_env = "flake8_ignore=E4,E51,W234"            <- По желанию
    style_checker_env = "max_line_length=120"                  <- По желанию. По умолчанию стоит 160


Либо можно прописать все эти параметры через GUI. В настройках контеста необходимо перейти на вкладку «Language settings»,
выбрать Python..., вставить ``flake8ejudge`` в поле «Style checker command:».


License
-------

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

Популярные ошибки (именно они русифицированы)
--------------------------------------------

Игнорируются по умолчанию::

    ('W293 blank line contains whitespace', 171558)
    ('W292 no newline at end of file', 105226)
    ('W291 trailing whitespace', 83670)
    ('W391 blank line at end of file', 12594)
    ('F405 $0 may be undefined, or defined from star imports: $1', 37415)
    ("E722 do not use bare except'", 858)
    ('E743 ambiguous function definition $0', 119)
    ('E101 indentation contains mixed spaces and tabs', 1)
    ('F403 ‘from module import *’ used; unable to detect undefined names', 13442)
    ('E721 Do not compare types, use isinstance()', 205)


Проверяются по умолчанию::

    ('E251 unexpected spaces around keyword / parameter equals', 148444)
    ('E226 missing whitespace around arithmetic operator', 22104)
    ('A001 $0 is a python builtin and is being shadowed, consider renaming the variable', 20994)
    ('E305 expected 2 blank lines after class or function definition, found $0', 20615)
    ("E211 whitespace before '('", 10875)
    ('E302 expected 2 blank lines, found $0', 9173)
    ('E741 ambiguous variable name $0', 7840)
    ('E111 indentation is not a multiple of four', 7619)
    ('F401 $0 imported but unused', 7017)
    ('F821 undefined name $0', 6865)
    ('C901 $0 is too complex $1', 6307)
    ('E225 missing whitespace around operator', 6088)
    ('E231 missing whitespace after $0', 5908)
    ('E303 too many blank lines $0', 4563)
    ('F841 local variable $0 is assigned to but never used', 4160)
    ('E203 whitespace before $0', 3218)
    ('E265 block comment should start with $0', 2942)
    ('E501 line too long $0', 2911)
    ('E271 multiple spaces after keyword', 1981)
    ('E402 module level import not at top of file', 1969)
    ('E301 expected 1 blank line, found $0', 1371)
    ('E711 comparison to None should be $0', 1277)
    ("E201 whitespace after '('", 1203)
    ('E221 multiple spaces before operator', 1175)
    ('A003 $0 is a python builtin, consider renaming the class attribute', 1157)
    ("E202 whitespace before ')'", 1110)
    ('E222 multiple spaces after operator', 1106)
    ('E999 SyntaxError: invalid syntax', 1060)
    ('E113 unexpected indentation', 1049)
    ('E112 expected an indented block', 1032)
    ('E702 multiple statements on one line $0', 1031)
    ('F811 redefinition of unused $0 from line $1', 764)
    ('E272 multiple spaces before keyword', 563)
    ('A002 $0 is used as an argument and thus shadows a python builtin, consider renaming the argument', 510)
    ('E241 multiple spaces after $0', 501)
    ('E261 at least two spaces before inline comment', 422)
    ('E712 comparison to True should be $0 or $1', 383)
    ('E262 inline comment should start with $0', 376)
    ('E902 TokenError: EOF in multi-line statement', 362)
    ('E703 statement ends with a semicolon', 259)
    ('E731 do not assign a lambda expression, use a def', 251)
    ('E228 missing whitespace around modulo operator', 240)
    ('E712 comparison to False should be $0 or $1', 235)
    ('E201 whitespace after $0', 232)
    ('E713 test for membership should be $0', 214)
    ('E116 unexpected indentation $0', 210)
    ('E202 whitespace before $0', 203)
    ('E266 too many leading $0 for block comment', 159)
    ('E128 continuation line under-indented for visual indent', 140)
    ('E999 SyntaxError: unexpected EOF while parsing', 131)
    ('E701 multiple statements on one line $0', 128)
    ('E211 whitespace before $0', 125)
    ('E704 multiple statements on one line $0', 99)
    ('E999 IndentationError: expected an indented block', 88)
    ('E227 missing whitespace around bitwise or shift operator', 80)
    ('E115 expected an indented block $0', 73)
    ('E114 indentation is not a multiple of four $0', 72)
    ('E999 IndentationError: unexpected indent', 59)
    ('E902 IndentationError: unindent does not match any outer indentation level', 56)
    ('E999 IndentationError: unindent does not match any outer indentation level', 52)
    ('E131 continuation line unaligned for hanging indent', 38)
    ('E401 multiple imports on one line', 32)
    ('W503 line break before binary operator', 29)
    ('W191 indentation contains tabs', 29)
    ('E306 expected 1 blank line before a nested definition, found $0', 26)
    ('E999 SyntaxError: EOL while scanning string literal', 16)
    ('F823 local variable $0 $1 referenced before assignment', 14)
    ('F706 $0 outside function', 14)
    ('E122 continuation line missing indentation or outdented', 13)
    ('E127 continuation line over-indented for visual indent', 13)
    ('E502 the backslash is redundant between brackets', 12)
    ('E999 SyntaxError: invalid character in identifier', 11)
    ('E999 SyntaxError: unexpected character after line continuation character', 10)
    ('F601 dictionary key $0 repeated with different values', 10)
    ('E129 visually indented line with same indent as next logical line', 9)
    ("E999 SyntaxError: can't assign to operator", 6)
    ("E999 SyntaxError: can't assign to function call", 5)
    ('E304 blank lines found after function decorator', 5)
    ('E124 closing bracket does not match visual indentation', 4)
    ('E126 continuation line over-indented for hanging indent', 4)
    ('E275 missing whitespace after keyword', 4)
    ("E999 SyntaxError: keyword can't be an expression", 3)
    ('E999 SyntaxError: invalid token', 3)
    ("E123 closing bracket does not match indentation of opening bracket's line", 3)
    ('E714 test for object identity should be $0', 2)
    ('F406 $0 only allowed at module level', 2)
    ('F701 $0 outside loop', 2)
    ('E121 continuation line under-indented for hanging indent', 1)
    ('E999 SyntaxError: positional argument follows keyword argument', 1)
    ("E999 SyntaxError: can't assign to comparison", 1)"""
