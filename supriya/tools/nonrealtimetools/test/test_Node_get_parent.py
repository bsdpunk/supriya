# -*- encoding: utf-8 -*-
from nonrealtimetools_testbase import TestCase
from supriya.tools import nonrealtimetools


class TestCase(TestCase):

    def test_01(self):
        """
        With Session.at(...) context manager.
        """
        session = nonrealtimetools.Session()
        with session.at(0):
            group_one = session.add_group()
            group_two = session.add_group()
            node = group_one.add_synth()
        with session.at(10):
            group_two.move_node(node)
        with session.at(5):
            parent = node.get_parent()
        assert parent is group_one
        with session.at(15):
            parent = node.get_parent()
        assert parent is group_two

    def test_02(self):
        """
        With offset=... keyword.
        """
        session = nonrealtimetools.Session()
        with session.at(0):
            group_one = session.add_group()
            group_two = session.add_group()
            node = group_one.add_synth()
        with session.at(10):
            group_two.move_node(node)
        parent = node.get_parent(offset=5)
        assert parent is group_one
        parent = node.get_parent(offset=15)
        assert parent is group_two

    def test_03(self):
        """
        Without Session.at(...) context manager or offset keyword.
        """
        session = nonrealtimetools.Session()
        with session.at(0):
            group_one = session.add_group()
            group_two = session.add_group()
            node = group_one.add_synth()
        with session.at(10):
            group_two.move_node(node)
        with self.assertRaises(ValueError):
            node.get_parent()

    def test_04(self):
        """
        With both Session.at(...) context manager and offset keyword.
        """
        session = nonrealtimetools.Session()
        with session.at(0):
            group_one = session.add_group()
            group_two = session.add_group()
            node = group_one.add_synth()
        with session.at(10):
            group_two.move_node(node)
        with session.at(5):
            parent = node.get_parent(offset=15)
        assert parent is group_two
