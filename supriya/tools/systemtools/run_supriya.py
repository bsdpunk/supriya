# -*- encoding: utf-8 -*-
import os
import sys


def run_supriya():
    r'''Runs Supriya.

    Returns none.
    '''
    from abjad.tools import systemtools

    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = ''

    commands = (
        "from supriya import *;",
        "server = Server(debug=True);",
        "server.boot();"
        )
    commands = ' '.join(commands)

    command = r'''python -i {} -c "{}"'''
    command = command.format(file_name, commands)
    systemtools.IOManager.spawn_subprocess(command)