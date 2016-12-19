# -*- encoding: utf-8 -*-
import re
import types
from abjad.tools import systemtools
from supriya import synthdefs
from supriya.tools import patterntools
from supriya.tools import servertools


class TestCase(systemtools.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.pseudo_server = types.SimpleNamespace(
            audio_bus_allocator=servertools.BlockAllocator(),
            control_bus_allocator=servertools.BlockAllocator(),
            node_id_allocator=servertools.NodeIdAllocator(),
            )
        self.server = servertools.Server.get_default_server().boot()
        synthdefs.default.allocate(self.server)
        self.server.debug_osc = True
        self.server.latency = 0.0

    def compare_objects_as_strings(self, objects, string, replace_uuids=False):
        pattern = re.compile(r"\bUUID\('(.*)'\)")
        objects_string = '\n'.join(format(x) for x in objects)
        if replace_uuids:
            matches = []
            search_offset = 0
            while True:
                match = pattern.search(objects_string, search_offset)
                if not match:
                    break
                group = match.groups()[0]
                if group not in matches:
                    matches.append(group)
                search_offset = match.end()
            for i, match in enumerate(matches, 65):
                objects_string = objects_string.replace(match, chr(i))
        return self.compare_strings(objects_string, string)

    def tearDown(self):
        self.server.debug_osc = False
        self.server.quit()
        super(TestCase, self).tearDown()

    def manual_incommunicado(self, pattern, timestamp=10):
        player = patterntools.RealtimeEventPlayer(
            pattern,
            server=self.pseudo_server,
            )
        lists, deltas, delta = [], [], True
        while delta is not None:
            bundle, delta = player(timestamp, timestamp, communicate=False)
            if delta is not None:
                timestamp += delta
            lists.append(bundle.to_list(True))
            deltas.append(delta)
        return lists, deltas
