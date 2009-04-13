from abjad.navigator.dfs import depth_first_search
from abjad.tools import check
from abjad.tools import containertools
from abjad.tools import iterate


def coalesce(expr):
   '''Fuse containers in self that are strictly contiguous and have
   the same name.'''
   from abjad.container.container import Container
   from abjad.tuplet.tuplet import _Tuplet
   merged = False
   if not isinstance(expr, list):
      expr = [expr]
   expr = Container(expr)

   g = depth_first_search(expr, direction = 'right')
   for cmp in g:
      next = cmp._navigator._nextNamesake
      if isinstance(next, Container) and not next.parallel and \
         not isinstance(next, _Tuplet) and \
         check.assess_components([cmp, next], contiguity = 'strict', 
            share = 'score', allow_orphans = False):
         cmp.extend(next)
         next.detach( )
         merged = True
   if merged:
      print expr
      containertools.remove_empty(expr)
      return expr.pop(0)
   else:
      return None
