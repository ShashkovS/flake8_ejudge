from unittest import TestCase
import io
import os
import base64

from flake8_ejudge import flake8_ejudge_runner

E225 = 'files_to_flake/E225.py'
TERRIBLE = 'files_to_flake/horrible.py'
LONG = 'files_to_flake/long.py'
REGEX_CHECK_NO = 'files_to_flake/regex_check_no.py'
REGEX_CHECK_YES = 'files_to_flake/regex_check_yes.py'
YES_NO = 'files_to_flake/yes_no.py'


def run(filename):
    log_capture_string = io.StringIO()
    flake8_ejudge_runner.style_check(filename, f_obj=log_capture_string)
    stdout_data = log_capture_string.getvalue()
    log_capture_string.close()
    return stdout_data


class SomeTest(TestCase):
    def test_E225(self):
        res = run(E225)
        self.assertTrue('Поставьте пробелы вокруг оператора' in res)

    def test_many_errors(self):
        res = run(TERRIBLE)
        self.assertTrue('Слишком много пустых строк' in res)
        self.assertTrue('Удалите пробел после' in res)
        self.assertTrue('Удалите пробел перед' in res)
        self.assertTrue('Имя "print" уже используется' in res)

    def test_env_setup(self):
        res = run(LONG)
        self.assertTrue('Эта строчка слишком длинная' in res)
        os.environ['max_line_length'] = '500'
        res = run(LONG)
        self.assertEqual(res, '')
        res = run(TERRIBLE)
        self.assertTrue('Используйте автоформатирование кода' in res)
        os.environ['max_errors_to_show'] = '500'
        res = run(TERRIBLE)
        self.assertFalse('Используйте автоформатирование кода' in res)

    def test_regex(self):
        os.environ["chk_pattern_1"] = r"\.find\b|\.rfind\b"
        os.environ["chk_in_or_not_1"] = "not"
        os.environ["chk_err_msg_1"] = "Запрещается использовать методы find и rfind"

        os.environ["chk_pattern_2"] = r"def my_func\(parm1: int, parm2: str\) -> bool:"
        os.environ["chk_in_or_not_2"] = "in"
        os.environ["chk_err_msg_2"] = "Необходима реализация функции сигнатуры `def my_func(parm1: int, parm2: str) -> bool:`"

        style_regex = r'(?m)^def\s+(\w+)\s*\(.*\n?(?:^(?:[ \t].*|)$\n)*[ \t].*?\b\1\s*\('
        encoded = 'b32_' + base64.b32encode(style_regex.encode('utf-8')).decode()
        os.environ["chk_pattern_13"] = encoded
        os.environ["chk_in_or_not_13"] = "in"
        os.environ["chk_err_msg_13"] = "Решение необходимо оформить в виде рекурсивной функции"

        res = run(REGEX_CHECK_NO)
        self.assertTrue('Запрещается использовать методы find и rfind' in res)
        self.assertTrue('Необходима реализация функции сигнатуры' in res)
        self.assertTrue('Решение необходимо оформить в виде рекурсивной функции' in res)

        res = run(REGEX_CHECK_YES)
        self.assertEqual(res, '')

    def test_yes_no(self):
        res = run(YES_NO)
        self.assertTrue('делайте return True/False' in res)
