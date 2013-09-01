# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_PitchClassSet___slots___01():
    r'''Named chromatic pitch-class set can not be changed after initialization.
    '''

    named_pitch_classes = ['gs', 'a', 'as', 'c', 'cs']
    named_pitch_class_set = pitchtools.PitchClassSet(named_pitch_classes)

    assert py.test.raises(AttributeError, 
        "named_pitch_class_set.foo = 'bar'")
