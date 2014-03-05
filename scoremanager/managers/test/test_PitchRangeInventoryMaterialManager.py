# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_PitchRangeInventoryMaterialManager_01():
    r'''Stub material package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materials.testpir'
    assert not score_manager._configuration.package_exists(string)
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        ]

    try:
        score_manager._run(pending_user_input=
            'lmm nmm pitch testpir default '
            'q'
            )
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testpir')
        manager = scoremanager.managers.PitchRangeInventoryMaterialManager(
            path=path)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_material_module()
        assert output_material is None
    finally:
        string = 'lmm testpir rm remove q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materials.testpir'
        assert not score_manager._configuration.package_exists(string)


def test_PitchRangeInventoryMaterialManager_02():
    r'''Populate output material module.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materials.testpir'
    assert not score_manager._configuration.package_exists(string)
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'output_material.py',
        ]
    inventory = pitchtools.PitchRangeInventory([
        pitchtools.PitchRange('[C2, G5]'), 
        pitchtools.PitchRange('[C2, F#5]'),
        ])

    try:
        score_manager._run(pending_user_input=
            'lmm nmm pitch testpir default '
            'testpir omi add [A0, C8] add [C2, F#5] add [C2, G5] '
            'rm 1 mv 1 2 b default '
            'q'
            )
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testpir')
        manager = scoremanager.managers.PitchRangeInventoryMaterialManager(
            path=path)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_material_module()
        assert output_material == inventory
    finally:
        string = 'lmm testpir rm remove q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materials.testpir'
        assert not score_manager._configuration.package_exists(string)
