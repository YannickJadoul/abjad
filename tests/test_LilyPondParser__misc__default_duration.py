import abjad


def test_LilyPondParser__misc__default_duration_01():

    target = abjad.Container(
        abjad.makers.make_notes(
            [0], [(1, 4), (1, 2), (1, 2), (1, 8), (1, 8), (3, 16), (3, 16)]
        )
    )
    target[-2].multiplier = (5, 17)
    target[-1].multiplier = (5, 17)

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            c'4
            c'2
            c'2
            c'8
            c'8
            c'8. * 5/17
            c'8. * 5/17
        }
        """
    )

    string = r"""{ c' c'2 c' c'8 c' c'8. * 5/17 c' }"""

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
