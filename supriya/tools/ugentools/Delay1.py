# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.Argument import Argument
from supriya.tools.ugentools.PureUGen import PureUGen


class Delay1(PureUGen):
    r'''One-sample delay line unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> source = ugentools.In.ar(bus=0)
        >>> ugentools.Delay1.ar(source=source)
        Delay1.ar()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        Argument('source'),
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=None,
        ):
        r'''Create an audio-rate one-sample delay line.

        ::

            >>> from supriya.tools import ugentools
            >>> source = ugentools.In.ar(bus=0)
            >>> ugentools.Delay1.ar(
            ...     source=source,
            ...     )
            Delay1.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        r'''Create a control-rate one-sample delay line.

        ::

            >>> from supriya.tools import ugentools
            >>> source = ugentools.In.kr(bus=0)
            >>> ugentools.Delay1.kr(
            ...     source=source,
            ...     )
            Delay1.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

