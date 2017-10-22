# -*- coding: UTF-8 -*-
"""Implement misc. functions."""

from __future__ import absolute_import, division, print_function, unicode_literals
from . import util, system, error

def runcmd(cmd):
    return util.to_unicodes(system.execute(cmd))

def get_reporoot(path):
    path = system.abspath(system.normpath(path))
    head, tail = system.pathsplit(path)
    while head and head!='/':
        if system.pathexists(system.pathjoin(head, tail, '.closeup')):
            return system.pathjoin(head, tail)
        head, tail = system.pathsplit(head)
    raise error.NoRepoRootFound(path, head)

