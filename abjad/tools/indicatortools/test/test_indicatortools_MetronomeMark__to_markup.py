# -*- coding: utf -*-
from abjad import *


def test_indicatortools_MetronomeMark__to_markup_01():

    mark = MetronomeMark(Duration(1, 4), 60)
    markup = mark._to_markup()

    assert format(markup) == String.normalize(
        r'''
        \markup {
            \fontsize
                #-6
                \general-align
                    #Y
                    #DOWN
                    \note-by-number
                        #2
                        #0
                        #1
            \upright
                {
                    =
                    60
                }
            }
        '''
        ), format(markup)


def test_indicatortools_MetronomeMark__to_markup_02():

    mark = MetronomeMark(Duration(3, 8), 60)
    markup = mark._to_markup()

    assert format(markup) == String.normalize(
        r'''
        \markup {
            \fontsize
                #-6
                \general-align
                    #Y
                    #DOWN
                    \note-by-number
                        #3
                        #1
                        #1
            \upright
                {
                    =
                    60
                }
            }
        '''
        ), format(markup)
