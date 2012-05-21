from abjad import *
from abjad.tools import pitcharraytools
from abjad.tools.pitcharraytools import PitchArrayCell
import py.test


def testPitchObjectArrayCell_prev_01():

    array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])

    '''
    [] [      ] []
    [      ] [] []
    '''

    assert array[0][1].prev is array[0][0]


def testPitchObjectArrayCell_prev_02():

    array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])

    '''
    [] [      ] []
    [      ] [] []
    '''

    assert py.test.raises(IndexError, 'array[0][0].prev')


def testPitchObjectArrayCell_prev_03():

    cell = PitchArrayCell([pitchtools.NamedChromaticPitch(1)])

    assert py.test.raises(IndexError, 'cell.prev')
