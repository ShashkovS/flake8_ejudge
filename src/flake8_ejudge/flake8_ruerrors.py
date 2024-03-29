# см. https://lintlyci.github.io/Flake8Rules/
code_to_ru_text = {
    'A001': 'Имя {0} уже используется в python. Назовите как-нибудь по-другому или добавьте "_" в конец',
    'A002': 'Имя {0} уже используется в python. Назовите как-нибудь по-другому или добавьте "_" в конец',
    'A003': 'Имя {0} уже используется в python. Назовите как-нибудь по-другому или добавьте "_" в конец',
    'C901': 'Цикломатическая сложность функции {0} (или всей программы) слишком велика: {1}. Разбейте её на подфункции, сделайте логику более линейной.',
    'E101': 'Отступ содержит и пробелы, и табуляции. Замените всё на пробелы.',
    'E111': 'Величина отступа должна делиться на 4',
    'E112': 'Здесь должен быть сдвинутый блок',
    'E113': 'Здесь не может быть такого отступа',
    'E114': 'Величина отступа должна делиться на 4, а не делится: {0}',
    'E115': 'Здесь должен быть сдвинутый блок {0}',
    'E116': 'Здесь не может быть такого отступа {0}',
    'E117': 'Слишком большой отступ. Должен быть самый маленький из делящихся на 4. Например, 4, а не 5 и не 8.',
    'E121': 'Строчка продолжает предыдущую со слишком маленьким отступом. Сделайте хотя бы 4.',
    'E122': 'Строчка продолжает предыдущую без отступа. Сделайте хотя бы 4.',
    'E123': "Закрывающая скобка в таком контексте должна стоять на том же уровне, что и начало строчки, в которой эта скобка открыта",
    'E124': 'Закрывающая скобка в таком контексте должна стоять на том же уровне, что и её открывающая',
    'E126': 'continuation line over-indented for hanging indent',
    'E127': 'continuation line over-indented for visual indent',
    'E128': 'continuation line under-indented for visual indent',
    'E129': 'visually indented line with same indent as next logical line',
    'E131': 'continuation line unaligned for hanging indent',
    'E201': 'Удалите пробел после {0}',
    'E202': 'Удалите пробел перед {0}',
    'E203': 'Удалите пробел перед {0}',
    'E211': 'Удалите пробел перед {0}',
    'E221': 'Тут больше 1 пробела, оставьте ровно 1',
    'E222': 'Тут больше 1 пробела, оставьте ровно 1',
    'E225': 'Поставьте пробелы вокруг оператора',
    'E226': 'Поставьте пробелы вокруг оператора',
    'E227': 'Поставьте пробелы вокруг оператора',
    'E228': 'Поставьте пробелы вокруг оператора',
    'E231': 'Добавьте пробел после {0}',
    'E241': 'Тут после {0} больше 1 пробела, оставьте ровно 1',
    'E251': 'В параметрах знак «=» пробелами не отделяется, удалите пробелы',
    'E261': 'Перед строчным комментарием поставьте 2 пробела',
    'E262': 'Строчный комментарий должен начинаться с {0}',
    'E265': 'Блочный комментарий должен начинаться с {0}',
    'E266': 'Слишком много символов "#" для комментария. Оставьте ровно 1',
    'E271': 'Оставьте ровно 1 пробел после ключевого слова',
    'E272': 'Оставьте ровно 1 пробел перед ключевым словов',
    'E275': 'Поставьте ровно 1 пробел после ключевого слова',
    'E301': 'Между методами класса оставляйте ровно 1 пустую строку (а не {0})',
    'E302': 'Между функциями и классами делайте ровно 2 пустых строчки (а не {0})',
    'E303': 'Слишком много пустых строк: {0}. Между функциями ставьте 2, между методами класса — 1.',
    'E304': 'Удалите пустую строку между декоратором и функцией',
    'E305': 'После функций и классов вставляйте ровно 2 пустых строки (а не {0})',
    'E306': 'Вложенные функции отделяйте ровно 1 пустой строкой (а не {0})',
    'E401': 'Разнесите импорты на несколько строчек',
    'E402': 'Импорт модулей перенесите в самое начало',
    'E501': 'Эта строчка слишком длинная: {0}. Разбейте её на несколько, используйте промежуточные переменные.',
    'E502': 'Удалите "\\", в данном контексте он не нужен',
    'E701': 'Разные команды должны быть на разных строчках. Так код лучше читается.',
    'E702': 'Разные команды должны быть на разных строчках. Так код лучше читается.',
    'E703': 'Удалите ";", точка с запятой не нужны в питоне',
    'E704': 'Разные команды должны быть на разных строчках. Так код лучше читается.',
    'E711': 'Сравнивать с None надо так: "if var is None"',
    'E712': 'Сравнивать с True/False надо так: "if var:" или "if not var:". Или так "if var is True:", если важна проверка типа',
    'E713': 'Лучше писать не "not var in list", а "var not in list", так легче читать',
    'E714': 'Лучше писать не "not var is None", а "var is not None", так легче читать',
    'E721': 'Лучше не сравнивать типы "type(var)==...", и спользовать isinstance: "isinstance(var, ...)"',
    'E722': "Лучше в except указывать список отлавливаемых ошибок (\"except SomeError\" или \"except (Err1, Err2)\"",
    'E731': 'Используйте def для определения функции, не присваивайте lambda функции переменным',
    'E741': 'Не используйте «I», «O» и «l» в качестве имён переменных, их легко спутать с 1 или 0',
    'E743': 'Не используйте «I», «O» и «l» в качестве имён функций, их легко спутать с 1 или 0',
    'F401': 'Объект {0} импортирован, но не использован. Удалите его',
    'F403': 'Не используйте "from module import *". Укажите явно список импортированных объектов ("from module import fun, obj")',
    'F405': 'Возможно, переменная {0} не инициализирована (или импортирована неявно "from module import *")',
    'F406': '‘from module import *’ нельзя делать внутри функии. Да и вообще лучше писать "from module import fun, obj" в начале модуля',
    'F601': 'В словаре ключ {0} перезаписывается разными значениями',
    'F701': 'break нельзя использовать вне цикла',
    'F706': 'return нельзя использовать вне функции',
    'F811': 'Здесь переопределение {0} из строчки {1}. Удалите одно из них.',
    'F821': 'Переменная {0} не определена там, где используется. Определите её',
    'F823': 'Локальная переменная {0}{1} используется до объявления. Определите её',
    'F841': 'Локальная переменная {0} определена, но нигде не используется. Удалите её',
    'W191': 'Отступ содержит табуляции. Замените на пробелы',
    'W291': 'Удалите пробелы из конца строки',
    'W292': 'Добавьте ровно 1 пустую строчку в конец файла',
    'W293': 'Из пустой строки удалите все пробелы и табуляции',
    'W391': 'Удалите лишние пустые строчки из конца файла, оставьте ровно 1',
    'W503': 'Сделайте перенос строки после бинарного оператора, а не до',
    'N179': 'Вместо return "YES"/"NO" делайте return True/False'
}

