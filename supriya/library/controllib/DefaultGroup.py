# -*- encoding: utf-8 -*0
from supriya.library.controllib.Group import Group


class DefaultGroup(Group):

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self):
        from supriya.library import controllib
        controllib.Node.__init__(self)
        self._is_playing = True
        self._is_running = True
        self._node_id = 1
        self._parent_group = self

    ### PUBLIC METHODS ###

    def allocate(self):
        pass

    def free(self):
        pass

    def move_after(self):
        pass

    def move_before(self):
        pass

    def move_to_head(self):
        pass

    def move_to_tail(self):
        pass

    def run(self):
        pass
