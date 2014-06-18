# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_go_back_01():

    input_ = 'red~example~score g b q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Red Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles


def test_SegmentPackageWrangler_go_back_02():

    input_ = 'G b q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - segments',
        'Abjad IDE - scores',
        ]
    assert score_manager._transcript.titles == titles