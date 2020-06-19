"""Utility functions to make life easier."""
from textwrap import dedent


def mls(mlstr):
    """Return a quoted JSON Multiline string."""
    mlstr = dedent(mlstr).strip().replace("\n", "\\n").replace('"', '\\"')
    return f'"{mlstr}"'


def KB(size):  # pylint: disable=invalid-name
    """Return number of bytes in a whole KB."""
    return str(size * 1024)


def MB(size):  # pylint: disable=invalid-name
    """Return number of bytes in a whole MB."""
    return str(size * 1024 * 1024)
