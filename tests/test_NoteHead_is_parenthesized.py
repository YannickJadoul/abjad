import abjad


def test_NoteHead_is_parenthesized_01():

    note_head = abjad.NoteHead(written_pitch="c'")
    assert note_head.is_parenthesized is None
    note_head.is_parenthesized = True
    assert note_head.is_parenthesized is True
    note_head.is_parenthesized = False
    assert note_head.is_parenthesized is False


def test_NoteHead_is_parenthesized_02():

    note_head = abjad.NoteHead(written_pitch="c'")
    note_head.is_parenthesized = True
    assert abjad.lilypond(note_head) == abjad.string.normalize(
        r"""
        \parenthesize
        c'
        """
    )


def test_NoteHead_is_parenthesized_03():

    note = abjad.Note("c'4")
    note.note_head.is_parenthesized = True
    assert abjad.lilypond(note) == abjad.string.normalize(
        r"""
        \parenthesize
        c'4
        """
    )


def test_NoteHead_is_parenthesized_04():

    chord = abjad.Chord("<c' e' g'>4")
    chord.note_heads[1].is_parenthesized = True
    assert abjad.lilypond(chord) == abjad.string.normalize(
        r"""
        <
            c'
            \parenthesize
            e'
            g'
        >4
        """
    )
