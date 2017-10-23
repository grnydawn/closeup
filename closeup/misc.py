# -*- coding: UTF-8 -*-
"""Implement misc. functions."""

from __future__ import absolute_import, division, print_function, unicode_literals
from . import util, system, error, extension as ext

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

def is_reglink(node):
    return isinstance(node, list) and len(node)==4 and \
        node[0]=='\x00' and ext.has_object_type(node[1])

