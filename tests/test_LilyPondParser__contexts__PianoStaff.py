import abjad


def test_LilyPondParser__contexts__PianoStaff_01():

    target = abjad.StaffGroup(
        [
            abjad.Staff(abjad.makers.make_notes([0, 2, 4, 5, 7], (1, 8))),
            abjad.Staff(abjad.makers.make_notes([0, 2, 4, 5, 7], (1, 8))),
        ]
    )
    target.lilypond_type = "PianoStaff"

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new PianoStaff
        <<
            \new Staff
            {
                c'8
                d'8
                e'8
                f'8
                g'8
            }
            \new Staff
            {
                c'8
                d'8
                e'8
                f'8
                g'8
            }
        >>
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
