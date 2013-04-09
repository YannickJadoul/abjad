from abjad import *
from abjad.tools import contexttools
from abjad.tools import durationtools
from scftools import specifiers


music_specifier = specifiers.MusicSpecifier([
	specifiers.MusicContributionSpecifier(
		[specifiers.InstrumentSpecifier(instrument=instrumenttools.Violin())],
		name='black violin pizzicati',
		description='lower register violin pizzicati'
		),
	specifiers.MusicContributionSpecifier(
		[specifiers.InstrumentSpecifier(instrument=instrumenttools.Cello())],
		name='black cello pizzicati',
		description='midrange cello pizzicati',
		)
	],
	name='black music'
	)
