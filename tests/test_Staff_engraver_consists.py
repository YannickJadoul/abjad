import abjad


def test_Staff_engraver_consists_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    staff.consists_commands.append("Horizontal_bracket_engraver")
    staff.consists_commands.append("Instrument_name_engraver")

    assert abjad.wf.wellformed(staff)
    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        \with
        {
            \consists Horizontal_bracket_engraver
            \consists Instrument_name_engraver
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
    )
