# -*- encoding: utf-8 -*-
import unittest
from supriya.tools import nonrealtimetools
from supriya.tools import requesttools


class TestCase(unittest.TestCase):

    def test_Session(self):
        session = nonrealtimetools.Session()
        request = requesttools.BufferReadRequest(
            buffer_id=1,
            file_path=session,
            frame_count=512,
            leave_open=True,
            starting_frame_in_buffer=0,
            starting_frame_in_file=0,
            )
        assert request.file_path is session
        osc_message = request.to_osc_message(with_textual_osc_command=True)
        assert osc_message.address == '/b_read'
        assert osc_message.contents == (1, session, 0, 512, 0, 1)
