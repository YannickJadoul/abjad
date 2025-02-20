import abjad


def test_Tuplet_grob_override_01():

    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8 f'8")
    abjad.override(tuplet).Glissando.thickness = 3

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \override Glissando.thickness = 3
        \tweak edge-height #'(0.7 . 0)
        \times 2/3
        {
            c'8
            d'8
            e'8
            f'8
        }
        \revert Glissando.thickness
        """
    )
