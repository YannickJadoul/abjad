import typing

from .. import bundle as _bundle
from .. import format as _format


class StopPhrasingSlur:
    r"""
    LilyPond ``\)`` command.

    ..  container:: example

        >>> abjad.StopPhrasingSlur()
        StopPhrasingSlur()

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_leak",)

    context = "Voice"
    parameter = "PHRASING_SLUR"
    persistent = True
    spanner_stop = True

    ### INITIALIZER ###

    def __init__(self, *, leak: bool = None) -> None:
        if leak is not None:
            leak = bool(leak)
        self._leak = leak

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        string = r"\)"
        if self.leak:
            string = f"<> {string}"
            bundle.after.leaks.append(string)
        else:
            bundle.after.spanner_stops.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def leak(self) -> typing.Optional[bool]:
        r"""
        Is true when stop slur leaks LilyPond ``<>`` empty chord.

        ..  container:: example

            Without leak:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> command = abjad.StartPhrasingSlur()
            >>> abjad.tweak(command).color = "#blue"
            >>> abjad.attach(command, staff[0])
            >>> command = abjad.StopPhrasingSlur()
            >>> abjad.attach(command, staff[-2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    \(
                    d'4
                    e'4
                    \)
                    r4
                }

            With leak:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> command = abjad.StartPhrasingSlur()
            >>> abjad.tweak(command).color = "#blue"
            >>> abjad.attach(command, staff[0])
            >>> command = abjad.StopPhrasingSlur(leak=True)
            >>> abjad.attach(command, staff[-2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    \(
                    d'4
                    e'4
                    <> \)
                    r4
                }

        ..  container:: example

            REGRESSION. Leaked contributions appear last in postevent format
            slot:

            >>> staff = abjad.Staff("c'8 d' e' f' r2")
            >>> abjad.beam(staff[:4])
            >>> command = abjad.StartPhrasingSlur()
            >>> abjad.tweak(command).color = "#blue"
            >>> abjad.attach(command, staff[0])
            >>> command = abjad.StopPhrasingSlur(leak=True)
            >>> abjad.attach(command, staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'8
                    [
                    - \tweak color #blue
                    \(
                    d'8
                    e'8
                    f'8
                    ]
                    <> \)
                    r2
                }

            The leaked text spanner above does not inadvertantly leak the beam.

        """
        return self._leak
