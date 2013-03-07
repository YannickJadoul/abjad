from experimental import *


def test_ReiteratedArticulationHandler_storage_format_01():

    handler = handlertools.ReiteratedArticulationHandler(
        articulation_list=['.', '^'],
        minimum_duration=Duration(1, 16),
        maximum_duration=Duration(1, 8),
        )

    r'''
    handlertools.ReiteratedArticulationHandler(
        articulation_list=['.', '^'],
        minimum_duration=durationtools.Duration(1, 16),
        maximum_duration=durationtools.Duration(1, 8)
        )
    '''

    assert handler.storage_format == "handlertools.ReiteratedArticulationHandler(\n\tarticulation_list=['.', '^'],\n\tminimum_duration=durationtools.Duration(1, 16),\n\tmaximum_duration=durationtools.Duration(1, 8)\n\t)"
