def iterate_sequence_forward_and_backward_overlapping(sequence):
   '''.. versionadded:: 1.1.2

   Iterate `sequence` first forward and then backward, 
   with first and last elements appearing only once::

      abjad> list(seqtools.iterate_sequence_forward_and_backward_overlapping([1, 2, 3, 4, 5]))
      [1, 2, 3, 4, 5, 4, 3, 2]

   Return generator.
   '''

   sequence_copy = [ ]
   for x in sequence:
      yield x
      sequence_copy.append(x)
   for x in reversed(sequence_copy[1:-1]):
      yield x
