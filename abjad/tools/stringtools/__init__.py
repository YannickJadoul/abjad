# -*- coding: utf-8 -*-
r'''The Abjad stringtools package imports no other Abjad packages.
'''
from abjad.tools import systemtools


systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    )

_documentation_section = 'core'
