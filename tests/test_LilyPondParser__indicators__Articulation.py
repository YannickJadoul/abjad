import abjad


def test_LilyPondParser__indicators__Articulation_01():

    target = abjad.Staff(abjad.makers.make_notes(["c''"], [(1, 4)] * 6 + [(1, 2)]))
    articulation = abjad.Articulation("marcato")
    abjad.attach(articulation, target[0], direction=abjad.UP)
    articulation = abjad.Articulation("stopped")
    abjad.attach(articulation, target[1], direction=abjad.DOWN)
    articulation = abjad.Articulation("tenuto")
    abjad.attach(articulation, target[2])
    articulation = abjad.Articulation("staccatissimo")
    abjad.attach(articulation, target[3])
    articulation = abjad.Articulation("accent")
    abjad.attach(articulation, target[4])
    articulation = abjad.Articulation("staccato")
    abjad.attach(articulation, target[5])
    articulation = abjad.Articulation("portato")
    abjad.attach(articulation, target[6])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c''4
            ^ \marcato
            c''4
            _ \stopped
            c''4
            - \tenuto
            c''4
            - \staccatissimo
            c''4
            - \accent
            c''4
            - \staccato
            c''2
            - \portato
        }
        """
    )

    string = r"""\new Staff { c''4^^ c''_+ c''-- c''-! c''4-> c''-. c''2-_ }"""

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    for x in result:
        assert 1 == len(abjad.get.indicators(x, abjad.Articulation))


def test_LilyPondParser__indicators__Articulation_02():

    target = abjad.Staff([abjad.Note("c'", (1, 4))])
    articulation = abjad.Articulation("marcato")
    abjad.attach(articulation, target[0], direction=abjad.UP)
    articulation = abjad.Articulation("stopped")
    abjad.attach(articulation, target[0], direction=abjad.DOWN)
    articulation = abjad.Articulation("tenuto")
    abjad.attach(articulation, target[0])
    articulation = abjad.Articulation("staccatissimo")
    abjad.attach(articulation, target[0])
    articulation = abjad.Articulation("accent")
    abjad.attach(articulation, target[0])
    articulation = abjad.Articulation("staccato")
    abjad.attach(articulation, target[0])
    articulation = abjad.Articulation("portato")
    abjad.attach(articulation, target[0])

    string = r"""\new Staff { c'4 ^^ _+ -- -! -> -. -_ }"""

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    assert 7 == len(abjad.get.indicators(result[0], abjad.Articulation))


def test_LilyPondParser__indicators__Articulation_03():

    target = abjad.Container(
        abjad.makers.make_notes(
            ["c''", "c''", "b'", "c''"], [(1, 4), (1, 4), (1, 2), (1, 1)]
        )
    )

    articulation = abjad.Articulation("staccato")
    abjad.attach(articulation, target[0])
    articulation = abjad.Articulation("mordent")
    abjad.attach(articulation, target[1])
    articulation = abjad.Articulation("turn")
    abjad.attach(articulation, target[2])
    articulation = abjad.Articulation("fermata")
    abjad.attach(articulation, target[3])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            c''4
            - \staccato
            c''4
            - \mordent
            b'2
            - \turn
            c''1
            - \fermata
        }
        """
    )

    string = r"""{ c''4\staccato c''\mordent b'2\turn c''1\fermata }"""

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
    for x in result:
        assert 1 == len(abjad.get.indicators(x, abjad.Articulation))
