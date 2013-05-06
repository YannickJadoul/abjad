from abjad.tools import contexttools
from experimental import *


def test_TempoMarkInventoryMaterialPackageMaker_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not packagepathtools.package_exists('system_materials.testtempoinventory')
    try:
        score_manager.run(user_input=
            'materials maker tempo testtempoinventory default '
            'testtempoinventory omi add ((1, 4), 60) add ((1, 4), 90) b default '
            'q '
            )
        mpp = scoremanagertools.materialpackagemakers.TempoMarkInventoryMaterialPackageMaker('system_materials.testtempoinventory')
        assert mpp.list_directory() == ['__init__.py', 'output_material.py', 'tags.py']
        inventory = contexttools.TempoMarkInventory([((1, 4), 60), ((1, 4), 90)])
        assert mpp.output_material == inventory
    finally:
        score_manager.run(user_input='m testtempoinventory del remove default q')
        assert not packagepathtools.package_exists('system_materials.testtempoinventory')
