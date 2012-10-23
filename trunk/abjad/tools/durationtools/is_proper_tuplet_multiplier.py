def is_proper_tuplet_multiplier(multiplier):
    '''True when ``1/2 < multiplier < 2``.

    ::

        >>> for n in range(17):
        ...     multiplier = Multiplier(n, 8)
        ...     result = durationtools.is_proper_tuplet_multiplier(multiplier)
        ...     print '%s   %s' % (multiplier, result)
        ...
        0         False
        1/8     False
        1/4     False
        3/8     False
        1/2     False
        5/8     True
        3/4     True
        7/8     True
        1         True
        9/8     True
        5/4     True
        11/8    True
        3/2     True
        13/8    True
        7/4     True
        15/8    True
        2         False

    This function models the idea that ``4:3``, ``4:5``, ``4:6``,
    ``4:7`` are valid tuplet multipliers while ``4:2`` and ``4:8``
    aren't.

    .. versionchanged:: 2.0
        renamed ``durationtools.is_tuplet_multiplier()`` to
        ``durationtools.is_proper_tuplet_multiplier()``.
    '''
    from abjad.tools import durationtools

    # check input
    multiplier = durationtools.Multiplier(multiplier)

    if durationtools.Multiplier(1, 2) < multiplier < durationtools.Multiplier(2):
        return True

    return False
