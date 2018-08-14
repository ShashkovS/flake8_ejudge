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

    style_checker_env = "chk_pattern_1=find|rfind"
    style_checker_env = "chk_in_or_not_1=in"
    style_checker_env = "chk_err_msg_1=Запрещается использовать find и rfind"
    style_checker_env = "chk_pattern_2=def my_func(parm1: type1, parm2: type2) -> type3:"
    style_checker_env = "chk_in_or_not_2=not"
    style_checker_env = "chk_err_msg_2=Необходима реализация функции сигнатуры `def my_func(parm1: type1, parm2: type2) -> type3:`"


Эти настройки можно выполнять на уровне каждой задачи, а также на уровне языкового процессора.
При необходимости можно добавить игнорирование отдельных ошибок такой настройкой::

    style_checker_env = "flake8_ignore=E4,E51,W234"
    style_checker_env = "max_line_length=120"  (по умолчанию стоит 160)



Установка
---------

Для установки пакета необходимо либо из под ``root``/``sudo`` выполнить в терминале

``pip install git+https://github.com/ShashkovS/flake8-ejudge``

либо из под юзера ``ejudge``

``pip install git+https://github.com/ShashkovS/flake8-ejudge --user``


После этого нужно добавить в ``serve.cfg`` в часть с описанием языкового процессора команду запуска::

    [language]
    id = **
    short_name = "python3"
    long_name = "Python3 3.6.5"
    arch = "linux-shared"
    src_sfx = ".py"
    style_checker_cmd = "flake8-ejudge"                        <- Вот здесь самое важное
    style_checker_env = "flake8_ignore=E4,E51,W234"            <- По желанию
    style_checker_env = "max_line_length=120"                  <- По желанию. По умолчанию стоит 160


License
-------

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.
