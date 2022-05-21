# -*- coding: utf-8 -*-
"""Nox Template Script."""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

def add_short_name(short_name):
    """Doit for short decorator.

    Args:
        short_name (str): short alias name.

    Returns:
        callable: decoartor function.
    """

    def decorator(func):
        globals()["task_{0}".format(short_name)] = func  # noqa: WPS421
        return func

    return decorator
