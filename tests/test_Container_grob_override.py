import abjad


def test_Container_grob_override_01():
    """
    Noncontext containers bracket grob overrides at opening and closing.
    """

    container = abjad.Container("c'8 d'8 e'8 f'8")
    abjad.override(container).Glissando.thickness = 3

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \override Glissando.thickness = 3
            c'8
            d'8
            e'8
            f'8
            \revert Glissando.thickness
        }
        """
    )
