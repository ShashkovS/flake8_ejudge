from flake8.formatting import base
from flake8_ejudge.flake8_ruerrors import code_to_ru_text, text_to_ru_text
from flake8.violation import Violation

LINE_STARTER = '>Line '

_SEPS = ['"', '(', ')', "'"]
_ERROR_FORMAT = LINE_STARTER + '{row}: {code} '


def _extract_template(code, text):
    seps = [(i, c) for i, c in enumerate(text) if c in _SEPS]
    # Если у нас один сепаратор внутри других сепараторов, то он — не сепаратор.
    for i in range(len(seps) - 2, 0, -1):
        i1, c1 = seps[i - 1]
        i2, c2 = seps[i]
        i3, c3 = seps[i + 1]
        if i1 + 1 == i2 == i3 - 1 and c1 == c3 != c2:
            seps.pop(i)
    replacers = []
    if seps:
        if len(seps) % 2 != 0:
            # print('Неуравновешено:', err_text)
            pass
        else:
            replacers = [text[seps[i][0]:seps[i + 1][0] + 1] for i in range(0, len(seps), 2)]
            for i in range(len(seps) - 2, -1, -2):
                ff = seps[i][0]
                tt = seps[i + 1][0]
                text = text[:ff] + '{' + str(i // 2) + '}' + text[tt + 1:]
    if code == 'F811':  # redefinition of unused $0 from line 273
        rsp = text.rfind(' ')
        replacers.append(text[rsp + 1:])
        text = text[:rsp + 1] + '{1}'
    elif code in ('E301', 'E302', 'E305', 'E306'):  # expected 2 blank lines after class or function definition, found
        rsp = text.rfind(' ')
        replacers.append(text[rsp + 1:])
        text = text[:rsp + 1] + '{0}'
    elif code == 'F405':  # $0 may be undefined, or defined from star imports:
        rsp = text.rfind('imports:')
        replacers.append(text[rsp + 9:])
        text = text[:rsp + 9] + '{1}'
    elif code == 'E712':  # comparison to False should be {0} or {1}
        if 'False' in text:
            text = text.replace('False', '{2}')
            replacers.append('False')
        elif 'True' in text:
            text = text.replace('True', '{2}')
            replacers.append('True')

    return text, replacers


_extract_template('E211', "whitespace before '('")


class Flake8EjudgeFormatter(base.BaseFormatter):
    """Flake8's formatter."""

    def format(self, error):
        code = error.code
        text = error.text
        path = error.filename
        row = error.line_number
        col = error.column_number
        text_r, replacers = _extract_template(code, text)
        if code in code_to_ru_text:
            try:
                rutext = code_to_ru_text[code].format(*replacers)
            except:
                rutext = code_to_ru_text[code]
        elif text_r in text_to_ru_text:
            try:
                rutext = text_to_ru_text[text_r].format(*replacers)
            except:
                rutext = text_to_ru_text[text_r]
        else:
            rutext = ''
        st = _ERROR_FORMAT.format(**locals())
        res = st + text
        if rutext:
            res += '\n' + ' ' * len(st) + rutext
        return res

    def show_source(self, error: Violation):
        """Show the physical line generating the error.

        This also adds an indicator for the particular part of the line that
        is reported as generating the problem.

        :param error:
            This will be an instance of
            :class:`~flake8.violation.Violation`.
        :returns:
            The formatted error string if the user wants to show the source.
            If the user does not want to show the source, this will return
            ``None``.
        """
        if not self.options.show_source or error.physical_line is None:
            return ""

        # Because column numbers are 1-indexed, we need to remove one to get
        # the proper number of space characters.
        indent = "".join(
            c if c.isspace() else " "
            for c in error.physical_line[: error.column_number - 1]
        )
        physical_line = error.physical_line.rstrip()
        return f"{physical_line}\n{indent}^"
