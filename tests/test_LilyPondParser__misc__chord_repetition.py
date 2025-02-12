import abjad


def test_LilyPondParser__misc__chord_repetition_01():

    target = abjad.Container(
        [
            abjad.Chord([0, 4, 7], (1, 4)),
            abjad.Chord([0, 4, 7], (1, 4)),
            abjad.Chord([0, 4, 7], (1, 4)),
            abjad.Chord([0, 4, 7], (1, 4)),
        ]
    )

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            <c' e' g'>4
            <c' e' g'>4
            <c' e' g'>4
            <c' e' g'>4
        }
        """
    )

    string = r"""{ <c' e' g'> q q q }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__misc__chord_repetition_02():

    target = abjad.Staff(
        [
            abjad.Chord([0, 4, 7], (1, 8)),
            abjad.Chord([0, 4, 7], (1, 8)),
            abjad.Chord([0, 4, 7], (1, 4)),
            abjad.Chord([0, 4, 7], (3, 16)),
            abjad.Chord([0, 4, 7], (1, 16)),
            abjad.Chord([0, 4, 7], (1, 4)),
        ]
    )

    dynamic = abjad.Dynamic("p")
    abjad.attach(dynamic, target[0])
    articulation = abjad.Articulation("staccatissimo")
    abjad.attach(articulation, target[2])
    markup = abjad.Markup(r"\markup { text }")
    abjad.attach(markup, target[3], direction=abjad.UP)
    articulation = abjad.Articulation("staccatissimo")
    abjad.attach(articulation, target[-1])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            <c' e' g'>8
            \p
            <c' e' g'>8
            <c' e' g'>4
            - \staccatissimo
            <c' e' g'>8.
            ^ \markup { text }
            <c' e' g'>16
            <c' e' g'>4
            - \staccatissimo
        }
        """
    )

    string = r"""\new Staff { <c' e' g'>8\p q q4-! q8.^"text" q16 q4-! }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__misc__chord_repetition_03():

    target = abjad.Container(
        [
            abjad.Chord([0, 4, 7], (1, 8)),
            abjad.Note(12, (1, 8)),
            abjad.Chord([0, 4, 7], (1, 8)),
            abjad.Note(12, (1, 8)),
            abjad.Rest((1, 4)),
            abjad.Chord([0, 4, 7], (1, 4)),
        ]
    )

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            <c' e' g'>8
            c''8
            <c' e' g'>8
            c''8
            r4
            <c' e' g'>4
        }
        """
    )

    string = r"""{ <c' e' g'>8 c'' q c'' r4 q }"""
    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
