from abjad.tools import contexttools
from experimental import quantizationtools
import py
py.test.skip('FIXME')


def test_MeasurewiseQSchema___call___01():

    schema = quantizationtools.MeasurewiseQSchema()

    target = schema(5000)
