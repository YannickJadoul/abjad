from abjad.components.Container._ContainerFormatter import _ContainerFormatter
from abjad.exceptions import NonbinaryMeterSuppressionError
from abjad.exceptions import OverfullMeasureError
from abjad.exceptions import UnderfullMeasureError
from abjad.components.Measure._MeasureFormatterNumberInterface import \
   _MeasureFormatterNumberInterface
from abjad.components.Measure._MeasureFormatterSlotsInterface import \
   _MeasureFormatterSlotsInterface


class _MeasureFormatter(_ContainerFormatter):
   '''Encapsulate all dynamic measure and anonymous measure
   format logic::

      abjad> measure = AnonymousMeasure(macros.scale(3))
      abjad> measure.formatter
      <_MeasureFormatter>

   ::

      abjad> measure = DynamicMeasure(macros.scale(3))
      abjad> measure.formatter
      <_MeasureFormatter>

   Measure instances implement a special formatter which inherits from this base class. ::

      abjad> measure = Measure((3, 8), macros.scale(3))
      abjad> measure.formatter
      <_MeasureFormatter>
   '''

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)
      self._number = _MeasureFormatterNumberInterface(self)
      self._slots = _MeasureFormatterSlotsInterface(self)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contents(self):
      result = [ ]
      client = self._client
      ## the class name test here is exclude scaleDurations from Anonymous and Dynamic measures
      if client.duration.is_nonbinary and client.__class__.__name__ == 'Measure':
         result.append("\t\\scaleDurations #'(%s . %s) {" % (
            client.duration.multiplier.numerator,
            client.duration.multiplier.denominator))
         #result.extend( ['\t' + x for x in _MeasureFormatter._contents.fget(self)])
         result.extend( ['\t' + x for x in _ContainerFormatter._contents.fget(self)])
         result.append('\t}')
      else:
         #result.extend(_MeasureFormatter._contents.fget(self))
         result.extend(_ContainerFormatter._contents.fget(self))
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      from abjad.tools import contexttools
      client = self._client
      effective_meter = contexttools.get_effective_time_signature(self._client)
      if effective_meter.is_nonbinary and effective_meter.suppress:
         raise NonbinaryMeterSuppressionError
      if effective_meter.duration < client.duration.preprolated:
         raise OverfullMeasureError
      if client.duration.preprolated < effective_meter.duration:
         raise UnderfullMeasureError
      #return _MeasureFormatter.format.fget(self)
      return _ContainerFormatter.format.fget(self)

   @property
   def slots(self):
      '''Read-only reference to measure formatter slots interface.
      '''
      return self._slots
