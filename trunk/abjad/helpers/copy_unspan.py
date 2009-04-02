from abjad.helpers.assert_components import assert_components
from abjad.helpers.cut_outgoing_reference_to_parent import \
   _cut_outgoing_reference_to_parent
from abjad.helpers.get_contained_spanners import get_contained_spanners
from abjad.helpers.restore_outgoing_reference_to_parent import \
   restore_outgoing_reference_to_parent
import copy


def copy_unspan(components, n = 1):
   '''Withdraw all components at any level in 'components' from spanners.
      Deep copy unspanned components in 'components'.
      Reapply spanners to all components at any level in 'components'.
      The 'components' must be thread-contiguous.'''

   assert_components(components, contiguity = 'thread')

   spanners = get_contained_spanners(components) 
   for spanner in spanners:
      spanner._blockAllComponents( )

   receipt = _cut_outgoing_reference_to_parent(components)

   result = copy.deepcopy(components)
   for component in result:
      component._update._markForUpdateToRoot( )

   restore_outgoing_reference_to_parent(receipt)

   for spanner in spanners:
      spanner._unblockAllComponents( )

   for i in range(n - 1):
      result += copy_unspan(components)
      
   return result
