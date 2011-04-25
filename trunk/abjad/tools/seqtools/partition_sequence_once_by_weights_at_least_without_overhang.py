from abjad.tools.seqtools._group_sequence_elements_by_weights_at_least import \
   _group_sequence_elements_by_weights_at_least


def partition_sequence_once_by_weights_at_least_without_overhang(sequence, weights):
   '''.. versionadded:: 1.1.1

   Partition `sequence` elements once by `weights` at least without overhang::

      abjad> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
      abjad> groups = seqtools.partition_sequence_once_by_weights_at_least_without_overhang(sequence, [10, 4])
      [[3, 3, 3, 3], [4]]

   Return list sequence element reference lists.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.group_sequence_elements_once_by_weights_at_least_without_overhang( )`` to
      ``seqtools.partition_sequence_once_by_weights_at_least_without_overhang( )``.
   '''

   return _group_sequence_elements_by_weights_at_least(
      sequence, weights, cyclic = False, overhang = False)
