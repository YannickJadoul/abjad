import abjad


def test_Staff___getitem___01():

    staff = abjad.Staff(
        [
            abjad.Note("c'4"),
            abjad.Rest((1, 4)),
            abjad.Chord([2, 3, 4], (1, 4)),
            abjad.Skip((1, 4)),
            abjad.Tuplet((4, 5), "c'16 c'16 c'16 c'16"),
        ]
    )

    assert len(staff) == 5
    assert abjad.wf.wellformed(staff)
    assert isinstance(staff[0], abjad.Note)
    assert isinstance(staff[1], abjad.Rest)
    assert isinstance(staff[2], abjad.Chord)
    assert isinstance(staff[3], abjad.Skip)
    assert isinstance(staff[4], abjad.Tuplet)
    assert isinstance(staff[-5], abjad.Note)
    assert isinstance(staff[-4], abjad.Rest)
    assert isinstance(staff[-3], abjad.Chord)
    assert isinstance(staff[-2], abjad.Skip)
    assert isinstance(staff[-1], abjad.Tuplet)


def test_Staff___getitem___02():

    staff = abjad.Staff(
        [
            abjad.Note("c'4"),
            abjad.Rest((1, 4)),
            abjad.Chord([2, 3, 4], (1, 4)),
            abjad.Skip((1, 4)),
            abjad.Tuplet((4, 5), "c'16 c'16 c'16 c'16"),
        ]
    )

    assert len(staff) == 5
    assert abjad.wf.wellformed(staff)
    selection = staff[0:0]
    assert len(selection) == 0
    assert abjad.wf.wellformed(staff)


def test_Staff___getitem___03():

    staff = abjad.Staff(
        [
            abjad.Note("c'4"),
            abjad.Rest((1, 4)),
            abjad.Chord([2, 3, 4], (1, 4)),
            abjad.Skip((1, 4)),
            abjad.Tuplet((4, 5), "c'16 c'16 c'16 c'16"),
        ]
    )

    assert len(staff) == 5
    assert abjad.wf.wellformed(staff)
    selection = staff[0:1]
    assert len(selection) == 1
    assert isinstance(selection[0], abjad.Note)
    for x in staff:
        assert x._parent == staff
    assert abjad.wf.wellformed(staff)


def test_Staff___getitem___04():

    staff = abjad.Staff(
        [
            abjad.Note("c'4"),
            abjad.Rest((1, 4)),
            abjad.Chord([2, 3, 4], (1, 4)),
            abjad.Skip((1, 4)),
            abjad.Tuplet((4, 5), "c'16 c'16 c'16 c'16"),
        ]
    )

    assert len(staff) == 5
    assert abjad.wf.wellformed(staff)
    selection = staff[-1:]
    assert len(selection) == 1
    assert isinstance(selection[0], abjad.Tuplet)
    for x in selection:
        assert x._parent == staff
    assert abjad.wf.wellformed(staff)


def test_Staff___getitem___05():

    staff = abjad.Staff(
        [
            abjad.Note("c'4"),
            abjad.Rest((1, 4)),
            abjad.Chord([2, 3, 4], (1, 4)),
            abjad.Skip((1, 4)),
            abjad.Tuplet((4, 5), "c'16 c'16 c'16 c'16"),
        ]
    )

    assert len(staff) == 5
    assert abjad.wf.wellformed(staff)
    selection = staff[1:-1]
    assert len(selection) == 3
    assert isinstance(selection[0], abjad.Rest)
    assert isinstance(selection[1], abjad.Chord)
    assert isinstance(selection[2], abjad.Skip)
    for x in selection:
        assert x._parent == staff
    assert abjad.wf.wellformed(staff)


def test_Staff___getitem___06():

    staff = abjad.Staff(
        [
            abjad.Note("c'4"),
            abjad.Rest((1, 4)),
            abjad.Chord([2, 3, 4], (1, 4)),
            abjad.Skip((1, 4)),
            abjad.Tuplet((4, 5), "c'16 c'16 c'16 c'16"),
        ]
    )

    assert len(staff) == 5
    assert abjad.wf.wellformed(staff)
    selection = staff[2:]
    assert len(selection) == 3
    assert isinstance(selection[0], abjad.Chord)
    assert isinstance(selection[1], abjad.Skip)
    assert isinstance(selection[2], abjad.Tuplet)
    for x in selection:
        assert x._parent == staff
    assert abjad.wf.wellformed(staff)


def test_Staff___getitem___07():

    staff = abjad.Staff(
        [
            abjad.Note("c'4"),
            abjad.Rest((1, 4)),
            abjad.Chord([2, 3, 4], (1, 4)),
            abjad.Skip((1, 4)),
            abjad.Tuplet((4, 5), "c'16 c'16 c'16 c'16"),
        ]
    )

    assert len(staff) == 5
    assert abjad.wf.wellformed(staff)
    selection = staff[:-2]
    assert len(selection) == 3
    assert isinstance(selection[0], abjad.Note)
    assert isinstance(selection[1], abjad.Rest)
    assert isinstance(selection[2], abjad.Chord)
    for x in selection:
        assert x._parent == staff
    assert abjad.wf.wellformed(staff)


def test_Staff___getitem___08():

    staff = abjad.Staff(
        [
            abjad.Note("c'4"),
            abjad.Rest((1, 4)),
            abjad.Chord([2, 3, 4], (1, 4)),
            abjad.Skip((1, 4)),
            abjad.Tuplet((4, 5), "c'16 c'16 c'16 c'16"),
        ]
    )

    assert len(staff) == 5
    assert abjad.wf.wellformed(staff)
    components = staff[:]
    assert len(components) == 5
    assert isinstance(components[0], abjad.Note)
    assert isinstance(components[1], abjad.Rest)
    assert isinstance(components[2], abjad.Chord)
    assert isinstance(components[3], abjad.Skip)
    assert isinstance(components[4], abjad.Tuplet)
    assert all(_._parent is staff for _ in staff)
