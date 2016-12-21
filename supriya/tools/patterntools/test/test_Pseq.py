# -*- encoding: utf-8 -*-
from patterntools_testbase import TestCase
from supriya.tools import patterntools


class TestCase(TestCase):

    pseq_01 = patterntools.Pseq(['A', 'B', 'C', 'D'])

    pseq_02 = patterntools.Pseq([
        patterntools.Pseq(['A', 'B', 'C']),
        patterntools.Pseq(['D', 'E', 'F']),
        ])

    pseq_03 = patterntools.Pseq([
        patterntools.Pbind(
            amplitude=1.0,
            duration=patterntools.Pseq([1.0, 2.0, 3.0], 1),
            frequency=patterntools.Pseq([440, 660, 880], 1),
            ),
        patterntools.Pbind(
            amplitude=1.0,
            duration=patterntools.Pseq([1.0, 2.0, 3.0], 1),
            frequency=patterntools.Pseq([550, 770, 990], 1),
            ),
        ])

    pseq_04 = patterntools.Pseq([
        patterntools.Pbind(
            amplitude=1.0,
            duration=patterntools.Pseq([1.0, 2.0, 3.0], 1),
            frequency=patterntools.Pseq([440, 660, 880], 1),
            ),
        patterntools.Pbus(
            patterntools.Pbind(
                amplitude=1.0,
                duration=patterntools.Pseq([1.0, 2.0, 3.0], 1),
                frequency=patterntools.Pseq([550, 770, 990], 1),
                ),
            ),
        ])

    def test___iter___01(self):
        events = list(self.pseq_01)
        assert events == ['A', 'B', 'C', 'D']

    def test___iter___02(self):
        events = list(self.pseq_02)
        assert events == ['A', 'B', 'C', 'D', 'E', 'F']

    def test___iter___03(self):
        events = list(self.pseq_03)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=2.0,
                frequency=660,
                is_stop=True,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=3.0,
                frequency=880,
                is_stop=True,
                uuid=UUID('C'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=550,
                is_stop=True,
                uuid=UUID('D'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=2.0,
                frequency=770,
                is_stop=True,
                uuid=UUID('E'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=3.0,
                frequency=990,
                is_stop=True,
                uuid=UUID('F'),
                )
            ''',
            replace_uuids=True,
            )

    def test___iter___04(self):
        events = list(self.pseq_04)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=2.0,
                frequency=660,
                is_stop=True,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=3.0,
                frequency=880,
                is_stop=True,
                uuid=UUID('C'),
                )
            supriya.tools.patterntools.BusEvent(
                calculation_rate=supriya.tools.synthdeftools.CalculationRate.AUDIO,
                channel_count=2,
                delta=0,
                uuid=UUID('D'),
                )
            supriya.tools.patterntools.GroupEvent(
                delta=0,
                uuid=UUID('E'),
                )
            supriya.tools.patterntools.SynthEvent(
                add_action=supriya.tools.servertools.AddAction.ADD_AFTER,
                amplitude=1.0,
                delta=0,
                in_=UUID('D'),
                synthdef=<supriya.tools.synthdeftools.SynthDef('454b69a7c505ddecc5b39762d291a5ec')>,
                target_node=UUID('E'),
                uuid=UUID('F'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=550,
                is_stop=True,
                out=UUID('D'),
                target_node=UUID('E'),
                uuid=UUID('G'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=2.0,
                frequency=770,
                is_stop=True,
                out=UUID('D'),
                target_node=UUID('E'),
                uuid=UUID('H'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=3.0,
                frequency=990,
                is_stop=True,
                out=UUID('D'),
                target_node=UUID('E'),
                uuid=UUID('I'),
                )
            supriya.tools.patterntools.NullEvent(
                delta=0.25,
                )
            supriya.tools.patterntools.SynthEvent(
                delta=0,
                is_stop=True,
                uuid=UUID('F'),
                )
            supriya.tools.patterntools.GroupEvent(
                delta=0,
                is_stop=True,
                uuid=UUID('E'),
                )
            supriya.tools.patterntools.BusEvent(
                delta=0,
                is_stop=True,
                uuid=UUID('D'),
                )
            ''',
            replace_uuids=True,
            )

    def test_send_01(self):
        events, iterator = [], iter(self.pseq_01)
        for _ in range(2):
            events.append(next(iterator))
        try:
            iterator.send(True)
            events.extend(iterator)
        except StopIteration:
            pass
        assert events == ['A', 'B']

    def test_send_02a(self):
        events, iterator = [], iter(self.pseq_02)
        for _ in range(2):
            events.append(next(iterator))
        try:
            iterator.send(True)
            events.extend(iterator)
        except StopIteration:
            pass
        assert events == ['A', 'B']

    def test_send_02b(self):
        events, iterator = [], iter(self.pseq_02)
        for _ in range(3):
            events.append(next(iterator))
        try:
            iterator.send(True)
            events.extend(iterator)
        except StopIteration:
            pass
        assert events == ['A', 'B', 'C']

    def test_send_02c(self):
        events, iterator = [], iter(self.pseq_02)
        for _ in range(4):
            events.append(next(iterator))
        try:
            iterator.send(True)
            events.extend(iterator)
        except StopIteration:
            pass
        assert events == ['A', 'B', 'C', 'D']

    def test_send_03a(self):
        events, iterator = [], iter(self.pseq_03)
        for _ in range(2):
            events.append(next(iterator))
        try:
            iterator.send(True)
            events.extend(iterator)
        except StopIteration:
            pass
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=2.0,
                frequency=660,
                is_stop=True,
                uuid=UUID('B'),
                )
            ''',
            replace_uuids=True,
            )

    def test_send_03b(self):
        events, iterator = [], iter(self.pseq_03)
        for _ in range(3):
            events.append(next(iterator))
        try:
            iterator.send(True)
            events.extend(iterator)
        except StopIteration:
            pass
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=2.0,
                frequency=660,
                is_stop=True,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=3.0,
                frequency=880,
                is_stop=True,
                uuid=UUID('C'),
                )
            ''',
            replace_uuids=True,
            )

    def test_send_03c(self):
        events, iterator = [], iter(self.pseq_03)
        for _ in range(4):
            events.append(next(iterator))
        try:
            iterator.send(True)
            events.extend(iterator)
        except StopIteration:
            pass
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=2.0,
                frequency=660,
                is_stop=True,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=3.0,
                frequency=880,
                is_stop=True,
                uuid=UUID('C'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=550,
                is_stop=True,
                uuid=UUID('D'),
                )
            ''',
            replace_uuids=True,
            )

    def test_send_04a(self):
        events, iterator = [], iter(self.pseq_04)
        for _ in range(4):
            events.append(next(iterator))
        try:
            iterator.send(True)
            events.extend(iterator)
        except StopIteration:
            pass
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=2.0,
                frequency=660,
                is_stop=True,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=3.0,
                frequency=880,
                is_stop=True,
                uuid=UUID('C'),
                )
            supriya.tools.patterntools.BusEvent(
                calculation_rate=supriya.tools.synthdeftools.CalculationRate.AUDIO,
                channel_count=2,
                delta=0,
                uuid=UUID('D'),
                )
            supriya.tools.patterntools.BusEvent(
                delta=0,
                is_stop=True,
                uuid=UUID('D'),
                )
            ''',
            replace_uuids=True,
            )

    def test_send_04b(self):
        events, iterator = [], iter(self.pseq_04)
        for _ in range(5):
            events.append(next(iterator))
        try:
            iterator.send(True)
            events.extend(iterator)
        except StopIteration:
            pass
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=2.0,
                frequency=660,
                is_stop=True,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=3.0,
                frequency=880,
                is_stop=True,
                uuid=UUID('C'),
                )
            supriya.tools.patterntools.BusEvent(
                calculation_rate=supriya.tools.synthdeftools.CalculationRate.AUDIO,
                channel_count=2,
                delta=0,
                uuid=UUID('D'),
                )
            supriya.tools.patterntools.GroupEvent(
                delta=0,
                uuid=UUID('E'),
                )
            supriya.tools.patterntools.GroupEvent(
                delta=0,
                is_stop=True,
                uuid=UUID('E'),
                )
            supriya.tools.patterntools.BusEvent(
                delta=0,
                is_stop=True,
                uuid=UUID('D'),
                )
            ''',
            replace_uuids=True,
            )
