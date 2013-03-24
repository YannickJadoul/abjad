from abjad import *
import py.test


def test_measuretools_pad_measures_in_expr_with_rests_01():

    t = Staff(2 * measuretools.Measure((2, 8), "c'8 d'8"))

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            c'8
            d'8
        }
    }
    '''

    measuretools.pad_measures_in_expr_with_rests(t, Duration(1, 32), Duration(1, 64))

    r'''
    \new Staff {
        {
            \time 19/64
            r32
            c'8
            d'8
            r64
        }
        {
            r32
            c'8
            d'8
            r64
        }
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 19/64\n\t\tr32\n\t\tc'8\n\t\td'8\n\t\tr64\n\t}\n\t{\n\t\tr32\n\t\tc'8\n\t\td'8\n\t\tr64\n\t}\n}"


def test_measuretools_pad_measures_in_expr_with_rests_02():
    '''Works when measures contain stacked voices.
    '''

    measure = Measure((2, 8), 2 * Voice(notetools.make_repeated_notes(2)))
    measure.is_parallel = True
    t = Staff(measure * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Staff {
        <<
            \time 1/4
            \new Voice {
                c'8
                d'8
            }
            \new Voice {
                e'8
                f'8
            }
        >>
        <<
            \time 1/4
            \new Voice {
                g'8
                a'8
            }
            \new Voice {
                b'8
                c''8
            }
        >>
    }
    '''

    measuretools.pad_measures_in_expr_with_rests(t, Duration(1, 32), Duration(1, 64))

    r'''
    \new Staff {
        <<
            \time 19/64
            \new Voice {
                r32
                c'8
                d'8
                r64
            }
            \new Voice {
                r32
                e'8
                f'8
                r64
            }
        >>
        <<
            \time 19/64
            \new Voice {
                r32
                g'8
                a'8
                r64
            }
            \new Voice {
                r32
                b'8
                c''8
                r64
            }
        >>
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Staff {\n\t<<\n\t\t\\time 19/64\n\t\t\\new Voice {\n\t\t\tr32\n\t\t\tc'8\n\t\t\td'8\n\t\t\tr64\n\t\t}\n\t\t\\new Voice {\n\t\t\tr32\n\t\t\te'8\n\t\t\tf'8\n\t\t\tr64\n\t\t}\n\t>>\n\t<<\n\t\t\\time 19/64\n\t\t\\new Voice {\n\t\t\tr32\n\t\t\tg'8\n\t\t\ta'8\n\t\t\tr64\n\t\t}\n\t\t\\new Voice {\n\t\t\tr32\n\t\t\tb'8\n\t\t\tc''8\n\t\t\tr64\n\t\t}\n\t>>\n}"


def test_measuretools_pad_measures_in_expr_with_rests_03():
    '''Set splice to true to extend edge spanners over newly insert rests.
    '''

    t = Measure((2, 8), "c'8 d'8")
    beamtools.BeamSpanner(t[:])
    measuretools.pad_measures_in_expr_with_rests(t, Duration(1, 32), Duration(1, 64), splice=True)

    r'''
    {
        \time 19/64
        r32 [
        c'8
        d'8
        r64 ]
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "{\n\t\\time 19/64\n\tr32 [\n\tc'8\n\td'8\n\tr64 ]\n}"
