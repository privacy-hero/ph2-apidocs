"""Utility functions to make life easier."""
from textwrap import dedent


def mls(mlstr):
    """Return a quoted JSON Multiline string."""
    mlstr = dedent(mlstr).strip().replace("\n", "\\n")
    return f'"{mlstr}"'
