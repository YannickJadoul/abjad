# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_NoteHeadList___setitem___01():
    r'''Set note-head with pitch number.
    '''

    chord = Chord("<c' d'>4")
    chord.note_heads[1] = 4

    assert format(chord) == "<c' e'>4"


def test_scoretools_NoteHeadList___setitem___02():
    '''Set note-head with pitch.
    '''

    chord = Chord("<c' d'>4")
    chord.note_heads[1] = NamedPitch("e'")

    assert format(chord) == "<c' e'>4"


def test_scoretools_NoteHeadList___setitem___03():
    r'''Set note-head with tweaked note-head.
    '''

    chord = Chord("<c' cs'' f''>4")
    note_head = scoretools.NoteHead(3)
    note_head.tweak.color = 'red'
    chord.note_heads[0] = note_head

    assert format(chord) == String.normalize(
        r'''
        <
            \tweak color #red
            ef'
            cs''
            f''
        >4
        '''
        )

    assert inspect(chord).is_well_formed()
