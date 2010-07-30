from abjad.component import _Component
import types


def all_are_contiguous_components_in_same_thread(expr, klasses = (_Component), 
   allow_orphans = True):
   '''True when expr is a Python list of Abjad components such that
         
         1. all components in list are strictly contiguous, and
         2. all components in list are in the same thread.

      Otherwise False.
   '''
   
   if not isinstance(expr, (list, tuple, types.GeneratorType)):
      raise TypeError('Must be list of Abjad components.')

   if len(expr) == 0:
      return True

   first = expr[0]
   if not isinstance(first, klasses):
      return False

   orphan_components = True
   if not first.parentage.orphan:
      orphan_components = False

   same_thread = True
   strictly_contiguous = True

   first_signature = first.thread.signature
   prev = first
   for cur in expr[1:]:
      if not isinstance(cur, klasses):
         return False
      if not cur.parentage.orphan:
         orphan_components = False
      cur_signature = cur.thread.signature
      if not cur_signature == first_signature:
         same_thread = False
      if not prev._navigator._is_immediate_temporal_successor_of(cur):
         strictly_contiguous = False
      if (not allow_orphans or (allow_orphans and not orphan_components)) and \
         (not same_thread or not strictly_contiguous):
         return False
      prev = cur

   return True
