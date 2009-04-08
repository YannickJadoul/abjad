def restore_outgoing_reference_to_parent(receipt):
   '''Use to restore parentage.
      Use after call to _ignore_parent(components).
      Return None.'''

   for component, parent in receipt:
      assert component.parentage.parent is None
      component.parentage._switchParentTo(parent)
