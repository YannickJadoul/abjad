# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageManager_edit_illustrate_py_01():

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'M example~numbers ie q'
    score_manager._run(input_=input_)

    assert score_manager._session._attempted_to_open_file