# -*- coding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.topleveltools import new
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Retrograde(AbjadValueObject):
    r'''Retrograde operator.

    ..  container:: example:

        ::

            >>> pitchtools.Retrograde()
            Retrograde()

    Object model of twelve-tone retrograde operator.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_period',
        )

    ### INITIALIZER ###

    def __init__(self, period=None):
        if period is not None:
            period = abs(int(period))
            assert 0 < period
        self._period = period

    ### SPECIAL METHODS ###

    def __add__(self, operator):
        r'''Composes retrograde and `operator`.

        ..  container:: example

            Example segment:

            ::

                >>> items = [0, 2, 4, 5]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP
    
            Example operators:

            ::

                >>> retrograde = pitchtools.Retrograde()
                >>> transposition = pitchtools.Transposition(n=3)

        ..  container:: example

            Transposition followed by retrograde:

            ::

                >>> operator = retrograde + transposition
                >>> str(operator)
                'RT3'

            ::

                >>> segment_ = operator(segment)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    af'8
                    g'8
                    f'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Same as above because retrograde and transposition commute:

            ::

                >>> operator = transposition + retrograde
                >>> str(operator)
                'T3R'

            ::

                >>> segment_ = operator(segment)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    af'8
                    g'8
                    f'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns compound operator:

            ::

                >>> print(format(operator))
                pitchtools.CompoundOperator(
                    operators=(
                        pitchtools.Retrograde(),
                        pitchtools.Transposition(
                            n=3,
                            ),
                        ),
                    )

        '''
        from abjad.tools import pitchtools
        return pitchtools.CompoundOperator._compose_operators(self, operator)

    def __call__(self, expr):
        r'''Calls retrograde on `expr`.

        ..  container:: example

            Gets retrograde pitch classes:

            ::

                >>> retrograde = pitchtools.Retrograde()
                >>> segment = pitchtools.PitchClassSegment([0, 1, 4, 7])
                >>> retrograde(segment)
                PitchClassSegment([7, 4, 1, 0])

        ..  container:: example

            Does not retrograde single pitches or pitch-classes:

            ::

                >>> retrogresion = pitchtools.Retrograde()
                >>> pitch_class = pitchtools.NumberedPitchClass(6)
                >>> retrograde(pitch_class)
                NumberedPitchClass(6)

        ..  container:: example

            Periodic retrograde:

            ..  todo:: Deprecated.

            ::

                >>> retrograde = pitchtools.Retrograde(period=3)
                >>> segment = pitchtools.PitchSegment("c' d' e' f' g' a' b' c''")
                >>> retrograde(segment)
                PitchSegment(["e'", "d'", "c'", "a'", "g'", "f'", "c''", "b'"])

        Returns new object with type equal to that of `expr`.
        '''
        from abjad.tools import pitchtools
        if isinstance(expr, (pitchtools.Pitch, pitchtools.PitchClass)):
            return expr
        if not isinstance(expr, (
            pitchtools.PitchSegment,
            pitchtools.PitchClassSegment,
            )):
            expr = pitchtools.PitchSegment(expr)
        if not self.period:
            return type(expr)(reversed(expr))
        result = new(expr, items=())
        for shard in sequencetools.partition_sequence_by_counts(
            expr,
            [self.period],
            cyclic=True,
            overhang=True,
            ):
            shard = type(expr)(shard)
            shard = type(expr)(reversed(shard))
            result = result + shard
        return result

    def __str__(self):
        r'''Gets string representation of operator.

        ..  container:: example

            ::

                >>> str(pitchtools.Retrograde())
                'R'

        '''
        return 'R'

    ### PRIVATE METHODS ###

    def _get_markup(self, direction=None):
        from abjad.tools import markuptools
        return markuptools.Markup('R', direction=direction)

    def _is_identity_operator(self):
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def period(self):
        r'''Gets optional period of retrograde.

        ..  todo:: Deprecated. Use Expression followed by Retrograde instead.

        ..  container:: example

            ::

                >>> retrograde = pitchtools.Retrograde(period=3)
                >>> retrograde.period
                3

        Returns integer or none.
        '''
        return self._period
