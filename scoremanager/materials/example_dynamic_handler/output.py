# -*- encoding: utf-8 -*-
from abjad import *
from experimental.tools import handlertools


example_dynamic_handler = handlertools.ReiteratedDynamicHandler(
    dynamic_name='f',
    minimum_duration=durationtools.Duration(1, 16),
    )