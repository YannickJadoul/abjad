import abjad


def test_Staff_engraver_removals_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    staff.remove_commands.append("Time_signature_engraver")
    staff.remove_commands.append("Bar_number_engraver")

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        \with
        {
            \remove Time_signature_engraver
            \remove Bar_number_engraver
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
    )

    assert abjad.wf.wellformed(staff)
