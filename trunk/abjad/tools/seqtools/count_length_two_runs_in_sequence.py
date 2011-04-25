from abjad.tools.seqtools.iterate_sequence_pairwise_strict import iterate_sequence_pairwise_strict


def count_length_two_runs_in_sequence(sequence):
   '''.. versionadded:: 1.1.1

   Count length-``2`` runs in `sequence`::

      abjad> seqtools.count_length_two_runs_in_sequence([0, 0, 1, 1, 1, 2, 3, 4, 5])
      3

   Return nonnegative integer.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.count_repetitions( )`` to
      ``seqtools.count_length_two_runs_in_sequence( )``.
   '''

   total_repetitions = 0
   for left, right in iterate_sequence_pairwise_strict(sequence):
      if left == right:
         total_repetitions += 1

   return total_repetitions
