# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class BinaryOpUGen(UGen):
    """
    A binary operator ugen, created by applying a binary operator to two
    ugens.

    ::
        
        >>> left_operand = ugentools.SinOsc.ar()
        >>> right_operand = ugentools.WhiteNoise.kr()
        >>> binary_op_ugen = left_operand * right_operand
        >>> binary_op_ugen
        BinaryOpUGen.ar()

    ::

        >>> binary_op_ugen.operator
        BinaryOperator.MULTIPLICATION

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Basic Operator UGens'

    __slots__ = ()

    _ordered_input_names = (
        'left',
        'right',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        left=None,
        right=None,
        calculation_rate=None,
        special_index=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            left=left,
            right=right,
            special_index=special_index,
            )

    ### PRIVATE METHODS ###

    @classmethod
    def _new_single(
        cls,
        calculation_rate=None,
        special_index=None,
        **kwargs
        ):
        from supriya.tools import synthdeftools
        a = kwargs['left']
        b = kwargs['right']
        if special_index == synthdeftools.BinaryOperator.MULTIPLICATION:
            if a == 0:
                return 0
            if b == 0:
                return 0
            if a == 1:
                return b
            if a == 1:
                return -b
            if b == 1:
                return a
            if b == -1:
                return -a
        if special_index == synthdeftools.BinaryOperator.ADDITION:
            if a == 0:
                return b
            if b == 0:
                return a
        if special_index == synthdeftools.BinaryOperator.SUBTRACTION:
            if a == 0:
                return -b
            if b == 0:
                return a
        if special_index == synthdeftools.BinaryOperator.FLOAT_DIVISION:
            if b == 1:
                return a
            if b == -1:
                return -a
        ugen = cls(
            calculation_rate=calculation_rate,
            special_index=special_index,
            left=a,
            right=b,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def left(self):
        """
        Gets `left` input of BinaryOpUGen.

        ::

            >>> left = ugentools.SinOsc.ar()
            >>> right = ugentools.WhiteNoise.kr()
            >>> binary_op_ugen = left * right
            >>> binary_op_ugen.left
            OutputProxy(
                source=SinOsc(
                    calculation_rate=CalculationRate.AUDIO,
                    frequency=440.0,
                    phase=0.0
                    ),
                output_index=0
                )

        Returns input.
        """
        index = self._ordered_input_names.index('left')
        return self._inputs[index]

    @property
    def operator(self):
        """
        Gets operator of BinaryOpUgen.

        ::

            >>> left = ugentools.SinOsc.ar()
            >>> right = ugentools.WhiteNoise.kr()
            >>> binary_op_ugen = left / right
            >>> binary_op_ugen.operator
            BinaryOperator.FLOAT_DIVISION

        Returns binary operator.
        """
        from supriya.tools import synthdeftools
        return synthdeftools.BinaryOperator(self.special_index)

    @property
    def right(self):
        """
        Gets `right` input of BinaryOpUGen.

        ::

            >>> left = ugentools.SinOsc.ar()
            >>> right = ugentools.WhiteNoise.kr()
            >>> binary_op_ugen = left * right
            >>> binary_op_ugen.right
            OutputProxy(
                source=WhiteNoise(
                    calculation_rate=CalculationRate.CONTROL
                    ),
                output_index=0
                )

        Returns input.
        """
        index = self._ordered_input_names.index('right')
        return self._inputs[index]
