from supriya.library.audiolib.UGen import UGen


class InfoUGenBase(UGen):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    @classmethod
    def ir(cls, **kwargs):
        ugen = cls._new(
            calculation_rate=UGen.Rate.SCALAR_RATE,
            **kwargs
            )
        return ugen
