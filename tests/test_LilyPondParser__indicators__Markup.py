import abjad


def test_LilyPondParser__indicators__Markup_01():

    target = abjad.Staff([abjad.Note(0, 1)])
    markup = abjad.Markup(r"\markup { hello! }")
    abjad.attach(markup, target[0], direction=abjad.UP)

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'1
            ^ \markup { hello! }
        }
        """
    )

    string = r"""\new Staff { c'1 ^ "hello!" }"""

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    assert 1 == len(abjad.get.markup(result[0]))


def test_LilyPondParser__indicators__Markup_02():

    target = abjad.Staff([abjad.Note(0, (1, 4))])
    markup = abjad.Markup(r'\markup { X Y Z "a b c" }')
    abjad.attach(markup, target[0], direction=abjad.DOWN)

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'4
            _ \markup { X Y Z "a b c" }
        }
        """
    ), repr(target)


def test_LilyPondParser__indicators__Markup_03():
    """
    Articulations following markup block are (re)lexed correctly after
    returning to the "notes" lexical state after popping the "markup lexical state.
    """

    target = abjad.Staff([abjad.Note(0, (1, 4)), abjad.Note(2, (1, 4))])
    markup = abjad.Markup(r"\markup { hello }")
    abjad.attach(markup, target[0], direction=abjad.UP)
    articulation = abjad.Articulation(".")
    abjad.attach(articulation, target[0])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'4
            - \staccato
            ^ \markup { hello }
            d'4
        }
        """
    )

    string = r"""\new Staff { c' ^ \markup { hello } -. d' }"""

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    assert 1 == len(abjad.get.markup(result[0]))


def test_LilyPondParser__indicators__Markup_04():

    string_1 = r"""\markup { \bold { A B C } \italic 123 }"""

    string_2 = r"""\markup { \bold
    {
        A
        B
        C
    } \italic
    123 }"""

    parser = abjad.parser.LilyPondParser()
    markup = parser(string_1)
    assert abjad.lilypond(markup) == string_2
