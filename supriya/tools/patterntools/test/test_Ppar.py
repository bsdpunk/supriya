# -*- encoding: utf-8 -*-
import time
from patterntools_testbase import TestCase
from supriya import synthdefs
from supriya.tools import nonrealtimetools
from supriya.tools import patterntools


class TestCase(TestCase):

    pattern = patterntools.Ppar([
        patterntools.Pmono(
            amplitude=1.0,
            duration=1.0,
            frequency=patterntools.Pseq([440, 660, 880, 990], 1),
            ),
        patterntools.Pbind(
            amplitude=1.0,
            duration=0.75,
            frequency=patterntools.Pseq([222, 333, 444, 555], 1),
            ),
        ])

    def test___iter__(self):
        events = list(self.pattern)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=440,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=222,
                is_stop=True,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.25,
                duration=0.75,
                frequency=333,
                is_stop=True,
                uuid=UUID('C'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.5,
                duration=1.0,
                frequency=660,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.5,
                duration=0.75,
                frequency=444,
                is_stop=True,
                uuid=UUID('D'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.25,
                duration=1.0,
                frequency=880,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=555,
                is_stop=True,
                uuid=UUID('E'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=990,
                is_stop=True,
                uuid=UUID('A'),
                )
            ''',
            replace_uuids=True,
            )

    def test_send_01(self):
        events, iterator = [], iter(self.pattern)
        for _ in range(1):
            events.append(next(iterator))
        iterator.send(True)
        events.extend(iterator)
        self.compare_objects_as_strings(
            events,
            '''
            ''',
            replace_uuids=True,
            )

    def test_manual_incommunicado(self):
        lists, deltas = self.manual_incommunicado(self.pattern, 10)
        assert lists == [
            [10, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1000, 0, 1,
                    'amplitude', 1.0, 'frequency', 440],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1001, 0, 1,
                    'amplitude', 1.0, 'frequency', 222]]],
            [10.75, [
                ['/n_set', 1001, 'gate', 0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 1,
                    'amplitude', 1.0, 'frequency', 333]]],
            [11.0, [['/n_set', 1000, 'amplitude', 1.0, 'frequency', 660]]],
            [11.5, [
                ['/n_set', 1002, 'gate', 0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1003, 0, 1,
                    'amplitude', 1.0, 'frequency', 444]]],
            [12.0, [['/n_set', 1000, 'amplitude', 1.0, 'frequency', 880]]],
            [12.25, [
                ['/n_set', 1003, 'gate', 0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1004, 0, 1,
                    'amplitude', 1.0, 'frequency', 555]]],
            [13.0, [
                ['/n_set', 1004, 'gate', 0],
                ['/n_set', 1000, 'amplitude', 1.0, 'frequency', 990]]],
            [14.0, [['/n_set', 1000, 'gate', 0]]]]
        assert deltas == [0.75, 0.25, 0.5, 0.5, 0.25, 0.75, 1.0, None]

    def test_manual_communicado(self):
        player = patterntools.RealtimeEventPlayer(
            self.pattern,
            server=self.server,
            )
        # Initial State
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
        NODE TREE 0 group
            1 group
        ''')
        # Step 1
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
        NODE TREE 0 group
            1 group
                1001 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 222.0, gate: 1.0, pan: 0.5
                1000 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 1.0, pan: 0.5
        ''')
        # Step 2
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
        NODE TREE 0 group
            1 group
                1002 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 333.0, gate: 1.0, pan: 0.5
                1001 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 222.0, gate: 0.0, pan: 0.5
                1000 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 1.0, pan: 0.5
        ''')
        # Wait for termination
        time.sleep(0.5)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
        NODE TREE 0 group
            1 group
                1002 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 333.0, gate: 1.0, pan: 0.5
                1000 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 440.0, gate: 1.0, pan: 0.5
        ''')
        # Step 3
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
        NODE TREE 0 group
            1 group
                1002 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 333.0, gate: 1.0, pan: 0.5
                1000 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
        ''')
        # Step 4
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
        NODE TREE 0 group
            1 group
                1003 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 444.0, gate: 1.0, pan: 0.5
                1002 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 333.0, gate: 0.0, pan: 0.5
                1000 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
        ''')
        # Wait for termination
        time.sleep(0.5)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
        NODE TREE 0 group
            1 group
                1003 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 444.0, gate: 1.0, pan: 0.5
                1000 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 660.0, gate: 1.0, pan: 0.5
        ''')
        # Step 5
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
        NODE TREE 0 group
            1 group
                1003 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 444.0, gate: 1.0, pan: 0.5
                1000 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 880.0, gate: 1.0, pan: 0.5
        ''')
        # Step 6
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
        NODE TREE 0 group
            1 group
                1004 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 555.0, gate: 1.0, pan: 0.5
                1003 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 444.0, gate: 0.0, pan: 0.5
                1000 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 880.0, gate: 1.0, pan: 0.5
        ''')
        # Wait for termination
        time.sleep(0.5)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
        NODE TREE 0 group
            1 group
                1004 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 555.0, gate: 1.0, pan: 0.5
                1000 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 880.0, gate: 1.0, pan: 0.5
        ''')
        # Step 7
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
        NODE TREE 0 group
            1 group
                1004 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 555.0, gate: 0.0, pan: 0.5
                1000 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 990.0, gate: 1.0, pan: 0.5
        ''')
        # Wait for termination
        time.sleep(0.5)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
        NODE TREE 0 group
            1 group
                1000 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 990.0, gate: 1.0, pan: 0.5
        ''')
        # Step 8
        player(0, 0)
        self.server.sync()
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
        NODE TREE 0 group
            1 group
                1000 da0982184cc8fa54cf9d288a0fe1f6ca
                    out: 0.0, amplitude: 1.0, frequency: 990.0, gate: 0.0, pan: 0.5
        ''')
        # Wait for termination
        time.sleep(0.5)
        server_state = str(self.server.query_remote_nodes(include_controls=True))
        assert server_state == self.normalize(r'''
        NODE TREE 0 group
            1 group
        ''')

    def test_automatic_communicado(self):
        self.pattern.play(server=self.server)
        time.sleep(4)

    def test_nonrealtime(self):
        session = nonrealtimetools.Session()
        with session.at(10):
            self.pattern.inscribe(session)
        assert session.to_lists() == [
            [10.0, [
                ['/d_recv', bytearray(synthdefs.default.compile())],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1000, 0, 0,
                    'amplitude', 1.0, 'frequency', 440],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1001, 0, 0,
                    'amplitude', 1.0, 'frequency', 222]]],
            [10.75, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 0,
                    'amplitude', 1.0, 'frequency', 333],
                ['/n_set', 1001, 'gate', 0]]],
            [11.0, [
                ['/n_set', 1000, 'amplitude', 1.0, 'frequency', 660]]],
            [11.5, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1003, 0, 0,
                    'amplitude', 1.0, 'frequency', 444],
                ['/n_set', 1002, 'gate', 0]]],
            [12.0, [
                ['/n_set', 1000, 'amplitude', 1.0, 'frequency', 880]]],
            [12.25, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1004, 0, 0,
                    'amplitude', 1.0, 'frequency', 555],
                ['/n_set', 1003, 'gate', 0]]],
            [13.0, [
                ['/n_set', 1000, 'amplitude', 1.0, 'frequency', 990],
                ['/n_set', 1004, 'gate', 0]]],
            [14.0, [
                ['/n_set', 1000, 'gate', 0],
                [0]]]]
