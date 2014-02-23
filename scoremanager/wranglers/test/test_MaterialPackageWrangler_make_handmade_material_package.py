# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_make_handmade_material_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.testnotes'
    assert not wrangler._configuration.package_exists(string)

    try:
        wrangler.make_handmade_material_package(
            pending_user_input='testnotes q')
        assert wrangler._configuration.package_exists(string)
        manager = scoremanager.managers.MaterialPackageManager(string)
        assert manager._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
    finally:
        manager._remove()
        assert not wrangler._configuration.package_exists(string)