text_to_ru_text = {
    "IndentationError: unindent does not match any outer indentation level": 'Отступ не соответствует ни одному использованному, исправьте',
    "TokenError: EOF in multi-line statement": 'Многострочное выражение прерывается в конце файла, что-то не закрыто или не дописано',
    "SyntaxError: can't assign to comparison": 'Нельзя присваивать сравнению',
    "SyntaxError: can't assign to function call": 'Нельзя присваивать вызову функции',
    "SyntaxError: can't assign to operator": 'Нельзя присваивать оператору',
    "SyntaxError: keyword can't be an expression": 'Нельзя использовать ключевое слово',
    "IndentationError: expected an indented block": 'Здесь должен быть отступ',
    "IndentationError: unexpected indent": 'Некорректный отступ',
    "SyntaxError: EOL while scanning string literal": 'Пропущена кавычка, завершающая строку',
    "SyntaxError: invalid character in identifier": 'Некорректный символ в имени',
    "SyntaxError: invalid syntax": 'Неверный синтаксис',
    "SyntaxError: invalid token": 'Недопустимый токен',
    "SyntaxError: positional argument follows keyword argument": 'После параметра, переданного по имени, могут идти только параметры, переданные по имени',
    "SyntaxError: unexpected character after line continuation character": 'Недопустимый символ после символа продолжения строки',
    "SyntaxError: unexpected EOF while parsing": 'Что-то не закрыто или не дописано',
}
