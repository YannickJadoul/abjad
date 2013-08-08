# -*- encoding: utf-8 -*-
# TODO: implement corresponding function with durations that increase monotonically
def fuse_leaves_in_tie_chain_by_immediate_parent(tie_chain):
    r'''Fuse leaves in `tie_chain` by immediate parent:

    ::

        >>> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        >>> spannertools.TieSpanner(staff.select_leaves())
        TieSpanner(c'8, c'8, c'8, c'8)
        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8 ~
                c'8 ~
            }
            {
                c'8 ~
                c'8
            }
        }

    ::

        >>> tie_chain = staff.select_leaves()[0].select_tie_chain()
        >>> leaftools.fuse_leaves_in_tie_chain_by_immediate_parent(tie_chain)
        [[Note("c'4")], [Note("c'4")]]

    ..  doctest::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'4 ~
            }
            {
                c'4
            }
        }

    Return list of fused notes by parent.
    '''
    from abjad.tools import leaftools
    from abjad.tools import selectiontools

    # check input
    if not isinstance(tie_chain, selectiontools.TieChain):
        raise TypeError('must be tie chain: {!r}.'.format(tie_chain))

    # init result
    result = []

    # group leaves in tie chain by parent
    parts = tie_chain.leaves_grouped_by_immediate_parents

    # fuse leaves in each part
    for part in parts:
        result.append(leaftools.fuse_leaves(part))

    # return result
    return result
