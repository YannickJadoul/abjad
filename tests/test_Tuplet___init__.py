import abjad


def test_Tuplet___init___01():
    """
    Initializes tuplet from empty input.
    """

    tuplet = abjad.Tuplet()

    assert abjad.lilypond(tuplet) == "\\times 2/3\n{\n}"
    assert tuplet.multiplier == abjad.Multiplier(2, 3)
    assert not len(tuplet)
