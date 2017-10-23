# -*- coding: UTF-8 -*-
"""Implement sub commands."""

from __future__ import absolute_import, division, print_function, unicode_literals
import logging
logger = logging.getLogger('closeup')

class CUPException(Exception):
    pass

class NoRepoRootFound(CUPException):
    def __init__(self, path, finalpath):
        self.path = path
        self.finalpath = finalpath

    def __str__(self):
        return 'fatal: Not a closeup repository (or any parent up to {})'.format(
            self.finalpath)

class WrongNamePath(CUPException):
    def __init__(self, namepath, nameitem):
        self.namepath = namepath
        self.nameitem = nameitem

    def __str__(self):
        return 'fatal: "{}" of "{}" caused namepath syntax error'.format(
            self.nameitem, self.namepath)

class NamePathExists(CUPException):
    def __init__(self, namepath, nameitem):
        self.namepath = namepath
        self.nameitem = nameitem

    def __str__(self):
        return 'fatal: "{}" of "{}" already exists.'.format(
            self.nameitem, self.namepath)

class NamePathNotFound(CUPException):
    def __init__(self, namepath, nameitem):
        self.namepath = namepath
        self.namepath = nameitem

    def __str__(self):
        return 'fatal: "{}" is not found at "{}".'.format(self.namepath,
            self.nameitem)

class NamePathOutOfRange(CUPException):
    def __init__(self, namepath, inrange, outrange, lastvalue):
        self.namepath = namepath
        self.inrange = inrange
        self.outrange = outrange
        self.lastvalue = lastvalue

    def __str__(self):
        return 'fatal: "{}" is out of range.'.format(self.namepath)


class PathTypeMismatch(CUPException):
    def __init__(self, node, prevpath, nextpath):
        self.node = node
        self.prevpath = prevpath
        self.nextpath = nextpath

    def __str__(self):
        return 'fatal: TypeError with node={}, prevpath={}, and nextpath={}.'.format(
            self.node, self.prevpath, self.nextpath)
