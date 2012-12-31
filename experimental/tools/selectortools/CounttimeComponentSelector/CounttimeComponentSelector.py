import copy
from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import iterationtools
from abjad.tools import leaftools
from abjad.tools import measuretools
from abjad.tools import selectiontools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from abjad.tools import tuplettools
from abjad.tools import wellformednesstools
from experimental.tools import helpertools
from experimental.tools.selectortools.Selector import Selector


class CounttimeComponentSelector(Selector):
    r'''Counttime component selector.

    ::

        >>> from experimental.tools import *

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Select voice ``1`` leaves that start during score::

        >>> selector = score_specification.interface.select_leaves('Voice 1')

    ::
        
        >>> z(selector)
        selectortools.CounttimeComponentSelector(
            classes=helpertools.KlassInventory([
                leaftools.Leaf
                ]),
            voice_name='Voice 1'
            )

    Select voice ``1`` leaves that start during segment ``'red'``::

        >>> selector = red_segment.select_leaves('Voice 1')

    ::

        >>> z(selector)
        selectortools.CounttimeComponentSelector(
            anchor='red',
            classes=helpertools.KlassInventory([
                leaftools.Leaf
                ]),
            voice_name='Voice 1'
            )

    Counttime component selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None, classes=None, predicate=None, 
        voice_name=None, time_relation=None,
        request_modifiers=None, timespan_modifiers=None):
        from experimental.tools import timeexpressiontools
        assert classes is None or self._is_counttime_component_class_expr(classes), repr(classes)
        assert isinstance(predicate, (helpertools.Callback, type(None))), repr(predicate)
        Selector.__init__(self, 
            anchor=anchor, 
            voice_name=voice_name, 
            time_relation=time_relation, 
            request_modifiers=request_modifiers,
            timespan_modifiers=timespan_modifiers)
        if isinstance(classes, tuple):
            classes = helpertools.KlassInventory(classes)
        self._classes = classes
        self._predicate = predicate
    
    ### PRIVATE METHODS ###

    def _get_timespan(self, score_specification, voice_name):
        # allow user-specified voice name to override passed-in voice name
        voice_name = self.voice_name or voice_name
        rhythm_region_expressions = score_specification.contexts[voice_name]['rhythm_region_expressions']
        if not rhythm_region_expressions:
            return selectiontools.Selection()
        if not rhythm_region_expressions[0].start_offset == durationtools.Offset(0):
            return selectiontools.Selection()
        counttime_component_pairs = []
        previous_rhythm_region_expression = None
        timespan_1 = score_specification[self.anchor].timespan
        if self.time_relation is None:
            time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=timespan_1)
        else:
            time_relation = self.time_relation.new(timespan_1=timespan_1)
        for current_rhythm_region_expression in rhythm_region_expressions:
            if previous_rhythm_region_expression is not None:
                if not previous_rhtyhm_region_expression.stops_when_expr_starts(
                    current_rhythm_region_expression):
                    return selectiontools.Selection()
            for counttime_component in iterationtools.iterate_components_in_expr(
                current_rhythm_region_expression.music, klass=tuple(self.classes)):
                if time_relation(timespan_2=counttime_component,
                    score_specification=score_specification,
                    context_name=voice_name):
                    counttime_component_pairs.append((
                        counttime_component, current_rhythm_region_expression.start_offset))
        counttime_component_pairs, dummy = self._apply_request_modifiers(counttime_component_pairs, None)
        first_component, first_component_expression_offset = counttime_component_pairs[0]
        last_component, last_component_expression_offset = counttime_component_pairs[-1]
        start_offset = first_component_expression_offset + first_component.start_offset
        stop_offset = last_component_expression_offset + last_component.stop_offset
        return timespantools.Timespan(start_offset, stop_offset)

    def _get_rhythm_region_expression(self, score_specification, voice_name,
        start_offset=None, stop_offset=None):
        from experimental.tools import settingtools
        assert voice_name == self.voice_name
        #self._debug((start_offset, stop_offset), 'offsets')
        anchor_timespan = score_specification.get_anchor_timespan(self, voice_name)
        voice_proxy = score_specification.contexts[voice_name]
        rhythm_region_expressions = voice_proxy['rhythm_region_expressions']
        #self._debug_values(rhythm_region_expressions, 'rhythm region expressions')
        timespan_time_relation = timerelationtools.timespan_2_intersects_timespan_1(
            timespan_1=anchor_timespan)
        rhythm_region_expressions = rhythm_region_expressions.get_timespans_that_satisfy_time_relation(
            timespan_time_relation)
        #self._debug_values(rhythm_region_expressions, 'rhythm region expressions')
        if not rhythm_region_expressions:
            return
        rhythm_region_expressions = copy.deepcopy(rhythm_region_expressions)
        rhythm_region_expressions = timespantools.TimespanInventory(rhythm_region_expressions)
        rhythm_region_expressions.sort()
        assert anchor_timespan.is_well_formed, repr(anchor_timespan)
        rhythm_region_expressions.keep_material_that_intersects_timespan(anchor_timespan)
        result = settingtools.RhythmRegionExpression(
            voice_name=voice_name, start_offset=start_offset)
        for rhythm_region_expression in rhythm_region_expressions:
            result.music.extend(rhythm_region_expression.music)
        assert wellformednesstools.is_well_formed_component(result.music)
        result, new_start_offset = self._apply_request_modifiers(result, result.start_offset)
        if not isinstance(result, settingtools.RhythmRegionExpression):
            assert componenttools.all_are_components(result)
            music = componenttools.copy_components_and_fracture_crossing_spanners(result)
            result = settingtools.RhythmRegionExpression(
                music=music, voice_name=voice_name, start_offset=start_offset)
        result.set_offsets(start_offset=start_offset, stop_offset=stop_offset)
        result.repeat_to_stop_offset(stop_offset)
        return result

    def _is_counttime_component_class_expr(self, expr):
        from experimental.tools import helpertools
        if isinstance(expr, tuple) and all([self._is_counttime_component_class_expr(x) for x in expr]):
            return True
        elif isinstance(expr, helpertools.KlassInventory):
            return True
        elif issubclass(expr, (measuretools.Measure, tuplettools.Tuplet, leaftools.Leaf)):
            return True
        elif expr == containertools.Container:
            return True
        else:
            return False

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def classes(self):
        '''Classes of counttime component selector.

        Return class inventory or none.
        '''
        return self._classes

    @property
    def predicate(self):
        '''Predicate of counttime component selector specified by user.

        Return predicate or none.
        '''
        return self._predicate
