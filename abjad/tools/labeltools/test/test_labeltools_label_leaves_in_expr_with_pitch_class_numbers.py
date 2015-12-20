# -*- coding: utf-8 -*-
from abjad import *


def test_labeltools_label_leaves_in_expr_with_pitch_class_numbers_01():
    r'''With number=True.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    labeltools.label_leaves_in_expr_with_pitch_class_numbers(
        staff, number=True)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8
                _ \markup {
                    \small
                        0
                    }
            d'8
                _ \markup {
                    \small
                        2
                    }
            e'8
                _ \markup {
                    \small
                        4
                    }
            f'8
                _ \markup {
                    \small
                        5
                    }
        }
        '''
        )

    assert inspect_(staff).is_well_formed()