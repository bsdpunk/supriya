# -*- encoding: utf-8 -*-
from patterntools_testbase import TestCase
from supriya.tools import patterntools


class TestCase(TestCase):

    pattern = patterntools.Pbus(
        pattern=patterntools.Pseq([
            patterntools.Pgpar([
                patterntools.Pbind(
                    amplitude=1.0,
                    duration=patterntools.Pseq([1.0], 1),
                    frequency=patterntools.Pseq([440], 1),
                    ),
                patterntools.Pbind(
                    amplitude=0.75,
                    duration=patterntools.Pseq([1.0], 1),
                    frequency=patterntools.Pseq([880], 1),
                    ),
                ], release_time=0,
                ),
            patterntools.Pgpar([
                patterntools.Pbind(
                    amplitude=0.5,
                    duration=patterntools.Pseq([2.0], 1),
                    frequency=patterntools.Pseq([330], 1),
                    ),
                patterntools.Pbind(
                    amplitude=0.25,
                    duration=patterntools.Pseq([2.0], 1),
                    frequency=patterntools.Pseq([660], 1),
                    ),
                ], release_time=0,
                ),
            ]),
        release_time=0.25,
        )

    def test___iter__(self):
        events = list(self.pattern)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.BusEvent(
                calculation_rate=supriya.tools.synthdeftools.CalculationRate.AUDIO,
                channel_count=2,
                delta=0,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.GroupEvent(
                delta=0,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.SynthEvent(
                add_action=supriya.tools.servertools.AddAction.ADD_AFTER,
                amplitude=1.0,
                delta=0,
                in_=UUID('A'),
                synthdef=<supriya.tools.synthdeftools.SynthDef('454b69a7c505ddecc5b39762d291a5ec')>,
                target_node=UUID('B'),
                uuid=UUID('C'),
                )
            supriya.tools.patterntools.GroupEvent(
                add_action=supriya.tools.servertools.AddAction.ADD_TO_TAIL,
                delta=0,
                target_node=UUID('B'),
                uuid=UUID('D'),
                )
            supriya.tools.patterntools.GroupEvent(
                add_action=supriya.tools.servertools.AddAction.ADD_TO_TAIL,
                delta=0,
                target_node=UUID('B'),
                uuid=UUID('E'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                out=UUID('A'),
                target_node=UUID('D'),
                uuid=UUID('F'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=0.75,
                duration=1.0,
                frequency=880,
                is_stop=True,
                out=UUID('A'),
                target_node=UUID('E'),
                uuid=UUID('G'),
                )
            supriya.tools.patterntools.GroupEvent(
                delta=0,
                is_stop=True,
                uuid=UUID('E'),
                )
            supriya.tools.patterntools.GroupEvent(
                delta=0,
                is_stop=True,
                uuid=UUID('D'),
                )
            supriya.tools.patterntools.GroupEvent(
                add_action=supriya.tools.servertools.AddAction.ADD_TO_TAIL,
                delta=0,
                target_node=UUID('B'),
                uuid=UUID('H'),
                )
            supriya.tools.patterntools.GroupEvent(
                add_action=supriya.tools.servertools.AddAction.ADD_TO_TAIL,
                delta=0,
                target_node=UUID('B'),
                uuid=UUID('I'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=0.5,
                delta=0.0,
                duration=2.0,
                frequency=330,
                is_stop=True,
                out=UUID('A'),
                target_node=UUID('H'),
                uuid=UUID('J'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=0.25,
                duration=2.0,
                frequency=660,
                is_stop=True,
                out=UUID('A'),
                target_node=UUID('I'),
                uuid=UUID('K'),
                )
            supriya.tools.patterntools.GroupEvent(
                delta=0,
                is_stop=True,
                uuid=UUID('I'),
                )
            supriya.tools.patterntools.GroupEvent(
                delta=0,
                is_stop=True,
                uuid=UUID('H'),
                )
            supriya.tools.patterntools.NullEvent(
                delta=0.25,
                )
            supriya.tools.patterntools.SynthEvent(
                delta=0,
                is_stop=True,
                uuid=UUID('C'),
                )
            supriya.tools.patterntools.GroupEvent(
                delta=0,
                is_stop=True,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.BusEvent(
                delta=0,
                is_stop=True,
                uuid=UUID('A'),
                )
            ''',
            replace_uuids=True,
            )
