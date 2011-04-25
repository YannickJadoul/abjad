def negate_absolute_value_of_sequence_elements_cyclically(sequence, indices, period):
   '''.. versionadded:: 1.1.2

   Negate the absolute value of `sequence` elements at `indices` cyclically
   according to `period`::

      abjad> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]

   ::

      abjad> seqtools.flip_sign_of_sequence_elements_cyclically(sequence, [0, 1, 2], 5)
      [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]

   Return newly constructed list.
   '''

   result = [ ]

   for i, element in enumerate(sequence):
      if (i in indices) or (period and i % period in indices):
         result.append(-abs(element))
      else:
         result.append(element)

   return result
