# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_agenttools_InspectionAgent_get_indicator_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    attach('color', staff)

    assert inspect(staff).get_indicator('color') == 'color'
    assert inspect(staff[0]).get_indicator('color') is None
    assert inspect(staff[1]).get_indicator('color') is None
    assert inspect(staff[2]).get_indicator('color') is None
    assert inspect(staff[3]).get_indicator('color') is None


def test_agenttools_InspectionAgent_get_indicator_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    attach('color', staff)

    assert inspect(staff).get_indicator(str) == 'color'
    assert inspect(staff[0]).get_indicator(str) is None
    assert inspect(staff[1]).get_indicator(str) is None
    assert inspect(staff[2]).get_indicator(str) is None
    assert inspect(staff[3]).get_indicator(str) is None


def test_agenttools_InspectionAgent_get_indicator_03():

    note = Note("c'8")
    articulation = Articulation('staccato')
    attach(articulation, note)

    assert inspect(note).get_indicator(Articulation) is articulation


def test_agenttools_InspectionAgent_get_indicator_04():

    note = Note("c'8")

    assert inspect(note).get_indicator(Articulation) is None


def test_agenttools_InspectionAgent_get_indicator_05():

    note = Note("c'8")
    articulation = Articulation('staccato')
    attach(articulation, note)
    articulation = Articulation('marcato')
    attach(articulation, note)

    statement = 'inspect(note).get_indicator(Articulation)'
    assert pytest.raises(Exception, statement)


def test_agenttools_InspectionAgent_get_indicator_06():

    note = Note("c'8")
    command = indicatortools.LilyPondCommand('stemUp')
    attach(command, note)

    result = inspect(note).get_indicator(indicatortools.LilyPondCommand)
    assert result is command


def test_agenttools_InspectionAgent_get_indicator_07():

    note = Note("c'8")

    assert inspect(note).get_indicator(indicatortools.LilyPondCommand) is None


def test_agenttools_InspectionAgent_get_indicator_08():

    note = Note("c'8")
    command = indicatortools.LilyPondCommand('stemUp')
    attach(command, note)
    command = indicatortools.LilyPondCommand('slurUp')
    attach(command, note)

    statement = 'inspect(note).get_indicator(indicatortools.LilyPondCommand)'
    assert pytest.raises(Exception, statement)


def test_agenttools_InspectionAgent_get_indicator_09():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = Slur()
    attach(slur, staff[:])
    command_1 = indicatortools.LilyPondCommand('slurDotted')
    attach(command_1, staff[0])
    command_2 = indicatortools.LilyPondCommand('slurUp')
    attach(command_2, staff[0])

    assert format(staff) == String.normalize(
        r'''
        \new Staff {
            \slurDotted
            \slurUp
            c'8 (
            d'8
            e'8
            f'8 )
        }
        '''
        )

    indicators = inspect(staff[0]).get_indicators(
        indicatortools.LilyPondCommand)

    assert command_1 in indicators
    assert command_2 in indicators
    assert len(indicators) == 2


def test_agenttools_InspectionAgent_get_indicator_10():

    note = Note("c'8")
    comment = indicatortools.LilyPondComment('comment')
    attach(comment, note)

    indicator = inspect(note).get_indicator(indicatortools.LilyPondComment)
    assert indicator is comment


def test_agenttools_InspectionAgent_get_indicator_11():

    note = Note("c'8")

    assert inspect(note).get_indicator(indicatortools.LilyPondComment) is None


def test_agenttools_InspectionAgent_get_indicator_12():

    note = Note("c'8")
    comment = indicatortools.LilyPondComment('comment')
    attach(comment, note)
    comment = indicatortools.LilyPondComment('another comment')
    attach(comment, note)

    statement = 'inspect(note).get_indicator(indicatortools.LilyPondComment)'
    assert pytest.raises(Exception, statement)


def test_agenttools_InspectionAgent_get_indicator_13():

    note = Note("c'8")

    assert inspect(note).get_indicator() is None


def test_agenttools_InspectionAgent_get_indicator_14():

    note = Note("c'4")
    stem_tremolo = indicatortools.StemTremolo(16)
    attach(stem_tremolo, note)
    stem_tremolo = inspect(note).get_indicator(indicatortools.StemTremolo)

    assert stem_tremolo is stem_tremolo


def test_agenttools_InspectionAgent_get_indicator_15():

    staff = Staff("c'8 d'8 e'8 f'8")
    violin = instrumenttools.Violin()
    attach(violin, staff)

    indicator = inspect(staff).get_indicator(instrumenttools.Instrument)

    assert indicator is violin


def test_agenttools_InspectionAgent_get_indicator_16():

    measure = Measure((4, 8), "c'8 d'8 e'8 f'8")
    indicator = inspect(measure).get_indicator(TimeSignature)

    assert indicator == TimeSignature((4, 8))
