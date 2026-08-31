from flake8.formatting import base
from flake8.violation import Violation

LINE_STARTER = '>Line '

_ERROR_FORMAT = LINE_STARTER + '{row}: {code} '


class Flake8EjudgeFormatter(base.BaseFormatter):
    """Flake8's formatter."""

    def format(self, error):
        code = error.code
        text = error.text
        row = error.line_number
        st = _ERROR_FORMAT.format(**locals())
        return st + text

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
