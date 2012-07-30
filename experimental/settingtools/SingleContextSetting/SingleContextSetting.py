from experimental import helpertools
from experimental.settingtools.MultipleContextSetting import MultipleContextSetting
import copy


class SingleContextSetting(MultipleContextSetting):
    r'''.. versionadded:: 1.0

    Frozen request to set one attribute against one context-specified selection.

    Initialize with mandatory `target`, `attribute`, `source`
    and optional `persist`, `truncate`, `fresh`::

        >>> from experimental import selectortools
        >>> from experimental import settingtools
        >>> from experimental import specificationtools
        >>> from experimental import timespantools

    ::

        >>> segment_selector = selectortools.SegmentSelector(index='red')
        >>> target = selectortools.SingleContextTimespanSelector('Voice 1', timespan=segment_selector.timespan)

    ::

        >>> setting = settingtools.SingleContextSetting(target, 'time_signatures', [(4, 8), (3, 8)], fresh=False)

    ::

        >>> z(setting)
        settingtools.SingleContextSetting(
            selectortools.SingleContextTimespanSelector(
                'Voice 1',
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    )
                ),
            'time_signatures',
            [(4, 8), (3, 8)],
            persist=True,
            truncate=False,
            fresh=False
            )

    Initialize from other context setting.
    '''

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _keyword_argument_names(self):
        return MultipleContextSetting._keyword_argument_names.fget(self) + ('fresh', )

    ### PRIVATE METHODS ###

    def _check_input_arguments(self, mandatory_argument_values, keyword_argument_values):
        from experimental import specificationtools
        attribute, source, target, = mandatory_argument_values
        persist, truncate, fresh = keyword_argument_values
        assert isinstance(target, selectortools.SingleContextTimespanSelector), repr(target)
        assert isinstance(attribute, str), repr(attribute)
        assert isinstance(persist, bool), repr(persist)
        assert isinstance(truncate, bool), repr(truncate)
        assert isinstance(fresh, type(True)), repr(fresh)

    def _get_input_argument_values(self, *args, **kwargs):
        if len(args) == 1:
            assert isinstance(args[0], type(self)), repr(args[0])
            mandatory_argument_values = args[0]._mandatory_argument_values
            keyword_argument_values = args[0]._keyword_argument_values
            if kwargs.get('persist') is not None:
                keyword_argment_values[0] = kwargs.get('persist')
            if kwargs.get('truncate') is not None:
                keyword_argment_values[0] = kwargs.get('truncate')
            if kwargs.get('fresh') is not None:
                keyword_argment_values[0] = kwargs.get('fresh')
        else:
            assert len(args) == 3, repr(args)
            mandatory_argument_values = args
            keyword_argument_values = []
            keyword_argument_values.append(kwargs.get('persist', True))
            keyword_argument_values.append(kwargs.get('truncate', False))
            keyword_argument_values.append(kwargs.get('fresh', True))
        return mandatory_argument_values, keyword_argument_values

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def fresh(self):
        return self._fresh

    ### PUBLIC METHODS ###

    def copy_to_segment(self, segment):
        '''Create new setting. Set new setting target to timespan of `segment`.
        Set new setting `fresh` to false.

        Only works when self encompasses one segment exactly.

        Return new setting.
        '''
        assert self.target.timespan.encompasses_one_segment_exactly, repr(self)
        new = copy.deepcopy(self)
        new.set_to_segment(segment)
        new._fresh = False
        return new

    def set_to_segment(self, segment):
        '''Set target of self to timespan of entire `segment`.

        Only works when self encompasses one segment exactly.

        Return none.
        '''
        from experimental import selectortools
        from experimental import specificationtools
        assert self.target.timespan.encompasses_one_segment_exactly, repr(self)
        segment_name = helpertools.expr_to_segment_name(segment)
        segment_selector = selectortools.SegmentSelector(index=segment_name)
        self.target._timespan = segment_selector.timespan
