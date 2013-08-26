# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.Vector import Vector


class NumberedPitchClassVector(Vector):
    '''Abjad model of numbered chromatic pitch-class vector:

    ::

        >>> ncpcv = pitchtools.NumberedPitchClassVector(
        ...     [13, 13, 14.5, 14.5, 14.5, 6, 6, 6])

    ::

        >>> print ncpcv
        0 2 0 0 0 0 | 3 0 0 0 0 0
        0 0 3 0 0 0 | 0 0 0 0 0 0

    Numbered chromatic pitch-class vectors are immutable.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        [13, 13, 14.5, 14.5, 14.5, 6, 6, 6],
        )

    ### INITIALIZER ###

    def __init__(self, pitch_class_tokens):
        from abjad.tools import pitchtools
        for pcn in range(12):
            dict.__setitem__(self, pcn, 0)
            dict.__setitem__(self, pcn + 0.5, 0)
        for token in pitch_class_tokens:
            pitch_class = pitchtools.NumberedPitchClass(token)
            dict.__setitem__(
                self, abs(pitch_class), self[abs(pitch_class)] + 1)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s)' % (self._class_name, self._format_string)

    def __str__(self):
        string = self._twelve_tone_format_string
        if self._has_quartertones:
            string += '\n%s' % self._quartertone_format_string
        return string

    ### PRIVATE PROPERTIES ###

    @property
    def _first_quartertone_sextet_string(self):
        items = self._quartertone_items[:6]
        substrings = []
        for pitch_class_number, count in sorted(items):
            substring = '%s' % count
            substrings.append(substring)
        return ' '.join(substrings)

    @property
    def _first_twelve_tone_sextet_string(self):
        items = self._twelve_tone_items[:6]
        substrings = []
        for pitch_class_number, count in sorted(items):
            substring = '%s' % count
            substrings.append(substring)
        return ' '.join(substrings)

    @property
    def _format_string(self):
        string = self._twelve_tone_format_string
        if self._has_quartertones:
            string += ' || %s' % self._quartertone_format_string
        return string

    @property
    def _has_quartertones(self):
        return any(0 < item[1] for item in self._quartertone_items)

    @property
    def _quartertone_format_string(self):
        return '%s | %s' % (
            self._first_quartertone_sextet_string,
            self._second_quartertone_sextet_string)

    @property
    def _quartertone_items(self):
        items = [item for item in self.items() if isinstance(item[0], float)]
        items.sort()
        return items

    @property
    def _second_quartertone_sextet_string(self):
        items = self._quartertone_items[6:]
        substrings = []
        for pitch_class_number, count in sorted(items):
            substring = '%s' % count
            substrings.append(substring)
        return ' '.join(substrings)

    @property
    def _second_twelve_tone_sextet_string(self):
        items = self._twelve_tone_items[6:]
        substrings = []
        for pitch_class_number, count in sorted(items):
            substring = '%s' % count
            substrings.append(substring)
        return ' '.join(substrings)

    @property
    def _twelve_tone_format_string(self):
        return '%s | %s' % (
            self._first_twelve_tone_sextet_string,
            self._second_twelve_tone_sextet_string)

    @property
    def _twelve_tone_items(self):
        items = [item for item in self.items() if isinstance(item[0], int)]
        items.sort()
        return items

