# -*- encoding: utf-8 -*-
import sys
from abjad import *


def test_systemtools_IOManager_count_function_calls_01():

    result = systemtools.IOManager.count_function_calls(
        "Note('c4')",
        globals(),
        )
    if sys.version_info[0] == 2:
        assert result == 10217
    else:
        assert result == 11289


def test_systemtools_IOManager_count_function_calls_02():

    result = systemtools.IOManager.count_function_calls(
        "Note(-12, (1, 4))",
        globals(),
        )
    if sys.version_info[0] == 2:
        assert result == 170
    else:
        assert result == 192
