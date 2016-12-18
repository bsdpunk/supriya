# -*- encoding: utf-8 -*-
import abc
import collections
import inspect
import itertools
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class Pattern(SupriyaValueObject):
    """
    Pattern base class.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _filename = __file__

    _rngs = {}

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        """
        Adds `expr` to pattern.

        ::

            >>> pattern = patterntools.Pseq([1, 2, 3])
            >>> expr = patterntools.Pseq([0, 10])
            >>> list(pattern + expr)
            [1, 12]

        ::

            >>> expr = 10
            >>> list(pattern + expr)
            [11, 12, 13]

        ::

            >>> expr = [10, [100, 1000]]
            >>> list(pattern + expr)
            [[11, [101, 1001]], [12, [102, 1002]], [13, [103, 1003]]]

        ::

            >>> pattern = patterntools.Pseq([[1, [2, 3]], [[4, 5], 6, 7]])
            >>> expr = [10, [100, 1000]]
            >>> for x in (pattern + expr):
            ...     x
            ...
            [11, [102, 1003]]
            [[14, 15], [106, 1006], 17]

        """
        from supriya.tools import patterntools
        return patterntools.Pbinop(self, '+', expr)

    def __div__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(self, '/', expr)

    def __mul__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(self, '*', expr)

    def __radd__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(expr, '+', self)

    def __rdiv__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(expr, '/', self)

    def __rmul__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(expr, '*', self)

    def __rsub__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(expr, '-', self)

    def __sub__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(self, '-', expr)

    def __iter__(self):
        should_stop = False
        state = self._setup_state()
        iterator = self._iterate(state)
        try:
            expr = next(iterator)
            expr = self._coerce_iterator_output(expr, state)
        except StopIteration:
            return
        peripheral_pairs = self._setup_peripherals(expr, state)
        peripheral_stops = []
        for peripheral_pair in peripheral_pairs:
            peripheral = peripheral_pair[0]
            should_stop = yield peripheral
            if len(peripheral_pair) > 1:
                peripheral_stops.extend(peripheral_pairs[1:])
            if should_stop:
                break
        if not should_stop:
            should_stop = yield expr
            while True:
                try:
                    expr = iterator.send(should_stop)
                    expr = self._coerce_iterator_output(expr, state)
                    should_stop = yield expr
                except StopIteration:
                    break
        expr = self._process_last_expr(state)
        if expr:
            yield expr
        for peripheral in reversed(peripheral_stops):
            yield peripheral

    ### PRIVATE METHODS ###

    def _coerce_iterator_output(self, expr, state=None):
        return expr

    @classmethod
    def _coerce_floats(cls, value):
        if isinstance(value, collections.Sequence):
            value = tuple(float(_) for _ in value)
            assert value
        else:
            value = float(value)
        return value

    @classmethod
    def _freeze_recursive(cls, value):
        if isinstance(value, str):
            return value
        elif (
            isinstance(value, collections.Sequence) and
            not isinstance(value, Pattern)
            ):
            return tuple(cls._freeze_recursive(_) for _ in value)
        return value

    @classmethod
    def _get_arity(cls, value):
        if isinstance(value, Pattern):
            return value.arity
        elif isinstance(value, collections.Sequence):
            return len(value)
        return 1

    @classmethod
    def _get_rng(cls):
        from supriya.tools import patterntools
        pseed_file_path = inspect.getfile(patterntools.Pseed)
        identifier = None
        try:
            stack = inspect.stack()
            for frame_info in stack:
                if (
                    frame_info.filename == pseed_file_path and
                    frame_info.function == '_iterate'
                    ):
                    identifier = id(frame_info.frame)
                    break
        finally:
            del(frame_info)
            del(stack)
        if identifier in cls._rngs:
            rng = cls._rngs[identifier]
        elif identifier is None:
            rng = patterntools.RandomNumberGenerator.get_stdlib_rng()
            cls._rngs[identifier] = rng
        return rng

    @classmethod
    def _loop(cls, repetitions=None):
        if repetitions is None:
            while True:
                yield True
        else:
            for _ in range(repetitions):
                yield True

    @classmethod
    def _process_recursive(cls, one, two, procedure):
        if not isinstance(one, collections.Sequence) and \
            not isinstance(two, collections.Sequence):
            return procedure(one, two)
        if not isinstance(one, collections.Sequence):
            one = [one]
        if not isinstance(two, collections.Sequence):
            two = [two]
        length = max(len(one), len(two))
        if len(one) < length:
            cycle = itertools.cycle(one)
            one = (next(cycle) for _ in range(length))
        if len(two) < length:
            cycle = itertools.cycle(two)
            two = (next(cycle) for _ in range(length))
        result = []
        for one, two in zip(one, two):
            result.append(cls._process_recursive(one, two, procedure))
        return result

    def _process_last_expr(self, state=None):
        pass

    def _setup_state(self):
        return {}

    def _setup_peripherals(self, expr=None, state=None):
        return ()

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def arity(self):
        raise NotImplementedError

    @abc.abstractproperty
    def is_infinite(self):
        raise NotImplementedError
