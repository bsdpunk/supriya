# -*- encoding: utf-8 -*-
from patterntools_testbase import TestCase
from supriya.tools import patterntools


class TestCase(TestCase):

    pattern = patterntools.Pseq([
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
        ])

    def test___iter__(self):
        events = list(self.pattern)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.GroupEvent(
                add_action=supriya.tools.servertools.AddAction.ADD_TO_TAIL,
                delta=0,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.GroupEvent(
                add_action=supriya.tools.servertools.AddAction.ADD_TO_TAIL,
                delta=0,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                target_node=UUID('A'),
                uuid=UUID('C'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=0.75,
                duration=1.0,
                frequency=880,
                is_stop=True,
                target_node=UUID('B'),
                uuid=UUID('D'),
                )
            supriya.tools.patterntools.GroupEvent(
                delta=0,
                is_stop=True,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.GroupEvent(
                delta=0,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.GroupEvent(
                add_action=supriya.tools.servertools.AddAction.ADD_TO_TAIL,
                delta=0,
                uuid=UUID('E'),
                )
            supriya.tools.patterntools.GroupEvent(
                add_action=supriya.tools.servertools.AddAction.ADD_TO_TAIL,
                delta=0,
                uuid=UUID('F'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=0.5,
                delta=0.0,
                duration=2.0,
                frequency=330,
                is_stop=True,
                target_node=UUID('E'),
                uuid=UUID('G'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=0.25,
                duration=2.0,
                frequency=660,
                is_stop=True,
                target_node=UUID('F'),
                uuid=UUID('H'),
                )
            supriya.tools.patterntools.GroupEvent(
                delta=0,
                is_stop=True,
                uuid=UUID('F'),
                )
            supriya.tools.patterntools.GroupEvent(
                delta=0,
                is_stop=True,
                uuid=UUID('E'),
                )
            ''',
            replace_uuids=True,
            )
