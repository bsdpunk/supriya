# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Duty(UGen):
    r'''

    ::

        >>> duty = ugentools.Duty.(
        ...     done_action=0,
        ...     duration=1,
        ...     level=1,
        ...     reset=0,
        ...     )
        >>> duty

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'duration',
        'reset',
        'level',
        'done_action',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        done_action=0,
        duration=1,
        level=1,
        reset=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            level=level,
            reset=reset,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        done_action=0,
        duration=1,
        level=1,
        reset=0,
        ):
        r'''Constructs an audio-rate Duty.

        ::

            >>> duty = ugentools.Duty.ar(
            ...     done_action=0,
            ...     duration=1,
            ...     level=1,
            ...     reset=0,
            ...     )
            >>> duty

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            level=level,
            reset=reset,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        done_action=0,
        duration=1,
        level=1,
        reset=0,
        ):
        r'''Constructs a control-rate Duty.

        ::

            >>> duty = ugentools.Duty.kr(
            ...     done_action=0,
            ...     duration=1,
            ...     level=1,
            ...     reset=0,
            ...     )
            >>> duty

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            level=level,
            reset=reset,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def done_action(self):
        r'''Gets `done_action` input of Duty.

        ::

            >>> duty = ugentools.Duty.ar(
            ...     done_action=0,
            ...     duration=1,
            ...     level=1,
            ...     reset=0,
            ...     )
            >>> duty.done_action

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('done_action')
        return self._inputs[index]

    @property
    def duration(self):
        r'''Gets `duration` input of Duty.

        ::

            >>> duty = ugentools.Duty.ar(
            ...     done_action=0,
            ...     duration=1,
            ...     level=1,
            ...     reset=0,
            ...     )
            >>> duty.duration

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('duration')
        return self._inputs[index]

    @property
    def level(self):
        r'''Gets `level` input of Duty.

        ::

            >>> duty = ugentools.Duty.ar(
            ...     done_action=0,
            ...     duration=1,
            ...     level=1,
            ...     reset=0,
            ...     )
            >>> duty.level

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('level')
        return self._inputs[index]

    @property
    def reset(self):
        r'''Gets `reset` input of Duty.

        ::

            >>> duty = ugentools.Duty.ar(
            ...     done_action=0,
            ...     duration=1,
            ...     level=1,
            ...     reset=0,
            ...     )
            >>> duty.reset

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('reset')
        return self._inputs[index]