import pytest

import abjad


def test_MetronomeMark_attach_01():

    score = abjad.Score(r"\new Staff { c'' d'' e'' f'' } \new Staff { c' d' e' f' }")
    mark_1 = abjad.MetronomeMark((1, 8), 52)
    mark_2 = abjad.MetronomeMark((1, 8), 73)
    abjad.attach(mark_1, score[0][0])

    with pytest.raises(Exception):
        abjad.attach(mark_2, score[1][0], check_duplicate_indicator=True)
