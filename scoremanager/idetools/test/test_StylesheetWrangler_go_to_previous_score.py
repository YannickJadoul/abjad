# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_go_to_previous_score_01():

    input_ = 'red~example~score y << q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Étude Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles


def test_StylesheetWrangler_go_to_previous_score_02():

    input_ = 'Y << q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - stylesheets',
        'Red Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles