# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class DegreeToKey(PureUGen):
    r'''

    ::

        >>> degree_to_key = ugentools.DegreeToKey.(
        ...     buffer_id=None,
        ...     octave=12,
        ...     source=None,
        ...     )
        >>> degree_to_key

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'source',
        'octave',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        octave=12,
        source=None,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            octave=octave,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        octave=12,
        source=None,
        ):
        r'''Constructs an audio-rate DegreeToKey.

        ::

            >>> degree_to_key = ugentools.DegreeToKey.ar(
            ...     buffer_id=None,
            ...     octave=12,
            ...     source=None,
            ...     )
            >>> degree_to_key

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            octave=octave,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        octave=12,
        source=None,
        ):
        r'''Constructs a control-rate DegreeToKey.

        ::

            >>> degree_to_key = ugentools.DegreeToKey.kr(
            ...     buffer_id=None,
            ...     octave=12,
            ...     source=None,
            ...     )
            >>> degree_to_key

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            octave=octave,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of DegreeToKey.

        ::

            >>> degree_to_key = ugentools.DegreeToKey.ar(
            ...     buffer_id=None,
            ...     octave=12,
            ...     source=None,
            ...     )
            >>> degree_to_key.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def octave(self):
        r'''Gets `octave` input of DegreeToKey.

        ::

            >>> degree_to_key = ugentools.DegreeToKey.ar(
            ...     buffer_id=None,
            ...     octave=12,
            ...     source=None,
            ...     )
            >>> degree_to_key.octave

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('octave')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of DegreeToKey.

        ::

            >>> degree_to_key = ugentools.DegreeToKey.ar(
            ...     buffer_id=None,
            ...     octave=12,
            ...     source=None,
            ...     )
            >>> degree_to_key.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]