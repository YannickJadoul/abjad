import abjad


def test_LilyPondParser__functions__grace_01():

    target = abjad.Container([abjad.Note("c'4"), abjad.Note("d'4"), abjad.Note("e'2")])

    grace = abjad.BeforeGraceContainer([abjad.Note("g''16"), abjad.Note("fs''16")])

    abjad.attach(grace, target[2])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            c'4
            d'4
            \grace {
                g''16
                fs''16
            }
            e'2
        }
        """
    )

    string = r"{ c'4 d'4 \grace { g''16 fs''16} e'2 }"
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
