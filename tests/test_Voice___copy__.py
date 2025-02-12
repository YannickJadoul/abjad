import copy

import abjad


def test_Voice___copy___01():
    """
    Voices copy name, engraver removals, engraver consists, grob overrides and
    context settings. Voices do not copy components.
    """

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_1.name = "SopranoVoice"
    voice_1.remove_commands.append("Forbid_line_break_engraver")
    voice_1.consists_commands.append("Time_signature_engraver")
    abjad.override(voice_1).NoteHead.color = "#red"
    abjad.setting(voice_1).tupletFullLength = True
    voice_2 = copy.copy(voice_1)

    assert abjad.lilypond(voice_2) == abjad.string.normalize(
        r"""
        \context Voice = "SopranoVoice"
        \with
        {
            \remove Forbid_line_break_engraver
            \consists Time_signature_engraver
            \override NoteHead.color = #red
            tupletFullLength = ##t
        }
        {
        }
        """
    )
