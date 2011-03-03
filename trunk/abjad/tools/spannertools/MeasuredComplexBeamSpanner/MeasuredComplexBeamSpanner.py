from abjad.tools.spannertools.ComplexBeamSpanner import ComplexBeamSpanner
from abjad.tools.spannertools.MeasuredComplexBeamSpanner._MeasuredComplexBeamSpannerFormatInterface import _MeasuredComplexBeamSpannerFormatInterface
from fractions import Fraction


class MeasuredComplexBeamSpanner(ComplexBeamSpanner):
   '''Abjad measured complex beam spanner.

   Return measured complex beam spanner.
   '''

   def __init__(self, components = None, lone = False, span = 1):
      ComplexBeamSpanner.__init__(self, components = components, lone = lone)
      self._format = _MeasuredComplexBeamSpannerFormatInterface(self)
      self.span = span

   ## PUBLIC ATTRIBUTES ##
      
   @apply
   def span( ):
      def fget(self):
         return self._span
      def fset(self, arg):
         assert isinstance(arg, (int, type(None)))
         self._span = arg 
      return property(**locals( ))
