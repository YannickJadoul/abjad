# -*- encoding: utf-8 -*-


def list_all_abjadide_functions(modules=None):
    r'''Lists all public functions defined in Abjad.

    ::

        >>> all_functions = documentationtools.list_all_abjadide_functions()  # doctest: +SKIP

    '''
    from abjad.tools import documentationtools
    return documentationtools.list_all_functions(modules='abjadide')