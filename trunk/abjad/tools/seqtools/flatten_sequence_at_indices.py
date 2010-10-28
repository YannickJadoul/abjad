from abjad.tools.seqtools.flatten_sequence import flatten_sequence


def flatten_sequence_at_indices(sequence, indices, klasses = None, depth = -1):
   '''.. versionadded:: 1.1.2

   Flatten `sequence` at `indices`::

      abjad> seqtools.flatten_sequence_at_indices([0, 1, [2, 3, 4], [5, 6, 7]], [3])
      [0, 1, [2, 3, 4], 5, 6, 7]

   Flatten `sequence` at negative `indices`::

      abjad> seqtools.flatten_sequence_at_indices([0, 1, [2, 3, 4], [5, 6, 7]], [-1])
      [0, 1, [2, 3, 4], 5, 6, 7]

   Return newly constructed `sequence` type.

   Leave `sequence` unchanged.

   .. versionchanged:: 1.1.2
      renamed ``listtools.flatten_at_indices( )`` to
      ``seqtools.flatten_sequence_at_indices( )``.
   '''

   if klasses is None:
      klasses = (list, tuple)

   if not isinstance(sequence, klasses):
      raise TypeError( )
   ltype = type(sequence)

   len_l = len(sequence)
   indices = [x if 0 <= x else len_l + x for x in indices]

   result = [ ]
   for i, element in enumerate(sequence):
      if i in indices:
         try:
            flattened = flatten_sequence(element, klasses = klasses, depth = depth)
            result.extend(flattened)
         except:
            result.append(element)
      else:
         result.append(element)

   result = ltype(result)
   return result
