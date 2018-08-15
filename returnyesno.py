import re

N179 = "N179 Do not return 'YES'/'NO', use return True/False"

yes_no_regex = re.compile(r'''\s*return\s*['"](?:yes|no)['"]\s*''', flags=re.IGNORECASE)


def returnyesno(physical_line):
    m = yes_no_regex.fullmatch(physical_line)
    if m:
        ps = physical_line.find('return')
        return (ps + 7, N179)


returnyesno.name = 'return_yes_no_checker'
returnyesno.version = '0.0.1'
