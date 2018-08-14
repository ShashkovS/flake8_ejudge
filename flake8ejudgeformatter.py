from flake8.formatting import base

_SEPS = ['"', '(', ')', "'"]
_ERROR_FORMAT = 'ej:{row}:{col}: {code} {text} ({rutext})'

def _extract_template(code, text):
    seps = [(i, c) for i, c in enumerate(text) if c in _SEPS]
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
                text = text[:ff] + '$' + str(i // 2) + text[tt + 1:]
    if code == 'F811':  # redefinition of unused $0 from line 273
        rsp = text.rfind(' ')
        replacers.append(text[rsp + 1:])
        text = text[:rsp + 1] + '$1'
    elif code in (
    'E301', 'E302', 'E305', 'E306'):  # expected 2 blank lines after class or function definition, found
        rsp = text.rfind(' ')
        replacers.append(text[rsp + 1:])
        text = text[:rsp + 1] + '$0'
    elif code == 'F405':  # $0 may be undefined, or defined from star imports:
        rsp = text.rfind('imports:')
        replacers.append(text[rsp + 9:])
        text = text[:rsp + 9] + '$1'
    return text, replacers


class Flake8EjudgeFormatter(base.BaseFormatter):
    """Flake8's formatter."""

    def format(self, error):
        code = error.code
        text = error.text
        path = error.filename
        row = error.line_number
        col = error.column_number
        text, replacers = _extract_template(code, text)
        rutext = ''
        return _ERROR_FORMAT.format(**locals())
